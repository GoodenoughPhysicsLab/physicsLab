# -*- coding: utf-8 -*-
import os
import sys
import json
import copy

import physicsLab._tools as _tools
import physicsLab.phy_errors as phy_errors
import physicsLab.savTemplate as savTemplate
import physicsLab._colorUtils as _colorUtils

from physicsLab.experimentType import experimentType
from physicsLab.typehint import Union, Optional, List, Self

# 最新被操作的存档
class stack_Experiment:
    __single_instance: Optional["stack_Experiment"] = None
    data: List["Experiment"] = []

    def __new__(cls) -> Self:
        if cls.__single_instance is None:
            cls.__single_instance = object.__new__(cls)

        return cls.__single_instance

    @classmethod
    def push(cls, data: "Experiment") -> None:
        if not isinstance(data, Experiment):
            raise TypeError

        cls.data.append(data)

    @classmethod
    def top(cls) -> "Experiment":
        if len(cls.data) == 0:
            raise phy_errors.ExperimentError("operate but no experiment(experiment stack is empty)")

        return cls.data[-1]

    @classmethod
    def pop(cls) -> "Experiment":
        res = cls.top()
        cls.data.pop()
        return res

def get_Experiment() -> stack_Experiment:
    return stack_Experiment.top()

# 实验（存档）类
class Experiment:
    FILE_HEAD = "physicsLabSav"
    if sys.platform == "win32":
        from getpass import getuser
        FILE_HEAD = f"C:/Users/{getuser()}/AppData/LocalLow/CIVITAS/Quantum Physics/Circuit"
    
    def __init__(self, sav_name: Optional[str] = None) -> None:
        self.is_open_or_crt: bool = False
        self.is_open: bool = False
        self.is_crt: bool = False
        self.is_read: bool = False

        self.FileName: Optional[str] = None # 存档的文件名
        self.SavPath: Optional[str] = None # 存档的完整路径, 为 f"{experiment.FILE_HEAD}/{self.FileName}"
        self.Elements: list = [] # 装原件的_arguments
        # 通过坐标索引元件
        self.elements_Position: dict = {}  # key: self._position, value: List[self...]
        # 通过index（元件生成顺序）索引元件
        self.elements_Index: list = [] # List[self]

        if sav_name is not None:
            self.open(sav_name)

    # 进行与experimentType有关的初始化
    def __experimentType_init(self, experiment_type: Union[int, experimentType]) -> None:
        if not (
            isinstance(experiment_type, experimentType)
            or (
                isinstance(experiment_type, int) and \
                experiment_type in \
                    (experimentType.Circuit.value, experimentType.Celestial.value, experimentType.Electromagnetism.value)
            )
        ):
            raise TypeError

        if isinstance(experiment_type, experimentType):
            self.ExperimentType: experimentType = experiment_type
        else:
            if experiment_type == experimentType.Circuit.value:
                self.ExperimentType = experimentType.Circuit
            elif experiment_type == experimentType.Celestial.value:
                self.ExperimentType = experimentType.Celestial
            elif experiment_type == experimentType.Electromagnetism.value:
                self.ExperimentType = experimentType.Electromagnetism

        if self.ExperimentType == experimentType.Circuit:
            self.PlSav: dict = copy.deepcopy(savTemplate.Circuit)
            self.Wires: List[dict] = [] # 存档对应的导线
            # 存档对应的StatusSave, 存放实验元件，导线（如果是电学实验的话）
            self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": [], "Wires": []}

        elif self.ExperimentType == experimentType.Celestial:
            self.PlSav: dict = copy.deepcopy(savTemplate.Celestial)
            self.StatusSave: dict = {"MainIdentifier": None, "Elements": {}, "WorldTime": 0.0,
                                     "ScalingName": "内太阳系", "LengthScale": 1.0, "SizeLinear": 0.0001,
                                     "SizeNonlinear": 0.5, "StarPresent": False, "Setting": None}

        elif self.ExperimentType == experimentType.Electromagnetism:
            self.PlSav: dict = copy.deepcopy(savTemplate.Electromagnetism)
            self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": []}

    # 只能通过sav文件名的方式打开文件
    def __open(self, _File) -> "Experiment":
        self.is_open = True

        self.SavPath = f"{Experiment.FILE_HEAD}/{_File}"
        with open(self.SavPath, encoding="utf-8") as f:
            sav_dict = json.loads(f.read().replace('\n', ''))
            sav_dict["Experiment"]["StatusSave"] = None
            self.PlSav = sav_dict

        self.ExperimentType = {
            experimentType.Circuit.value: experimentType.Circuit,
            experimentType.Celestial.value: experimentType.Celestial,
            experimentType.Electromagnetism.value: experimentType.Electromagnetism
        }[self.PlSav["Type"]]

        if self.ExperimentType == experimentType.Circuit:
            self.Wires: List[dict] = [] # 存档对应的导线
            # 存档对应的StatusSave, 存放实验元件，导线（如果是电学实验的话）
            self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": [], "Wires": []}
            if self.PlSav["Summary"] is None:
                self.PlSav["Summary"] = savTemplate.Circuit["Summary"]

        elif self.ExperimentType == experimentType.Celestial:
            self.StatusSave: dict = {"MainIdentifier": None, "Elements": {}, "WorldTime": 0.0,
                                    "ScalingName": "内太阳系", "LengthScale": 1.0, "SizeLinear": 0.0001,
                                    "SizeNonlinear": 0.5, "StarPresent": False, "Setting": None}
            if self.PlSav["Summary"] is None:
                self.PlSav["Summary"] = savTemplate.Celestial["Summary"]


        elif self.ExperimentType == experimentType.Electromagnetism:
            self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": []}
            if self.PlSav["Summary"] is None:
                self.PlSav["Summary"] = savTemplate.Electromagnetism["Summary"]

        return self

    # 打开一个指定的sav文件（支持输入本地实验的名字或sav文件名）
    def open(self, sav_name : str) -> "Experiment":
        if self.is_open_or_crt:
            raise phy_errors.experimentExistError
        self.is_open_or_crt = True
        stack_Experiment.push(self)

        sav_name = sav_name.strip()
        if sav_name.endswith('.sav'):
            self.FileName = sav_name
            self.__open(sav_name)
            return

        self.FileName = search_Experiment(sav_name)
        if self.FileName is None:
            stack_Experiment.pop()
            raise phy_errors.OpenExperimentError(f'No such experiment "{sav_name}"')

        self.__open(self.FileName)
        return self

    def __crt(self, sav_name: str, experiment_type: experimentType = experimentType.Circuit) -> None:
        self.is_crt = True

        self.FileName = _tools.randString(34)
        self.SavPath = f"{Experiment.FILE_HEAD}/{self.FileName}.sav"
        self.__experimentType_init(experiment_type)
        self.entitle(sav_name)
    
    # 创建存档，输入为存档名
    def crt(self, sav_name: str, experimentType: experimentType = experimentType.Circuit) -> "Experiment":
        if self.is_open_or_crt:
            raise phy_errors.experimentExistError
        self.is_open_or_crt = True

        if search_Experiment(sav_name) is not None:
            raise phy_errors.crtExperimentFailError
        if not isinstance(sav_name, str):
            raise TypeError
        
        stack_Experiment.push(self)

        self.__crt(sav_name, experimentType)
        return self
    
    # 先尝试打开实验, 若失败则创建实验
    def open_or_crt(self, savName: str, experimentType: experimentType = experimentType.Circuit) -> "Experiment":
        if self.is_open_or_crt:
            raise phy_errors.experimentExistError
        self.is_open_or_crt = True

        if not isinstance(savName, str):
            raise TypeError
        stack_Experiment.push(self)
        
        self.FileName = search_Experiment(savName)
        if self.FileName is not None:
            self.__open(self.FileName)
        else:
            self.__crt(savName, experimentType)
        return self
    
    # 读取实验已有状态
    def read(self):
        if self.SavPath is None: # 是否已.open()或.crt()
            raise TypeError
        if self.is_read:
            raise phy_errors.ExperimentError("experiment have been read")
        self.is_read = True

        with open(self.SavPath, encoding='utf-8') as f:
            status_sav = json.loads(json.loads(f.read().replace('\n', ''))["Experiment"]["StatusSave"])
            # 元件
            _local_Elements = status_sav["Elements"]
            # 导线
            if self.ExperimentType == experimentType.Circuit:
                self.Wires = status_sav['Wires']

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
                x = rotation[0]
                z = rotation[1]
                y = rotation[2]
                obj.set_Rotation(x, y, z)
                obj._arguments['Identifier'] = element['Identifier']
                from .circuit.elements.logicCircuit import Logic_Input, eight_bit_Input
                # 如果obj是逻辑输入
                if isinstance(obj, Logic_Input) and element['Properties'].get('开关') == 1:
                    obj.set_highLevel()
                # 如果obj是8位输入器
                elif isinstance(obj, eight_bit_Input):
                    obj._arguments['Statistics'] = element['Statistics']
                    obj._arguments['Properties']['十进制'] = element['Properties']['十进制']

    # 以物实存档的格式导出实验
    def write(self, extra_filepath: Optional[str] = None, ln: bool = False, no_pop: bool = False) -> "Experiment":
        def _format_StatusSave(stringJson: str) -> str:
            stringJson = stringJson.replace('{\\\"ModelID', '\n      {\\\"ModelID') # format element json
            stringJson = stringJson.replace('DiagramRotation\\\": 0}]', 'DiagramRotation\\\": 0}\n    ]') # format end element json
            stringJson = stringJson.replace('{\\\"Source', '\n      {\\\"Source')
            stringJson = stringJson.replace(u"色导线\\\"}]}", "色导线\\\"}\n    ]}")
            return stringJson

        if self.SavPath is None: # 检查是否已经.open()或.crt()
            raise phy_errors.ExperimentError("write after open or crt")
        if self.is_open_or_crt == True:
            self.is_open_or_crt = False
        else:
            raise phy_errors.ExperimentError("write after open or crt")

        if not no_pop:
            stack_Experiment.pop()

        self.StatusSave["Elements"] = self.Elements
        if self.ExperimentType == experimentType.Circuit:
            self.StatusSave["Wires"] = self.Wires
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
        if self.ExperimentType == experimentType.Circuit:
            _colorUtils.color_print(
                f"Successfully compiled experiment \"{self.PlSav['InternalName']}\"! "
                f"{self.Elements.__len__()} elements, {self.Wires.__len__()} wires.",
                color=_colorUtils.COLOR.GREEN
            )
        else:
            _colorUtils.color_print(
                f"Successfully compiled experiment \"{self.PlSav['InternalName']}\"! "
                f"{self.Elements.__len__()} elements.",
                color=_colorUtils.COLOR.GREEN
            )

        return self
    
    # 删除存档
    def delete(self) -> None:
        if self.SavPath is None:
            raise TypeError

        if os.path.exists(self.SavPath): # 如果一个实验被创建但还未被写入, 就会触发错误
            os.remove(self.SavPath)
            _colorUtils.color_print("Successfully delete experiment!", _colorUtils.COLOR.BLUE)
        else:
            phy_errors.warning(f"experiment {self.PlSav['InternalName']}({self.FileName}) do not exist.")

        if os.path.exists(self.SavPath.replace(".sav", ".jpg")): # 用存档生成的实验无图片，因此可能删除失败
            os.remove(self.SavPath.replace(".sav", ".jpg"))

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
                 force_crt: bool = False # 强制创建一个实验, 若已存在则删除已有实验
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

    # 上下文管理器，搭配with使用
    def __enter__(self):
        if not self.force_crt:
            self._Experiment: Experiment = Experiment().open_or_crt(self.savName, self.experimentType)
        else:
            temp = search_Experiment(self.savName)
            if temp is not None:
                Experiment(temp).delete()
            
            self._Experiment: Experiment = Experiment().crt(self.savName)

        if self.read:
            self._Experiment.read()
        if self.elementXYZ:
            if self._Experiment.ExperimentType != experimentType.Circuit:
                stack_Experiment.pop()
                raise phy_errors.ExperimentTypeError
            import physicsLab.circuit.elementXYZ as _elementXYZ
            _elementXYZ.set_elementXYZ(True)

        return self._Experiment

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.write:
            self._Experiment.write(extra_filepath=self.extra_filepath, no_pop=self.delete)
        if self.delete:
            self._Experiment.delete()

# 索取所有物实存档的文件名
def getAllSav() -> List:
    from os import walk
    savs = [i for i in walk(Experiment.FILE_HEAD)][0]
    savs = savs[savs.__len__() - 1]
    return [aSav for aSav in savs if aSav.endswith('sav')]

# 检测实验是否存在，输入为存档名，若存在则返回存档对应的文件名，若不存在则返回None
def search_Experiment(sav_name: str) -> Union[str, None]:
    savs = getAllSav()
    for aSav in savs:
        with open(f"{Experiment.FILE_HEAD}/{aSav}", encoding='utf-8') as f:
            try:
                f = json.loads(f.read().replace('\n', ''))
            except json.decoder.JSONDecodeError: # 文件不是物实存档
                continue
            else:
                if f["InternalName"] == sav_name:
                    return aSav
    return None

# 以下为旧式调用方式， 为兼容代码
# 打开实验
def open_Experiment(sav_name: str) -> Experiment:
    return Experiment().open(sav_name)

# 创建存档，输入为存档名
def crt_Experiment(sav_name: str, experimentType: experimentType = experimentType.Circuit) -> Experiment:
    return Experiment().crt(sav_name, experimentType)

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
