# -*- coding: utf-8 -*-
from physicsLab import plAR
from physicsLab import _warn
from physicsLab import errors
from physicsLab._core import _Experiment
from .._circuit_core import CircuitBase, InputPin, OutputPin
from physicsLab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    Self,
    Generate,
    final,
    LiteralString,
)

class _LogicBase(CircuitBase):
    @property
    @final
    def high_level(self) -> num_type:
        ''' 高电平的值 '''
        result = self.properties["高电平"]
        errors.assert_true(result is not Generate)
        return result

    @high_level.setter
    @final
    def high_level(self, value) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"high_level must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`")
        if self.properties["低电平"] is not Generate and self.low_level > value:
            raise ValueError(f"high_level is smaller than low_level")

        self.properties["高电平"] = value
        return value

    @property
    @final
    def low_level(self) -> num_type:
        ''' 低电平的值  '''
        result = self.properties["低电平"]
        errors.assert_true(result is not Generate)
        return result

    @low_level.setter
    @final
    def low_level(self, value) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"low_level must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`")
        if self.properties["高电平"] is not Generate and value > self.high_level:
            raise ValueError(f"high_level is smaller than low_level")

        self.properties["低电平"] = value
        return value

class Logic_Input(_LogicBase):
    ''' 逻辑输入 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            output_status: bool = False,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Logic Input", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"高电平": Generate, "低电平": Generate, "锁定": 1.0, "开关": Generate},
            "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }
        self.output_status = output_status
        self.high_level = high_level
        self.low_level = low_level

    @property
    @final
    def output_status(self) -> bool:
        ''' 设置开关的状态
        '''
        if "开关" not in self.properties:
            self.properties["开关"] = 0

        result = self.properties["开关"]
        errors.assert_true(result is not Generate)
        return bool(result)

    @output_status.setter
    @final
    def output_status(self, value: bool) -> bool:
        if not isinstance(value, (int, float)):
            errors.type_error(f"output_status must be of type `bool`, but got value `{value}` of type `{type(value).__name__}`")
        self.properties["开关"] = int(value)
        return value

    def __repr__(self) -> str:
        res = f"Logic_Input({self._position.x}, {self._position.y}, {self._position.z}, " \
              f"elementXYZ={self.is_elementXYZ}, " \
              f"output_status={self.output_status})"

        return res

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "逻辑输入"

    @property
    def o(self) -> OutputPin:
        return OutputPin(self, 0)

class Logic_Output(_LogicBase):
    ''' 逻辑输出 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Logic Output", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"状态": 0.0, "高电平": Generate, "低电平": Generate, "锁定": 1.0}, "Statistics": {},
            "Position": Generate,
            "Rotation": "0,180,0", "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }
        self.high_level = high_level
        self.low_level = low_level

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "逻辑输出"

    @property
    def i(self) -> InputPin:
            return InputPin(self, 0)

class _2_Pin_Gate(_LogicBase):
    ''' 2引脚门电路基类 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            high_level: num_type,
            low_level: num_type,
            /,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": Generate, "Identifier": Generate,"IsBroken": False, "IsLocked": False,
            "Properties": {"高电平": Generate, "低电平": Generate, "最大电流": 0.1, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }
        self.high_level = high_level
        self.low_level = low_level

    @property
    def i(self) -> InputPin:
        return InputPin(self, 0)

    @property
    def o(self) -> OutputPin:
        return OutputPin(self, 1)

class Yes_Gate(_2_Pin_Gate):
    ''' 是门 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Yes Gate"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "是门"

class No_Gate(_2_Pin_Gate):
    ''' 非门 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "No Gate"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "非门"

class _3_Pin_Gate(_LogicBase):
    ''' 3引脚门电路基类 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            high_level: num_type,
            low_level: num_type,
            /,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "", "Identifier": Generate, "IsBroken": False, "IsLocked": False,
            "Properties": {"高电平": Generate, "低电平": Generate, "最大电流": 0.1, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }
        self.high_level = high_level
        self.low_level = low_level

    @property
    def i_up(self) -> InputPin:
        return InputPin(self, 0)

    @property
    def i_low(self) -> InputPin:
        return InputPin(self, 1)

    @property
    def o(self) -> OutputPin:
        return OutputPin(self, 2)

class Or_Gate(_3_Pin_Gate):
    ''' 或门 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Or Gate"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "或门"

class And_Gate(_3_Pin_Gate):
    ''' 与门 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "And Gate"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "与门"

class Nor_Gate(_3_Pin_Gate):
    ''' 或非门 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Nor Gate"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "或非门"

class Nand_Gate(_3_Pin_Gate):
    ''' 与非门 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Nand Gate"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "与非门"

class Xor_Gate(_3_Pin_Gate):
    ''' 异或门 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Xor Gate"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "异或门"

class Xnor_Gate(_3_Pin_Gate):
    ''' 同或门 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Xnor Gate"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "同或门"

class Imp_Gate(_3_Pin_Gate):
    ''' 蕴含门 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Imp Gate"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "蕴含门"

class Nimp_Gate(_3_Pin_Gate):
    ''' 蕴含非门 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Nimp Gate"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "蕴含非门"

class _BigElement(_LogicBase):
    ''' 2体积元件父类 '''
    is_bigElement = True

    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            high_level: num_type,
            low_level: num_type,
            /,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "", "Identifier": Generate, "IsBroken": False,
            "IsLocked": False, "Properties": {"高电平": Generate, "低电平": Generate, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }
        self.high_level = high_level
        self.low_level = low_level

class Half_Adder(_BigElement):
    ''' 半加器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Half Adder"

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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "半加器"

class Full_Adder(_BigElement):
    ''' 全加器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Full Adder"

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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "全加器"

class Half_Subtractor(_BigElement):
    ''' 半减器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        plAR_version = plAR.get_plAR_version()
        if plAR_version is not None and plAR_version < (2, 5, 0):
            _warn.warning("Physics-Lab-AR's version less than 2.5.0")

        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Half Subtractor"

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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "半减器"

class Full_Subtractor(_BigElement):
    ''' 全减器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        plAR_version = plAR.get_plAR_version()
        if plAR_version is not None and plAR_version < (2, 5, 0):
            _warn.warning("Physics-Lab-AR's version less than 2.5.0")

        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Full Subtractor"

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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "全减器"

class Multiplier(_BigElement):
    ''' 二位乘法器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Multiplier"

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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "二位乘法器"

class D_Flipflop(_BigElement):
    ''' D触发器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "D Flipflop"

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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "D触发器"

class T_Flipflop(_BigElement):
    ''' T'触发器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "T Flipflop"

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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "T'触发器"

class Real_T_Flipflop(_BigElement):
    ''' T触发器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Real-T Flipflop"

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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "T触发器"

class JK_Flipflop(_BigElement):
    ''' JK触发器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "JK Flipflop"

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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "JK触发器"

class Counter(_BigElement):
    ''' 计数器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Counter"

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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "计数器"

class Random_Generator(_BigElement):
    ''' 随机数发生器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Random Generator"

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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "随机数发生器"

class Eight_Bit_Input(_LogicBase):
    ''' 八位输入器 '''
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
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "8bit Input", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"高电平": Generate, "低电平": Generate, "十进制": 0.0, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }
        self.high_level = high_level
        self.low_level = low_level

    def __repr__(self) -> str:
        res = f"Eight_Bit_Input({self._position.x}, {self._position.y}, {self._position.z}, " \
              f"elementXYZ={self.is_elementXYZ})"

        if self.data["Properties"]["十进制"] != 0:
            res += f".set_num({self.data['Properties']['十进制']})"
        return res

    # TODO 改为@property
    def set_num(self, num : int):
        if 0 <= num <= 255:
            self.data["Properties"]["十进制"] = num
        else:
            raise RuntimeError("The number range entered is incorrect")

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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "八位输入器"

class Eight_Bit_Display(_LogicBase):
    ''' 八位显示器 '''
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
            high_level: num_type = 3,
            low_level: num_type = 0,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "8bit Display", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"高电平": Generate, "低电平": Generate, "状态": 0.0, "锁定": 1.0},
            "Statistics": {"7": 0.0, "6": 0.0, "5": 0.0, "4": 0.0,
                            "3": 0.0, "2": 0.0, "1": 0.0, "0": 0.0, "十进制": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }
        self.high_level = high_level
        self.low_level = low_level

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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "八位显示器"

class Schmitt_Trigger(CircuitBase):
    ''' 施密特触发器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            high_level: num_type = 5.0,
            low_level: Optional[num_type] = None,
            inverted: bool = False,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Schmitt Trigger", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"工作模式": Generate, "切变速率": 0.5, "高电准位": Generate,
                           "锁定": 1.0, "正向阈值": 3.3333332538604736,
                           "低电准位": Generate, "负向阈值": 1.6666666269302368},
            "Statistics": {"输入电压": 0.0, "输出电压": 0.0, "1": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }
        self.high_level = high_level
        self.low_level = low_level
        self.inverted = inverted

    @property
    def high_level(self) -> num_type:
        ''' 高电准位
        '''
        result = self.properties["高电准位"]
        errors.assert_true(result is not Generate)
        return result

    @high_level.setter
    def high_level(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            errors.type_error(f"high_level must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`")

        if self.properties["低电准位"] is not Generate and self.low_level >= value:
            raise ValueError("The high level must be greater than the low level")

        self.properties["高电准位"] = value
        return value

    @property
    def low_level(self) -> num_type:
        ''' 低电准位
        '''
        result = self.properties["低电准位"]
        errors.assert_true(result is not Generate)
        return result

    @low_level.setter
    def low_level(self, value: Optional[num_type]) -> num_type:
        # None means auto derivation
        # TODO maybe we should use physicsLab.auto instead of None
        if not isinstance(value, (int, float, type(None))):
            errors.type_error(f"low_level must be of type `Optional[int | float]`, but got value `{value}` of type `{type(value).__name__}`")

        if value is None:
            self.properties["低电准位"] = min(self.high_level, 0)
        else:
            self.properties["低电准位"] = value

        if self.properties["高电准位"] is not Generate and self.properties["高电准位"] < self.properties["低电准位"]:
            raise ValueError("The high level must be greater than the low level")
        return value

    @property
    def inverted(self) -> bool:
        ''' 是否翻转
        '''
        errors.assert_true(self.properties["工作模式"] is not Generate)
        return bool(self.properties["工作模式"])

    @inverted.setter
    def inverted(self, value: bool) -> bool:
        if not isinstance(value, bool):
            errors.type_error(f"inverted must be of type `bool`, but got value `{value}` of type `{type(value).__name__}`")

        self.properties["工作模式"] = int(value)
        return value

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "施密特触发器"

    def __repr__(self) -> str:
        res = f"Schmitt_Trigger({self._position.x}, {self._position.y}, {self._position.z}, " \
            f"elementXYZ={self.is_elementXYZ}"

        # TODO 显示指明而非使用默认值
        if self.properties["高电准位"] != 5.0:
            res += f", high_level={self.properties['高电准位']}"
        if self.properties["低电准位"] != 0.0:
            res += f", low_level={self.properties['低电准位']}"
        if self.properties["工作模式"] != 0.0:
            res += f", inverted=True"
        return res + ")"

    @property
    def i(self) -> InputPin:
        return InputPin(self, 0)

    @property
    def o(self) -> OutputPin:
        return OutputPin(self, 1)
