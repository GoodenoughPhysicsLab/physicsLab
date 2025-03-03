# -*- coding: utf-8 -*-
from physicsLab._tools import round_data
from .._circuit_core import CircuitBase, _TwoPinMixIn, Pin
from physicsLab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    Self,
    Generate,
    override,
    LiteralString,
    final,
)

class _SwitchBase(CircuitBase):
    ''' 开关基类 '''
    def __init__(self, x: num_type, y: num_type, z: num_type, /) -> None:
        self.data: CircuitElementData = {
            "ModelID": Generate, "Identifier": Generate, "IsBroken": False,
            "IsLocked": False, "Properties": {"开关": 0, "锁定": 1.0},
            "Statistics": {}, "Position": Generate,
            "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0}, "DiagramRotation": 0
        }

    def turn_off_switch(self) -> Self:
        ''' 断开开关 '''
        self.data["Properties"]["开关"] = 0
        return self

class Simple_Switch(_SwitchBase, _TwoPinMixIn):
    ''' 简单开关 '''
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
        self.data["ModelID"] = "Simple Switch"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "简单开关"

    def __repr__(self) -> str:
        res = f"Simple_Switch({self._position.x}, {self._position.y}, {self._position.z}, " \
              f"elementXYZ={self.is_elementXYZ})"

        if self.data["Properties"]["开关"] == 1:
            res += ".turn_on_switch()"
        return res

    def turn_on_switch(self) -> Self:
        ''' 闭合开关 '''
        self.data["Properties"]["开关"] = 1
        return self

class SPDT_Switch(_SwitchBase):
    ''' 单刀双掷开关 '''
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
        self.data["ModelID"] = "SPDT Switch"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "单刀双掷开关"

    def __repr__(self) -> str:
        res = f"SPDT_Switch({self._position.x}, {self._position.y}, {self._position.z}, " \
              f"elementXYZ={self.is_elementXYZ})"

        if self.data["Properties"]["开关"] == 1:
            res += ".left_turn_on_switch()"
        elif self.data["Properties"]["开关"] == 2:
            res += ".right_turn_on_switch()"
        return res

    def left_turn_on_switch(self) -> Self:
        ''' 向左闭合开关 '''
        self.data["Properties"]["开关"] = 1
        return self

    def right_turn_on_switch(self) -> Self:
        ''' 向右闭合开关 '''
        self.data["Properties"]["开关"] = 2
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

class DPDT_Switch(_SwitchBase):
    ''' 双刀双掷开关 '''
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
        self.data["ModelID"] = "DPDT Switch"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "双刀双掷开关"

    def __repr__(self) -> str:
        res = f"DPDT_Switch({self._position.x}, {self._position.y}, {self._position.z}, " \
              f"elementXYZ={self.is_elementXYZ})"

        if self.data["Properties"]["开关"] == 1:
            res += ".left_turn_on_switch()"
        elif self.data["Properties"]["开关"] == 2:
            res += ".right_turn_on_switch()"
        return res

    def left_turn_on_switch(self) -> Self:
        ''' 向左闭合开关 '''
        self.data["Properties"]["开关"] = 1
        return self

    def right_turn_on_switch(self) -> Self:
        ''' 向右闭合开关 '''
        self.data["Properties"]["开关"] = 2
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

class Push_Switch(_TwoPinMixIn):
    ''' 按钮开关 '''
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
            "ModelID": "Push Switch", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"开关": 0.0, "默认开关": 0.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "按钮开关"

class Air_Switch(_TwoPinMixIn):
    ''' 空气开关 '''
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
            "ModelID": "Air Switch", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"开关": 0.0, "额定电流": 10.0, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "空气开关"

    @override
    def __repr__(self) -> str:
        res = f"Air_Switch({self._position.x}, {self._position.y}, {self._position.z}, " \
              f"elementXYZ={self.is_elementXYZ})"

        if self.data["Properties"]["开关"] == 1:
            res += ".turn_on_switch()"
        return res

    def turn_off_switch(self) -> Self:
        ''' 断开开关 '''
        self.data["Properties"]["开关"] = 0
        return self

    def turn_on_switch(self) -> Self:
        ''' 闭合开关 '''
        self.data["Properties"]["开关"] = 1
        return self

class Incandescent_Lamp(_TwoPinMixIn):
    ''' 白炽灯泡 '''
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
            "ModelID": "Incandescent Lamp", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"额定电压": 3.0, "额定功率": 0.85, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0,
                            "功率": 0.0, "电压": 0.0, "电流": 0.0,
                            "灯泡温度": 300.0, "电阻": 0.5},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "白炽灯泡"

class Battery_Source(_TwoPinMixIn):
    ''' 一节电池 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            voltage: num_type = 1.5,
            internal_resistance: num_type = 0,
    ) -> None:
        if not isinstance(voltage, (int, float)) \
                or not isinstance(internal_resistance, (int, float)):
            raise TypeError

        self.data: CircuitElementData = {
            "ModelID": "Battery Source", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"最大功率": 16.2, "电压": Generate, "内阻": Generate, "锁定": 1.0},
            "Statistics": {"电流": 0, "功率": 0, "电压": 0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

        self.set_properties(voltage=voltage, internal_resistance=internal_resistance)

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "一节电池"

    def set_properties(
            self,
            *,
            voltage: Optional[num_type] = None,
            internal_resistance: Optional[num_type] = None,
    ) -> Self:
        ''' 设置 一节电池 的属性
            @param voltage: 电压
            @param internal_resistance: 内阻
        '''
        if not isinstance(voltage, (int, float, type(None))) \
                or not isinstance(internal_resistance, (int, float, type(None))):
            raise TypeError

        if voltage is not None:
            self.properties["电压"] = voltage
        if internal_resistance is not None:
            self.properties["内阻"] = internal_resistance

        return self

class Student_Source(CircuitBase):
    ''' 学生电源 '''
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
            "ModelID": "Student Source", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"交流电压": 3.0, "直流电压": 3.0, "开关": 0.0, "频率": 50.0, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电压": 0.0, "瞬间电流": 0.0,
                            "瞬间电阻": 0.0, "功率": 0.0, "电阻": 0.0, "电流": 0.0,
                            "瞬间功率1": 0.0, "瞬间电压1": 0.0, "瞬间电流1": 0.0,
                            "瞬间电阻1": 0.0, "功率1": 0.0, "电阻1": 0.0, "电流1": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "学生电源"

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

class Resistor(_TwoPinMixIn):
    ''' 电阻 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None, identifier: Optional[str] = None,
            resistance: num_type = 10,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Resistor", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"最大电阻": 10_000_000.0, "最小电阻": 0.1, "电阻": Generate, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0, "瞬间电流": 0, "瞬间电压": 0, "功率": 0,
                            "电压": 0, "电流": 0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }
        self.set_resistance(resistance)

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "电阻"

    def set_resistance(self, resistance: num_type) -> Self:
        ''' 设置电阻值 '''
        if not isinstance(resistance, (int, float)):
            raise TypeError

        self.properties["电阻"] = resistance
        return self

    def fix_resistance(self) -> Self:
        ''' 修正电阻值的浮点误差 '''
        self.properties["电阻"] = round_data(self.properties["电阻"])
        return self

    def __repr__(self) -> str:
        return f"Resistor({self._position.x}, {self._position.y}, {self._position.z}, " \
              f"elementXYZ={self.is_elementXYZ}, " \
              f"resistance={self.properties['电阻']})"

class Fuse_Component(_TwoPinMixIn):
    ''' 保险丝 '''
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
            "ModelID": "Fuse Component", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"开关": 1.0, "额定电流": 0.3, "熔断电流": 0.5, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0,
                            "功率": 0.0, "电压": 0.0, "电流": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "保险丝"

class Slide_Rheostat(CircuitBase):
    ''' 滑动变阻器 '''
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
            "ModelID": "Slide Rheostat", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"额定电阻": 10.0, "滑块位置": 0.0,
                            "电阻1": 10, "电阻2": 10.0, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0,
                            "功率": 0.0, "电压": 0.0, "电流": 0.0,
                            "瞬间功率1": 0.0, "瞬间电流1": 0.0, "瞬间电压1": 0.0,
                            "功率1": 0.0, "电压1": 0.0, "电流1": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "滑动变阻器"

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

class Multimeter(_TwoPinMixIn):
    ''' 多用电表 '''
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
            "ModelID": "Multimeter", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"状态": 0.0, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0,
                            "功率": 0.0, "电压": 0.0, "电流": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "多用电表"

class Galvanometer(CircuitBase):
    ''' 灵敏电流计 '''
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
            "ModelID": "Galvanometer", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"量程": 3.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "灵敏电流计"

    @property
    def l(self) -> Pin:
        return Pin(self, 0)

    @property
    def mid(self) -> Pin:
        return Pin(self, 1)

    @property
    def r(self) -> Pin:
        return Pin(self, 2)

class Microammeter(CircuitBase):
    ''' 微安表 '''
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
            "ModelID": "Microammeter", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"量程": 0.1, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "微安表"

    @property
    def l(self) -> Pin:
        return Pin(self, 0)

    @property
    def mid(self) -> Pin:
        return Pin(self, 1)

    @property
    def r(self) -> Pin:
        return Pin(self, 2)

class Electricity_Meter(CircuitBase):
    ''' 电能表 '''
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
            "ModelID": "Electricity Meter", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"示数": 0.0, "额定电流": 6.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "电能表"

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

class Resistance_Box(CircuitBase):
    ''' 电阻箱 '''
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
            "ModelID": "Resistance Box", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"最大电阻": 10000.0, "最小电阻": 0.1,
                            "电阻": 10.0, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0,
                            "功率": 0.0, "电压": 0.0, "电流": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "电阻箱"

    @property
    def l(self) -> Pin:
        return Pin(self, 0)

    @property
    def r(self) -> Pin:
        return Pin(self, 1)

    def set_resistance(self, num: num_type) -> Self:
        ''' 设置电阻值
        '''
        if not isinstance(num, (int, float)):
            raise TypeError

        self.data["Properties"]["电阻"] = num
        return self

class Simple_Ammeter(CircuitBase):
    ''' 直流安培表 '''
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
            "ModelID": "Simple Ammeter", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"量程": 0.007, "内阻": 0.007,
                            "名义量程": 3.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "直流安培表"

    @property
    def l(self) -> Pin:
        return Pin(self, 0)

    @property
    def mid(self) -> Pin:
        return Pin(self, 1)

    @property
    def r(self) -> Pin:
        return Pin(self, 2)

class Simple_Voltmeter(CircuitBase):
    ''' 直流电压表 '''
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
            "ModelID": "Simple Voltmeter", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"量程": 0.001, "名义量程": 15.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "直流电压表"

    @property
    def l(self) -> Pin:
        return Pin(self, 0)

    @property
    def mid(self) -> Pin:
        return Pin(self, 1)

    @property
    def r(self) -> Pin:
        return Pin(self, 2)
