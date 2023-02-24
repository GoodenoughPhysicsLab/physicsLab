#coding=utf-8
from electricity.elementsClass._elementClassHead import *

# _arguments是参数的意思

# 逻辑输入
@logic_Circuit_Method
class Logic_Input(elementObject):
    @element_Init_HEAD
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
@logic_Circuit_Method
class Logic_Output(elementObject):
    @element_Init_HEAD
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
@logic_Circuit_Method
class _2_pin_Gate(elementObject):
    @element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': '', 'Identifier': "", 'IsBroken': False,
                          'IsLocked': False, 'Properties': {'高电平': 3.0, '低电平': 0.0, '最大电流': 0.1, '锁定': 1.0},
                          'Statistics': {}, 'Position': "", 'Rotation': '', 'DiagramCached': False,
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
@logic_Circuit_Method
class _3_pin_Gate(elementObject):
    @element_Init_HEAD
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

# 2体积元件父类
@logic_Circuit_Method
class _big_element(elementObject):
    @element_Init_HEAD
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
@logic_Circuit_Method
class eight_bit_Input(elementObject):
    @element_Init_HEAD
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
@logic_Circuit_Method
class eight_bit_Display(elementObject):
    @element_Init_HEAD
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