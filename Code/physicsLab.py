import json
from typing import Union, Callable

# define
FILE_HEAD = "C:/Users/Administrator/AppData/LocalLow/CIVITAS/Quantum Physics/Circuit/"
# end define

# _xxx 不是文件向外暴露出的接口，文件外无法访问
_savName = "" # sav的文件名
_StatusSave = {"SimulationSpeed":1.0, "Elements":[], "Wires":[]}
_Elements = [] # 装原件的arguments
_wires = []
_sav = {"Type": 0, "Experiment": {"ID": None, "Type": 0, "Components": 7, "Subject": None,
    "StatusSave": "",  # elements and wires: __sav["Experiment"]["StatusSave"] = json.dumps(__StatusSave)
    "CameraSave": "{\"Mode\":0,\"Distance\":2.7,\"VisionCenter\":\"0.3623461,1.08,-0.4681728\",\"TargetRotation\":\"50,0,0\"}","Version": 2404,
    "CreationDate": 1673100860436,"Paused": False,"Summary": None,"Plots": None},"ID": None,"Summary": {"Type": 0,"ParentID": None,"ParentName": None,
    "ParentCategory": None,"ContentID": None,"Editor": None,"Coauthors": [],"Description": None,"LocalizedDescription": None,"Tags": ["Type-0"],
    "ModelID": None,"ModelName": None,"ModelTags": [],"Version": 0,"Language": None,"Visits": 0,"Stars": 0,"Supports": 0,"Remixes": 0,"Comments": 0,"Price": 0,
    "Popularity": 0,"CreationDate": 1673086932246,"UpdateDate": 0,"SortingDate": 0,"ID": None,"Category": None,
    "Subject": "", # file name
    "LocalizedSubject": None,"Image": 0,"ImageRegion": 0,"User": {"ID": None,"Nickname": None,"Signature": None,"Avatar": 0,"AvatarRegion": 0,"Decoration": 0,
      "Verification": None},"Visibility": 0,"Settings": {},"Multilingual": False},"CreationDate": 0,
    "InternalName": "",  # file name twice
        "Speed": 1.0, "SpeedMinimum": 0.0002, "SpeedMaximum": 2.0, "SpeedReal": 0.0, "Paused": False, "Version": 0, "CameraSnapshot": None, "Plots": [], "Widgets": [],
        "WidgetGroups": [], "Bookmarks": {}, "Interfaces": {"Play-Expanded": False,"Chart-Expanded": False}}
_ifndef_open_Experiment = False
_elements_Address = {} # key为position，value为self

'''
原件引脚编号：

D触发器：       逻辑输入、逻辑输出：      是门、非门：       比较器
2    0         0                     0 1              1
                                                          2
3    1                                                0

三引脚门电路：   全加器：
0             2    0
    2         3
1             4    1

继电器pin
0   4
  1  
2   3

二位乘法器：
4  0
5  1
6  2
7  3

原件大小规范：
大原件长宽为0.2
小元件长为0.2，宽为0.1
所有原件高为0.1

'''

def print_Elements():
    print(_Elements)

def print_wires():
    print(_wires)

# 打开一个指定的sav文件
def open_Experiment(file: str) -> None:
    file = file.strip()
    if (file[len(file) - 4: len(file)] != ".sav"):
        raise RuntimeError("The open file must be of type sav")

    global _ifndef_open_Experiment
    if (_ifndef_open_Experiment):
        raise RuntimeError("This function can only be run once")
    _ifndef_open_Experiment = True

    global _savName
    _savName = FILE_HEAD + file
    with open(_savName, encoding="UTF-8") as f:
        InternalName = (json.loads(f.read().__str__()))["Summary"]["Subject"]
        _sav["Summary"]["Subject"] = InternalName
        _sav["InternalName"] = _sav["Summary"]["Subject"]

# 将编译完成的json写入sav
def write_Experiment() -> None:
    global _savName, _sav, _StatusSave
    _StatusSave["Elements"] = _Elements
    _StatusSave["Wires"] = _wires
    _sav["Experiment"]["StatusSave"] = json.dumps(_StatusSave)
    with open(_savName, "w", encoding="UTF-8") as f:
        f.write(json.dumps(_sav))

# 创建原件，本质上仍然是实例化
def crt_Element(name: str, x : float = 0, y : float = 0, z : float = 0) -> _Elements:
    return eval(name.replace(' ', '_') + f'({round(x, 1)},{round(z, 1)},{round(y, 1)})')

# 读取sav文件已有的原件与导线
def read_Experiment() -> None:
    global _wires
    with open(_savName, encoding='UTF-8') as f:
        readmem = json.loads(f.read())
        _local_Elements = json.loads(readmem["Experiment"]["StatusSave"])["Elements"]
        _wires = json.loads(readmem['Experiment']['StatusSave'])['Wires']

        for element in _local_Elements:
            # 坐标标准化（消除浮点误差）
            sign1 = element['Position'].find(',')
            sign2 = element['Position'].find(',', sign1 + 1)
            num1 = round(float(element['Position'][:sign1:]), 1)
            num2 = round(float(element['Position'][sign1 + 1: sign2:]), 1)
            num3 = round(float(element['Position'][sign2 + 1::]), 1)
            element['Position'] = f"{num1},{num2},{num3}"  # x, z, y
            # 实例化对象
            obj = eval(element["ModelID"].replace(' ', '_') + f"({num1},{num3},{num2})")
            sign1 = element['Rotation'].find(',')
            sign2 = element['Rotation'].find(',', sign1 + 1)
            x = float(element['Rotation'][:sign1:])
            z = float(element['Rotation'][sign1 + 1: sign2:])
            y = float(element['Rotation'][sign2 + 1::])
            obj.set_Rotation(x, y, z)


# 重命名sav
def rename_sav(name: str) -> None:
    global _sav
    name = str(name)
    _sav["Summary"]["Subject"] = name
    _sav["InternalName"] = name

# 获取对应坐标的self
def get_element(position: tuple) -> _Elements:
    if (type(position) != tuple or position.__len__() != 3):
        raise RuntimeError("Position must be a tuple of length three but gets some other value")
    return _elements_Address[(position)]

# 所有原件的父类，不要实例化
class _element:
    def set_Rotation(self, xRotation: float = 0, yRotation: float = 0, zRotation: float = 180):
        self.arguments["Rotation"] = f"{round(xRotation)},{round(zRotation)},{round(yRotation)}"
        return self.arguments["Rotation"]

    def format_Positon(self) -> tuple:
        if (type(self.position) != tuple or self.position.__len__() != 3):
            raise RuntimeError("Position must be a tuple of length three but gets some other value")
        self.position = (round(self.position[0], 1), round(self.position[1], 1), round(self.position[2], 1))
        return (round(self.position[0], 1), round(self.position[1], 1), round(self.position[2], 1))

    def type(self):
        return self.arguments["ModelID"]


# 装饰器
def _element_Init_HEAD(func : Callable) -> Callable:
    def result(self, x : float = 0, y : float = 0, z : float = 0) -> None:
        global _Elements
        self.position = (round(x, 1), round(y, 1), round(z, 1))
        if (self.position in _elements_Address.keys()):
            raise RuntimeError("The position already exists")
        func(self, x, y, z)
        _Elements.append(self.arguments)
        _elements_Address[self.position] = self
        self.arguments["Identifier"] = hash(self.position).__str__()
        self.arguments["Position"] = f"{self.position[0]},{self.position[2]},{self.position[1]}"
        self.set_Rotation()
    return result

# arguments这个名字取得真糟糕，但懒得改了

class Logic_Input(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {"ModelID": "Logic Input", "Identifier": "",
                          "IsBroken": False, "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
                          "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
                          "Position": "",
                          "Rotation": "", "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
                          "DiagramRotation": 0}

class Logic_Output(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Logic Output', 'Identifier': "",
                          'IsBroken': False, 'IsLocked': False,
                          'Properties': {'状态': 0.0, '高电平': 3.0, '低电平': 0.0, '锁定': 1.0}, 'Statistics': {},
                          'Position': "",
                          'Rotation': '0,180,0', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

class Yes_Gate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Yes Gate', 'Identifier': "", 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "",
                          'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

class No_Gate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'No Gate', 'Identifier': "", 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "", 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

class Or_Gate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Or Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "", 'Rotation': "", 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

class And_Gate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'And Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "", 'Rotation': "", 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

class Nor_Gate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Nor Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "", 'Rotation': "", 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

class Nand_Gate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Nand Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

class Xor_Gate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Xor Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 同或门
class Xnor_Gate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Xnor Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 蕴含门
class Imp_Gate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Imp Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 蕴含非门
class Nimp_Gate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Nimp Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 半加器
class Half_Adder(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Half Adder', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '锁定': 1.0}, 'Statistics': {},
                          'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 全加器
class Full_Adder(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Full Adder', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '锁定': 1.0}, 'Statistics': {},
                          'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Z': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 二位乘法器
class Multiplier(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Multiplier', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '锁定': 1.0}, 'Statistics': {},
                          'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# D触发器
class D_Fiopflop(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {"ModelID": "D Flipflop", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

# T触发器
class T_Fiopflop(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {"ModelID": "T Flipflop", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

# JK触发器
class JK_Fiopflop(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {"ModelID": "JK Flipflop", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

# 计数器
class Counter(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {"ModelID": "Counter", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

# 随机数发生器
class Random_Generator(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {"ModelID": "Random Generator", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

class Simple_Switch(_element):
    @_element_Init_HEAD
    def __init__(self):
        self.arguments = {"ModelID": "Simple Switch", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"开关": 0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}


# 可以支持传入 self 与 位置（tuple） 来连接导线
def wire(SourceLabel : Union[_element, tuple], SourcePin : int, TargetLabel, TargetPin : int, color = "蓝"):
    SourcePin, TargetPin = int(SourcePin), int(TargetPin)
    if (type(SourceLabel) == tuple and len(SourceLabel) == 3):
        SourceLabel = _elements_Address[SourceLabel]
    elif (SourceLabel not in _elements_Address.values()):
        raise RuntimeError("SourceLabel must be a Positon or self")
    if (type(TargetLabel) == tuple and len(TargetLabel) == 3):
        TargetLabel = _elements_Address[TargetLabel]
    elif (TargetLabel not in _elements_Address.values()):
        raise RuntimeError("TargetLabel must be a Positon or self")

    if (color not in ["黑", "蓝", "红", "绿", "黄"]):
        raise RuntimeError("illegal color")
    _wires.append({"Source": SourceLabel.arguments["Identifier"], "SourcePin": SourcePin,
                   "Target": TargetLabel.arguments["Identifier"], "TargetPin": TargetPin,
                   "ColorName": f"{color}色导线"})
