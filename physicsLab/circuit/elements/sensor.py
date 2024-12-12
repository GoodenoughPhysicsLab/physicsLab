# -*- coding: utf-8 -*-
from ..wire import Pin
from ._circuitbase import TwoPinMixIn, CircuitBase
from .logicCircuit import _LogicBase
from physicsLab.typehint import Optional, numType, CircuitElementData, Generate

class _MemsBase(CircuitBase):
    ''' 三引脚集成式传感器基类 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None):
        self.data: CircuitElementData = {
            "ModelID": Generate, "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"量程": Generate, "输出阻抗": 10000, "偏移": Generate,
                            "响应系数": Generate,"锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": { "X": 0, "Y": 0, "Magnitude": 0 },
            "DiagramRotation": 0
        }

    @property
    def x(self) -> Pin:
        return Pin(self, 0)

    @property
    def y(self) -> Pin:
        return Pin(self, 1)

    @property
    def z(self) -> Pin:
        return Pin(self, 2)

class Accelerometer(_MemsBase):
    ''' 加速度计 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None):
        super().__init__(x, y, z, elementXYZ)
        self.data["ModelID"] = "Accelerometer"
        self.data["Properties"]["量程"] = 2
        self.data["Properties"]["偏移"] = 0.75
        self.data["Properties"]["响应系数"] = 0.2290000021457672

class Analog_Joystick(CircuitBase):
    ''' 模拟摇杆 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None):
        self.data: CircuitElementData = {
            "ModelID": "Analog Joystick", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"额定电阻": 10000, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": { "X": 0, "Y": 0, "Magnitude": 0 },
            "DiagramRotation": 0
        }

    @property
    def x1(self) -> Pin:
        return Pin(self, 0)

    @property
    def x2(self) -> Pin:
        return Pin(self, 1)

    @property
    def x3(self) -> Pin:
        return Pin(self, 2)

    @property
    def y1(self) -> Pin:
        return Pin(self, 3)

    @property
    def y2(self) -> Pin:
        return Pin(self, 4)

    @property
    def y3(self) -> Pin:
        return Pin(self, 5)

class Attitude_Sensor(_MemsBase):
    ''' 姿态传感器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None):
        super().__init__(x, y, z, elementXYZ)
        self.data["ModelID"] = "Attitude Sensor"
        self.data["Properties"]["量程"] = 180
        self.data["Properties"]["偏移"] = 2.5
        self.data["Properties"]["响应系数"] = 0.012500000186264515

class Gravity_Sensor(_MemsBase):
    ''' 重力加速计 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None):
        super().__init__(x, y, z, elementXYZ)
        self.data["ModelID"] = "Gravity Sensor"
        self.data["Properties"]["量程"] = 2
        self.data["Properties"]["偏移"] = 0.75
        self.data["Properties"]["响应系数"] = 0.2290000021457672

class Gyroscope(_MemsBase):
    ''' 陀螺仪传感器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None):
        super().__init__(x, y, z, elementXYZ)
        self.data["ModelID"] = "Gyroscope"
        self.data["Properties"]["量程"] = 150
        self.data["Properties"]["偏移"] = 2.5
        self.data["Properties"]["响应系数"] = 0.012500000186264515

class Linear_Accelerometer(_MemsBase):
    ''' 线性加速度计 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None):
        super().__init__(x, y, z, elementXYZ)
        self.data["ModelID"] = "Linear Accelerometer"
        self.data["Properties"]["量程"] = 2
        self.data["Properties"]["偏移"] = 0.75
        self.data["Properties"]["响应系数"] = 0.2290000021457672

class Magnetic_Field_Sensor(_MemsBase):
    ''' 磁场传感器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None):
        super().__init__(x, y, z, elementXYZ)
        self.data["ModelID"] = "Magnetic Field Sensor"
        self.data["Properties"]["量程"] = 0.03999999910593033
        self.data["Properties"]["偏移"] = 3.200000047683716
        self.data["Properties"]["响应系数"] = 80

class Photodiode(TwoPinMixIn):
    ''' 光电二极管 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None):
        self.data: CircuitElementData = {
            "ModelID": "Photodiode", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"前向压降": 0.6, "击穿电压": 0, "额定电流": 1,
                            "响应系数": 0.1, "响应时间": 0.03, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": { "X": 0, "Y": 0, "Magnitude": 0 },
            "DiagramRotation": 0
        }

class Photoresistor(TwoPinMixIn):
    ''' 光敏电阻 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None):
        self.data: CircuitElementData = {
            "ModelID": "Photoresistor", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"亮电阻": 10000, "暗电阻": 1000000, "响应时间": 0.03,
                            "最大电压": 150, "响应系数": 0.6, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": { "X": 0, "Y": 0, "Magnitude": 0 },
            "DiagramRotation": 0
        }

class Proximity_Sensor(_LogicBase):
    ''' 临近传感器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None):
        self.data: CircuitElementData = {
            "ModelID": "Proximity Sensor", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"高电平": 3, "低电平": 0, "输出阻抗": 10000, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": { "X": 0, "Y": 0, "Magnitude": 0 },
            "DiagramRotation": 0
        }

    @property
    def o(self) -> Pin:
        return Pin(self, 0)
