#coding=utf-8
from random import sample
from string import ascii_letters, digits
from typing import Callable
from _fileGlobals import *
from electricity._elementPin import *

# 原件装饰器
def _element_Method(cls):
    # 设置原件的角度
    def set_Rotation(self, xRotation: Union[int, float] = 0, yRotation: Union[int, float] = 0, zRotation: Union[int, float] = 180) -> None:
        if not (isinstance(xRotation, (int, float)) and isinstance(yRotation, (int, float)) and isinstance(zRotation, (int, float))):
            raise RuntimeError('illegal argument')
        self._arguments["Rotation"] = f"{myRound(xRotation)},{myRound(zRotation)},{myRound(yRotation)}"
        return self._arguments["Rotation"]
    cls.set_Rotation = set_Rotation

    # 重新设置元件的坐标
    def set_Position(self, x : Union[int, float], y : Union[int, float], z : Union[int, float]) -> None:
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
            raise RuntimeError('illegal argument')
        x, y, z = myRound(x), myRound(y), myRound(z)
        del elements_Address[self._position]
        self._position = (x, y, z)
        self._arguments['Position'] = f"{x},{z},{y}"
        elements_Address[self._position] = self
    cls.set_Position = set_Position

    # 格式化坐标参数，主要避免浮点误差
    def format_Position(self) -> tuple:
        if not isinstance(self._position, tuple) or self._position.__len__() != 3:
            raise RuntimeError("Position must be a tuple of length three but gets some other value")
        self._position = (myRound(self._position[0]), myRound(self._position[1]), myRound(self._position[2]))
        return self._position
    cls.format_Position = format_Position

    # 获取原件的坐标
    def get_Position(self) -> tuple:
        return self._position
    cls.get_Position = get_Position

    # 获取父类的类型
    def father_type(self) -> str:
        return 'element'
    cls.father_type = father_type

    # 获取子类的类型（也就是ModelID）
    def type(self) -> str:
        return self._arguments['ModelID']
    cls.type = type

    # 打印参数
    def print_arguments(self) -> None:
        print(self._arguments)
    cls.print_arguments = print_arguments

    return cls

# __init__ 装饰器
def _element_Init_HEAD(func : Callable) -> Callable:
    def result(self, x : Union[int, float] = 0, y : Union[int, float] = 0, z : Union[int, float] = 0) -> None:
        if not isinstance(x, (float, int)) and isinstance(y, (float, int)) and isinstance(z, (float, int)):
            raise RuntimeError('illegal argument')
        global Elements
        x, y, z = myRound(x), myRound(y), myRound(z)
        self._position = (x, y, z)
        if self._position in elements_Address.keys():
            raise RuntimeError("The position already exists")
        func(self, x, y, z)
        self._arguments["Identifier"] = ''.join(sample(ascii_letters + digits, 32))
        self._arguments["Position"] = f"{self._position[0]},{self._position[2]},{self._position[1]}"
        Elements.append(self._arguments)
        elements_Address[self._position] = self
        self.set_Rotation()
    return result

# 逻辑电路类装饰器
def _logic_Circuit_Method(cls):
    # 设置高电平的值
    def set_HighLeaveValue(self, num: Union[int, float]) -> None:
        if not isinstance(num, (int, float)):
            raise RuntimeError('illegal argument')
        self._arguments['Properties']['高电平'] = num
    cls.set_HighLeaveValue = set_HighLeaveValue

    # 设置低电平的值
    def set_LowLeaveValue(self, num : Union[int, float]) -> None:
        if not isinstance(num, (int, float)):
            raise RuntimeError('illegal argument')
        self._arguments['Properties']['低电平'] = num
    cls.set_LowLeaveValue = set_LowLeaveValue

    # end decorator
    return cls

# 双引脚模拟电路原件的引脚
def _two_pin_ArtificialCircuit_Pin(cls):
    @property
    def red(self):
        return element_Pin(self, 0)
    cls.red, cls.l = red, red

    @property
    def black(self):
        return element_Pin(self, 1)
    cls.black, cls.r = black, black

    return cls

# _arguments是参数的意思

# 逻辑输入
@_element_Method
@_logic_Circuit_Method
class Logic_Input:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
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
        return element_Pin(self, 0)

# 逻辑输出
@_element_Method
@_logic_Circuit_Method
class Logic_Output:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': 'Logic Output', 'Identifier': "",
                          'IsBroken': False, 'IsLocked': False,
                          'Properties': {'状态': 0.0, '高电平': 3.0, '低电平': 0.0, '锁定': 1.0}, 'Statistics': {},
                          'Position': "",
                          'Rotation': '0,180,0', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i(self):
            return element_Pin(self, 0)

# 2引脚门电路
@_element_Method
@_logic_Circuit_Method
class _2_pin_Gate:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': '', 'Identifier': "", 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "",
                          'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i(self):
        return element_Pin(self, 0)

    @property
    def o(self):
        return element_Pin(self, 1)

# 是门
class Yes_Gate(_2_pin_Gate):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Yes_Gate, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Yes Gate'

# 非门
class No_Gate(_2_pin_Gate):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(No_Gate, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'No Gate'

# 3引脚门电路
@_element_Method
@_logic_Circuit_Method
class _3_pin_Gate:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': '', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "", 'Rotation': "", 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i_up(self):
        return element_Pin(self, 0)

    @property
    def i_low(self):
        return element_Pin(self, 1)

    @property
    def o(self):
        return element_Pin(self, 2)

# 或门
class Or_Gate(_3_pin_Gate):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Or_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'Or Gate'

# 与门
class And_Gate(_3_pin_Gate):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(And_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'And Gate'

# 或非门
class Nor_Gate(_3_pin_Gate):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Nor_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'Nor Gate'

# 与非门
class Nand_Gate(_3_pin_Gate):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Nand_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'Nand Gate'

# 异或门
class Xor_Gate(_3_pin_Gate):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Xor_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'Xor Gate'

# 同或门
class Xnor_Gate(_3_pin_Gate):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Xnor_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'Xnor Gate'

# 蕴含门
class Imp_Gate(_3_pin_Gate):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Imp_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'Imp Gate'

# 蕴含非门
class Nimp_Gate(_3_pin_Gate):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Nimp_Gate, self).__init__(x, y, z)
        self._arguments["ModelID"] = 'Nimp Gate'

@_element_Method
@_logic_Circuit_Method
class _big_element:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': '', 'Identifier': '', 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '锁定': 1.0}, 'Statistics': {},
                          'Position': '', 'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 半加器
class Half_Adder(_big_element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Half_Adder, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Half Adder'

    @property
    def i_up(self):
        return element_Pin(self, 2)

    @property
    def i_low(self):
        return element_Pin(self, 3)

    @property
    def o_up(self):
        return element_Pin(self, 0)

    @property
    def o_low(self):
        return element_Pin(self, 1)

# 全加器
class Full_Adder(_big_element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Full_Adder, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Full Adder'

    @property
    def i_up(self):
        return element_Pin(self, 2)

    @property
    def i_mid(self):
        return element_Pin(self, 3)

    @property
    def i_low(self):
        return element_Pin(self, 4)

    @property
    def o_up(self):
        return element_Pin(self, 0)

    @property
    def o_low(self):
        return element_Pin(self, 1)

# 二位乘法器
class Multiplier(_big_element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Multiplier, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Multiplier'

    @property
    def i_up(self):
        return element_Pin(self, 4)

    @property
    def i_upmid(self):
        return element_Pin(self, 5)

    @property
    def i_lowmid(self):
        return element_Pin(self, 6)

    @property
    def i_low(self):
        return element_Pin(self, 7)

    @property
    def o_up(self):
        return element_Pin(self, 0)

    @property
    def o_upmid(self):
        return element_Pin(self, 1)

    @property
    def o_lowmid(self):
        return element_Pin(self, 2)

    @property
    def o_low(self):
        return element_Pin(self, 3)

# D触发器
class D_Flipflop(_big_element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(D_Flipflop, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'D Flipflop'

    @property
    def i_up(self):
        return element_Pin(self, 2)

    @property
    def i_low(self):
        return element_Pin(self, 3)

    @property
    def o_up(self):
        return element_Pin(self, 0)

    @property
    def o_low(self):
        return element_Pin(self, 1)

# T触发器
class T_Flipflop(_big_element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(T_Flipflop, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'T Flipflop'

    @property
    def i_up(self):
        return element_Pin(self, 2)

    @property
    def i_low(self):
        return element_Pin(self, 3)

    @property
    def o_up(self):
        return element_Pin(self, 0)

    @property
    def o_low(self):
        return element_Pin(self, 1)

# JK触发器
class JK_Flipflop(_big_element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(JK_Flipflop, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'JK Flipflop'

    @property
    def i_up(self):
        return element_Pin(self, 2)

    @property
    def i_mid(self):
        return element_Pin(self, 3)

    @property
    def i_low(self):
        return element_Pin(self, 4)

    @property
    def o_up(self):
        return element_Pin(self, 0)

    @property
    def o_low(self):
        return element_Pin(self, 1)

# 计数器
class Counter(_big_element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Counter, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Counter'

    @property
    def i_up(self):
        return element_Pin(self, 4)

    @property
    def i_low(self):
        return element_Pin(self, 5)

    @property
    def o_up(self):
        return element_Pin(self, 0)

    @property
    def o_upmid(self):
        return element_Pin(self, 1)

    @property
    def o_lowmid(self):
        return element_Pin(self, 2)

    @property
    def o_low(self):
        return element_Pin(self, 3)

# 随机数发生器
class Random_Generator(_big_element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Random_Generator, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Random Generator'

    @property
    def i_up(self):
        return element_Pin(self, 4)

    @property
    def i_low(self):
        return element_Pin(self, 5)

    @property
    def o_up(self):
        return element_Pin(self, 0)

    @property
    def o_upmid(self):
        return element_Pin(self, 1)

    @property
    def o_lowmid(self):
        return element_Pin(self, 2)

    @property
    def o_low(self):
        return element_Pin(self, 3)

# 8位输入器
@_element_Method
@_logic_Circuit_Method
class eight_bit_Input:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
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
        return element_Pin(self, 0)

    @property
    def i_upmid(self):
        return element_Pin(self, 1)

    @property
    def i_lowmid(self):
        return element_Pin(self, 2)

    @property
    def i_low(self):
        return element_Pin(self, 3)

    @property
    def o_up(self):
        return element_Pin(self, 4)

    @property
    def o_upmid(self):
        return element_Pin(self, 5)

    @property
    def o_lowmid(self):
        return element_Pin(self, 6)

    @property
    def o_low(self):
        return element_Pin(self, 7)

# 8位显示器
@_element_Method
@_logic_Circuit_Method
class eight_bit_Display:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': '8bit Display', 'Identifier': '',
                          'IsBroken': False, 'IsLocked': False,
                          'Properties': {'高电平': 3.0, '低电平': 0.0, '状态': 0.0, '锁定': 1.0},
                          'Statistics': {'7': 0.0, '6': 0.0, '5': 0.0, '4': 0.0, '3': 0.0, '2': 0.0, '1': 0.0, '0': 0.0,
                                         '十进制': 0.0}, 'Position': '',
                          'Rotation': '', 'DiagramCached': False,
                          'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i_up(self):
        return element_Pin(self, 0)

    @property
    def i_upmid(self):
        return element_Pin(self, 1)

    @property
    def i_lowmid(self):
        return element_Pin(self, 2)

    @property
    def i_low(self):
        return element_Pin(self, 3)

    @property
    def o_up(self):
        return element_Pin(self, 4)

    @property
    def o_upmid(self):
        return element_Pin(self, 5)

    @property
    def o_lowmid(self):
        return element_Pin(self, 6)

    @property
    def o_low(self):
        return element_Pin(self, 7)

# 开关基类
@_element_Method
class _switch_Element:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {"ModelID": "", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"开关": 0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": '', "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

# 简单开关
@_two_pin_ArtificialCircuit_Pin
class Simple_Switch(_switch_Element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Simple_Switch, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Simple Switch'

# 单刀双掷开关
class SPDT_Switch(_switch_Element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(SPDT_Switch, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'SPDT Switch'

    @property
    def l(self):
        return element_Pin(self, 0)

    @property
    def mid(self):
        return element_Pin(self, 1)

    @property
    def r(self):
        return element_Pin(self, 2)

# 双刀双掷开关
class DPDT_Switch(_switch_Element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(DPDT_Switch, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'DPDT Switch'

    @property
    def l_up(self):
        return element_Pin(self, 3)

    @property
    def mid_up(self):
        return element_Pin(self, 4)

    @property
    def r_up(self):
        return element_Pin(self, 5)

    @property
    def l_low(self):
        return element_Pin(self, 0)

    @property
    def mid_low(self):
        return element_Pin(self, 1)

    @property
    def r_low(self):
        return element_Pin(self, 2)

# 按钮开关
@_element_Method
@_two_pin_ArtificialCircuit_Pin
class Push_Switch:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {
            'ModelID': 'Push Switch', 'Identifier': '', 'IsBroken': False, 'IsLocked': False,
            'Properties': {'开关': 0.0, '默认开关': 0.0, '锁定': 1.0}, 'Statistics': {'电流': 0.0}, 'Position': '',
            'Rotation': '', 'DiagramCached': False, 'DiagramPosition': {
                'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 555定时器
@_element_Method
class NE555:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': '555 Timer', 'Identifier': '', 'IsBroken': False,
                           'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '锁定': 1.0},
                           'Statistics': {'供电': 10, '放电': 0.0, '阈值': 4,
                                          '控制': 6.6666666666666666, '触发': 4,
                                          '输出': 0, '重设': 10, '接地': 0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def VCC(self):
        return element_Pin(self, 0)

    @property
    def Dis(self):
        return element_Pin(self, 1)

    @property
    def Thr(self):
        return element_Pin(self, 2)

    @property
    def Ctrl(self):
        return element_Pin(self, 3)

    @property
    def Trig(self):
        return element_Pin(self, 4)

    @property
    def Out(self):
        return element_Pin(self, 5)

    @property
    def Reset(self):
        return element_Pin(self, 6)

    @property
    def Ground(self):
        return element_Pin(self, 7)

# 电容
@_element_Method
@_two_pin_ArtificialCircuit_Pin
class Basic_Capacitor:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': 'Basic Capacitor', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False, 'Properties': {'耐压': 16.0, '电容': 1e-06, '内阻': 5.0, '锁定': 1.0},
                           'Statistics': {}, 'Position': '',
                           'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 一节电池
@_element_Method
@_two_pin_ArtificialCircuit_Pin
class Battery_Source:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': 'Battery Source', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False, 'Properties': {'最大功率': 16.2, '电压': 3.0, '内阻': 0.5},
                           'Statistics': {'电流': 0, '功率': 0, '电压': 0},
                           'Position': '',
                           'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 学生电源
@_element_Method
class Student_Source:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
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
        return element_Pin(self, 0)

    @property
    def l_mid(self):
        return element_Pin(self, 1)

    @property
    def r_mid(self):
        return element_Pin(self, 2)

    @property
    def r(self):
        return element_Pin(self, 3)

# 接地
@_element_Method
class Ground_Component:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': 'Ground Component', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False, 'Properties': {'锁定': 1.0},
                           'Statistics': {'电流': 0}, 'Position': '',
                           'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i(self):
        return element_Pin(self, 0)

# 电阻
@_element_Method
@_two_pin_ArtificialCircuit_Pin
class Resistor:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': 'Resistor', 'Identifier': '', 'IsBroken': False,
                           'IsLocked': False,
                           'Properties': {'最大电阻': 1000_0000.0, '最小电阻': 0.1, '电阻': 10, '锁定': 1.0},
                           'Statistics': {'瞬间功率': 0, '瞬间电流': 0,
                                          '瞬间电压': 0, '功率': 0,
                                          '电压': 0, '电流': 0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 运算放大器
@_element_Method
class Operational_Amplifier:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
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
        return element_Pin(self, 0)

    @property
    def i_low(self):
        return element_Pin(self, 1)

    @property
    def o(self):
        return element_Pin(self, 2)

# 小电扇
@_element_Method
@_two_pin_ArtificialCircuit_Pin
class Electric_Fan:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': 'Electric Fan', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False,
                           'Properties': {'额定电阻': 1.0, '马达常数': 0.1, '转动惯量': 0.01, '电感': 5e-05, '负荷扭矩': 0.01,
                                          '反电动势系数': 0.001, '粘性摩擦系数': 0.01, '角速度': 0, '锁定': 1.0},
                           'Statistics': {'瞬间功率': 0, '瞬间电流': 0, '瞬间电压': 0, '功率': 0,
                                          '电压': 0, '电流': 0, '摩擦扭矩': 0, '角速度': 0,
                                          '反电动势': 0, '转速': 0, '输入功率': 0, '输出功率': 0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 继电器
@_element_Method
class Relay_Component:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': 'Relay Component', 'Identifier': '', 'IsBroken': False, 'IsLocked': False,
                           'Properties': {'开关': 0.0, '线圈电感': 0.2, '线圈电阻': 20.0,
                                          '接通电流': 0.02, '额定电流': 1.0, '锁定': 1.0}, 'Statistics': {},
                           'Position': '', 'Rotation': '',
                           'DiagramCached': False, 'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0},
                           'DiagramRotation': 0}

    @property
    def l_up(self):
        return element_Pin(self, 0)

    @property
    def l_low(self):
        return element_Pin(self, 2)

    @property
    def mid(self):
        return element_Pin(self, 1)

    @property
    def r_up(self):
        return element_Pin(self, 4)

    @property
    def r_low(self):
        return element_Pin(self, 5)

# n mos
@_element_Method
class N_MOSFET:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': 'N-MOSFET', 'Identifier': '', 'IsBroken': False,
                           'IsLocked': False, 'Properties': {'PNP': 1.0, '放大系数': 0.027, '阈值电压': 1.5, '最大功率': 100.0, '锁定': 1.0},
                           'Statistics': {'电压GS': 0.0, '电压': 0.0, '电流': 0.0, '功率': 0.0, '状态': 0.0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def D(self):
        return element_Pin(self, 2)

    @property
    def S(self):
        return element_Pin(self, 1)

    @property
    def G(self):
        return element_Pin(self, 0)

# 波形发生器基类
@_element_Method
class _source_element:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': '', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False,
                           'Properties': {'电压': 3.0, '内阻': 0.5, '频率': 20000.0, '偏移': 0.0, '占空比': 0.5, '锁定': 1.0},
                           'Statistics': {'电流': 0.0, '功率': 0.0, '电压': -3.0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def l(self):
        return element_Pin(self, 0)
    i = l

    @property
    def r(self):
        return element_Pin(self, 1)
    o = r

# 正弦波发生器
class Sinewave_Source(_source_element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Sinewave_Source, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Sinewave Source'

# 方波发生器
class Square_Source(_source_element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Square_Source, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Square Source'

# 三角波发生器
class Triangle_Source(_source_element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Triangle_Source, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Triangle Source'

# 锯齿波发生器
class Sawtooth_Source(_source_element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Sawtooth_Source, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Sawtooth Source'

# 尖峰波发生器
class Pulse_Source(_source_element):
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        super(Pulse_Source, self).__init__(x, y, z)
        self._arguments['ModelID'] = 'Pulse Source'

# 保险丝
@_element_Method
@_two_pin_ArtificialCircuit_Pin
class Fuse_Component:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': 'Fuse Component', 'Identifier': '', 'IsBroken': False, 'IsLocked': False,
                           'Properties': {'开关': 1.0, '额定电流': 0.30000001192092896, '熔断电流': 0.5, '锁定': 1.0},
                           'Statistics': {'瞬间功率': 0.0, '瞬间电流': 0.0, '瞬间电压': 0.0, '功率': 0.0, '电压': 0.0, '电流': 0.0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 滑动变阻器
@_element_Method
class Slide_Rheostat:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': 'Slide Rheostat', 'Identifier': '', 'IsBroken': False, 'IsLocked': False,
                           'Properties': {'额定电阻': 10.0, '滑块位置': 0.0, '电阻1': 10, '电阻2': 10.0, '锁定': 1.0},
                           'Statistics': {'瞬间功率': 0.0, '瞬间电流': 0.0, '瞬间电压': 0.0, '功率': 0.0, '电压': 0.0, '电流': 0.0,
                                          '瞬间功率1': 0.0, '瞬间电流1': 0.0, '瞬间电压1': 0.0, '功率1': 0.0, '电压1': 0.0, '电流1': 0.0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def l_low(self):
        return element_Pin(self, 0)

    @property
    def r_low(self):
        return element_Pin(self, 1)

    @property
    def l_up(self):
        return element_Pin(self, 2)

    @property
    def r_up(self):
        return element_Pin(self, 3)

# 简单乐器（更多功能的源代码在union_music）
@_element_Method
class Simple_Instrument:
    @_element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': 'Simple Instrument', 'Identifier': '', 'IsBroken': False, 'IsLocked': False,
                           'Properties': {'额定电压': 3.0, '额定功率': 0.3, '音量': 1.0, '音高': 60.0, '节拍': 70.0, '锁定': 1.0,
                                          '乐器': 1.0},
                           'Statistics': {'瞬间功率': 0, '瞬间电流': 0, '瞬间电压': 0, '功率': 0, '电压': 0, '电流': 0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i(self):
        return element_Pin(self, 0)

    @property
    def o(self):
        return element_Pin(self, 1)

    # 设置音高
    '''
    输入格式：
        中音区： 
            '1' -> do,
            '1#' or '2b' -> do#,
            '2' -> ri 
            ... 
            7 -> xi
        低1个八度： '.1', '.1#', '.2' ...
        低2个八度： '..1', '..1#', '..2' ...
        升1个八度： '1.', '1#.', '2' ...
        以此类推即可
    '''
    def set_Tonality(self, tonality: Union[int, str]) -> None:
        if isinstance(tonality, int):
            if 0 < tonality < 8:
                raise RuntimeError('Input data error')
            tonality = str(tonality)
        elif isinstance(tonality, str):
            tonality.strip()
            for char in tonality:
                if char not in digits[1:8] and char not in '.#b':
                    raise RuntimeError('Input data error')
        else:
            raise RuntimeError('The entered data type is incorrect')

        pitch, pitchIndex = None, None
        for char in tonality:
            if char in digits[1:8]:
                pitch = [60, 62, 64, 65, 67, 69, 71][int(char) - 1]
                pitchIndex = tonality.find(char)
        if pitch == None:
            raise RuntimeError('Input data error')
        for charIndex in range(tonality.__len__()):
            char = tonality[charIndex]
            if char == '.':
                if charIndex < pitchIndex:
                    pitch -= 12
                else:
                    pitch += 12
            elif char in digits:
                continue
            elif char == '#':
                if charIndex != pitchIndex + 1:
                    raise RuntimeError('Input data error')
                pitch += 1
            elif char == 'b':
                if charIndex != pitchIndex + 1:
                    raise RuntimeError('Input data error')
                pitch -= 1
            else:
                raise RuntimeError('Input data error')
        self._arguments['Properties']['音高'] = pitch

### end 原件类 ###
