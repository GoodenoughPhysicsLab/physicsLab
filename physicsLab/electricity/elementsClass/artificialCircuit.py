#coding=utf-8
from electricity.elementsClass._elementClassHead import *

# 555定时器
class NE555(elementObject):
    @element_Init_HEAD
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
@two_pin_ArtificialCircuit_Pin
class Basic_Capacitor(elementObject):
    @element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': 'Basic Capacitor', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False, 'Properties': {'耐压': 16.0, '电容': 1e-06, '内阻': 5.0, '锁定': 1.0},
                           'Statistics': {}, 'Position': '',
                           'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 接地
class Ground_Component(elementObject):
    @element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': 'Ground Component', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False, 'Properties': {'锁定': 1.0},
                           'Statistics': {'电流': 0}, 'Position': '',
                           'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i(self):
        return element_Pin(self, 0)

# 运算放大器
class Operational_Amplifier(elementObject):
    @element_Init_HEAD
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

# 继电器
class Relay_Component(elementObject):
    @element_Init_HEAD
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
class N_MOSFET(elementObject):
    @element_Init_HEAD
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
class _source_element(elementObject):
    @element_Init_HEAD
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
