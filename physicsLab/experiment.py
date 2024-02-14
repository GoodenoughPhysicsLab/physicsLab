# -*- coding: utf-8 -*-
import os
import json
import copy
import time
import platform

from physicsLab import  _tools
from physicsLab import errors
from physicsLab import savTemplate
from physicsLab import _colorUtils
from .savTemplate import Generate
from .experimentType import experimentType
from .typehint import Union, Optional, List, Dict, numType

# 最新被操作的存档
class stack_Experiment:
    data: List["Experiment"] = []

    def __new__(cls):
        return cls

    @classmethod
    def push(cls, data: "Experiment") -> None:
        if not isinstance(data, Experiment):
            raise TypeError

        cls.data.append(data)

    @classmethod
    def top(cls) -> "Experiment":
        if len(cls.data) == 0:
            raise errors.ExperimentError("no experiment can be operated(experiment stack is empty)")

        return cls.data[-1]

    @classmethod
    def pop(cls) -> "Experiment":
        res = cls.top()
        cls.data.pop()
        return res

# 获取当前正在操作的存档
def get_Experiment() -> "Experiment":
    return stack_Experiment.top()

# 实验（存档）类
class Experiment:
    FILE_HEAD = "physicsLabSav"
    if platform.system() == "Windows":
        from getpass import getuser
        FILE_HEAD = f"C:/Users/{getuser()}/AppData/LocalLow/CIVITAS/Quantum Physics/Circuit"

    def __init__(self, sav_name: Optional[str] = None) -> None:
        self.is_open_or_crt: bool = False
        self.is_open: bool = False
        self.is_crt: bool = False
        self.is_read: bool = False
        self.is_elementXYZ: bool = False

        self.FileName: Optional[str] = None # 存档的文件名
        self.SavPath: Optional[str] = None # 存档的完整路径, 为 f"{experiment.FILE_HEAD}/{self.FileName}"
        # 通过坐标索引元件
        self.elements_Position: Dict[tuple, list] = {}  # key: self._position, value: List[self...]
        # 通过index（元件生成顺序）索引元件
        self.Elements: list = [] # List[CircuitBase]

        if sav_name is not None:
            self.open_or_crt(sav_name)

    # 通过_arguments["Identifier"]获取元件
    def get_element_from_identifier(self, identifier: str):
        for element in self.Elements:
            if element._arguments["Identifier"] == identifier:
                return element
        raise errors.ExperimentError

    def __open(self) -> None:
        self.is_open = True
        self.CameraSave = json.loads(self.PlSav["Experiment"]["CameraSave"])
        temp = eval(f"({self.CameraSave['VisionCenter']})")
        self.VisionCenter: _tools.position = _tools.position(temp[0], temp[2], temp[1]) # x, z, y
        temp = eval(f"({self.CameraSave['TargetRotation']})")
        self.TargetRotation: _tools.position = _tools.position(temp[0], temp[2], temp[1]) # x, z, y

        self.ExperimentType: experimentType = {
            experimentType.Circuit.value: experimentType.Circuit,
            experimentType.Celestial.value: experimentType.Celestial,
            experimentType.Electromagnetism.value: experimentType.Electromagnetism
        }[self.PlSav["Type"]]

        if self.PlSav["Summary"] is None:
            self.PlSav["Summary"] = savTemplate.Circuit["Summary"]

        if self.ExperimentType == experimentType.Circuit:
            self.Wires: list = [] # List[Wire] # 存档对应的导线
            # 存档对应的StatusSave, 存放实验元件，导线（如果是电学实验的话）
            self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": [], "Wires": []}

        elif self.ExperimentType == experimentType.Celestial:
            self.StatusSave: dict = {"MainIdentifier": None, "Elements": {}, "WorldTime": 0.0,
                                    "ScalingName": "内太阳系", "LengthScale": 1.0, "SizeLinear": 0.0001,
                                    "SizeNonlinear": 0.5, "StarPresent": False, "Setting": None}

        elif self.ExperimentType == experimentType.Electromagnetism:
            self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": []}

    # 打开一个指定的sav文件 (支持输入本地实验的名字或sav文件名)
    def open(self, sav_name : str) -> "Experiment":
        if self.is_open_or_crt:
            raise errors.experimentExistError
        self.is_open_or_crt = True
        stack_Experiment.push(self)

        sav_name = sav_name.strip()
        if sav_name.endswith('.sav'):
            self.FileName = sav_name
            self.SavPath = f"{Experiment.FILE_HEAD}/{sav_name}"
            if not os.path.exists(self.SavPath):
                stack_Experiment.pop()
                raise errors.OpenExperimentError(f'No such experiment "{sav_name}"')
            self.PlSav = _open_sav(self.SavPath)
            self.__open()
            return self

        self.FileName = search_Experiment(sav_name)
        self.SavPath = f"{Experiment.FILE_HEAD}/{self.FileName}"
        if self.FileName is None:
            stack_Experiment.pop()
            raise errors.OpenExperimentError(f'No such experiment "{sav_name}"')

        self.PlSav = search_Experiment.sav
        self.__open()

        return self

    def __crt(self, sav_name: str, experiment_type: experimentType = experimentType.Circuit) -> None:
        self.is_crt = True
        self.ExperimentType = experiment_type

        self.FileName = f"{_tools.randString(34)}.sav"
        self.SavPath = f"{Experiment.FILE_HEAD}/{self.FileName}"

        if self.ExperimentType == experimentType.Circuit:
            self.PlSav: dict = copy.deepcopy(savTemplate.Circuit)
            self.Wires = [] # List[Wire] # 存档对应的导线
            # 存档对应的StatusSave, 存放实验元件，导线（如果是电学实验的话）
            self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": [], "Wires": []}
            self.CameraSave: dict = {"Mode": 0, "Distance": 2.7, "VisionCenter": Generate, "TargetRotation": Generate}
            self.VisionCenter: _tools.position = _tools.position(0, 1.08, -0.45)
            self.TargetRotation: _tools.position = _tools.position(50, 0, 0)

        elif self.ExperimentType == experimentType.Celestial:
            self.PlSav: dict = copy.deepcopy(savTemplate.Celestial)
            self.StatusSave: dict = {"MainIdentifier": None, "Elements": {}, "WorldTime": 0.0,
                                     "ScalingName": "内太阳系", "LengthScale": 1.0, "SizeLinear": 0.0001,
                                     "SizeNonlinear": 0.5, "StarPresent": False, "Setting": None}
            self.CameraSave: dict = {"Mode": 2, "Distance": 2.75, "VisionCenter": Generate, "TargetRotation": Generate}
            self.VisionCenter: _tools.position = _tools.position(0 ,0, 1.08)
            self.TargetRotation: _tools.position = _tools.position(90, 0, 0)

        elif self.ExperimentType == experimentType.Electromagnetism:
            self.PlSav: dict = copy.deepcopy(savTemplate.Electromagnetism)
            self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": []}
            self.CameraSave: dict = {"Mode": 0, "Distance": 3.25, "VisionCenter": Generate, "TargetRotation": Generate}
            self.VisionCenter: _tools.position = _tools.position(0, 0 ,0.88)
            self.TargetRotation: _tools.position = _tools.position(90, 0, 0)

        self.entitle(sav_name)

    # 创建存档，输入为存档名 sav_name: 存档名; experiment_type: 实验类型; force_crt: 不论实验是否已经存在,强制创建
    def crt(self, sav_name: str, experiment_type: experimentType = experimentType.Circuit, force_crt: bool=False) -> "Experiment":
        if self.is_open_or_crt:
            raise errors.experimentExistError
        self.is_open_or_crt = True

        if not isinstance(sav_name, str) or not isinstance(experiment_type, experimentType):
            raise TypeError

        search = search_Experiment(sav_name)
        if not force_crt and search is not None:
            raise errors.crtExperimentFailError
        elif force_crt and search is not None:
            path = f"{Experiment.FILE_HEAD}/{search}"
            os.remove(path)
            if os.path.exists(path.replace(".sav", ".jpg")): # 用存档生成的实验无图片，因此可能删除失败
                os.remove(path.replace(".sav", ".jpg"))

        stack_Experiment.push(self)

        self.__crt(sav_name, experiment_type)
        return self

    # 先尝试打开实验, 若失败则创建实验
    def open_or_crt(self, savName: str, experimentType: experimentType = experimentType.Circuit) -> "Experiment":
        if self.is_open_or_crt:
            raise errors.experimentExistError
        self.is_open_or_crt = True

        if not isinstance(savName, str):
            raise TypeError
        stack_Experiment.push(self)

        self.FileName = search_Experiment(savName)
        if self.FileName is not None:
            self.SavPath = f"{Experiment.FILE_HEAD}/{self.FileName}"
            self.PlSav = search_Experiment.sav
            self.__open()
        else:
            self.__crt(savName, experimentType)
        return self

    # 读取实验已有状态
    def read(self) -> "Experiment":
        if self.SavPath is None: # 是否已.open()或.crt()
            raise TypeError
        if self.is_read:
            errors.warning("experiment has been read")
            return self
        self.is_read = True
        if self.is_crt:
            errors.warning("can not read because you create this experiment")
            return self

        status_sav = json.loads(self.PlSav["Experiment"]["StatusSave"])
        # 元件
        _local_Elements = status_sav["Elements"]

        for element in _local_Elements:
            # 坐标标准化 (消除浮点误差)
            position = eval(f"({element['Position']})")
            x, y, z = position[0], position[2], position[1]

            # 实例化对象
            from physicsLab.element import crt_Element

            if self.ExperimentType == experimentType.Circuit:
                if element["ModelID"] == "Simple Instrument":
                    from .circuit.elements.otherCircuit import Simple_Instrument
                    obj = Simple_Instrument(
                        x, y, z, elementXYZ=False,
                        instrument=element["Properties"]["乐器"],
                        pitch=element["Properties"]["音高"],
                        velocity=element["Properties"]["音量"],
                        rated_oltage=element["Properties"]["额定电压"],
                        is_ideal_model=bool(element["Properties"]["理想模式"]),
                        is_single=int(element["Properties"]["脉冲"])
                    )
                    for attr, val in element["Properties"].items():
                        if attr.startswith("音高"):
                            obj.add_note(val)
                else:
                    obj = crt_Element(element["ModelID"], x, y, z, elementXYZ=False)
            else:
                obj = crt_Element(element["ModelID"], x, y, z) # type: ignore -> num type: int | float

            rotation = eval(f'({element["Rotation"]})')
            r_x, r_y, r_z = rotation[0], rotation[2], rotation[1]
            obj.set_Rotation(r_x, r_y, r_z)
            obj._arguments['Identifier'] = element['Identifier']
            from .circuit.elements.logicCircuit import Logic_Input, eight_bit_Input
            # 如果obj是逻辑输入
            if isinstance(obj, Logic_Input) and element['Properties'].get('开关') == 1:
                obj.set_highLevel()
            # 如果obj是8位输入器
            elif isinstance(obj, eight_bit_Input):
                obj._arguments['Statistics'] = element['Statistics']
                obj._arguments['Properties']['十进制'] = element['Properties']['十进制']

        # 导线
        if self.ExperimentType == experimentType.Circuit:
            from .circuit.wire import Wire, Pin
            self.Wires = [
                Wire(
                    Pin(self.get_element_from_identifier(wire_dict["Source"]), wire_dict["SourcePin"]),
                    Pin(self.get_element_from_identifier(wire_dict["Target"]), wire_dict["TargetPin"]),
                    wire_dict["ColorName"][0] # e.g. "蓝"
                )
                for wire_dict in status_sav['Wires']
            ]

    # 以物实存档的格式导出实验
    def write(self, extra_filepath: Optional[str] = None, ln: bool = False, no_pop: bool = False) -> "Experiment":
        def _format_StatusSave(stringJson: str) -> str:
            stringJson = stringJson.replace('{\\\"ModelID', '\n      {\\\"ModelID') # format element json
            stringJson = stringJson.replace('DiagramRotation\\\": 0}]', 'DiagramRotation\\\": 0}\n    ]') # format end element json
            stringJson = stringJson.replace('{\\\"Source', '\n      {\\\"Source')
            stringJson = stringJson.replace(u"色导线\\\"}]}", "色导线\\\"}\n    ]}")
            return stringJson

        if self.SavPath is None: # 检查是否已经.open()或.crt()
            raise errors.ExperimentError("write before open or crt")
        if self.is_open_or_crt is True:
            self.is_open_or_crt = False
        else:
            raise errors.ExperimentError("write before open or crt")

        if not no_pop:
            stack_Experiment.pop()

        self.PlSav["Experiment"]["CreationDate"] = int(time.time() * 1000)
        self.PlSav["Summary"]["CreationDate"] = int(time.time() * 1000)

        self.CameraSave["VisionCenter"] = f"{self.VisionCenter.x},{self.VisionCenter.z},{self.VisionCenter.y}"
        self.CameraSave["TargetRotation"] = f"{self.TargetRotation.x},{self.TargetRotation.z},{self.TargetRotation.y}"
        self.PlSav["Experiment"]["CameraSave"] = json.dumps(self.CameraSave)

        self.StatusSave["Elements"] = [a_element._arguments for a_element in self.Elements]
        if self.ExperimentType == experimentType.Circuit:
            self.StatusSave["Wires"] = [a_wire.release() for a_wire in self.Wires]
        self.PlSav["Experiment"]["StatusSave"] = json.dumps(self.StatusSave, ensure_ascii=False, separators=(',', ': '))

        context: str = json.dumps(self.PlSav, indent=2, ensure_ascii=False, separators=(',', ': '))
        if ln:
            context = _format_StatusSave(context)

        with open(self.SavPath, "w", encoding="utf-8") as f:
            f.write(context)
        if extra_filepath is not None:
            if not extra_filepath.endswith(".sav"):
                extra_filepath += ".sav"
            with open(extra_filepath, "w", encoding="utf-8") as f:
                f.write(context)

        # 编译成功，打印信息
        if self.is_open:
            status = "update"
        elif self.is_crt:
            status = "create"
        if self.ExperimentType == experimentType.Circuit:
            _colorUtils.color_print(
                f"Successfully {status} experiment \"{self.PlSav['InternalName']}\"! "
                f"{self.Elements.__len__()} elements, {self.Wires.__len__()} wires.",
                color=_colorUtils.COLOR.GREEN
            )
        else:
            _colorUtils.color_print(
                f"Successfully {status} experiment \"{self.PlSav['InternalName']}\"! "
                f"{self.Elements.__len__()} elements.",
                color=_colorUtils.COLOR.GREEN
            )

        return self

    # 删除存档
    def delete(self, warning_status: Optional[bool]=None) -> None:
        if self.SavPath is None:
            raise TypeError

        if os.path.exists(self.SavPath): # 如果一个实验被创建但还未被写入, 就会触发错误
            os.remove(self.SavPath)
            _colorUtils.color_print(f"Successfully delete experiment {self.PlSav['InternalName']}({self.FileName})!", _colorUtils.COLOR.BLUE)
        else:
            if warning_status is None:
                warning_status = errors.warning_status
            errors.warning(f"experiment {self.PlSav['InternalName']}({self.FileName}) do not exist.", warning_status)

        if os.path.exists(self.SavPath.replace(".sav", ".jpg")): # 用存档生成的实验无图片，因此可能删除失败
            os.remove(self.SavPath.replace(".sav", ".jpg"))

        stack_Experiment.pop()

    # 退出实验而不进行任何操作
    def exit(self) -> None:
        stack_Experiment.pop()

    # 对存档名进行重命名
    def entitle(self, sav_name: str) -> "Experiment":
        if not isinstance(sav_name, str):
            raise TypeError

        self.PlSav["Summary"]["Subject"] = sav_name
        self.PlSav["InternalName"] = sav_name

        return self

    # 使用notepad打开改存档
    def show(self) -> "Experiment":
        if self.SavPath is None:
            raise TypeError

        if platform.system() != "Windows":
            return self

        os.popen(f'notepad {self.SavPath}')
        return self

    # 生成与发布实验有关的存档内容
    def publish(self, title: Optional[str] = None, introduction: Optional[str] = None) -> "Experiment":
        # 发布实验时输入实验介绍
        def introduce_Experiment(introduction: Union[str, None]) -> None:
            if introduction is not None:
                self.PlSav['Summary']['Description'] = introduction.split('\n')

        # 发布实验时输入实验标题
        def name_Experiment(title: Union[str, None]) -> None:
            if title is not None:
                self.PlSav['Summary']['Subject'] = title

        introduce_Experiment(introduction)
        name_Experiment(title)

        return self

    # 设置实验者的视角
    # x, y, z : 实验者观察的坐标
    # distance: 实验者到(x, y, z)的距离
    # rotation: 实验者观察的角度
    def observe(self,
                x: Optional[numType] = None,
                y: Optional[numType] = None,
                z: Optional[numType] = None,
                distance: Optional[numType] = None,
                rotation_x: Optional[numType] = None,
                rotation_y: Optional[numType] = None,
                rotation_z: Optional[numType] = None
    ) -> "Experiment":
        if self.SavPath is None:
            raise TypeError

        if x is None:
            x = self.VisionCenter.x
        if y is None:
            y = self.VisionCenter.y
        if z is None:
            z = self.VisionCenter.z
        if distance is None:
            distance = self.CameraSave["Distance"]
        if rotation_x is None:
            rotation_x = self.TargetRotation.x
        if rotation_y is None:
            rotation_y = self.TargetRotation.y
        if rotation_z is None:
            rotation_z = self.TargetRotation.z

        if not isinstance(x, (int, float)):
            raise TypeError
        if not isinstance(y, (int, float)):
            raise TypeError
        if not isinstance(z, (int, float)):
            raise TypeError
        if not isinstance(distance, (int, float)):
            raise TypeError
        if not isinstance(rotation_x, (int, float)):
            raise TypeError
        if not isinstance(rotation_y, (int, float)):
            raise TypeError
        if not isinstance(rotation_z, (int, float)):
            raise TypeError

        self.VisionCenter = _tools.position(x, y, z)
        self.CameraSave["Distance"] = distance
        self.TargetRotation = _tools.position(rotation_x, rotation_y, rotation_z)

        return self

    # 与物实示波器图表有关的支持
    def graph(self) -> "Experiment":
        if self.SavPath is None:
            raise TypeError

        pass
        return self

    # 以physicsLab代码的形式导出实验
    def export(self, output_path: str = "temp.pl.py", sav_name: str = "temp") -> "Experiment":
        if self.SavPath is None:
            raise TypeError

        res: str = f"from physicsLab import *\nexp = Experiment('{sav_name}')\n"

        for a_element in self.Elements:
            res += f"{a_element._arguments['Identifier']} = {str(a_element)}\n"
        # 连接导线未完成(暂时不想调用更原始的primitive_crt_wire)
        for a_wire in self.Wires:
            res += str(a_wire) + '\n'
        res += "\nexp.write()"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(res)

        return self

# 仅供with时使用
class experiment:
    def __init__(self,
                 sav_name: str, # 实验名(非存档文件名)
                 read: bool = False, # 是否读取存档原有状态
                 delete: bool = False, # 是否删除实验
                 write: bool = True, # 是否写入实验
                 elementXYZ: bool = False, # 元件坐标系
                 experiment_type: experimentType = experimentType.Circuit, # 若创建实验，支持传入指定实验类型
                 extra_filepath: Optional[str] = None, # 将存档写入额外的路径
                 force_crt: bool = False, # 强制创建一个实验, 若已存在则删除已有实验
                 is_exit: bool = False, # 退出试验
    ):
        if not (
            isinstance(sav_name, str) and
            isinstance(read, bool) and
            isinstance(delete, bool) and
            isinstance(elementXYZ, bool) and
            isinstance(write, bool) and
            isinstance(experiment_type, experimentType)
        ) and (
            not isinstance(extra_filepath, str) and
            extra_filepath is not None
        ):
            raise TypeError

        self.savName: str = sav_name
        self.read: bool = read
        self.delete: bool = delete
        self.write: bool = write
        self.elementXYZ: bool = elementXYZ
        self.experimentType: experimentType = experiment_type
        self.extra_filepath: Optional[str] = extra_filepath
        self.force_crt = force_crt
        self.is_exit = is_exit

    # 上下文管理器，搭配with使用
    def __enter__(self) -> Experiment:
        if not self.force_crt:
            self._Experiment: Experiment = Experiment().open_or_crt(self.savName, self.experimentType)
        else:
            self._Experiment: Experiment = Experiment().crt(self.savName, self.experimentType, self.force_crt)

        if self.read:
            self._Experiment.read()
        if self.elementXYZ:
            if self._Experiment.ExperimentType != experimentType.Circuit:
                stack_Experiment.pop()
                raise errors.ExperimentTypeError
            import physicsLab.circuit.elementXYZ as _elementXYZ
            _elementXYZ.set_elementXYZ(True)

        return self._Experiment

    def __exit__(self, exc_type, exc_val, traceback) -> None:
        if exc_type is not None:
            self._Experiment.exit()
            return

        if self.is_exit:
            self._Experiment.exit()
            return
        if self.write:
            self._Experiment.write(extra_filepath=self.extra_filepath, no_pop=self.delete)
        if self.delete:
            self._Experiment.delete()
            return

# 获取所有物实存档的文件名
def getAllSav() -> List[str]:
    from os import walk
    savs = [i for i in walk(Experiment.FILE_HEAD)][0]
    savs = savs[savs.__len__() - 1]
    return [aSav for aSav in savs if aSav.endswith('sav')]

# 打开一个存档, 返回存档对应的dict
def _open_sav(sav_name) -> dict:
    def encode_sav(path: str, encoding: str) -> Optional[dict]:
        try:
            with open(path, encoding=encoding) as f:
                d = json.loads(f.read().replace('\n', ''))
        except (json.decoder.JSONDecodeError, UnicodeDecodeError): # 文件不是物实存档
            return None
        else:
            return d

    res = encode_sav(f"{Experiment.FILE_HEAD}/{sav_name}", "utf-8")
    if res is not None:
        return res

    try:
        import chardet
    except ImportError:
        for encoding in ("utf-8-sig", "gbk"):
            res = encode_sav(f"{Experiment.FILE_HEAD}/{sav_name}", encoding)
            if res is not None:
                return res
    else:
        with open(f"{Experiment.FILE_HEAD}/{sav_name}", "rb") as f:
            encoding = chardet.detect(f.read())["encoding"]
        return encode_sav(f"{Experiment.FILE_HEAD}/{sav_name}", encoding)

# 检测实验是否存在，输入为存档名，若存在则返回存档对应的文件名，若不存在则返回None
def search_Experiment(sav_name: str) -> Optional[str]:
    for aSav in getAllSav():
        sav = _open_sav(aSav)
        if sav["InternalName"] == sav_name:
            search_Experiment.sav = sav
            return aSav

    return None

# 以下为旧式调用方式， 为兼容代码
# 打开实验
def open_Experiment(sav_name: str) -> Experiment:
    return Experiment().open(sav_name)

# 创建存档，输入为存档名
def crt_Experiment(sav_name: str, experimentType: experimentType = experimentType.Circuit, force_crt: bool=False) -> Experiment:
    return Experiment().crt(sav_name, experimentType, force_crt)

# 先尝试打开实验，若失败则创建实验。只支持输入存档名
def open_or_crt_Experiment(sav_name: str, experimentType: experimentType = experimentType.Circuit) -> Experiment:
    return Experiment().open_or_crt(sav_name, experimentType)

# 读取sav文件已有的原件与导线
def read_Experiment() -> None:
    stack_Experiment.top().read()

# 将编译完成的json写入sav, ln: 是否将存档中字符串格式json换行
def write_Experiment(extra_filepath: Optional[str] = None, ln: bool = False, no_pop: bool = False) -> None:
    stack_Experiment.top().write(extra_filepath, ln, no_pop)

# 删除存档
def del_Experiment() -> None:
    stack_Experiment.top().delete()

# 使用notepad打开该存档
def show_Experiment() -> None:
    # os.system() 在文件夹有空格的时候会出现错误
    stack_Experiment.top().show()

# 重命名存档
def entitle_Experiment(sav_name: str):
    stack_Experiment.top().entitle(sav_name)

# 发布实验
def publish_Experiment(title: Optional[str] = None, introduction: Optional[str] = None) -> None:
    stack_Experiment.top().publish(title, introduction)

# 退出实验而不进行任何操作
def exit_Experiment():
    stack_Experiment.top().exit()