# -*- coding: utf-8 -*-
from physicsLab.typehint import numType
from ..wire import InputPin, OutputPin
from ._elementBase import CircuitBase
from physicsLab.typehint import Optional, Self

class _logicBase(CircuitBase):
    # 设置高电平的值
    def set_HighLeaveValue(self, num: numType) -> Self:
        if not isinstance(num, (int, float)):
            raise TypeError("illegal argument")
        if num < self.get_LowLeaveValue():
            raise TypeError("illegal range")
        self._arguments["Properties"]["高电平"] = num # type: ignore -> subclass must has attr _arguments

        return self

    # 获取高电平的值
    def get_HighLeaveValue(self) -> numType:
        return self._arguments["Properties"]["高电平"] # type: ignore -> subclass must has attr _arguments

    # 设置低电平的值
    def set_LowLeaveValue(self, num: numType) -> Self:
        if not isinstance(num, (int, float)):
            raise TypeError("illegal argument")
        if num > self.get_HighLeaveValue():
            raise TypeError("illegal range")
        self._arguments["Properties"]["低电平"] = num # type: ignore -> subclass must has attr _arguments

        return self

    # 获取高电平的值
    def get_LowLeaveValue(self):
        return self._arguments["Properties"]["低电平"] # type: ignore -> subclass must has attr _arguments

# 逻辑输入
class Logic_Input(_logicBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Logic Input", "Identifier": "",
                          "IsBroken": False, "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0, "开关": 0},
                          "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
                          "Position": "",
                          "Rotation": "", "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
                          "DiagramRotation": 0}

    # 将逻辑输入的状态设置为1
    def set_highLevel(self) -> "Logic_Input":
        self._arguments["Properties"][u"开关"] = 1.0
        return self

    @property
    def o(self) -> OutputPin:
        return OutputPin(self, 0)

# 逻辑输出
class Logic_Output(_logicBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Logic Output", "Identifier": "",
                          "IsBroken": False, "IsLocked": False,
                          "Properties": {"状态": 0.0, "高电平": 3.0, "低电平": 0.0, "锁定": 1.0}, "Statistics": {},
                          "Position": "",
                          "Rotation": "0,180,0", "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

    @property
    def i(self) -> InputPin:
            return InputPin(self, 0)

# 2引脚门电路
class _2_pin_Gate(_logicBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "最大电流": 0.1, "锁定": 1.0},
                          "Statistics": {}, "Position": "", "Rotation": "", "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

    @property
    def i(self) -> InputPin:
        return InputPin(self, 0)

    @property
    def o(self) -> OutputPin:
        return OutputPin(self, 1)

# 是门
class Yes_Gate(_2_pin_Gate):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Yes_Gate, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Yes Gate"

# 非门
class No_Gate(_2_pin_Gate):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(No_Gate, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "No Gate"

# 3引脚门电路
class _3_pin_Gate(_logicBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "最大电流": 0.1, "锁定": 1.0},
                          "Statistics": {}, "Position": "", "Rotation": "", "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

    @property
    def i_up(self) -> InputPin:
        return InputPin(self, 0)

    @property
    def i_low(self) -> InputPin:
        return InputPin(self, 1)

    @property
    def o(self) -> OutputPin:
        return OutputPin(self, 2)

# 或门
class Or_Gate(_3_pin_Gate):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Or_Gate, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Or Gate"

# 与门
class And_Gate(_3_pin_Gate):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(And_Gate, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "And Gate"

# 或非门
class Nor_Gate(_3_pin_Gate):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Nor_Gate, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Nor Gate"

# 与非门
class Nand_Gate(_3_pin_Gate):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Nand_Gate, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Nand Gate"

# 异或门
class Xor_Gate(_3_pin_Gate):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Xor_Gate, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Xor Gate"

# 同或门
class Xnor_Gate(_3_pin_Gate):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Xnor_Gate, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Xnor Gate"

# 蕴含门
class Imp_Gate(_3_pin_Gate):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Imp_Gate, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Imp Gate"

# 蕴含非门
class Nimp_Gate(_3_pin_Gate):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Nimp_Gate, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Nimp Gate"

# 2体积元件父类
class _big_element(_logicBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0}, "Statistics": {},
                          "Position": "", "Rotation": "", "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

    @property
    def is_bigElement(self):
        return True

# 半加器
class Half_Adder(_big_element):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Half_Adder, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Half Adder"

    @property
    def i_up(self) -> InputPin:
        return InputPin(self, 2)

    @property
    def i_low(self) -> InputPin:
        return InputPin(self, 3)

    @property
    def o_up(self) -> OutputPin:
        return OutputPin(self, 0)

    @property
    def o_low(self) -> OutputPin:
        return OutputPin(self, 1)

# 全加器
class Full_Adder(_big_element):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Full_Adder, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Full Adder"

    @property
    def i_up(self) -> InputPin:
        return InputPin(self, 2)

    @property
    def i_mid(self) -> InputPin:
        return InputPin(self, 3)

    @property
    def i_low(self) -> InputPin:
        return InputPin(self, 4)

    @property
    def o_up(self) -> OutputPin:
        return OutputPin(self, 0)

    @property
    def o_low(self) -> OutputPin:
        return OutputPin(self, 1)

# 二位乘法器
class Multiplier(_big_element):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Multiplier, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Multiplier"

    @property
    def i_up(self) -> InputPin:
        return InputPin(self, 4)

    @property
    def i_upmid(self) -> InputPin:
        return InputPin(self, 5)

    @property
    def i_lowmid(self) -> InputPin:
        return InputPin(self, 6)

    @property
    def i_low(self) -> InputPin:
        return InputPin(self, 7)

    @property
    def o_up(self) -> OutputPin:
        return OutputPin(self, 0)

    @property
    def o_upmid(self) -> OutputPin:
        return OutputPin(self, 1)

    @property
    def o_lowmid(self) -> OutputPin:
        return OutputPin(self, 2)

    @property
    def o_low(self) -> OutputPin:
        return OutputPin(self, 3)

# D触发器
class D_Flipflop(_big_element):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(D_Flipflop, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "D Flipflop"

    @property
    def i_up(self) -> InputPin:
        return InputPin(self, 2)

    @property
    def i_low(self) -> InputPin:
        return InputPin(self, 3)

    @property
    def o_up(self) -> OutputPin:
        return OutputPin(self, 0)

    @property
    def o_low(self) -> OutputPin:
        return OutputPin(self, 1)

# T触发器
class T_Flipflop(_big_element):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(T_Flipflop, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "T Flipflop"

    @property
    def i_up(self) -> InputPin:
        return InputPin(self, 2)

    @property
    def i_low(self) -> InputPin:
        return InputPin(self, 3)

    @property
    def o_up(self) -> OutputPin:
        return OutputPin(self, 0)

    @property
    def o_low(self) -> OutputPin:
        return OutputPin(self, 1)

# JK触发器
class JK_Flipflop(_big_element):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(JK_Flipflop, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "JK Flipflop"

    @property
    def i_up(self) -> InputPin:
        return InputPin(self, 2)

    @property
    def i_mid(self) -> InputPin:
        return InputPin(self, 3)

    @property
    def i_low(self) -> InputPin:
        return InputPin(self, 4)

    @property
    def o_up(self) -> OutputPin:
        return OutputPin(self, 0)

    @property
    def o_low(self) -> OutputPin:
        return OutputPin(self, 1)

# 计数器
class Counter(_big_element):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Counter, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Counter"

    @property
    def i_up(self) -> InputPin:
        return InputPin(self, 4)

    @property
    def i_low(self) -> InputPin:
        return InputPin(self, 5)

    @property
    def o_up(self) -> OutputPin:
        return OutputPin(self, 0)

    @property
    def o_upmid(self) -> OutputPin:
        return OutputPin(self, 1)

    @property
    def o_lowmid(self) -> OutputPin:
        return OutputPin(self, 2)

    @property
    def o_low(self) -> OutputPin:
        return OutputPin(self, 3)

# 随机数发生器
class Random_Generator(_big_element):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Random_Generator, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Random Generator"

    @property
    def i_up(self) -> InputPin:
        return InputPin(self, 4)

    @property
    def i_low(self) -> InputPin:
        return InputPin(self, 5)

    @property
    def o_up(self) -> OutputPin:
        return OutputPin(self, 0)

    @property
    def o_upmid(self) -> OutputPin:
        return OutputPin(self, 1)

    @property
    def o_lowmid(self) -> OutputPin:
        return OutputPin(self, 2)

    @property
    def o_low(self) -> OutputPin:
        return OutputPin(self, 3)

# 8位输入器
class eight_bit_Input(_logicBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "8bit Input", "Identifier": "", "IsBroken": False,
                           "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "十进制": 0.0, "锁定": 1.0},
                           "Statistics": {}, "Position": "", "Rotation": "", "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

    def set_num(self, num : int):
        if 0 <= num <= 255:
            self._arguments["Properties"]["十进制"] = num
        else:
            raise RuntimeError("The number range entered is incorrect")

    @property
    def is_bigElement(self):
        return True

    @property
    def i_up(self) -> InputPin:
        return InputPin(self, 0)

    @property
    def i_upmid(self) -> InputPin:
        return InputPin(self, 1)

    @property
    def i_lowmid(self) -> InputPin:
        return InputPin(self, 2)

    @property
    def i_low(self) -> InputPin:
        return InputPin(self, 3)

    @property
    def o_up(self) -> OutputPin:
        return OutputPin(self, 4)

    @property
    def o_upmid(self) -> OutputPin:
        return OutputPin(self, 5)

    @property
    def o_lowmid(self) -> OutputPin:
        return OutputPin(self, 6)

    @property
    def o_low(self) -> OutputPin:
        return OutputPin(self, 7)

# 8位显示器
class eight_bit_Display(_logicBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "8bit Display", "Identifier": "",
                          "IsBroken": False, "IsLocked": False,
                          "Properties": {"高电平": 3.0, "低电平": 0.0, "状态": 0.0, "锁定": 1.0},
                          "Statistics": {"7": 0.0, "6": 0.0, "5": 0.0, "4": 0.0, "3": 0.0, "2": 0.0, "1": 0.0, "0": 0.0,
                                         "十进制": 0.0}, "Position": "",
                          "Rotation": "", "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

    @property
    def is_bigElement(self):
        return True

    @property
    def i_up(self) -> InputPin:
        return InputPin(self, 0)

    @property
    def i_upmid(self) -> InputPin:
        return InputPin(self, 1)

    @property
    def i_lowmid(self) -> InputPin:
        return InputPin(self, 2)

    @property
    def i_low(self) -> InputPin:
        return InputPin(self, 3)

    @property
    def o_up(self) -> OutputPin:
        return OutputPin(self, 4)

    @property
    def o_upmid(self) -> OutputPin:
        return OutputPin(self, 5)

    @property
    def o_lowmid(self) -> OutputPin:
        return OutputPin(self, 6)

    @property
    def o_low(self) -> OutputPin:
        return OutputPin(self, 7)