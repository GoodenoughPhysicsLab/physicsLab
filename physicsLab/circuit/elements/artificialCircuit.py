# -*- coding: utf-8 -*-
from ..wire import Pin
from ._circuitbase import CircuitBase, TwoPinMixIn
from physicsLab.typehint import Optional, numType, CircuitElementData, Generate

class NE555(CircuitBase):
    ''' 555定时器 '''
    is_bigElement = True

    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "555 Timer", "Identifier": Generate, "IsBroken": False,
            "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
            "Statistics": {"供电": 10, "放电": 0.0, "阈值": 4,
                            "控制": 6.6666666666666666, "触发": 4,
                            "输出": 0, "重设": 10, "接地": 0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @property
    def VCC(self) -> Pin:
        return Pin(self, 0)

    @property
    def Dis(self) -> Pin:
        return Pin(self, 1)

    @property
    def Thr(self) -> Pin:
        return Pin(self, 2)

    @property
    def Ctrl(self) -> Pin:
        return Pin(self, 3)

    @property
    def Trig(self) -> Pin:
        return Pin(self, 4)

    @property
    def Out(self) -> Pin:
        return Pin(self, 5)

    @property
    def Reset(self) -> Pin:
        return Pin(self, 6)

    @property
    def Ground(self) -> Pin:
        return Pin(self, 7)

class Basic_Capacitor(TwoPinMixIn):
    ''' 电容 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Basic Capacitor", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"耐压": 16.0, "电容": 1e-06, "内阻": 5.0, "锁定": 1.0},
            "Statistics": {}, "Position": Generate,
            "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

class Basic_Inductor(TwoPinMixIn):
    ''' 电感 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Basic Inductor", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"额定电流": 1.0, "电感": 0.05, "内阻": 1.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

class Basic_Diode(TwoPinMixIn):
    ''' 二极管 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Basic Diode", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"击穿电压": 0.0, "前向压降": 0.6, "额定电流": 1.0,
                            "工作电压": 3.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

class Light_Emitting_Diode(TwoPinMixIn):
    ''' 发光二极管 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Light-Emitting Diode", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"反向耐压": 6.0, "击穿电压": 0.0, "前向压降": 2.1024259,
                            "工作电流": 0.01, "工作电压": 3.0, "锁定": 1.0},
            "Statistics": {"电流1": 0.0, "电压1": 0.0, "功率1": 0.0, "亮度1": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

class Ground_Component(CircuitBase):
    ''' 接地元件 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Ground Component", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False, "Properties": {"锁定": 1.0},
            "Statistics": {"电流": 0}, "Position": Generate,
            "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @property
    def i(self) -> Pin:
        return Pin(self, 0)

class Transformer(CircuitBase):
    ''' 理想变压器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Transformer", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"输入电压": 3.0, "输出电压": 36.0,
                            "额定功率": 20.0, "耦合系数": 1.0, "锁定": 1.0},
            "Statistics": {"电流1": 0.0, "电压1": 0.0, "功率1": 0.0, "电流2": 0.0,
                            "电压2": 0.0, "功率2": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @property
    def l_up(self) -> Pin:
        return Pin(self, 0)

    @property
    def r_up(self) -> Pin:
        return Pin(self, 1)

    @property
    def l_low(self) -> Pin:
        return Pin(self, 2)

    @property
    def r_low(self) -> Pin:
        return Pin(self, 3)

class Tapped_Transformer(CircuitBase):
    ''' 中心抽头变压器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Tapped Transformer", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"输入电压": 3.0, "输出电压": 36.0, "额定功率": 20.0,
                            "耦合系数": 1.0, "锁定": 1.0},
            "Statistics": {"电流1": 0.0, "电压1": 0.0, "功率1": 0.0, "电流2": 0.0, "电压2": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @property
    def l_up(self) -> Pin:
        return Pin(self, 0)

    @property
    def r_up(self) -> Pin:
        return Pin(self, 1)

    @property
    def l_low(self) -> Pin:
        return Pin(self, 2)

    @property
    def r_low(self) -> Pin:
        return Pin(self, 3)

    @property
    def mid(self) -> Pin:
        return Pin(self, 4)

class Mutual_Inductor(CircuitBase):
    ''' 理想互感 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Mutual Inductor", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"电感1": 4.0, "电感2": 1.0, "耦合系数": 1.0, "锁定": 1.0},
            "Statistics": {"电流1": 0.0, "电压1": 0.0, "功率1": 0.0, "电流2": 0.0,
                            "电压2": 0.0, "功率2": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @property
    def l_up(self) -> Pin:
        return Pin(self, 0)

    @property
    def r_up(self) -> Pin:
        return Pin(self, 1)

    @property
    def l_low(self) -> Pin:
        return Pin(self, 2)

    @property
    def r_low(self) -> Pin:
        return Pin(self, 3)

class Rectifier(CircuitBase):
    ''' 全波整流器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Rectifier", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"前向压降": 0.8, "额定电流": 1.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0}, "Position": Generate, "Rotation": Generate,
            "DiagramCached": False, "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @property
    def l_up(self) -> Pin:
        return Pin(self, 0)

    @property
    def r_up(self) -> Pin:
        return Pin(self, 1)

    @property
    def l_low(self) -> Pin:
        return Pin(self, 2)

    @property
    def r_low(self) -> Pin:
        return Pin(self, 3)

class Transistor(CircuitBase):
    ''' 三极管 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Transistor", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"PNP": 1.0, "放大系数": 100.0, "最大功率": 5.0, "锁定": 1.0},
            "Statistics": {"电压BC": 0.0, "电压BE": 0.0, "电压CE": 0.0, "功率": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @property
    def B(self) -> Pin:
        return Pin(self, 0)

    @property
    def C(self) -> Pin:
        return Pin(self, 1)

    @property
    def E(self) -> Pin:
        return Pin(self, 2)

class Comparator(CircuitBase):
    ''' 比较器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Comparator", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @property
    def o(self) -> Pin:
        return Pin(self, 0)

    @property
    def i_up(self) -> Pin:
        return Pin(self, 1)

    @property
    def i_low(self) -> Pin:
        return Pin(self, 2)

class Operational_Amplifier(CircuitBase):
    ''' 运算放大器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Operational Amplifier", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"增益系数": 100_0000.0, "最大电压": 15.0, "最小电压": -15.0, "锁定": 1.0},
            "Statistics": {"电压-": 0, "电压+": 0, "输出电压": 0,
                            "输出电流": 0, "输出功率": 0},
            "Position": Generate,"Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @property
    def i_up(self) -> Pin:
        return Pin(self, 0)

    @property
    def i_low(self) -> Pin:
        return Pin(self, 1)

    @property
    def o(self) -> Pin:
        return Pin(self, 2)

class Relay_Component(CircuitBase):
    ''' 继电器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Relay Component", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"开关": 0.0, "线圈电感": 0.2, "线圈电阻": 20.0,
                            "接通电流": 0.02, "额定电流": 1.0, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @property
    def l_up(self) -> Pin:
        return Pin(self, 0)

    @property
    def l_low(self) -> Pin:
        return Pin(self, 2)

    @property
    def mid(self) -> Pin:
        return Pin(self, 1)

    @property
    def r_up(self) -> Pin:
        return Pin(self, 4)

    @property
    def r_low(self) -> Pin:
        return Pin(self, 5)

class N_MOSFET(CircuitBase):
    ''' N-MOSFET '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "N-MOSFET", "Identifier": Generate, "IsBroken": False,
            "IsLocked": False, "Properties": {"PNP": 1.0, "放大系数": 0.027,
                                                "阈值电压": 1.5, "最大功率": 100.0, "锁定": 1.0},
            "Statistics": {"电压GS": 0.0, "电压": 0.0, "电流": 0.0, "功率": 0.0, "状态": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @property
    def D(self) -> Pin:
        return Pin(self, 2)

    @property
    def S(self) -> Pin:
        return Pin(self, 1)

    @property
    def G(self) -> Pin:
        return Pin(self, 0)

class P_MOSFET(CircuitBase):
    ''' P-MOSFET '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ=None):
        self.data: CircuitElementData = {
            "ModelID": "P-MOSFET", "Identifier": Generate, "IsBroken": False,
            "IsLocked": False, "Properties": {"PNP": 1.0, "放大系数": 0.027,
                                                "阈值电压": 1.5, "最大功率": 100.0, "锁定": 1.0},
            "Statistics": {"电压GS": 0.0, "电压": 0.0, "电流": 0.0, "功率": 0.0, "状态": 1.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @property
    def G(self) -> Pin:
        return Pin(self, 0)

    @property
    def S(self) -> Pin:
        return Pin(self, 2)

    @property
    def D(self) -> Pin:
        return Pin(self, 1)

class _source_electricity(TwoPinMixIn):
    """ 波形发生器基类 """
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": Generate, "Identifier": Generate, "IsBroken": False, "IsLocked": False,
            "Properties": {"电压": 3.0, "内阻": 0.5, "频率": 20000.0, "偏移": 0.0,
                            "占空比": 0.5, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": -3.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

class Sinewave_Source(_source_electricity):
    ''' 正弦波发生器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        super().__init__(x, y, z, elementXYZ)
        self.data["ModelID"] = "Sinewave Source"

class Square_Source(_source_electricity):
    ''' 方波发生器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        super().__init__(x, y, z, elementXYZ)
        self.data["ModelID"] = "Square Source"

class Triangle_Source(_source_electricity):
    ''' 三角波发生器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        super().__init__(x, y, z, elementXYZ)
        self.data["ModelID"] = "Triangle Source"

class Sawtooth_Source(_source_electricity):
    ''' 锯齿波发生器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        super().__init__(x, y, z, elementXYZ)
        self.data["ModelID"] = "Sawtooth Source"

class Pulse_Source(_source_electricity):
    ''' 尖峰波发生器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        super().__init__(x, y, z, elementXYZ)
        self.data["ModelID"] = "Pulse Source"
