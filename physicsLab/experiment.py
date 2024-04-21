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
from .typehint import Union, Optional, List, Dict, numType, Self

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

def get_Experiment() -> "Experiment":
    ''' 获取当前正在操作的存档 '''
    return stack_Experiment.top()

class Experiment:
    ''' 实验（存档）类 '''
    FILE_HEAD = "physicsLabSav"
    if platform.system() == "Windows":
        from getpass import getuser
        FILE_HEAD = f"C:/Users/{getuser()}/AppData/LocalLow/CIVITAS/Quantum Physics/Circuit"

    def __init__(self, sav_name: Optional[str] = None) -> None:
        self.is_open_or_crt: bool = False
        self.is_open: bool = False
        self.is_crt: bool = False
        self.is_read: bool = False

        self.FileName: Optional[str] = None # 存档的文件名
        self.SavPath: Optional[str] = None # 存档的完整路径, 为 f"{experiment.FILE_HEAD}/{self.FileName}"
        # 通过坐标索引元件
        self.elements_Position: Dict[tuple, list] = {}  # key: self._position, value: List[self...]
        # 通过index（元件生成顺序）索引元件
        from .circuit.elements._elementBase import CircuitBase
        self.Elements: List[CircuitBase] = []

        if sav_name is not None:
            self.open_or_crt(sav_name)

    def get_element_from_identifier(self, identifier: str):
        ''' 通过_arguments["Identifier"]获取元件 '''
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
            self.is_elementXYZ: bool = False
            # 元件坐标系的坐标原点
            self.elementXYZ_origin_position: _tools.position = _tools.position(0, 0, 0)
            self.Wires: set = set() # Set[Wire] # 存档对应的导线
            # 存档对应的StatusSave, 存放实验元件，导线（如果是电学实验的话）
            self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": Generate, "Wires": Generate}

        elif self.ExperimentType == experimentType.Celestial:
            self.StatusSave: dict = {"MainIdentifier": None, "Elements": {}, "WorldTime": 0.0,
                                    "ScalingName": "内太阳系", "LengthScale": 1.0, "SizeLinear": 0.0001,
                                    "SizeNonlinear": 0.5, "StarPresent": False, "Setting": None}

        elif self.ExperimentType == experimentType.Electromagnetism:
            self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": []}

    def open(self, sav_name : str) -> Self:
        ''' 打开一个指定的sav文件 (支持输入本地实验的名字或sav文件名) '''
        if self.is_open_or_crt:
            raise errors.experimentExistError
        self.is_open_or_crt = True
        stack_Experiment.push(self)

        # .sav文件名
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

        # 存档名(本地实验的名字)
        self.FileName = search_Experiment(sav_name)
        self.SavPath = f"{Experiment.FILE_HEAD}/{self.FileName}"
        if self.FileName is None:
            stack_Experiment.pop()
            raise errors.OpenExperimentError(f'No such experiment "{sav_name}"')

        self.PlSav = search_Experiment.sav
        self.__open()

        return self

    def __crt(self,
              sav_name: str,
              experiment_type: experimentType = experimentType.Circuit
    ) -> None:
        self.is_crt = True
        self.ExperimentType = experiment_type

        self.FileName = f"{_tools.randString(34)}.sav"
        self.SavPath = f"{Experiment.FILE_HEAD}/{self.FileName}"

        if self.ExperimentType == experimentType.Circuit:
            self.is_elementXYZ: bool = False
            # 元件坐标系的坐标原点
            self.elementXYZ_origin_position: _tools.position = _tools.position(0, 0, 0)
            self.PlSav: dict = copy.deepcopy(savTemplate.Circuit)
            self.Wires: set = set() # Set[Wire] # 存档对应的导线
            # 存档对应的StatusSave, 存放实验元件，导线（如果是电学实验的话）
            self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": Generate, "Wires": Generate}
            self.CameraSave: dict = {
                "Mode": 0, "Distance": 2.7, "VisionCenter": Generate, "TargetRotation": Generate
            }
            self.VisionCenter: _tools.position = _tools.position(0, -0.45, 1.08)
            self.TargetRotation: _tools.position = _tools.position(50, 0, 0)

        elif self.ExperimentType == experimentType.Celestial:
            self.PlSav: dict = copy.deepcopy(savTemplate.Celestial)
            self.StatusSave: dict = {
                "MainIdentifier": None, "Elements": {}, "WorldTime": 0.0,
                "ScalingName": "内太阳系", "LengthScale": 1.0, "SizeLinear": 0.0001,
                "SizeNonlinear": 0.5, "StarPresent": False, "Setting": None
            }
            self.CameraSave: dict = {
                "Mode": 2, "Distance": 2.75, "VisionCenter": Generate, "TargetRotation": Generate
            }
            self.VisionCenter: _tools.position = _tools.position(0 ,0, 1.08)
            self.TargetRotation: _tools.position = _tools.position(90, 0, 0)

        elif self.ExperimentType == experimentType.Electromagnetism:
            self.PlSav: dict = copy.deepcopy(savTemplate.Electromagnetism)
            self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": []}
            self.CameraSave: dict = {
                "Mode": 0, "Distance": 3.25, "VisionCenter": Generate, "TargetRotation": Generate
            }
            self.VisionCenter: _tools.position = _tools.position(0, 0 ,0.88)
            self.TargetRotation: _tools.position = _tools.position(90, 0, 0)

        self.entitle(sav_name)

    def crt(self,
            sav_name: str,
            experiment_type: experimentType = experimentType.Circuit,
            force_crt: bool=False
    ) -> Self:
        ''' 创建存档，输入为存档名 sav_name: 存档名;
            experiment_type: 实验类型;
            force_crt: 不论实验是否已经存在,强制创建
        '''
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

    def open_or_crt(self,
                    savName: str,
                    experimentType: experimentType = experimentType.Circuit
    ) -> Self:
        ''' 先尝试打开实验, 若失败则创建实验 '''
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

    def read(self) -> Self:
        ''' 读取实验已有状态 '''
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
            from .circuit.elements.basicCircuit import Simple_Switch, SPDT_Switch, DPDT_Switch, Air_Switch

            if isinstance(obj, Logic_Input) and element['Properties'].get('开关') == 1:
                obj.set_highLevel()

            elif isinstance(obj, eight_bit_Input):
                obj._arguments['Statistics'] = element['Statistics']
                obj._arguments['Properties']['十进制'] = element['Properties']['十进制']

            elif isinstance(obj, Simple_Switch) and element["Properties"]["开关"] == 1:
                obj.turn_on_switch()

            elif isinstance(obj, Air_Switch) and element["Properties"]["开关"] == 1:
                obj.turn_on_switch()

            elif isinstance(obj, SPDT_Switch) or isinstance(obj, DPDT_Switch):
                if element["Properties"]["开关"] == 1:
                    obj.left_turn_on_switch()
                elif element["Properties"]["开关"] == 2:
                    obj.right_turn_on_switch()

        # 导线
        if self.ExperimentType == experimentType.Circuit:
            from .circuit.wire import Wire, Pin
            for wire_dict in status_sav['Wires']:
                self.Wires.add(
                    Wire(
                        Pin(self.get_element_from_identifier(wire_dict["Source"]), wire_dict["SourcePin"]),
                        Pin(self.get_element_from_identifier(wire_dict["Target"]), wire_dict["TargetPin"]),
                        wire_dict["ColorName"][0] # e.g. "蓝"
                    )
                )

        return self

    def write(self,
              extra_filepath: Optional[str] = None,
              ln: bool = False,
              no_pop: bool = False
    ) -> Self:
        ''' 以物实存档的格式导出实验 '''
        def _format_StatusSave(stringJson: str) -> str:
            stringJson = stringJson.replace( # format element json
                "{\\\"ModelID', '\n      {\\\"ModelID"
            )
            stringJson = stringJson.replace( # format end element json
                "DiagramRotation\\\": 0}]', 'DiagramRotation\\\": 0}\n    ]"
            )
            stringJson = stringJson.replace('{\\\"Source', '\n      {\\\"Source')
            stringJson = stringJson.replace("色导线\\\"}]}", "色导线\\\"}\n    ]}")
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
            status: str = "update"
        elif self.is_crt:
            status: str = "create"
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

    def delete(self, warning_status: Optional[bool]=None) -> None:
        ''' 删除存档 '''
        if self.SavPath is None:
            raise TypeError

        if os.path.exists(self.SavPath): # 如果一个实验被创建但还未被写入, 就会触发错误
            os.remove(self.SavPath)
            _colorUtils.color_print(
                f"Successfully delete experiment {self.PlSav['InternalName']}({self.FileName})!",
                _colorUtils.COLOR.BLUE
            )
        else:
            if warning_status is None:
                warning_status = errors.warning_status
            errors.warning(
                f"experiment {self.PlSav['InternalName']}({self.FileName}) do not exist.",
                warning_status
            )

        if os.path.exists(self.SavPath.replace(".sav", ".jpg")): # 用存档生成的实验无图片，因此可能删除失败
            os.remove(self.SavPath.replace(".sav", ".jpg"))

        stack_Experiment.pop()

    def exit(self) -> None:
        ''' 退出实验而不进行任何操作 '''
        stack_Experiment.pop()

    def entitle(self, sav_name: str) -> Self:
        ''' 对存档名进行重命名 '''
        if not isinstance(sav_name, str):
            raise TypeError

        self.PlSav["Summary"]["Subject"] = sav_name
        self.PlSav["InternalName"] = sav_name

        return self

    def show(self) -> Self:
        ''' 使用notepad打开改存档 '''
        if self.SavPath is None:
            raise TypeError

        if platform.system() != "Windows":
            return self

        os.popen(f'notepad {self.SavPath}')
        return self

    def publish(self, title: Optional[str] = None, introduction: Optional[str] = None) -> Self:
        ''' 生成与发布实验有关的存档内容 '''
        def introduce_Experiment(introduction: Union[str, None]) -> None:
            '''  发布实验时输入实验介绍 '''
            if introduction is not None:
                self.PlSav['Summary']['Description'] = introduction.split('\n')

        def name_Experiment(title: Union[str, None]) -> None:
            ''' 发布实验时输入实验标题 '''
            if title is not None:
                self.PlSav['Summary']['Subject'] = title

        introduce_Experiment(introduction)
        name_Experiment(title)

        return self

    def observe(self,
                x: Optional[numType] = None,
                y: Optional[numType] = None,
                z: Optional[numType] = None,
                distance: Optional[numType] = None,
                rotation_x: Optional[numType] = None,
                rotation_y: Optional[numType] = None,
                rotation_z: Optional[numType] = None
    ) -> Self:
        ''' 设置实验者的视角
            x, y, z : 实验者观察的坐标
            distance: 实验者到(x, y, z)的距离
            rotation: 实验者观察的角度
        '''
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

    def graph(self) -> Self:
        ''' 与物实示波器图表有关的支持 '''
        if self.SavPath is None:
            raise TypeError

        pass
        return self

    def export(self, output_path: str = "temp.pl.py", sav_name: str = "temp") -> Self:
        ''' 以physicsLab代码的形式导出实验 '''
        if self.SavPath is None:
            raise TypeError

        res: str = f"from physicsLab import *\nexp = Experiment('{sav_name}')\n"

        for a_element in self.Elements:
            res += f"e{a_element.get_Index()} = {str(a_element)}\n"
        for a_wire in self.Wires:
            res += str(a_wire) + '\n'
        res += "\nexp.write()"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(res)

        return self

    def merge(self,
              other: "Experiment",
              x: numType = 0,
              y: numType = 0,
              z: numType = 0,
              elementXYZ: Optional[bool] = None
    ) -> Self:
        ''' 合并另一实验
            x, y, z, elementXYZ为重新设置要合并的实验的坐标系原点在self的坐标系的位置
        '''
        if self.SavPath is None:
            raise TypeError
        if other.SavPath is None:
            raise TypeError

        if self is other:
            return self

        identifier_to_element: dict = {}

        for a_element in other.Elements:
            a_element = copy.deepcopy(a_element, memo={id(a_element.experiment): self})
            e_x, e_y, e_z = a_element.get_Position()
            if self.ExperimentType == experimentType.Circuit:
                from .circuit.elementXYZ import xyzTranslate, translateXYZ
                if elementXYZ and not a_element.is_elementXYZ:
                    e_x, e_y, e_z = translateXYZ(e_x, e_y, e_z, a_element.is_bigElement)
                elif not elementXYZ and a_element.is_elementXYZ:
                    e_x, e_y, e_z = xyzTranslate(e_x, e_y, e_z, a_element.is_bigElement)
            a_element.set_Position(e_x + x, e_y + y, e_z + z, elementXYZ)
            # set_Position已处理与elements_Position有关的操作
            self.Elements.append(a_element)

            identifier_to_element[a_element._arguments["Identifier"]] = a_element

        if self.ExperimentType == experimentType.Circuit and other.ExperimentType == experimentType.Circuit:
            for a_wire in other.Wires:
                a_wire = copy.deepcopy(
                    a_wire, memo={
                        id(a_wire.Source.element_self):
                            identifier_to_element[a_wire.Source.element_self._arguments["Identifier"]],
                        id(a_wire.Target.element_self):
                            identifier_to_element[a_wire.Target.element_self._arguments["Identifier"]],
                })
                self.Wires.add(a_wire)

        return self

class experiment:
    ''' 仅提供通过with操作存档 '''
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

def getAllSav() -> List[str]:
    ''' 获取所有物实存档的文件名 '''
    from os import walk
    savs = [i for i in walk(Experiment.FILE_HEAD)][0]
    savs = savs[savs.__len__() - 1]
    return [aSav for aSav in savs if aSav.endswith('sav')]

def _open_sav(sav_name) -> Optional[dict]:
    ''' 打开一个存档, 返回存档对应的dict '''
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

def search_Experiment(sav_name: str) -> Optional[str]:
    '''  检测实验是否存在, 输入为存档名, 若存在则返回存档对应的文件名, 若不存在则返回None'''
    for aSav in getAllSav():
        sav = _open_sav(aSav)
        if sav["InternalName"] == sav_name:
            search_Experiment.sav = sav
            return aSav

    return None