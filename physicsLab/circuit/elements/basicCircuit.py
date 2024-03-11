# -*- coding: utf-8 -*-
from typing import Optional

from ..wire import Pin
from physicsLab.savTemplate import Generate
from physicsLab.typehint import numType, Self
from ._elementBase import CircuitBase, TwoPinMixIn

# 开关基类
class _switch_Base(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "", "Identifier": Generate, "IsBroken": False,
                          "IsLocked": False, "Properties": {"开关": 0, "锁定": 1.0},
                          "Statistics": {}, "Position": Generate,
                          "Rotation": Generate, "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

    # 断开开关
    def turn_off_switch(self) -> Self:
        self._arguments["Properties"]["开关"] = 0
        return self

# 简单开关
class Simple_Switch(_switch_Base, TwoPinMixIn):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Simple_Switch, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Simple Switch"

    # 闭合开关
    def turn_on_switch(self) -> Self:
        self._arguments["Properties"]["开关"] = 1
        return self

# 单刀双掷开关
class SPDT_Switch(_switch_Base):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(SPDT_Switch, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "SPDT Switch"

    # 向左闭合开关
    def left_turn_on_switch(self) -> Self:
        self._arguments["Properties"]["开关"] = 1
        return self

    # 向右闭合开关
    def right_turn_on_switch(self) -> Self:
        self._arguments["Properties"]["开关"] = 2
        return self

    @property
    def l(self) -> Pin:
        return Pin(self, 0)

    @property
    def mid(self) -> Pin:
        return Pin(self, 1)

    @property
    def r(self) -> Pin:
        return Pin(self, 2)

# 双刀双掷开关
class DPDT_Switch(_switch_Base):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(DPDT_Switch, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "DPDT Switch"

    # 向左闭合开关
    def left_turn_on_switch(self) -> Self:
        self._arguments["Properties"]["开关"] = 1
        return self

    # 向右闭合开关
    def right_turn_on_switch(self) -> Self:
        self._arguments["Properties"]["开关"] = 2
        return self

    @property
    def l_up(self) -> Pin:
        return Pin(self, 3)

    @property
    def mid_up(self) -> Pin:
        return Pin(self, 4)

    @property
    def r_up(self) -> Pin:
        return Pin(self, 5)

    @property
    def l_low(self) -> Pin:
        return Pin(self, 0)

    @property
    def mid_low(self) -> Pin:
        return Pin(self, 1)

    @property
    def r_low(self) -> Pin:
        return Pin(self, 2)

# 按钮开关
class Push_Switch(TwoPinMixIn):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Push Switch", "Identifier": Generate,
                           "IsBroken": False, "IsLocked": False,
                           "Properties": {"开关": 0.0, "默认开关": 0.0, "锁定": 1.0},
                           "Statistics": {"电流": 0.0},
                           "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

# 空气开关
class Air_Switch(TwoPinMixIn):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Air Switch", "Identifier": Generate,
                           "IsBroken": False, "IsLocked": False,
                           "Properties": {"开关": 0.0, "额定电流": 10.0, "锁定": 1.0},
                           "Statistics": {},
                           "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

    # 断开开关
    def turn_off_switch(self) -> Self:
        self._arguments["Properties"]["开关"] = 0
        return self

    # 闭合开关
    def turn_on_switch(self) -> Self:
        self._arguments["Properties"]["开关"] = 1
        return self

# 白炽灯泡
class Incandescent_Lamp(TwoPinMixIn):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Incandescent Lamp", "Identifier": Generate,
                           "IsBroken": False, "IsLocked": False,
                           "Properties": {"额定电压": 3.0, "额定功率": 0.85},
                           "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0,
                                          "功率": 0.0, "电压": 0.0, "电流": 0.0,
                                          "灯泡温度": 300.0, "电阻": 0.5},
                            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
                            "DiagramRotation": 0}

# 一节电池
class Battery_Source(TwoPinMixIn):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Battery Source", "Identifier": Generate,
                           "IsBroken": False, "IsLocked": False,
                           "Properties": {"最大功率": 16.2, "电压": 3.0, "内阻": 0.5},
                           "Statistics": {"电流": 0, "功率": 0, "电压": 0},
                           "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

# 学生电源
class Student_Source(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Student Source", "Identifier": Generate,
                           "IsBroken": False, "IsLocked": False,
                           "Properties": {"交流电压": 3.0, "直流电压": 3.0, "开关": 0.0, "频率": 50.0},
                           "Statistics": {"瞬间功率": 0.0, "瞬间电压": 0.0, "瞬间电流": 0.0,
                                          "瞬间电阻": 0.0, "功率": 0.0, "电阻": 0.0, "电流": 0.0,
                                          "瞬间功率1": 0.0, "瞬间电压1": 0.0, "瞬间电流1": 0.0,
                                          "瞬间电阻1": 0.0, "功率1": 0.0, "电阻1": 0.0, "电流1": 0.0},
                           "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
                           "DiagramRotation": 0}

    @property
    def l(self) -> Pin:
        return Pin(self, 0)

    @property
    def l_mid(self) -> Pin:
        return Pin(self, 1)

    @property
    def r_mid(self) -> Pin:
        return Pin(self, 2)

    @property
    def r(self) -> Pin:
        return Pin(self, 3)

# 电阻
class Resistor(TwoPinMixIn):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Resistor", "Identifier": Generate, "IsBroken": False,
                           "IsLocked": False,
                           "Properties": {"最大电阻": 1000_0000.0, "最小电阻": 0.1, "电阻": 10, "锁定": 1.0},
                           "Statistics": {"瞬间功率": 0, "瞬间电流": 0, "瞬间电压": 0, "功率": 0,
                                          "电压": 0, "电流": 0},
                           "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

# 保险丝
class Fuse_Component(TwoPinMixIn):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Fuse Component", "Identifier": Generate,
                           "IsBroken": False, "IsLocked": False,
                           "Properties": {"开关": 1.0, "额定电流": 0.3, "熔断电流": 0.5, "锁定": 1.0},
                           "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0,
                                          "功率": 0.0, "电压": 0.0, "电流": 0.0},
                           "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

# 滑动变阻器
class Slide_Rheostat(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Slide Rheostat", "Identifier": Generate,
                           "IsBroken": False, "IsLocked": False,
                           "Properties": {"额定电阻": 10.0, "滑块位置": 0.0,
                                          "电阻1": 10, "电阻2": 10.0, "锁定": 1.0},
                           "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0,
                                          "功率": 0.0, "电压": 0.0, "电流": 0.0,
                                          "瞬间功率1": 0.0, "瞬间电流1": 0.0, "瞬间电压1": 0.0,
                                          "功率1": 0.0, "电压1": 0.0, "电流1": 0.0},
                           "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

    @property
    def l_low(self) -> Pin:
        return Pin(self, 0)

    @property
    def r_low(self) -> Pin:
        return Pin(self, 1)

    @property
    def l_up(self) -> Pin:
        return Pin(self, 2)

    @property
    def r_up(self) -> Pin:
        return Pin(self, 3)

# 多用电表
class Multimeter(TwoPinMixIn):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Multimeter", "Identifier": Generate,
                           "IsBroken": False, "IsLocked": False,
                           "Properties": {"状态": 0.0, "锁定": 1.0},
                           "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0,
                                          "功率": 0.0, "电压": 0.0, "电流": 0.0},
                            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
                            "DiagramRotation": 0}

# 灵敏电流计
class Galvanometer(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Galvanometer", "Identifier": Generate,
                           "IsBroken": False, "IsLocked": False,
                           "Properties": {"量程": 3.0, "锁定": 1.0},
                           "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
                           "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
                           "DiagramRotation": 0}
    @property
    def l(self) -> Pin:
        return Pin(self, 0)

    @property
    def mid(self) -> Pin:
        return Pin(self, 1)

    @property
    def r(self) -> Pin:
        return Pin(self, 2)

# 微安表
class Microammeter(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Microammeter", "Identifier": Generate,
                           "IsBroken": False, "IsLocked": False,
                           "Properties": {"量程": 0.1, "锁定": 1.0},
                           "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
                           "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
                           "DiagramRotation": 0}

    @property
    def l(self) -> Pin:
        return Pin(self, 0)

    @property
    def mid(self) -> Pin:
        return Pin(self, 1)

    @property
    def r(self) -> Pin:
        return Pin(self, 2)

# 电能表
class Electricity_Meter(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Electricity Meter", "Identifier": Generate,
                           "IsBroken": False, "IsLocked": False,
                           "Properties": {"示数": 0.0, "额定电流": 6.0, "锁定": 1.0},
                           "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
                           "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
                           "DiagramRotation": 0}

    @property
    def l(self) -> Pin:
        return Pin(self, 0)

    @property
    def l_mid(self) -> Pin:
        return Pin(self, 2)

    @property
    def r_mid(self) -> Pin:
        return Pin(self, 1)

    @property
    def r(self) -> Pin:
        return Pin(self, 3)

# 电阻箱
class Resistance_Box(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Resistance Box", "Identifier": Generate,
                           "IsBroken": False, "IsLocked": False,
                           "Properties": {"最大电阻": 10000.0, "最小电阻": 0.1,
                                          "电阻": 10.0, "锁定": 1.0},
                           "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0,
                                          "功率": 0.0, "电压": 0.0, "电流": 0.0},
                            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
                            "DiagramRotation": 0}

    @property
    def l(self) -> Pin:
        return Pin(self, 0)

    @property
    def r(self) -> Pin:
        return Pin(self, 1)

# 直流安培表
class Simple_Ammeter(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Simple Ammeter", "Identifier": Generate,
                           "IsBroken": False, "IsLocked": False,
                           "Properties": {"量程": 0.007, "内阻": 0.007,
                                          "名义量程": 3.0, "锁定": 1.0},
                           "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
                           "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
                           "DiagramRotation": 0}

    @property
    def l(self) -> Pin:
        return Pin(self, 0)

    @property
    def mid(self) -> Pin:
        return Pin(self, 1)

    @property
    def r(self) -> Pin:
        return Pin(self, 2)

# 直流电压表
class Simple_Voltmeter(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Simple Voltmeter", "Identifier": Generate,
                           "IsBroken": False, "IsLocked": False,
                           "Properties": {"量程": 0.001, "名义量程": 15.0, "锁定": 1.0},
                           "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
                           "Position": Generate, "Rotation": Generate, "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
                           "DiagramRotation": 0}

    @property
    def l(self) -> Pin:
        return Pin(self, 0)

    @property
    def mid(self) -> Pin:
        return Pin(self, 1)

    @property
    def r(self) -> Pin:
        return Pin(self, 2)