# -*- coding: utf-8 -*-
import os
import copy
import json
import pathlib

from . import _tools
from . import errors
from . import savTemplate
from physicsLab import circuit
from physicsLab import celestial
from physicsLab import electromagnetism
from .web._api import _User
from .savTemplate import Generate
from .circuit._circuit_core import crt_wire, Pin
from .enums import ExperimentType, Category, OpenMode, WireColor
from ._core import _Experiment, _ExperimentStack, _check_not_closed, ElementBase
from ._typing import num_type, Optional, Union, List, overload, Tuple, Self

def _get_all_pl_sav() -> List[str]:
    ''' 获取所有物实存档的文件名 '''
    savs = [i for i in os.walk(_Experiment.SAV_PATH_DIR)][0][-1]
    return [aSav for aSav in savs if aSav.endswith('.sav')]

def _open_sav(sav_path) -> dict:
    ''' 打开一个存档, 返回存档对应的dict
        @param sav_path: 存档的绝对路径
    '''
    def encode_sav(path: str, encoding: str) -> Optional[dict]:
        try:
            with open(path, encoding=encoding) as f:
                d = json.loads(f.read().replace('\n', ''))
        except (json.decoder.JSONDecodeError, UnicodeDecodeError): # 文件不是物实存档
            return None
        else:
            return d

    assert os.path.exists(sav_path)

    res = encode_sav(sav_path, "utf-8")
    if res is not None:
        return res

    try:
        import chardet # type: ignore
    except ImportError:
        for encoding in ("utf-8-sig", "gbk"):
            res = encode_sav(sav_path, encoding)
            if res is not None:
                return res
    else:
        with open(sav_path, "rb") as f:
            encoding = chardet.detect(f.read())["encoding"]
        res = encode_sav(sav_path, encoding)
        if res is not None:
            return res

    raise errors.InvalidSavError

def search_experiment(sav_name: str) -> Tuple[Optional[str], Optional[dict]]:
    ''' 检测实验是否存在
        @param sav_name: 存档名

        若存在则返回存档对应的文件名, 若不存在则返回None
    '''
    if not isinstance(sav_name, str):
        raise TypeError

    for a_sav in _get_all_pl_sav():
        try:
            sav = _open_sav(os.path.join(_Experiment.SAV_PATH_DIR, a_sav))
        except errors.InvalidSavError:
            continue
        if sav.get("InternalName") == sav_name:
            return a_sav, sav

    return None, None

class Experiment(_Experiment):
    _user: Optional[_User] = None

    @overload
    def __init__(self, open_mode: OpenMode, filepath: Union[str, pathlib.Path]) -> None:
        ''' 根据存档对应的文件路径打开存档
            @open_mode = OpenMode.load_by_filepath
            @filepath: 存档对应的文件的完整路径
        '''

    @overload
    def __init__(self, open_mode: OpenMode, sav_name: str) -> None:
        ''' 根据存档名打开存档
            @open_mode = OpenMode.load_by_sav_name
            @sav_name: 存档的名字
        '''

    @overload
    def __init__(
            self,
            open_mode: OpenMode,
            content_id: str,
            category: Category,
            /, *,
            user: Optional[_User] = None
    ) -> None:
        ''' 从物实服务器中获取存档
            @open_mode = OpenMode.load_by_plar_app
            @content_id: 物实 实验/讨论 的id
            @category: 实验区还是黑洞区
            @user: 执行获取实验操作的用户, 若未指定则会创建一个临时匿名用户执行该操作 (会导致程序变慢)
        '''

    @overload
    def __init__(
            self,
            open_mode: OpenMode,
            sav_name: str,
            experiment_type: ExperimentType,
            /, *,
            force_crt: bool = False
    ) -> None:
        ''' 创建一个新实验
            @open_mode = OpenMode.crt
            @sav_name: 存档的名字
            @experiment_type: 实验类型
            @force_crt: 强制创建一个实验, 若已存在则覆盖已有实验
        '''

    def __init__(self, open_mode: OpenMode, *args, **kwargs) -> None:
        if not isinstance(open_mode, OpenMode) or len(args) == 0:
            raise TypeError

        self.open_mode: OpenMode = open_mode
        # 通过坐标索引元件
        self._position2elements = {}
        # 通过元件的Identifier索引元件
        self._id2element = {}
        # 通过index（元件生成顺序）索引元件
        self.Elements = []

        # 尽管读取存档时会将元件的字符串一并读入, 但只有在调用 load_elements 将元件的信息
        # 导入self.Elements与self._element_position之后, 元件信息才被完全导入
        if open_mode == OpenMode.load_by_filepath:
            sav_name, *rest = args
            if not isinstance(sav_name, (str, pathlib.Path)) or len(rest) != 0:
                raise TypeError
            if isinstance(sav_name, pathlib.Path):
                sav_name = str(sav_name)

            self.SAV_PATH = os.path.abspath(sav_name)

            if not os.path.exists(self.SAV_PATH):
                raise FileNotFoundError(f"\"{self.SAV_PATH}\" not found")
            if _ExperimentStack.inside(self):
                raise errors.ExperimentOpenedError

            _temp = _open_sav(self.SAV_PATH)

            if "Experiment" in _temp.keys():
                self.PlSav = _temp
            else: # 读取物实导出的存档只含有.sav的Experiment部分
                if _temp["Type"] == ExperimentType.Circuit.value:
                    self.PlSav = copy.deepcopy(savTemplate.Circuit)
                elif _temp["Type"] == ExperimentType.Celestial.value:
                    self.PlSav = copy.deepcopy(savTemplate.Celestial)
                elif _temp["Type"] == ExperimentType.Electromagnetism.value:
                    self.PlSav = copy.deepcopy(savTemplate.Electromagnetism)
                else:
                    errors.unreachable()

                self.PlSav["Experiment"] = _temp
                # .sav的Experiment不包含存档名, 会产生一个匿名存档
            self.__load()
        elif open_mode == OpenMode.load_by_sav_name:
            sav_name, *rest = args
            if not isinstance(sav_name, str) or len(rest) != 0:
                raise TypeError

            filename, _plsav = search_experiment(sav_name)
            if filename is None:
                raise errors.ExperimentNotExistError(f'No such experiment "{sav_name}"')

            self.SAV_PATH = os.path.join(_Experiment.SAV_PATH_DIR, filename)
            if _ExperimentStack.inside(self):
                raise errors.ExperimentOpenedError

            assert _plsav is not None
            self.PlSav = _plsav
            self.__load()
        elif open_mode == OpenMode.load_by_plar_app:
            content_id, category, *rest = args

            if not isinstance(content_id, str) or not isinstance(category, Category) or len(rest) != 0:
                raise TypeError
            user = kwargs.get("user")
            if not isinstance(user, (_User, type(None))):
                raise TypeError

            if user is None:
                if Experiment._user is None:
                    Experiment._user = _User()
                user = Experiment._user

            self.SAV_PATH = os.path.join(_Experiment.SAV_PATH_DIR, f"{content_id}.sav")
            if _ExperimentStack.inside(self):
                    raise errors.ExperimentOpenedError

            # TODO 如果从物实读取的实验不存在的话，将异常转换为 ExperimentNotExistError
            assert user is not None
            _summary = user.get_summary(content_id, category)["Data"]
            del _summary["$type"]
            _experiment = user.get_experiment(_summary["ContentID"])["Data"]
            del _experiment["$type"]

            if _experiment["Type"] == ExperimentType.Circuit.value:
                self.PlSav = copy.deepcopy(savTemplate.Circuit)
            elif _experiment["Type"] == ExperimentType.Celestial.value:
                self.PlSav = copy.deepcopy(savTemplate.Celestial)
            elif _experiment["Type"] == ExperimentType.Electromagnetism.value:
                self.PlSav = copy.deepcopy(savTemplate.Electromagnetism)
            else:
                errors.unreachable()

            self.PlSav["Experiment"] = _experiment
            self.PlSav["Summary"] = _summary
            self.PlSav["InternalName"] = _summary["Subject"]
            self.__load()
        elif open_mode == OpenMode.crt:
            sav_name, experiment_type, *rest = args

            if not isinstance(sav_name, str) \
                    or not isinstance(experiment_type, ExperimentType) \
                    or len(rest) != 0:
                raise TypeError
            force_crt = kwargs.get("force_crt", False)
            if not isinstance(force_crt, bool):
                raise TypeError

            filepath, _ = search_experiment(sav_name)
            if not force_crt and filepath is not None:
                raise errors.ExperimentExistError
            elif force_crt and filepath is not None:
                # TODO 要是在一个force_crt的实验中又force_crt这个实验呢？
                path = os.path.join(_Experiment.SAV_PATH_DIR, filepath)
                os.remove(path)
                if os.path.exists(path.replace(".sav", ".jpg")): # 用存档生成的实验无图片，因此可能删除失败
                    os.remove(path.replace(".sav", ".jpg"))

            self.experiment_type = experiment_type
            self.SAV_PATH = os.path.join(_Experiment.SAV_PATH_DIR, f"{_tools.randString(34)}.sav")

            if self.experiment_type == ExperimentType.Circuit:
                self._is_elementXYZ: bool = False
                self.PlSav: dict = copy.deepcopy(savTemplate.Circuit)
                self.Wires: set = set() # Set[Wire] # 存档对应的导线
                # 存档对应的StatusSave, 存放实验元件，导线（如果是电学实验的话）
                self.CameraSave: dict = {
                    "Mode": 0, "Distance": 2.7, "VisionCenter": Generate, "TargetRotation": Generate
                }
                self.VisionCenter: _tools.position = _tools.position(0, -0.45, 1.08)
                self.TargetRotation: _tools.position = _tools.position(50, 0, 0)
            elif self.experiment_type == ExperimentType.Celestial:
                self.PlSav: dict = copy.deepcopy(savTemplate.Celestial)
                self.CameraSave: dict = {
                    "Mode": 2, "Distance": 2.75, "VisionCenter": Generate, "TargetRotation": Generate
                }
                self.VisionCenter: _tools.position = _tools.position(0 ,0, 1.08)
                self.TargetRotation: _tools.position = _tools.position(90, 0, 0)
            elif self.experiment_type == ExperimentType.Electromagnetism:
                self.PlSav: dict = copy.deepcopy(savTemplate.Electromagnetism)
                self.CameraSave: dict = {
                    "Mode": 0, "Distance": 3.25, "VisionCenter": Generate, "TargetRotation": Generate,
                }
                self.VisionCenter: _tools.position = _tools.position(0, 0 ,0.88)
                self.TargetRotation: _tools.position = _tools.position(90, 0, 0)
            else:
                errors.unreachable()

            self.__entitle(sav_name)
        else:
            errors.unreachable()

        assert isinstance(self.open_mode, OpenMode)
        assert isinstance(self._position2elements, dict)
        assert isinstance(self._id2element, dict)
        assert isinstance(self.Elements, list)
        assert isinstance(self.SAV_PATH, str)
        assert isinstance(self.PlSav, dict)
        assert isinstance(self.CameraSave, dict)
        assert isinstance(self.VisionCenter, _tools.position)
        assert isinstance(self.TargetRotation, _tools.position)
        assert isinstance(self.experiment_type, ExperimentType)
        if self.experiment_type == ExperimentType.Circuit:
            assert isinstance(self.Wires, set)
            assert isinstance(self._is_elementXYZ, bool)

        _ExperimentStack.push(self)

        if self.open_mode == OpenMode.load_by_sav_name \
                or self.open_mode == OpenMode.load_by_filepath \
                or self.open_mode == OpenMode.load_by_plar_app:
            status_sav = json.loads(self.PlSav["Experiment"]["StatusSave"])

            if self.experiment_type == ExperimentType.Circuit:
                self.__load_elements(status_sav["Elements"])
                self.__load_wires(status_sav["Wires"])
            elif self.experiment_type == ExperimentType.Celestial:
                self.__load_elements(list(status_sav["Elements"].values()))
            elif self.experiment_type == ExperimentType.Electromagnetism:
                self.__load_elements(status_sav["Elements"])
            else:
                errors.unreachable()

    def __load(self) -> None:
        assert isinstance(self.PlSav["Experiment"]["CameraSave"], str)
        self.CameraSave = json.loads(self.PlSav["Experiment"]["CameraSave"])
        temp = eval(f"({self.CameraSave['VisionCenter']})")
        self.VisionCenter: _tools.position = _tools.position(temp[0], temp[2], temp[1]) # x, z, y
        temp = eval(f"({self.CameraSave['TargetRotation']})")
        self.TargetRotation: _tools.position = _tools.position(temp[0], temp[2], temp[1]) # x, z, y

        if self.PlSav["Summary"] is None:
            self.PlSav["Summary"] = savTemplate.Circuit["Summary"]

        if self.PlSav["Experiment"]["Type"] == ExperimentType.Circuit.value:
            self.experiment_type = ExperimentType.Circuit
            # 是否将该实验在全局范围中设置为元件坐标系
            self._is_elementXYZ: bool = False
            self.Wires: set = set() # Set[Wire] # 存档对应的导线
        elif self.PlSav["Experiment"]["Type"] == ExperimentType.Celestial.value:
            self.experiment_type = ExperimentType.Celestial
        elif self.PlSav["Experiment"]["Type"] == ExperimentType.Electromagnetism.value:
            self.experiment_type = ExperimentType.Electromagnetism
        else:
            errors.unreachable()

    def __load_wires(self, _wires: list) -> None:
        assert self.experiment_type == ExperimentType.Circuit

        for wire_dict in _wires:
            if wire_dict["ColorName"][0] == '蓝':
                color = WireColor.blue
            elif wire_dict["ColorName"][0] == '红':
                color = WireColor.red
            elif wire_dict["ColorName"][0] == '绿':
                color = WireColor.green
            elif wire_dict["ColorName"][0] == '黄':
                color = WireColor.yellow
            elif wire_dict["ColorName"][0] == '黑':
                color = WireColor.black
            else:
                errors.unreachable()

            crt_wire(
                Pin(self.get_element_from_identifier(wire_dict["Source"]), wire_dict["SourcePin"]),
                Pin(self.get_element_from_identifier(wire_dict["Target"]), wire_dict["TargetPin"]),
                color=color,
            )

    def __load_elements(self, _elements: list) -> None:
        assert isinstance(_elements, list)

        for element in _elements:
            # Unity 采用左手坐标系
            x, z, y = eval(f"({element['Position']})")

            # 实例化对象
            if self.experiment_type == ExperimentType.Circuit:
                if element["ModelID"] == "Simple Instrument":
                    from .circuit.elements.otherCircuit import Simple_Instrument
                    pitches = []
                    for attr, val in element["Properties"].items():
                        if attr.startswith("音高"):
                            pitches.append(int(val))

                    obj = Simple_Instrument(
                        x, y, z,
                        pitches=pitches,
                        identifier=element["Identifier"],
                        elementXYZ=False,
                        instrument=int(element["Properties"].get("乐器", 0)),
                        volume=element["Properties"]["音量"],
                        rated_oltage=element["Properties"]["额定电压"],
                        is_ideal=bool(element["Properties"]["理想模式"]),
                        is_pulse=bool(element["Properties"]["脉冲"])
                    )
                else:
                    obj = self.crt_element(
                        element["ModelID"], x, y, z, elementXYZ=False, identifier=element["Identifier"]
                    )
                    obj.data["Properties"] = element["Properties"]
                # 设置角度信息
                rotation = eval(f'({element["Rotation"]})')
                r_x, r_y, r_z = rotation[0], rotation[2], rotation[1]
                obj.set_rotation(r_x, r_y, r_z)

            elif self.experiment_type == ExperimentType.Celestial:
                obj = self.crt_element(element["Model"], x, y, z, identifier=element['Identifier'])
                obj.data = element
            elif self.experiment_type == ExperimentType.Electromagnetism:
                obj = self.crt_element(element["ModelID"], x, y, z, identifier=element['Identifier'])
                obj.data = element
            else:
                errors.unreachable()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # 如果无异常抛出且用户未在with语句里调用过.close(), 则保存存档并退出实验
        if _ExperimentStack.inside(self):
            if exc_type is None:
                self.save()
            self.close(delete=False)

    @_check_not_closed
    def crt_element(
            self,
            name: str,
            x: num_type,
            y: num_type,
            z: num_type,
            *args,
            **kwargs,
    ) -> ElementBase:
        ''' 通过元件的ModelID或其类名创建元件 '''
        if not isinstance(name, str) \
                or not isinstance(x, (int, float)) \
                or not isinstance(y, (int, float)) \
                or not isinstance(z, (int, float)):
            raise TypeError

        name = name.strip().replace(' ', '_').replace('-', '_')
        x, y, z = _tools.round_data(x), _tools.round_data(y), _tools.round_data(z)

        if self.experiment_type == ExperimentType.Circuit:
            if name == "555_Timer":
                return circuit.NE555(x, y, z, *args, **kwargs)
            elif name == "8bit_Input":
                return circuit.Eight_Bit_Input(x, y, z, *args, **kwargs)
            elif name == "8bit_Display":
                return circuit.Eight_Bit_Display(x, y, z, *args, **kwargs)
            else:
                return eval(f"circuit.{name}({x}, {y}, {z}, *{args}, **{kwargs})")
        elif self.experiment_type == ExperimentType.Celestial:
            return eval(f"celestial.{name}({x}, {y}, {z}, **{kwargs})")
        elif self.experiment_type == ExperimentType.Electromagnetism:
            return eval(f"electromagnetism.{name}({x}, {y}, {z}, **{kwargs})")
        else:
            errors.unreachable()
