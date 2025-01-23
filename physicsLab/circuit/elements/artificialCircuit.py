# -*- coding: utf-8 -*-
from physicsLab._tools import round_data
from .._circuit_core import CircuitBase, _TwoPinMixIn, Pin
from physicsLab._typing import Optional, num_type, CircuitElementData, Generate, Self, override

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
        self.set_properties(
            peak_voltage=peak_voltage,
            capacitance=capacitance,
            internal_resistance=internal_resistance,
            is_ideal=is_ideal,
        )

    def set_properties(
            self,
            *,
            peak_voltage: Optional[num_type] = None,
            capacitance: Optional[num_type] = None,
            internal_resistance: Optional[num_type] = None,
            is_ideal: Optional[bool] = None,
    ) -> Self:
        ''' 修改电容属性
            @param capacitance: 电容, 单位为F
            @param is_ideal: 是否为理想模式
            @param peak_voltage: 峰值电压, 单位为V
            @param internal_resistance: 内阻, 单位为Ω
        '''
        if not isinstance(peak_voltage, (int, float, type(None))) \
                or not isinstance(capacitance, (int, float, type(None))) \
                or not isinstance(internal_resistance, (int, float, type(None))) \
                or not isinstance(is_ideal, (bool, type(None))):
            raise TypeError

        if peak_voltage is not None:
            self.properties["耐压"] = peak_voltage
        if capacitance is not None:
            self.properties["电容"] = capacitance
        if internal_resistance is not None:
            self.properties["内阻"] = internal_resistance
        if is_ideal is not None:
            self.properties["理想模式"] = int(is_ideal)

        return self

    @override
    def __repr__(self) -> str:
        return f"Basic_Capacitor({self._position.x}, {self._position.y}, {self._position.z}, " \
                f"elementXYZ={self.is_elementXYZ}, " \
                f"peak_voltage={self.properties['耐压']}, " \
                f"capacitance={self.properties['电容']}, " \
                f"internal_resistance={self.properties['内阻']}, " \
                f"is_ideal={bool(self.properties['理想模式'])})"

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
        self.set_properties(
            rated_current=rated_current,
            inductance=inductance,
            internal_resistance=internal_resistance,
            is_ideal=is_ideal,
        )

    def set_properties(
            self,
            *,
            rated_current: Optional[num_type] = None,
            inductance: Optional[num_type] = None,
            internal_resistance: Optional[num_type] = None,
            is_ideal: Optional[bool] = None,
    ) -> Self:
        ''' 修改电感属性
            @param rated_current: 电感额定电流，单位为 A
            @param inductance: 电感，单位为 Henry
            @param internal_resistance: 电感内部阻抗，单位为 Ohm
            @param is_ideal: 是否为理想模式
        '''
        if not isinstance(rated_current, (int, float, type(None))) \
                or not isinstance(inductance, (int, float, type(None))) \
                or not isinstance(internal_resistance, (int, float, type(None))) \
                or not isinstance(is_ideal, (bool, type(None))):
            raise TypeError

        if not rated_current is None:
            self.properties["额定电流"] = rated_current
        if not inductance is None:
            self.properties["电感"] = inductance
        if not internal_resistance is None:
            self.properties["内阻"] = internal_resistance
        if not is_ideal is None:
            self.properties["理想模式"] = int(is_ideal)

        return self

    def fix_inductance(self) -> Self:
        ''' 修正电感值的浮点误差 '''
        self.properties["电感"] = round_data(self.properties["电感"])
        return self

    @override
    def __repr__(self) -> str:
        return f"Basic_Inductor({self._position.x}, {self._position.y}, {self._position.z}, " \
              f"elementXYZ={self.is_elementXYZ}, " \
              f"rated_current={self.properties['额定电流']}" \
              f"inductance={self.properties['电感']}, " \
              f"internal_resistance={self.properties['内阻']}" \
              f"is_ideal={bool(self.properties['理想模式'])}"

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
    ) -> None:
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
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
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
    ) -> None:
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
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            is_PNP: bool = True,
            gain: num_type = 100,
            max_power: num_type = 1000,
    ) -> None:
        if not isinstance(is_PNP, bool) \
                or not isinstance(gain, (int, float)) \
                or not isinstance(max_power, (int, float)):
            raise TypeError

        self.data: CircuitElementData = {
            "ModelID": "Transistor", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"PNP": Generate, "放大系数": Generate, "最大功率": Generate, "锁定": 1.0},
            "Statistics": {"电压BC": 0.0, "电压BE": 0.0, "电压CE": 0.0, "功率": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }
        self.set_properties(is_PNP=is_PNP, gain=gain, max_power=max_power)

    def set_properties(
            self,
            *,
            is_PNP: Optional[bool] = None,
            gain: Optional[num_type] = None,
            max_power: Optional[num_type] = None,
    ) -> Self:
        ''' 修改三极管属性
            @param is_PNP: 是PNP还是NPN, True时为PNP
            @param gain: 放大系数
            @param max_power: 最大功率
        '''
        if not isinstance(is_PNP, (bool, type(None))) \
                or not isinstance(gain, (int, float, type(None))) \
                or not isinstance(max_power, (int, float, type(None))):
            raise TypeError

        if is_PNP is not None:
            self.properties["PNP"] = float(is_PNP)
        if gain is not None:
            self.properties["放大系数"] = gain
        if max_power is not None:
            self.properties["最大功率"] = max_power

        return self

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
    ) -> None:
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
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
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
        self.set_properties(gain=gain, max_voltage=max_voltage, min_voltage=min_voltage)

    def set_properties(
            self,
            *,
            gain: Optional[num_type] = None,
            max_voltage: Optional[num_type] = None,
            min_voltage: Optional[num_type] = None,
    ) -> Self:
        ''' 修改运放属性
            @param gain: 增益系数
            @param max_voltage: 最大电压
            @param min_voltage: 最小电压
        '''
        if not isinstance(gain, (int, float, type(None))) \
                or not isinstance(max_voltage, (int, float, type(None))) \
                or not isinstance(min_voltage, (int, float, type(None))):
            raise TypeError

        if gain is None:
            gain = self.properties["增益系数"]
        if max_voltage is None:
            max_voltage = self.properties["最大电压"]
        if min_voltage is None:
            min_voltage = self.properties["最小电压"]

        assert gain is not None and max_voltage is not None and min_voltage is not None
        if max_voltage <= min_voltage:
            raise ValueError("Maximun voltage must be greater than minimum voltage")

        self.properties["增益系数"] = gain
        self.properties["最大电压"] = max_voltage
        self.properties["最小电压"] = min_voltage
        return self

    @override
    def __repr__(self) -> str:
        return f"Operational_Amplifier({self._position.x}, {self._position.y}, {self._position.z}, " \
            f"elementXYZ={self.is_elementXYZ}, " \
            f"gain={self.properties['增益系数']}, " \
            f"max_voltage={self.properties['最大电压']}, " \
            f"min_voltage={self.properties['最小电压']})"

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
            pull_in_current: num_type = 0.02,
            rated_current: num_type = 10,
            coil_inductance: num_type = 0.2,
            coil_resistance: num_type = 20,
    ) -> None:
        if not isinstance(pull_in_current, (int, float)) \
                or not isinstance(rated_current, (int, float)) \
                or not isinstance(coil_inductance, (int, float)) \
                or not isinstance(coil_resistance, (int, float)):
            raise TypeError

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
        self.set_properties(
            pull_in_current=pull_in_current,
            rated_current=rated_current,
            coil_inductance=coil_inductance,
            coil_resistance=coil_resistance,
        )

    def set_properties(
             self,
             *,
             pull_in_current: Optional[num_type] = None,
             rated_current: Optional[num_type] = None,
             coil_inductance: Optional[num_type] = None,
             coil_resistance: Optional[num_type] = None,
     ) -> Self:
         ''' 修改运放属性
             @param pull_in_current: 接通电流
             @param rated_current: 额定电流
             @param coil_inductance: 线圈电感
             @param coil_resistance: 线圈电阻
         '''
         if not isinstance(pull_in_current, (int, float, type(None))) \
                 or not isinstance(rated_current, (int, float, type(None))) \
                 or not isinstance(coil_inductance, (int, float, type(None))) \
                 or not isinstance(coil_resistance, (int, float, type(None))):
             raise TypeError

         if pull_in_current is not None:
             self.properties["接通电流"] = pull_in_current
         if rated_current is not None:
             self.properties["额定电流"] = rated_current
         if coil_inductance is not None:
             self.properties["线圈电感"] = coil_inductance
         if coil_resistance is not None:
             self.properties["线圈电阻"] = coil_resistance
         return self

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
            beta: num_type = 0.027,
            threshold: num_type = 1.5,
            max_power: num_type = 1000,
    ) -> None:
        if not isinstance(beta, (int, float)) \
                or not isinstance(threshold, (int, float)) \
                or not isinstance(max_power, (int, float)):
            raise TypeError

        self.data: CircuitElementData = {
            "ModelID": "N-MOSFET", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"PNP": 1.0, "放大系数": Generate,
                        "阈值电压": Generate, "最大功率": Generate, "锁定": 1.0},
            "Statistics": {"电压GS": 0.0, "电压": 0.0, "电流": 0.0, "功率": 0.0, "状态": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }
        self.set_properties(beta=beta, threshold=threshold, max_power=max_power)

    def set_properties(
            self,
            *,
            beta: Optional[num_type] = None,
            threshold: Optional[num_type] = None,
            max_power: Optional[num_type] = None,
    ) -> Self:
        ''' 设置 N-MOSFET 属性
            @param beta: 放大系数
            @param threshold: 阈值电压
            @param max_power: 最大功率
        '''
        if not isinstance(threshold, (int, float, type(None))) \
                or not isinstance(max_power, (int, float, type(None))) \
                or not isinstance(beta, (int, float, type(None))):
            raise TypeError

        if beta is not None:
            self.properties["放大系数"] = beta
        if threshold is not None:
            self.properties["阈值电压"] = threshold
        if max_power is not None:
            self.properties["最大功率"] = max_power
        return self

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
    ) -> None:
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
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Current Source", "Identifier": Generate, "IsBroken": False, "IsLocked": False,
            "Properties": {"电流": 0.0099999997764825821, "内阻": 1000000000.0, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation":Generate, "DiagramCached":False,
            "DiagramPosition": {"X": 0,"Y": 0,"Magnitude": 0.0}, "DiagramRotation":0
        }

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
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Sinewave Source"

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
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Square Source"

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
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Triangle Source"

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
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Sawtooth Source"

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
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Pulse Source"
