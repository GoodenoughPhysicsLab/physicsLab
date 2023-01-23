import json
import sys
import getpass
from random import sample
from string import ascii_letters, digits
from os import walk, popen, remove
from typing import Union, Callable

### define ###

_FILE_HEAD = f'C:\\Users\\{getpass.getuser()}\\AppData\\LocalLow\\CIVITAS\\Quantum Physics\\Circuit'
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

def _myRound(num : Union[int, float]):
    if isinstance(num, int):
        return float(num)
    return round(num, 4)

def print_Elements():
    print(_Elements)

def print_wires():
    print(_wires)

def print_elements_Address():
    print(_elements_Address)

### end define ###

### 文件读写操作 Experiment ###

# 输入sav文件名并读取（旧函数，不建议使用）
def old_open_Experiment(file: str) -> None:
    file = file.strip()
    if (not file.endswith('.sav')):
        raise RuntimeError("The input parameters are incorrect")

    global _ifndef_open_Experiment
    if (_ifndef_open_Experiment):
        raise RuntimeError("This function can only be run once")
    _ifndef_open_Experiment = True

    global _savName
    _savName = f"{_FILE_HEAD}\\{file}"
    with open(_savName, encoding="UTF-8") as f:
        try:
            InternalName = (json.loads(f.read().__str__()))["Summary"]["Subject"]
            _sav["Summary"]["Subject"] = InternalName
            _sav["InternalName"] = _sav["Summary"]["Subject"]
        except:
            raise RuntimeError('Data errors in the file')

# 打开一个指定的sav文件（支持输入本地实验的名字或sav文件名）
def open_Experiment(file : str) -> None:
    file = file.strip()
    if file.endswith('.sav'):
        old_open_Experiment(file)
    else:
        savs = [i for i in walk(_FILE_HEAD)][0]
        savs = savs[savs.__len__() - 1]
        savs = [sav for sav in savs if sav.endswith('sav')]
        is_error = True
        for sav in savs:
            try:
                with open(f"{_FILE_HEAD}\\{sav}", encoding='utf-8') as f:
                    f = json.loads(f.read())
                    if (f.get("InternalName") == file):
                        if f.get('InternalName') == '自动保存-电学':
                            rename_Experiment('自动保存-电学')
                        old_open_Experiment(sav)
                        return
                is_error = False
            except:
                if is_error:
                    raise RuntimeError('The input parameters are incorrect')

# 将编译完成的json写入sav
def write_Experiment() -> None:
    global _savName, _sav, _StatusSave
    _StatusSave["Elements"] = _Elements
    _StatusSave["Wires"] = _wires
    _sav["Experiment"]["StatusSave"] = json.dumps(_StatusSave)
    with open(_savName, "w", encoding="UTF-8") as f:
        f.write(json.dumps(_sav))

# 读取sav文件已有的原件与导线
def read_Experiment() -> None:
    global _wires
    with open(_savName, encoding='UTF-8') as f:
        readmem = json.loads(f.read())
        _local_Elements = json.loads(readmem["Experiment"]["StatusSave"])["Elements"]

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
            obj._arguments['Identifier'] = element['Identifier']
            # 如果obj是逻辑输入
            if obj.type() == 'Logic Input' and element['Properties'].get('开关') == 1:
                obj.set_highLevel()
            # 如果obj是8位输入器
            if obj.type() == '8bit Input':
                obj._arguments['Statistics'] = element['Statistics']
                obj._arguments['Properties']['十进制'] = element['Properties']['十进制']
            # 导线
        _wires = json.loads(readmem['Experiment']['StatusSave'])['Wires']

# 规范化实验中原件的坐标与角度
def format_Experiment() -> None:
    pass

# 重命名sav
def rename_Experiment(name: str) -> None:
    # 检查是否重名
    savs = [i for i in walk(_FILE_HEAD)][0]
    savs = savs[savs.__len__() - 1]
    savs = [sav for sav in savs if sav.endswith('sav')]
    for sav in savs:
        with open(f"{_FILE_HEAD}\\{sav}", encoding='utf-8') as f:
            f = json.loads(f.read())
            if f['InternalName'] == name:
                raise RuntimeError('Duplicate name archives are forbidden')
    # 重命名存档
    global _sav
    name = str(name)
    _sav["Summary"]["Subject"] = name
    _sav["InternalName"] = name

# 打开一个存档的窗口
def os_Experiment() -> None:
    popen(_savName)

# 删除存档
def del_Experiment() -> None:
    remove(_savName)
    try:
        remove(_savName.replace('.sav', '.jpg'))
    except:
        sys.exit()

# 创建存档
def crt_Experiment(name : str) -> None:
    global _savName, _ifndef_open_Experiment
    # 该函数与open_Experiment一起，每次只能运行一次
    if (_ifndef_open_Experiment):
        raise RuntimeError("This function can only be run once")
    _ifndef_open_Experiment = True
    # 检查是否存在重名的存档
    savs = [i for i in walk(_FILE_HEAD)][0]
    savs = savs[savs.__len__() - 1]
    savs = [sav for sav in savs if sav.endswith('sav')]
    for sav in savs:
        with open(f"{_FILE_HEAD}\\{sav}", encoding='utf-8') as f:
            f = json.loads(f.read())
            if f['InternalName'] == name:
                raise RuntimeError('Duplicate name archives are forbidden')
    # 创建存档
    if not isinstance(name, str):
        name = str(name)
    _savName = ''.join(sample(ascii_letters + digits, 34))
    _savName = f'{_FILE_HEAD}\\{_savName}.sav'
    with open(_savName, 'w', encoding='utf-8') as f:
        pass
    rename_Experiment(name)
    write_Experiment()

### end Experiment ###

### 操作原件 Element ###

# 创建原件，本质上仍然是实例化
def crt_Element(name: str, x : float = 0, y : float = 0, z : float = 0):
    if not (isinstance(name, str) and isinstance(x, float) and isinstance(y, float) and isinstance(z, float)):
        raise RuntimeError("Wrong parameter type")
    if name == '':
        raise RuntimeError('Name cannot be an empty string')
    x, y, z = _myRound(x), _myRound(y), _myRound(z)
    if (name == '555 Timer'):
        return NE555(x, y, z)
    elif (name == '8bit Input'):
        return eight_bit_Input(x, y, z)
    elif (name == '8bit Display'):
        return eight_bit_Display(x, y, z)
    else:
        try:
            return eval(name.replace(' ', '_').replace('-', '_') + f'({x},{y},{z})')
        except SyntaxError:
            raise RuntimeError(f"{name} original that does not exist")

# 获取对应坐标的self
def get_Element(x : float, y : float, z : float = 0):
    x, y, z = _myRound(x), _myRound(y), _myRound(z)
    if (x, y, z) not in _elements_Address.keys():
        raise RuntimeError("Error coordinates that do not exist")
    return _elements_Address[(x, y, z)]

# 删除原件
def del_Element(self) -> None:
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

### end Element ###

### 操作导线 wire ###

# 老版本连接导线函数，不推荐使用
def old_crt_wire(SourceLabel, SourcePin : int, TargetLabel, TargetPin : int, color = "蓝") -> None: # SourceLabel : Union[_element, tuple]
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

### end wire ###

### 模块化电路 ###

class union_Sum:
    def __init__(self, x : float = 0, y : float = 0, z : float = 0, bitCount : int = 1):
        if not (
                (isinstance(x, float) or isinstance(x, int)) and
                (isinstance(y, float) or isinstance(y, int)) and
                (isinstance(z, float) or isinstance(z, int)) and
                isinstance(bitCount, int) and bitCount > 0
        ):
            raise RuntimeError('Error in input parameters')
        x, y, z = _myRound(x), _myRound(y), _myRound(z)
        Full_Adder(x, y, z)
        for count in range(1, bitCount):
            if count % 8 != 0:
                y = _myRound(y + 0.2)
                crt_wire(
                    Full_Adder(x, y, z).i_low,
                    get_Element(x, y - 0.2, z).o_low
                )
            else:
                y -= 1.4
                z = _myRound(z + 0.1)
                crt_wire(
                    Full_Adder(x, y, z).i_low,
                    get_Element(x, y + 1.4, z - 0.1).o_low
                )

class union_Sub:
    pass

class union_4_16_Decoder:
    def __init__(self, x : float = 0, y : float = 0, z : float = 0):
        self.x = x
        self.y = y
        self.z = z
        obj1 = Nor_Gate(x, y, z); obj2 = Nimp_Gate(x, y + 0.1, z)
        obj3 = Nimp_Gate(x, y + 0.2, z); obj4 = And_Gate(x, y + 0.3, z)
        obj5 = Nor_Gate(x + 0.15, y, z); obj6 = Nimp_Gate(x + 0.15, y + 0.1, z)
        obj7 = Nimp_Gate(x + 0.15, y + 0.2, z); obj8 = And_Gate(x + 0.15, y + 0.3, z)
        crt_wire(obj1.i_up, obj2.i_low), crt_wire(obj2.i_low, obj3.i_up), crt_wire(obj3.i_up, obj4.i_up)
        crt_wire(obj5.i_up, obj6.i_low), crt_wire(obj6.i_low, obj7.i_up), crt_wire(obj7.i_up, obj8.i_up)
        crt_wire(obj1.i_low, obj2.i_up), crt_wire(obj2.i_up, obj3.i_low), crt_wire(obj3.i_low, obj4.i_low)
        crt_wire(obj5.i_low, obj6.i_up), crt_wire(obj6.i_up, obj7.i_low), crt_wire(obj7.i_low, obj8.i_low)
        for i in [0.3, 0.45, 0.6, 0.75]:
            for j in [0.05, 0.25]:
                obj = Multiplier(x + i, y + j, z)
                if j == 0.05:
                    crt_wire(obj1.o, obj.i_low)
                    crt_wire(obj2.o, obj.i_up)
                else:
                    crt_wire(obj3.o, obj.i_low)
                    crt_wire(obj4.o, obj.i_up)
                eval(f'crt_wire(obj{round((i - 0.3) / 0.15) + 5}.o, obj.i_upmid)')
                eval(f'crt_wire(obj{round((i - 0.3) / 0.15) + 5}.o, obj.i_lowmid)')

    @property
    def i_up(self):
        return _element_Pin(get_Element(self.x + 0.15, self.y + 0.3, self.z), 0)

    @property
    def i_upmid(self):
        return _element_Pin(get_Element(self.x + 0.15, self.y + 0.3, self.z), 1)

    @property
    def i_lowmid(self):
        return _element_Pin(get_Element(self.x, self.y + 0.3, self.z), 0)

    @property
    def i_low(self):
        return _element_Pin(get_Element(self.x, self.y + 0.3, self.z), 1)

    @property
    def o0(self):
        return get_Element(self.x + 0.3, self.y + 0.05, self.z).o_lowmid

    @property
    def o1(self):
        return get_Element(self.x + 0.3, self.y + 0.05, self.z).o_upmid

    @property
    def o2(self):
        return get_Element(self.x + 0.3, self.y + 0.25, self.z).o_lowmid

    @property
    def o3(self):
        return get_Element(self.x + 0.45, self.y + 0.25, self.z).o_upmid

    @property
    def o4(self):
        return get_Element(self.x + 0.45, self.y + 0.05, self.z).o_lowmid

    @property
    def o5(self):
        return get_Element(self.x + 0.45, self.y + 0.05, self.z).o_upmid

    @property
    def o6(self):
        return get_Element(self.x + 0.45, self.y + 0.25, self.z).o_lowmid

    @property
    def o7(self):
        return get_Element(self.x + 0.45, self.y + 0.25, self.z).o_upmid

    @property
    def o8(self):
        return get_Element(self.x + 0.6, self.y + 0.05, self.z).o_lowmid

    @property
    def o9(self):
        return get_Element(self.x + 0.6, self.y + 0.05, self.z).o_upmid

    @property
    def o10(self):
        return get_Element(self.x + 0.6, self.y + 0.25, self.z).o_lowmid

    @property
    def o11(self):
        return get_Element(self.x + 0.6, self.y + 0.25, self.z).o_upmid

    @property
    def o12(self):
        return get_Element(self.x + 0.3, self.y + 0.05, self.z).o_lowmid

    @property
    def o13(self):
        return get_Element(self.x + 0.3, self.y + 0.05, self.z).o_upmid

    @property
    def o14(self):
        return get_Element(self.x + 0.3, self.y + 0.25, self.z).o_lowmid

    @property
    def o15(self):
        return get_Element(self.x + 0.3, self.y + 0.25, self.z).o_upmid


### end 模块化电路 ###

### 原件类 class ###

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
        _elements_Address[self._position] = self


    # 格式化坐标参数，主要避免浮点误差
    def format_Position(self) -> tuple:
        if (type(self._position) != tuple or self._position.__len__() != 3):
            raise RuntimeError("Position must be a tuple of length three but gets some other value")
        self._position = (_myRound(self._position[0]), _myRound(self._position[1]), _myRound(self._position[2]))
        return self._position

    # 获取原件的坐标
    @property
    def position(self):
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

# __init__ 装饰器
def _element_Init_HEAD(func : Callable) -> Callable:
    def result(self, x : float = 0, y : float = 0, z : float = 0) -> None:
        global _Elements
        x, y, z = _myRound(x), _myRound(y), _myRound(z)
        self._position = (x, y, z)
        if (self._position in _elements_Address.keys()):
            raise RuntimeError("The position already exists")
        func(self, x, y, z)
        self._arguments["Identifier"] = ''.join(sample(ascii_letters + digits, 32))
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
        self._arguments['ModelID'] = 'No Gate'

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
    def o_low(self):
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

class _switch_Element(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {"ModelID": "", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"开关": 0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

# 简单开关
class Simple_Switch(_switch_Element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Simple_Switch, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Simple Switch'

    @property
    def l(self):
        return _element_Pin(self, 0)

    @property
    def r(self):
        return _element_Pin(self, 1)

# 单刀双掷开关
class SPDT_Switch(_switch_Element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(SPDT_Switch, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'SPDT Switch'

    @property
    def l(self):
        return _element_Pin(self, 0)

    @property
    def mid(self):
        return _element_Pin(self, 1)

    @property
    def r(self):
        return _element_Pin(self, 2)

# 双刀双掷开关
class DPDT_Switch(_switch_Element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(DPDT_Switch, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'DPDT Switch'

    @property
    def l_up(self):
        return _element_Pin(self, 3)

    @property
    def mid_up(self):
        return _element_Pin(self, 4)

    @property
    def r_up(self):
        return _element_Pin(self, 5)

    @property
    def l_low(self):
        return _element_Pin(self, 0)

    @property
    def mid_low(self):
        return _element_Pin(self, 1)

    @property
    def r_low(self):
        return _element_Pin(self, 2)

# 按钮开关
class Push_Switch(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {
            'ModelID': 'Push Switch', 'Identifier': '', 'IsBroken': False, 'IsLocked': False,
            'Properties': {'开关': 0.0, '默认开关': 0.0, '锁定': 1.0}, 'Statistics': {'电流': 0.0}, 'Position': '',
            'Rotation': '', 'DiagramCached': False, 'DiagramPosition': {
                'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def l(self):
        return _element_Pin(self, 0)

    @property
    def r(self):
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

    def set_num(self, num : int):
        if 0 <= num <= 255:
            self._arguments['Properties']['十进制'] = num
        else:
            raise RuntimeError('The number range entered is incorrect')

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

# 电容
class Basic_Capacitor(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': 'Basic Capacitor', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False, 'Properties': {'耐压': 16.0, '电容': 1e-06, '内阻': 5.0, '锁定': 1.0},
                           'Statistics': {}, 'Position': '',
                           'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def l(self):
        return _element_Pin(self, 0)

    @property
    def r(self):
        return _element_Pin(self, 1)

# 一节电池
class Battery_Source(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': 'Battery Source', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False, 'Properties': {'最大功率': 16.2, '电压': 3.0, '内阻': 0.5},
                           'Statistics': {'电流': 0, '功率': 0, '电压': 0},
                           'Position': '',
                           'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def l(self):
        return _element_Pin(self, 0)

    @property
    def r(self):
        return _element_Pin(self, 1)

# 学生电源
class Student_Source(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': 'Student Source', 'Identifier': '', 'IsBroken': False, 'IsLocked': False,
                           'Properties': {'交流电压': 3.0, '直流电压': 3.0, '开关': 0.0, '频率': 50.0},
                           'Statistics': {'瞬间功率': 0.0, '瞬间电压': 0.0, '瞬间电流': 0.0,
                                          '瞬间电阻': 0.0, '功率': 0.0, '电阻': 0.0, '电流': 0.0,
                                          '瞬间功率1': 0.0, '瞬间电压1': 0.0, '瞬间电流1': 0.0,
                                          '瞬间电阻1': 0.0,
                                          '功率1': 0.0, '电阻1': 0.0, '电流1': 0.0},
                           'Position': '',
                           'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0},
                           'DiagramRotation': 0}

    @property
    def l(self):
        return _element_Pin(self, 0)

    @property
    def l_mid(self):
        return _element_Pin(self, 1)

    @property
    def r_mid(self):
        return _element_Pin(self, 2)

    @property
    def r(self):
        return _element_Pin(self, 3)

# 接地
class Ground_Component(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': 'Ground Component', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False, 'Properties': {'锁定': 1.0},
                           'Statistics': {'电流': 0}, 'Position': '',
                           'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i(self):
        return _element_Pin(self, 0)

# 电阻
class Resistor(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': 'Resistor', 'Identifier': '', 'IsBroken': False,
                           'IsLocked': False,
                           'Properties': {'最大电阻': 1000_0000.0, '最小电阻': 0.1, '电阻': 10, '锁定': 1.0},
                           'Statistics': {'瞬间功率': 0, '瞬间电流': 0,
                                          '瞬间电压': 0, '功率': 0,
                                          '电压': 0, '电流': 0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def l(self):
        return _element_Pin(self, 0)

    @property
    def r(self):
        return _element_Pin(self, 1)

# 运算放大器
class Operational_Amplifier(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': 'Operational Amplifier', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False,
                           'Properties': {'增益系数': 100_0000.0, '最大电压': 15.0, '最小电压': -15.0, '锁定': 1.0},
                           'Statistics': {'电压-': 0, '电压+': 0, '输出电压': 0,
                                          '输出电流': 0, '输出功率': 0},
                           'Position': '',
                           'Rotation': '', 'DiagramCached': False,
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

# 小电扇
class Electric_Fan(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': 'Electric Fan', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False,
                           'Properties': {'额定电阻': 1.0, '马达常数': 0.1, '转动惯量': 0.01, '电感': 5e-05, '负荷扭矩': 0.01,
                                          '反电动势系数': 0.001, '粘性摩擦系数': 0.01, '角速度': 0, '锁定': 1.0},
                           'Statistics': {'瞬间功率': 0, '瞬间电流': 0,
                                          '瞬间电压': 0, '功率': 0,
                                          '电压': 0, '电流': 0,
                                          '摩擦扭矩': 0, '角速度': 0,
                                          '反电动势': 0, '转速': 0,
                                          '输入功率': 0, '输出功率': 0},
                           'Position': '',
                           'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def l(self):
        return _element_Pin(self, 0)

    @property
    def r(self):
        return _element_Pin(self, 1)

# 继电器
class Relay_Component(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': 'Relay Component', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False,
                           'Properties': {'开关': 0.0, '线圈电感': 0.2, '线圈电阻': 20.0,
                                          '接通电流': 0.02, '额定电流': 1.0, '锁定': 1.0}, 'Statistics': {},
                           'Position': '', 'Rotation': '',
                           'DiagramCached': False, 'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0},
                           'DiagramRotation': 0}

    @property
    def l_up(self):
        return _element_Pin(self, 0)

    @property
    def l_low(self):
        return _element_Pin(self, 2)

    @property
    def mid(self):
        return _element_Pin(self, 1)

    @property
    def r_up(self):
        return _element_Pin(self, 4)

    @property
    def r_low(self):
        return _element_Pin(self, 5)

# n mos
class N_MOSFET(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': 'N-MOSFET', 'Identifier': '', 'IsBroken': False,
                           'IsLocked': False, 'Properties': {'PNP': 1.0, '放大系数': 0.027, '阈值电压': 1.5, '最大功率': 100.0, '锁定': 1.0},
                           'Statistics': {'电压GS': 0.0, '电压': 0.0, '电流': 0.0, '功率': 0.0, '状态': 0.0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def D(self):
        return _element_Pin(self, 2)

    @property
    def S(self):
        return _element_Pin(self, 1)

    @property
    def G(self):
        return _element_Pin(self, 0)

class _source_Element(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': '', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False,
                           'Properties': {'电压': 3.0, '内阻': 0.5, '频率': 20000.0, '偏移': 0.0, '占空比': 0.5, '锁定': 1.0},
                           'Statistics': {'电流': 0.0, '功率': 0.0, '电压': -3.0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def l(self):
        return _element_Pin(self, 0)

    @property
    def r(self):
        return _element_Pin(self, 1)

    @property
    def i(self):
        return _element_Pin(self, 0)

    @property
    def o(self):
        return _element_Pin(self, 1)

# 正弦波发生器
class Sinewave_Source(_source_Element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Sinewave_Source, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Sinewave Source'

# 方波发生器
class Square_Source(_source_Element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Square_Source, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Square Source'

# 三角波发生器
class Triangle_Source(_source_Element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Triangle_Source, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Triangle Source'

# 锯齿波发生器
class Sawtooth_Source(_source_Element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Sawtooth_Source, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Sawtooth Source'

# 尖峰波发生器
class Pulse_Source(_source_Element):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super(Pulse_Source, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Pulse Source'

# 保险丝
class Fuse_Component(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': 'Fuse Component', 'Identifier': '', 'IsBroken': False, 'IsLocked': False,
                           'Properties': {'开关': 1.0, '额定电流': 0.30000001192092896, '熔断电流': 0.5, '锁定': 1.0},
                           'Statistics': {'瞬间功率': 0.0, '瞬间电流': 0.0, '瞬间电压': 0.0, '功率': 0.0, '电压': 0.0, '电流': 0.0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def l(self):
        return _element_Pin(self, 0)

    @property
    def r(self):
        return _element_Pin(self, 1)

# 滑动变阻器
class Slide_Rheostat(_element):
    @_element_Init_HEAD
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self._arguments = {'ModelID': 'Slide Rheostat', 'Identifier': '', 'IsBroken': False, 'IsLocked': False,
                           'Properties': {'额定电阻': 10.0, '滑块位置': 0.0, '电阻1': 10, '电阻2': 10.0, '锁定': 1.0},
                           'Statistics': {'瞬间功率': 0.0, '瞬间电流': 0.0, '瞬间电压': 0.0, '功率': 0.0, '电压': 0.0, '电流': 0.0,
                                          '瞬间功率1': 0.0, '瞬间电流1': 0.0, '瞬间电压1': 0.0, '功率1': 0.0, '电压1': 0.0, '电流1': 0.0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def l_low(self):
        return _element_Pin(self, 0)

    @property
    def r_low(self):
        return _element_Pin(self, 1)

    @property
    def l_up(self):
        return _element_Pin(self, 2)

    @property
    def r_up(self):
        return _element_Pin(self, 3)

### end 原件类 ###