# -*- coding: utf-8 -*-
from physicsLab import errors
from .._circuit_core import _TwoPinMixIn, CircuitBase, Pin
from physicsLab._core import _Experiment
from .logicCircuit import _LogicBase
from physicsLab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    Generate,
    LiteralString,
    final,
    Self,
)

class _MemsBase(CircuitBase):
    ''' 三引脚集成式传感器基类 '''
    def __init__(self, x: num_type, y: num_type, z: num_type, /) -> None:
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

    @property
    @final
    def ranges(self) -> num_type:
        ''' 量程
        '''
        result = self.properties["量程"]
        errors.assert_true(result is not Generate)
        return result

    @ranges.setter
    @final
    def ranges(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"ranges must be of type `int | float`, but got value {value} of type `{type(value).__name__}`")

        self.properties["量程"] = value
        return value

    @property
    @final
    def shifting(self) -> num_type:
        ''' 偏移
        '''
        result = self.properties["偏移"]
        errors.assert_true(result is not Generate)
        return result

    @shifting.setter
    @final
    def shifting(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"shifting must be of type `int | float`, but got value {value} of type `{type(value).__name__}`")

        self.properties["偏移"] = value
        return value

    @property
    @final
    def response_factor(self) -> num_type:
        result = self.properties["响应系数"]
        errors.assert_true(result is not Generate)
        return result

    @response_factor.setter
    @final
    def response_factor(self, value: num_type) -> num_type:
        ''' 响应系数
        '''
        if not isinstance(value, (int, float)):
            errors.type_error(f"response_factor must be of type `int | float`, but got value {value} of type `{type(value).__name__}`")

        self.properties["响应系数"] = value
        return value

class Accelerometer(_MemsBase):
    ''' 加速度计 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            ranges: num_type = 2,
            shifting: num_type = 0.75,
            response_factor: num_type = 0.2290000021457672,
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Accelerometer"
        self.ranges = ranges
        self.shifting = shifting
        self.response_factor = response_factor

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "加速度计"

class Analog_Joystick(CircuitBase):
    ''' 模拟摇杆 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Analog Joystick", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"额定电阻": 10000, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": { "X": 0, "Y": 0, "Magnitude": 0 },
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "模拟摇杆"

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
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            ranges: num_type = 180,
            shifting: num_type = 2.5,
            response_factor: num_type = 0.0125,
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Attitude Sensor"
        self.ranges = ranges
        self.shifting = shifting
        self.response_factor = response_factor

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "姿态传感器"

class Gravity_Sensor(_MemsBase):
    ''' 重力加速计 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            ranges: num_type = 2,
            shifting: num_type = 0.75,
            response_factor: num_type = 0.229,
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Gravity Sensor"
        self.ranges = ranges
        self.shifting = shifting
        self.response_factor = response_factor

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "重力加速计"

class Gyroscope(_MemsBase):
    ''' 陀螺仪传感器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            ranges: num_type = 150,
            shifting: num_type = 2.5,
            response_factor: num_type = 0.0125,
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Gyroscope"
        self.ranges = ranges
        self.shifting = shifting
        self.response_factor = response_factor

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "陀螺仪传感器"

class Linear_Accelerometer(_MemsBase):
    ''' 线性加速度计 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            ranges: num_type = 2,
            shifting: num_type = 0.75,
            response_factor: num_type = 0.229,
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Linear Accelerometer"
        self.ranges = ranges
        self.shifting = shifting
        self.response_factor = response_factor

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "线性加速度计"

class Magnetic_Field_Sensor(_MemsBase):
    ''' 磁场传感器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            ranges: num_type = 0.04,
            shifting: num_type = 3.2,
            response_factor: num_type = 80,
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Magnetic Field Sensor"
        self.ranges = ranges
        self.shifting = shifting
        self.response_factor = response_factor

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "磁场传感器"

class Photodiode(_TwoPinMixIn):
    ''' 光电二极管 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
    ) -> None:
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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "光电二极管"

class Photoresistor(_TwoPinMixIn):
    ''' 光敏电阻 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
    ) -> None:
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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "光敏电阻"

class Proximity_Sensor(_LogicBase):
    ''' 临近传感器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Proximity Sensor", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"高电平": 3, "低电平": 0, "输出阻抗": 10000, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": { "X": 0, "Y": 0, "Magnitude": 0 },
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "临近传感器"

    @property
    def o(self) -> Pin:
        return Pin(self, 0)
