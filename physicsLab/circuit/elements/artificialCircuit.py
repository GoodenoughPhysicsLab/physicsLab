# -*- coding: utf-8 -*-
from physicsLab import errors
from physicsLab._core import _Experiment
from physicsLab._tools import round_data
from .._circuit_core import CircuitBase, _TwoPinMixIn, Pin
from physicsLab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    Generate,
    Self,
    override,
    LiteralString,
    final,
    Self,
)

class NE555(CircuitBase):
    ''' 555定时器 '''
    is_bigElement = True

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
            "ModelID": "555 Timer", "Identifier": Generate, "IsBroken": False,
            "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
            "Statistics": {"供电": 10, "放电": 0.0, "阈值": 4,
                            "控制": 6.6666666666666666, "触发": 4,
                            "输出": 0, "重设": 10, "接地": 0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "555定时器"

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

class Basic_Capacitor(_TwoPinMixIn):
    ''' 电容 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            peak_voltage: num_type = 16,
            capacitance: num_type = 1e-06,
            internal_resistance: num_type = 5,
            is_ideal: bool = False,
    ) -> None:
        ''' @param capacitance: 电容, 单位为F
            @param is_ideal: 是否为理想模式
            @param peak_voltage: 峰值电压, 单位为V
            @param internal_resistance: 内阻, 单位为Ω
        '''
        self.data: CircuitElementData = {
            "ModelID": "Basic Capacitor", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"耐压": Generate, "电容": Generate, "内阻": Generate,
                           "理想模式": Generate, "锁定": 1.0},
            "Statistics": {}, "Position": Generate,
            "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }
        self.peak_voltage = peak_voltage
        self.capacitance = capacitance
        self.internal_resistance = internal_resistance
        self.is_ideal = is_ideal

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "电容"

    @property
    @final
    def peak_voltage(self) -> num_type:
        ''' 峰值电压属性, 单位为V
        '''
        result = self.properties["耐压"]
        errors.assert_true(result is not Generate)
        return result

    @peak_voltage.setter
    @final
    def peak_voltage(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"peak_voltage must be of type `int | float`, but got value `{value}` of type {type(value).__name__}")

        self.properties["耐压"] = value
        return value

    @property
    @final
    def capacitance(self) -> num_type:
        ''' 电容属性, 单位为F
        '''
        result = self.properties["电容"]
        errors.assert_true(result is not Generate)
        return result

    @capacitance.setter
    @final
    def capacitance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"capacitance must be of type `int | float`, but got value `{value}` of type {type(value).__name__}")

        self.properties["电容"] = value
        return value

    @property
    @final
    def internal_resistance(self) -> num_type:
        ''' 内阻属性, 单位为Ω
        '''
        result = self.properties["内阻"]
        errors.assert_true(result is not Generate)
        return result

    @internal_resistance.setter
    @final
    def internal_resistance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"internal_resistance must be of type `int | float`, but got value `{value}` of type {type(value).__name__}")

        self.properties["内阻"] = value
        return value

    @property
    @final
    def is_ideal(self) -> bool:
        ''' 元件是否为理想模式
        '''
        if "理想模式" not in self.properties:
            self.properties["理想模式"] = 0
        result = bool(self.properties["理想模式"])
        errors.assert_true(result is not Generate)
        return result

    @is_ideal.setter
    @final
    def is_ideal(self, value: bool) -> bool:
        if not isinstance(value, bool):
            errors.type_error(f"is_ideal must be of type `bool`, but got value `{value}` of type {type(value).__name__}")

        self.properties["理想模式"] = int(value)
        return value

    @override
    def __repr__(self) -> str:
        return f"Basic_Capacitor({self._position.x}, {self._position.y}, {self._position.z}, " \
                f"elementXYZ={self.is_elementXYZ}, " \
                f"peak_voltage={self.peak_voltage}, " \
                f"capacitance={self.capacitance}, " \
                f"internal_resistance={self.internal_resistance}, " \
                f"is_ideal={self.is_ideal})"

class Basic_Inductor(_TwoPinMixIn):
    ''' 电感 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            rated_current: num_type = 1,
            inductance: num_type = 0.05,
            internal_resistance: num_type = 1,
            is_ideal: bool = False,
    ) -> None:
        ''' @param rated_current: 电感额定电流，单位为 A
            @param inductance: 电感，单位为 Henry
            @param internal_resistance: 电感内部阻抗，单位为 Ohm
            @param is_ideal: 是否为理想模式
        '''
        self.data: CircuitElementData = {
            "ModelID": "Basic Inductor", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"额定电流": Generate, "电感": Generate, "内阻": Generate,
                           "锁定": 1.0, "理想模式": Generate},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }
        self.rated_current = rated_current
        self.inductance = inductance
        self.internal_resistance = internal_resistance
        self.is_ideal = is_ideal

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "电感"

    @property
    @final
    def rated_current(self) -> num_type:
        ''' 电感额定电流，单位为 A
        '''
        result = self.properties["额定电流"]
        errors.assert_true(result is not Generate)
        return result

    @rated_current.setter
    @final
    def rated_current(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"rated_current must be of type `int | float`, but got value `{value}` of type {type(value).__name__}")

        self.properties["额定电流"] = value
        return value

    @property
    @final
    def inductance(self) -> num_type:
        ''' 电感，单位为 Henry
        '''
        result = self.properties["电感"]
        errors.assert_true(result is not Generate)
        return result

    @inductance.setter
    @final
    def inductance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"inductance must be of type `int | float`, but got value `{value}` of type {type(value).__name__}")

        self.properties["电感"] = value
        return value

    @property
    @final
    def internal_resistance(self) -> num_type:
        ''' 电感内部阻抗, 单位为Ohm
        '''
        result = self.properties["内阻"]
        errors.assert_true(result is not Generate)
        return result

    @internal_resistance.setter
    @final
    def internal_resistance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"internal_resisitance must be of type `int | float`, but got value `{value}` of type {type(value).__name__}")

        self.properties["内阻"] = value
        return value

    @property
    @final
    def is_ideal(self) -> bool:
        ''' 元件是否为理想模式
        '''
        if "理想模式" not in self.properties:
            self.properties["理想模式"] = 0
        result = self.properties["理想模式"]
        errors.assert_true(result is not Generate)
        return bool(result)

    @is_ideal.setter
    @final
    def is_ideal(self, value: bool) -> bool:
        if not isinstance(value, bool):
            errors.type_error(f"is_ideal must be of type `bool`, but got value `{value}` of type {type(value).__name__}")

        self.properties["理想模式"] = int(value)
        return value

    def fix_inductance(self) -> Self:
        ''' 修正电感值的浮点误差 '''
        self.properties["电感"] = round_data(self.properties["电感"])
        return self

    @override
    def __repr__(self) -> str:
        return f"Basic_Inductor({self._position.x}, {self._position.y}, {self._position.z}, " \
              f"elementXYZ={self.is_elementXYZ}, " \
              f"rated_current={self.rated_current}, " \
              f"inductance={self.inductance}, " \
              f"internal_resistance={self.internal_resistance}, " \
              f"is_ideal={self.is_ideal})"

class Basic_Diode(_TwoPinMixIn):
    ''' 二极管 '''
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
            "ModelID": "Basic Diode", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"击穿电压": 0.0, "前向压降": 0.6, "额定电流": 1.0,
                            "工作电压": 3.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "二极管"

class Light_Emitting_Diode(_TwoPinMixIn):
    ''' 发光二极管 '''
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
            "ModelID": "Light-Emitting Diode", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"反向耐压": 6.0, "击穿电压": 0.0, "前向压降": 2.1024259,
                            "工作电流": 0.01, "工作电压": 3.0, "锁定": 1.0},
            "Statistics": {"电流1": 0.0, "电压1": 0.0, "功率1": 0.0, "亮度1": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "发光二极管"

class Ground_Component(CircuitBase):
    ''' 接地元件 '''
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
            "ModelID": "Ground Component", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False, "Properties": {"锁定": 1.0},
            "Statistics": {"电流": 0}, "Position": Generate,
            "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "接地"

    @property
    def i(self) -> Pin:
        return Pin(self, 0)

class Transformer(CircuitBase):
    ''' 理想变压器 '''
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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "理想变压器"

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
            "ModelID": "Tapped Transformer", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"输入电压": 3.0, "输出电压": 36.0, "额定功率": 20.0,
                            "耦合系数": 1.0, "锁定": 1.0},
            "Statistics": {"电流1": 0.0, "电压1": 0.0, "功率1": 0.0, "电流2": 0.0, "电压2": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "中心抽头变压器"

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
            "ModelID": "Mutual Inductor", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"电感1": 4.0, "电感2": 1.0, "耦合系数": 1.0, "锁定": 1.0},
            "Statistics": {"电流1": 0.0, "电压1": 0.0, "功率1": 0.0, "电流2": 0.0,
                            "电压2": 0.0, "功率2": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "理想互感"

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
            "ModelID": "Rectifier", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"前向压降": 0.8, "额定电流": 1.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0}, "Position": Generate, "Rotation": Generate,
            "DiagramCached": False, "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "全波整流器"

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
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            is_PNP: bool = True,
            gain: num_type = 100,
            max_power: num_type = 1000,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Transistor", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"PNP": Generate, "放大系数": Generate, "最大功率": Generate, "锁定": 1.0},
            "Statistics": {"电压BC": 0.0, "电压BE": 0.0, "电压CE": 0.0, "功率": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }
        self.is_PNP = is_PNP
        self.gain = gain
        self.max_power = max_power

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "三极管"

    @property
    def is_PNP(self) -> bool:
        ''' 是PNP还是NPN, True时为PNP '''
        result = self.properties["PNP"]
        errors.assert_true(result is not Generate)
        return bool(result)

    @is_PNP.setter
    def is_PNP(self, value: bool) -> bool:
        if not isinstance(value, bool):
            errors.type_error(f"is_PNP must be of type `bool`, but got value `{value}` of type `{type(value).__name__}`")

        self.properties["PNP"] = int(value)
        return value

    @property
    def gain(self) -> num_type:
        result = self.properties["放大系数"]
        errors.assert_true(result is not Generate)
        return result

    @gain.setter
    def gain(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"gain must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`")

        self.properties["放大系数"] = value
        return value

    @property
    def max_power(self) -> num_type:
        result = self.properties["最大功率"]
        errors.assert_true(result is not Generate)
        return result

    @max_power.setter
    def max_power(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"max_power must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`")

        self.properties["最大功率"] = value
        return value

    def __repr__(self) -> str:
        res = f"Transistor({self._position.x}, {self._position.y}, {self._position.z}, " \
              f"elementXYZ={self.is_elementXYZ}, is_PNP={bool(self.properties['PNP'])}"

        # TODO 不论是否是默认参数都显示写到res里
        if self.properties["放大系数"] != 100.0:
            res += f", gain={self.properties['放大系数']}"
        if self.properties["最大功率"] != 5.0:
            res += f", max_power={self.properties['最大功率']}"
        return res + ")"

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
            "ModelID": "Comparator", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "比较器"

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
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            gain: num_type = 10_000_000,
            max_voltage: num_type = 1000,
            min_voltage: num_type = -1000,
    ) -> None:
        ''' @param gain: 增益系数
            @param max_voltage: 最大电压
            @param min_voltage: 最小电压
        '''
        self.data: CircuitElementData = {
            "ModelID": "Operational Amplifier", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"增益系数": Generate, "最大电压": Generate, "最小电压": Generate, "锁定": 1.0},
            "Statistics": {"电压-": 0, "电压+": 0, "输出电压": 0,
                            "输出电流": 0, "输出功率": 0},
            "Position": Generate,"Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }
        self.gain = gain
        self.max_voltage = max_voltage
        self.min_voltage = min_voltage

    @property
    def gain(self) -> num_type:
        ''' 增益系数
        '''
        result = self.properties["增益系数"]
        errors.assert_true(result is not Generate)
        return result

    @gain.setter
    def gain(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"gain must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`")

        self.properties["增益系数"] = value
        return value

    @property
    def max_voltage(self) -> num_type:
        result = self.properties["最大电压"]
        errors.assert_true(result is not Generate)
        return result

    @max_voltage.setter
    def max_voltage(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"max_voltage must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`")
        if self.properties["最小电压"] is not Generate and self.min_voltage >= value:
            raise ValueError(f"min_voltage must must less than max_voltage")

        self.properties["最大电压"] = value
        return value

    @property
    def min_voltage(self) -> num_type:
        result = self.properties["最小电压"]
        errors.assert_true(result is not Generate)
        return result

    @min_voltage.setter
    def min_voltage(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"min_voltage must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`")
        if self.properties["最大电压"] is not Generate and self.max_voltage <= value:
            raise ValueError("min_voltage must less than max_voltage")

        self.properties["最小电压"] = value
        return value

    @override
    def __repr__(self) -> str:
        return f"Operational_Amplifier({self._position.x}, {self._position.y}, {self._position.z}, " \
            f"elementXYZ={self.is_elementXYZ}, " \
            f"gain={self.properties['增益系数']}, " \
            f"max_voltage={self.properties['最大电压']}, " \
            f"min_voltage={self.properties['最小电压']})"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "运算放大器"

    @property
    def i_neg(self) -> Pin:
        return Pin(self, 0)

    @property
    def i_pos(self) -> Pin:
        return Pin(self, 1)

    @property
    def o(self) -> Pin:
        return Pin(self, 2)

class Relay_Component(CircuitBase):
    ''' 继电器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            pull_in_current: num_type = 0.02,
            rated_current: num_type = 10,
            coil_inductance: num_type = 0.2,
            coil_resistance: num_type = 20,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Relay Component", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"开关": 0.0, "线圈电感": Generate, "线圈电阻": Generate,
                            "接通电流": Generate, "额定电流": Generate, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }
        self.pull_in_current = pull_in_current
        self.rated_current = rated_current
        self.coil_inductance = coil_inductance
        self.coil_resistance = coil_resistance

    @property
    def pull_in_current(self) -> num_type:
        ''' 接通电流
        '''
        result = self.properties["接通电流"]
        errors.assert_true(result is not Generate)
        return result

    @pull_in_current.setter
    def pull_in_current(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"pull_in_current must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`")

        self.properties["接通电流"] = value
        return value

    @property
    def rated_current(self) -> num_type:
        ''' 额定电流
        '''
        result = self.properties["额定电流"]
        errors.assert_true(result is not Generate)
        return result

    @rated_current.setter
    def rated_current(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"rated_current must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`")

        self.properties["额定电流"] = value
        return value

    @property
    def coil_inductance(self) -> num_type:
        ''' 线圈电感
        '''
        result = self.properties["线圈电感"]
        errors.assert_true(result is not Generate)
        return result

    @coil_inductance.setter
    def coil_inductance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"coil_inductance must be of type `int | flaot`, but got value `{value}` of type `{type(value).__name__}`")

        self.properties["线圈电感"] = value
        return value

    @property
    def coil_resistance(self) -> num_type:
        ''' 线圈电阻
        '''
        result = self.properties["线圈电阻"]
        errors.assert_true(result is not Generate)
        return result

    @coil_resistance.setter
    def coil_resistance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"coil_resistance must be of type `int | flaot`, but got value `{value}` of type `{type(value).__name__}`")

        self.properties["线圈电阻"] = value
        return value

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "继电器"

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
        return Pin(self, 3)

    @property
    def r_low(self) -> Pin:
        return Pin(self, 4)

class N_MOSFET(CircuitBase):
    ''' N-MOSFET '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            beta: num_type = 0.027,
            threshold: num_type = 1.5,
            max_power: num_type = 1000,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "N-MOSFET", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"PNP": 1.0, "放大系数": Generate,
                        "阈值电压": Generate, "最大功率": Generate, "锁定": 1.0},
            "Statistics": {"电压GS": 0.0, "电压": 0.0, "电流": 0.0, "功率": 0.0, "状态": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }
        self. beta = beta
        self.threshold = threshold
        self.max_power = max_power

    @property
    def beta(self) -> num_type:
        ''' 放大系数
        '''
        result = self.properties["放大系数"]
        errors.assert_true(result is not Generate)
        return result

    @beta.setter
    def beta(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"beta must be of type `int | float`, but got value `{value}` of type {type(value).__name__}")

        self.properties["放大系数"] = value
        return value

    @property
    def threshold(self) -> num_type:
        ''' 阈值电压
        '''
        result = self.properties["阈值电压"]
        errors.assert_true(result is not Generate)
        return result

    @threshold.setter
    def threshold(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"threshold must be of type `int | float`, but got value `{value}` of type {type(value).__name__}")

        self.properties["阈值电压"] = value
        return value

    @property
    def max_power(self) -> num_type:
        ''' 最大功率
        '''
        result = self.properties["最大功率"]
        errors.assert_true(result is not Generate)
        return result

    @max_power.setter
    def max_power(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"max_power must be of type `int | float`, but got value `{value}` of type {type(value).__name__}")

        self.properties["最大功率"] = value
        return value

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "N-MOSFET"

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
            "ModelID": "P-MOSFET", "Identifier": Generate, "IsBroken": False,
            "IsLocked": False, "Properties": {"PNP": 1.0, "放大系数": 0.027,
                                                "阈值电压": 1.5, "最大功率": 100.0, "锁定": 1.0},
            "Statistics": {"电压GS": 0.0, "电压": 0.0, "电流": 0.0, "功率": 0.0, "状态": 1.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "P-MOSFET"

    @property
    def G(self) -> Pin:
        return Pin(self, 0)

    @property
    def S(self) -> Pin:
        return Pin(self, 2)

    @property
    def D(self) -> Pin:
        return Pin(self, 1)

class Current_Source(_TwoPinMixIn):
    ''' 电流源 '''
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
            "ModelID": "Current Source", "Identifier": Generate, "IsBroken": False, "IsLocked": False,
            "Properties": {"电流": 0.0099999997764825821, "内阻": 1000000000.0, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation":Generate, "DiagramCached":False,
            "DiagramPosition": {"X": 0,"Y": 0,"Magnitude": 0.0}, "DiagramRotation":0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "电流源"

class _SourceElectricity(_TwoPinMixIn):
    ''' 波形发生器基类 '''
    def __init__(self, x: num_type, y: num_type, z: num_type, /) -> None:
        self.data: CircuitElementData = {
            "ModelID": Generate, "Identifier": Generate, "IsBroken": False, "IsLocked": False,
            "Properties": {"电压": 3.0, "内阻": 0.5, "频率": 20000.0, "偏移": 0.0,
                            "占空比": 0.5, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": -3.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0}

class Sinewave_Source(_SourceElectricity):
    ''' 正弦波发生器 '''
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
        super().__init__(x, y, z)
        self.data["ModelID"] = "Sinewave Source"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "正弦波发生器"

class Square_Source(_SourceElectricity):
    ''' 方波发生器 '''
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
        super().__init__(x, y, z)
        self.data["ModelID"] = "Square Source"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "方波发生器"

class Triangle_Source(_SourceElectricity):
    ''' 三角波发生器 '''
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
        super().__init__(x, y, z)
        self.data["ModelID"] = "Triangle Source"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "三角波发生器"

class Sawtooth_Source(_SourceElectricity):
    ''' 锯齿波发生器 '''
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
        super().__init__(x, y, z)
        self.data["ModelID"] = "Sawtooth Source"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "锯齿波发生器"

class Pulse_Source(_SourceElectricity):
    ''' 尖峰波发生器 '''
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
        super().__init__(x, y, z)
        self.data["ModelID"] = "Pulse Source"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "尖峰波发生器"
