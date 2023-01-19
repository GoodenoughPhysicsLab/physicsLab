import json
from typing import Union, Callable

# define
FILE_HEAD = "C:/Users/Administrator/AppData/LocalLow/CIVITAS/Quantum Physics/Circuit/"
# end define

# _xxx 不是文件向外暴露出的接口，文件外无法访问
_savName = "" # sav的文件名
_StatusSave = {"SimulationSpeed":1.0, "Elements":[], "Wires":[]}
_Elements = [] # 装原件的_arguments
_wires = []
_sav = {"Type": 0, "Experiment": {"ID": None, "Type": 0, "Components": 7, "Subject": None,
    "StatusSave": "", # _StatusSave
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
def _myRound(num):
    return round(num, 3)

def print_Elements():
    print(_Elements)

def print_wires():
    print(_wires)

# 打开一个指定的sav文件
def open_Experiment(file: str) -> None:
    file = file.strip()
    if (not file.endswith('.sav')):
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
def crt_Element(name: str, x : float = 0, y : float = 0, z : float = 0):
    if not (isinstance(name, str) and isinstance(x, float) and isinstance(y, float) and isinstance(z, float)):
        raise RuntimeError("Wrong parameter type")
    x, y, z = _myRound(x), _myRound(y), _myRound(z)
    if (name == '555 Timer'):
        return NE555(x, y, z)
    elif (name == '8bit Input'):
        return eight_bit_Input(x, y, z)
    elif (name == '8bit Display'):
        return eight_bit_Display(x, y, z)
    else:
        try:
            return eval(name.replace(' ', '_') + f'({x},{y},{z})')
        except SyntaxError:
            raise RuntimeError(f"{name} original that does not exist")

# 读取sav文件已有的原件与导线
def read_Experiment() -> None:
    global _wires
    with open(_savName, encoding='UTF-8') as f:
        readmem = json.loads(f.read())
        _local_Elements = json.loads(readmem["Experiment"]["StatusSave"])["Elements"]
        from_unix_to_Identifier = {}

        for element in _local_Elements:
            # 坐标标准化（消除浮点误差）
            sign1 = element['Position'].find(',')
            sign2 = element['Position'].find(',', sign1 + 1)
            num1 = _myRound(float(element['Position'][:sign1:]))
            num2 = _myRound(float(element['Position'][sign1 + 1: sign2:]))
            num3 = _myRound(float(element['Position'][sign2 + 1::]))
            element['Position'] = f"{num1},{num2},{num3}"  # x, z, y
            # 实例化对象
            obj = crt_Element(element["ModelID"], num1, num3, num2)
            sign1 = element['Rotation'].find(',')
            sign2 = element['Rotation'].find(',', sign1 + 1)
            x = float(element['Rotation'][:sign1:])
            z = float(element['Rotation'][sign1 + 1: sign2:])
            y = float(element['Rotation'][sign2 + 1::])
            obj.set_Rotation(x, y, z)
            # 如果obj是逻辑输入
            if obj.type() == 'Logic Input' and element['Properties']['开关'] == 1:
                obj.set_highLevel()
            # 导线
            Unix_timer = element['Identifier']
            from_unix_to_Identifier[Unix_timer] = (num1, num3, num2).__hash__().__str__()
        _wires = json.loads(readmem['Experiment']['StatusSave'])['Wires']
        for wire in _wires:
            wire['Source'] = from_unix_to_Identifier[wire['Source']]
            wire['Target'] = from_unix_to_Identifier[wire['Target']]

# 规范化实验中原件的坐标与角度
def format_Experiment() -> None:
    pass

# 重命名sav
def rename_sav(name: str) -> None:
    global _sav
    name = str(name)
    _sav["Summary"]["Subject"] = name
    _sav["InternalName"] = name

# 获取对应坐标的self
def get_element(x : float, y : float, z : float = 0):
    x, y, z = _myRound(x), _myRound(y), _myRound(z)
    if (x, y, z) not in _elements_Address.keys():
        raise RuntimeError("Error coordinates that do not exist")
    return _elements_Address[(x, y, z)]

# 删除原件
def del_element(self) -> None:
    try:
        identifier = self._arguments['Identifier']
        if (self.father_type() == 'element'):
            for element in _Elements:
                if (identifier == element['Identifier']):
                    # 删除原件
                    _Elements.remove(element)
                    # 删除导线
                    i = 0
                    while (i < _wires.__len__()):
                        wire = _wires[i]
                        if (wire['Source'] == identifier or wire['Target'] == identifier):
                            _wires.pop(i)
                        else:
                            i += 1
                    return
    except:
        raise RuntimeError('Unable to delete a nonexistent element')

# 所有原件的父类，不要实例化
class _element:
    # 设置原件的角度
    def set_Rotation(self, xRotation: float = 0, yRotation: float = 0, zRotation: float = 180):
        self._arguments["Rotation"] = f"{_myRound(xRotation)},{_myRound(zRotation)},{_myRound(yRotation)}"
        return self._arguments["Rotation"]

    # 重新设置元件的坐标
    def reset_Position(self, x : float, y : float, z : float) -> None:
        x, y, z = _myRound(x), _myRound(y), _myRound(z)
        del _elements_Address[self._position]
        self._position = (x, y, z)
        self._arguments['Position'] = f"{x},{z},{y}"
        identifier = self._arguments['Identifier']
        self._arguments['Identifier'] = self._position.__hash__().__str__()
        _elements_Address[self._position] = self
        for wire in _wires:
            if wire['Source'] == identifier:
                wire['Source'] = self._arguments['Identifier']
            if wire['Target'] == identifier:
                wire['Target'] = self._arguments['Identifier']

    # 格式化坐标参数，主要避免浮点误差
    def format_Position(self) -> tuple:
        if (type(self._position) != tuple or self._position.__len__() != 3):
            raise RuntimeError("Position must be a tuple of length three but gets some other value")
        self._position = (_myRound(self._position[0]), _myRound(self._position[1]), _myRound(self._position[2]))
        return (_myRound(self._position[0]), _myRound(self._position[1]), _myRound(self._position[2]))

    # 获取原件的坐标
    def get_Position(self):
        return self._position

    # 获取父类的类型
    def father_type(self) -> str:
        return 'element'

    # 获取子类的类型（也就是ModelID）
    def type(self) -> str:
        return self._arguments['ModelID']

    # 打印参数
    def print_arguments(self) -> None:
        print(self._arguments)


# 装饰器
def _element_Init_HEAD(func : Callable) -> Callable:
    def result(self, x : float = 0, y : float = 0, z : float = 0) -> None:
        global _Elements
        self._position = (_myRound(x), _myRound(y), _myRound(z))
        if (self._position in _elements_Address.keys()):
            raise RuntimeError("The position already exists")
        func(self, x, y, z)
        self._arguments["Identifier"] = hash(self._position).__str__()
        self._arguments["Position"] = f"{self._position[0]},{self._position[2]},{self._position[1]}"
        _Elements.append(self._arguments)
        _elements_Address[self._position] = self
        self.set_Rotation()
    return result

# 引脚类
class _element_Pin:
    def __init__(self, input_self,  pinLabel : int):
        self.element_self = input_self
        self.pinLabel = pinLabel

    def type(self) -> str:
        return 'element Pin'

# _arguments这里是参数的意思

class Logic_Input(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {"ModelID": "Logic Input", "Identifier": "",
                          "IsBroken": False, "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0, "开关": 0},
                          "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
                          "Position": "",
                          "Rotation": "", "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
                          "DiagramRotation": 0}

    def set_highLevel(self) -> None:
        self._arguments['Properties']['开关'] = 1.0

    @property
    def o(self):
        return _element_Pin(self, 0)

class Logic_Output(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': 'Logic Output', 'Identifier': "",
                          'IsBroken': False, 'IsLocked': False,
                          'Properties': {'状态': 0.0, '高电平': 3.0, '低电平': 0.0, '锁定': 1.0}, 'Statistics': {},
                          'Position': "",
                          'Rotation': '0,180,0', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i(self):
            return _element_Pin(self, 0)

class _2_pin_Gate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': '', 'Identifier': "", 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "",
                          'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i(self):
        return _element_Pin(self, 0)

    @property
    def o(self):
        return _element_Pin(self, 1)

# 是门
class Yes_Gate(_2_pin_Gate):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Yes_Gate, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Yes Gate'

# 非门
class No_Gate(_2_pin_Gate):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(No_Gate, self).__init__(x, y, z)
        self._arguments['MOdelID'] = 'No Gate'

# 3引脚门电路
class _3_pin_Gate(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': '', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "", 'Rotation': "", 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i_up(self):
        return _element_Pin(self, 0)

    @property
    def i_low(self):
        return _element_Pin(self, 1)

    @property
    def o(self):
        return _element_Pin(self, 2)

# 或门
class Or_Gate(_3_pin_Gate):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Or_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'Or Gate'

# 与门
class And_Gate(_3_pin_Gate):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(And_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'And Gate'

# 或非门
class Nor_Gate(_3_pin_Gate):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Nor_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'Nor Gate'

# 与非门
class Nand_Gate(_3_pin_Gate):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Nand_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'Nand Gate'

# 异或门
class Xor_Gate(_3_pin_Gate):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Xor_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'Xor Gate'

# 同或门
class Xnor_Gate(_3_pin_Gate):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Xnor_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'Xnor Gate'

# 蕴含门
class Imp_Gate(_3_pin_Gate):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Imp_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'Imp Gate'

# 蕴含非门
class Nimp_Gate(_3_pin_Gate):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Nimp_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'Nimp Gate'

class _big_element(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': '', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '锁定': 1.0}, 'Statistics': {},
                          'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 半加器
class Half_Adder(_big_element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Half_Adder, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Half Adder'

    @property
    def i_up(self):
        return _element_Pin(self, 2)

    @property
    def i_low(self):
        return _element_Pin(self, 3)

    @property
    def o_up(self):
        return _element_Pin(self, 0)

    @property
    def o_low(self):
        return _element_Pin(self, 1)

# 全加器
class Full_Adder(_big_element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Full_Adder, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Full Adder'

    @property
    def i_up(self):
        return _element_Pin(self, 2)

    @property
    def i_mid(self):
        return _element_Pin(self, 3)

    @property
    def i_low(self):
        return _element_Pin(self, 4)

    @property
    def o_up(self):
        return _element_Pin(self, 0)

    @property
    def o_low(self):
        return _element_Pin(self, 1)

# 二位乘法器
class Multiplier(_big_element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Multiplier, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Multiplier'

    @property
    def i_up(self):
        return _element_Pin(self, 4)

    @property
    def i_upmid(self):
        return _element_Pin(self, 5)

    @property
    def i_lowmid(self):
        return _element_Pin(self, 6)

    @property
    def i_low(self):
        return _element_Pin(self,7)

    @property
    def o_up(self):
        return _element_Pin(self, 0)

    @property
    def o_upmid(self):
        return _element_Pin(self, 1)

    @property
    def o_lowmid(self):
        return _element_Pin(self, 2)

    @property
    def o_low(self):
        return _element_Pin(self, 3)

# D触发器
class D_Flipflop(_big_element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(D_Flipflop, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'D Flipflop'

    @property
    def i_up(self):
        return _element_Pin(self, 2)

    @property
    def i_low(self):
        return _element_Pin(self, 3)

    @property
    def o_up(self):
        return _element_Pin(self, 0)

    @property
    def o_low(self):
        return _element_Pin(self, 1)

# T触发器
class T_Flipflop(_big_element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(T_Flipflop, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'T Flipflop'

    @property
    def i_up(self):
        return _element_Pin(self, 2)

    @property
    def i_low(self):
        return _element_Pin(self, 3)

    @property
    def o_up(self):
        return _element_Pin(self, 0)

    @property
    def o_low(self):
        return _element_Pin(self, 1)

# JK触发器
class JK_Flipflop(_big_element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(JK_Flipflop, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'JK Flipflop'

    @property
    def i_up(self):
        return _element_Pin(self, 2)

    @property
    def i_mid(self):
        return _element_Pin(self, 3)

    @property
    def i_low(self):
        return _element_Pin(self, 4)

    @property
    def o_up(self):
        return _element_Pin(self, 0)

    @property
    def o_down(self):
        return _element_Pin(self, 1)

# 计数器
class Counter(_big_element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Counter, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Counter'

    @property
    def i_up(self):
        return _element_Pin(self, 4)

    @property
    def i_low(self):
        return _element_Pin(self, 5)

    @property
    def o_up(self):
        return _element_Pin(self, 0)

    @property
    def o_upmid(self):
        return _element_Pin(self, 1)

    @property
    def o_lowmid(self):
        return _element_Pin(self, 2)

    @property
    def o_low(self):
        return _element_Pin(self, 3)

# 随机数发生器
class Random_Generator(_big_element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Random_Generator, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Random Generator'

    @property
    def i_up(self):
        return _element_Pin(self, 4)

    @property
    def i_low(self):
        return _element_Pin(self, 5)

    @property
    def o_up(self):
        return _element_Pin(self, 0)

    @property
    def o_upmid(self):
        return _element_Pin(self, 1)

    @property
    def o_lowmid(self):
        return _element_Pin(self, 2)

    @property
    def o_low(self):
        return _element_Pin(self, 3)

# 简单开关
class Simple_Switch(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {"ModelID": "Simple Switch", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"开关": 0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

    @property
    def i(self):
        return _element_Pin(self, 0)

    @property
    def o(self):
        return _element_Pin(self, 1)

# 555定时器
class NE555(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': '555 Timer', 'Identifier': '', 'IsBroken': False,
                           'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '锁定': 1.0},
                           'Statistics': {'供电': 10, '放电': 0.0, '阈值': 4,
                                          '控制': 6.6666666666666666, '触发': 4,
                                          '输出': 0, '重设': 10, '接地': 0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def VCC(self):
        return _element_Pin(self, 0)

    @property
    def Dis(self):
        return _element_Pin(self, 1)

    @property
    def Thr(self):
        return _element_Pin(self, 2)

    @property
    def Ctrl(self):
        return _element_Pin(self, 3)

    @property
    def Trig(self):
        return _element_Pin(self, 4)

    @property
    def Out(self):
        return _element_Pin(self, 5)

    @property
    def Reset(self):
        return _element_Pin(self, 6)

    @property
    def Ground(self):
        return _element_Pin(self, 7)

# 8位输入器
class eight_bit_Input(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': '8bit Input', 'Identifier': '', 'IsBroken': False,
                           'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '十进制': 0.0, '锁定': 1.0},
                           'Statistics': {}, 'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i_up(self):
        return _element_Pin(self, 0)

    @property
    def i_upmid(self):
        return _element_Pin(self, 1)

    @property
    def i_lowmid(self):
        return _element_Pin(self, 2)

    @property
    def i_low(self):
        return _element_Pin(self, 3)

    @property
    def o_up(self):
        return _element_Pin(self, 4)

    @property
    def o_upmid(self):
        return _element_Pin(self, 5)

    @property
    def o_lowmid(self):
        return _element_Pin(self, 6)

    @property
    def o_low(self):
        return _element_Pin(self, 7)

# 8位显示器
class eight_bit_Display(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': '8bit Display', 'Identifier': '',
                          'IsBroken': False, 'IsLocked': False,
                          'Properties': {'高电平': 3.0, '低电平': 0.0, '状态': 0.0, '锁定': 1.0},
                          'Statistics': {'7': 0.0, '6': 0.0, '5': 0.0, '4': 0.0, '3': 0.0, '2': 0.0, '1': 0.0, '0': 0.0,
                                         '十进制': 0.0}, 'Position': '',
                          'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i_up(self):
        return _element_Pin(self, 0)

    @property
    def i_upmid(self):
        return _element_Pin(self, 1)

    @property
    def i_lowmid(self):
        return _element_Pin(self, 2)

    @property
    def i_low(self):
        return _element_Pin(self, 3)

    @property
    def o_up(self):
        return _element_Pin(self, 4)

    @property
    def o_upmid(self):
        return _element_Pin(self, 5)

    @property
    def o_lowmid(self):
        return _element_Pin(self, 6)

    @property
    def o_low(self):
        return _element_Pin(self, 7)

# 学生电源
# Student Source

# 可以支持传入 self 与 位置（tuple） 来连接导线

# 老版本连接导线函数，不推荐使用
def old_crt_wire(SourceLabel : Union[_element, tuple], SourcePin : int, TargetLabel, TargetPin : int, color = "蓝") -> None:
    SourcePin, TargetPin = int(SourcePin), int(TargetPin)
    if (isinstance(SourceLabel, tuple) and len(SourceLabel) == 3):
        SourceLabel = _elements_Address[SourceLabel]
    elif (SourceLabel not in _elements_Address.values()):
        raise RuntimeError("SourceLabel must be a Positon or self")
    if (isinstance(TargetLabel, tuple) and len(TargetLabel) == 3):
        TargetLabel = _elements_Address[TargetLabel]
    elif (TargetLabel not in _elements_Address.values()):
        raise RuntimeError("TargetLabel must be a Positon or self")

    if (color not in ["黑", "蓝", "红", "绿", "黄"]):
        raise RuntimeError("illegal color")
    _wires.append({"Source": SourceLabel._arguments["Identifier"], "SourcePin": SourcePin,
                   "Target": TargetLabel._arguments["Identifier"], "TargetPin": TargetPin,
                   "ColorName": f"{color}色导线"})

# 检查函数参数是否是导线
def _check_typeWire(func):
    def result(SourcePin , TargetPin, color : str = '蓝') -> None:
        try:
            if (SourcePin.type() == 'element Pin' and TargetPin.type() == 'element Pin'):
                if (color not in ["黑", "蓝", "红", "绿", "黄"]):
                    raise RuntimeError("illegal color")

                func(SourcePin, TargetPin, color)
        except:
            raise RuntimeError('Error type of input function argument')
    return result

# 新版连接导线
@_check_typeWire
def crt_wire(SourcePin, TargetPin, color: str = '蓝') -> None:
    _wires.append({"Source": SourcePin.element_self._arguments["Identifier"], "SourcePin": SourcePin.pinLabel,
                   "Target": TargetPin.element_self._arguments["Identifier"], "TargetPin": TargetPin.pinLabel,
                   "ColorName": f"{color}色导线"})

# 删除导线
@_check_typeWire
def del_wire(SourcePin, TargetPin, color : str = '蓝') -> None:
    a_wire = {"Source": SourcePin.element_self._arguments["Identifier"], "SourcePin": SourcePin.pinLabel,
                   "Target": TargetPin.element_self._arguments["Identifier"], "TargetPin": TargetPin.pinLabel,
                   "ColorName": f"{color}色导线"}
    if (a_wire in _wires):
        _wires.remove(a_wire)
    else:
        raise RuntimeError("Unable to delete a nonexistent wire")