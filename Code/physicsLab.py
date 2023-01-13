import json

# define
FILE_HEAD = "C:/Users/Administrator/AppData/LocalLow/CIVITAS/Quantum Physics/Circuit/"
# end define

# _xxx 不是文件向外暴露出的接口，文件外请谨慎访问与修改
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

D触发器：       逻辑输入、逻辑输出：
2 0            0
3 1          

与门，或门，或非门，蕴含非门：
0
    2
1

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

def show_Elements():
    print(_Elements)

def show_wires():
    print(_wires)

# 打开一个指定的sav文件
def open_Experiment(file: str):
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
def write_Experiment():
    global _savName, _sav, _StatusSave
    _StatusSave["Elements"] = _Elements
    _StatusSave["Wires"] = _wires
    _sav["Experiment"]["StatusSave"] = json.dumps(_StatusSave)
    with open(_savName, "w", encoding="UTF-8") as f:
        f.write(json.dumps(_sav))

# 读取sav文件已有的原件与导线
def read_Experiment():
    global _Elements, _wires
    with open(_savName, encoding='UTF-8') as f:
        readmem = json.loads(f.read())
        _Elements = json.loads(readmem["Experiment"]["StatusSave"])["Elements"]
        _wires = json.loads(readmem['Experiment']['StatusSave'])['Wires']

        for element in _Elements:
            sign1 = element['Position'].find(',')
            sign2 = element['Position'].find(',', sign1 + 1)
            num1 = round(float(element['Position'][:sign1:]), 1)
            num2 = round(float(element['Position'][sign1 + 1: sign2:]), 1)
            num3 = round(float(element['Position'][sign2 + 1::]), 1)
            element['Position'] = f"{num1},{num2},{num3}"

# 重命名sav
def rename_sav(name: str):
    global _sav
    name = str(name)
    _sav["Summary"]["Subject"] = name
    _sav["InternalName"] = name

# 获取对应坐标的self
def get_element(position):
    if (type(position) != tuple or position.__len__() != 3):
        raise RuntimeError("Position must be a tuple of length three but gets some other value")
    return _elements_Address[(position)]

# 所有原件的父类，不要实例化
class _element:
    def set_Rotation(self, xRotation: float = 0, yRotation: float = 0, zRotation: float = 180):
        self.arguments["Rotation"] = f"{round(xRotation)},{round(zRotation)},{round(yRotation)}"
        return self.arguments["Rotation"]

    def format_Positon(self, position):
        if (type(position) != tuple or position.__len__() != 3):
            raise RuntimeError("Position must be a tuple of length three but gets some other value")
        return (round(position[0], 1), round(position[1], 1), round(position[2], 1))

    def set_Position(self, position):
        input_self = _elements_Address[position]
        input_self.position = input_self.format_Positon(position)
        input_self.arguments["Position"] = f"{input_self.position[0]},{input_self.position[2]},{input_self.position[1]}"
        return input_self.arguments["Position"]

    def type(self):
        return self.arguments["ModelID"]

def _element_Init_HEAD(func):
    def result(self, x : float = 0, y : float = 0, z : float = 0):
        global _Elements
        self.position = self.format_Positon((x, y, z))
        if (self.position in _Elements):
            raise RuntimeError("The position already exists")
        func(self, x, y, z)
        _Elements.append(self.arguments)
        _elements_Address[self.position] = self
        self.arguments["Identifier"] = hash(self.position).__str__()
        self.set_Position(self.position)
        self.set_Rotation()
    return result

# arguments这个名字取得真糟糕，但懒得改了

class logicInput(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {"ModelID": "Logic Input", "Identifier": "",
                          "IsBroken": False, "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
                          "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
                          "Position": "",
                          "Rotation": "", "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
                          "DiagramRotation": 0}

class logicOutput(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Logic Output', 'Identifier': "",
                          'IsBroken': False, 'IsLocked': False,
                          'Properties': {'状态': 0.0, '高电平': 3.0, '低电平': 0.0, '锁定': 1.0}, 'Statistics': {},
                          'Position': "",
                          'Rotation': '0,180,0', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

class yesGate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Yes Gate', 'Identifier': "", 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "",
                          'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

class noGate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'No Gate', 'Identifier': "", 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "", 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

class orGate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Or Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "", 'Rotation': "", 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

class andGate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'And Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "", 'Rotation': "", 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

class norGate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Nor Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "", 'Rotation': "", 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

class nAndGate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Nand Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

class xorGate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Xor Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 同或门
class xNorGate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Xnor Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 蕴含门
class impGate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Imp Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 蕴含非门
class nImpGate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Nimp Gate', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 半加器
class halfAdder(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Half Adder', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '锁定': 1.0}, 'Statistics': {},
                          'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 全加器
class fullAdder(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Full Adder', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '锁定': 1.0}, 'Statistics': {},
                          'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Z': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 二位乘法器
class multiplier(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {'ModelID': 'Multiplier', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '锁定': 1.0}, 'Statistics': {},
                          'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# D触发器
class d_Fiopflop(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {"ModelID": "D Flipflop", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

# T触发器
class t_Fiopflop(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {"ModelID": "T Flipflop", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

# JK触发器
class jk_Fiopflop(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {"ModelID": "JK Flipflop", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

# 计数器
class counter(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {"ModelID": "Counter", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

# 随机数发生器
class random_Generator(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.arguments = {"ModelID": "Random Generator", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

class simpleSwitch(_element):
    @_element_Init_HEAD
    def __init__(self):
        self.arguments = {"ModelID": "Simple Switch", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"开关": 0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}


# 可以支持传入 self 与 位置 来连接导线
def wire(SourceLabel, SourcePin : int, TargetLabel, TargetPin : int, color = "蓝"):
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
