# -*- coding: utf-8 -*-
from typing import Optional

from ..wire import Pin
from physicsLab.typehint import numType
from ._elementBase import CircuitBase, two_pin_ArtificialCircuit_Pin

# 开关基类
class _switch_Base(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "", "Identifier": "", "IsBroken": False,
                          "IsLocked": False, "Properties": {"开关": 0, "锁定": 1.0},
                          "Statistics": {}, "Position": "",
                          "Rotation": "", "DiagramCached": False,
                          "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0}

# 简单开关
@two_pin_ArtificialCircuit_Pin
class Simple_Switch(_switch_Base):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(Simple_Switch, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "Simple Switch"

# 单刀双掷开关
class SPDT_Switch(_switch_Base):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        super(SPDT_Switch, self).__init__(x, y, z, elementXYZ)
        self._arguments["ModelID"] = "SPDT Switch"

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
@two_pin_ArtificialCircuit_Pin
class Push_Switch(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {
            "ModelID": "Push Switch", "Identifier": "", "IsBroken": False, "IsLocked": False,
            "Properties": {"开关": 0.0, "默认开关": 0.0, "锁定": 1.0}, "Statistics": {"电流": 0.0}, "Position": "",
            "Rotation": "", "DiagramCached": False, "DiagramPosition": {
                "X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}


# 一节电池
@two_pin_ArtificialCircuit_Pin
class Battery_Source(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Battery Source", "Identifier": "",
                           "IsBroken": False, "IsLocked": False, "Properties": {"最大功率": 16.2, "电压": 3.0, "内阻": 0.5},
                           "Statistics": {"电流": 0, "功率": 0, "电压": 0},
                           "Position": "",
                           "Rotation": "", "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

# 学生电源
class Student_Source(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Student Source", "Identifier": "", "IsBroken": False, "IsLocked": False,
                           "Properties": {"交流电压": 3.0, "直流电压": 3.0, "开关": 0.0, "频率": 50.0},
                           "Statistics": {"瞬间功率": 0.0, "瞬间电压": 0.0, "瞬间电流": 0.0,
                                          "瞬间电阻": 0.0, "功率": 0.0, "电阻": 0.0, "电流": 0.0,
                                          "瞬间功率1": 0.0, "瞬间电压1": 0.0, "瞬间电流1": 0.0,
                                          "瞬间电阻1": 0.0,
                                          "功率1": 0.0, "电阻1": 0.0, "电流1": 0.0},
                           "Position": "",
                           "Rotation": "", "DiagramCached": False,
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
@two_pin_ArtificialCircuit_Pin
class Resistor(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Resistor", "Identifier": "", "IsBroken": False,
                           "IsLocked": False,
                           "Properties": {"最大电阻": 1000_0000.0, "最小电阻": 0.1, "电阻": 10, "锁定": 1.0},
                           "Statistics": {"瞬间功率": 0, "瞬间电流": 0,
                                          "瞬间电压": 0, "功率": 0,
                                          "电压": 0, "电流": 0},
                           "Position": "", "Rotation": "", "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

# 保险丝
@two_pin_ArtificialCircuit_Pin
class Fuse_Component(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Fuse Component", "Identifier": "", "IsBroken": False, "IsLocked": False,
                           "Properties": {"开关": 1.0, "额定电流": 0.30000001192092896, "熔断电流": 0.5, "锁定": 1.0},
                           "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0, "功率": 0.0, "电压": 0.0, "电流": 0.0},
                           "Position": "", "Rotation": "", "DiagramCached": False,
                           "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

# 滑动变阻器
class Slide_Rheostat(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
        self._arguments = {"ModelID": "Slide Rheostat", "Identifier": "", "IsBroken": False, "IsLocked": False,
                           "Properties": {"额定电阻": 10.0, "滑块位置": 0.0, "电阻1": 10, "电阻2": 10.0, "锁定": 1.0},
                           "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0, "功率": 0.0, "电压": 0.0, "电流": 0.0,
                                          "瞬间功率1": 0.0, "瞬间电流1": 0.0, "瞬间电压1": 0.0, "功率1": 0.0, "电压1": 0.0, "电流1": 0.0},
                           "Position": "", "Rotation": "", "DiagramCached": False,
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