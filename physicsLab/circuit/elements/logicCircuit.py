# -*- coding: utf-8 -*-
from physicsLab import plAR
from physicsLab import errors
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
    @final
    def set_high_level_value(self, num: num_type) -> Self:
        ''' 设置高电平的值 '''
        if not isinstance(num, (int, float)) or num < self.get_low_level_value():
            raise TypeError

        self.data["Properties"]["高电平"] = num

        return self

    @final
    def get_high_level_value(self) -> num_type:
        ''' 获取高电平的值 '''
        return self.data["Properties"]["高电平"]

    @final
    def set_low_level_value(self, num: num_type) -> Self:
        ''' 设置低电平的值 '''
        if not isinstance(num, (int, float)) or num < self.get_low_level_value():
            raise TypeError

        self.data["Properties"]["低电平"] = num

        return self

    @final
    def get_low_level_value(self):
        ''' 获取低电平的值 '''
        return self.data["Properties"]["低电平"]

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
            output_status: bool = False,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Logic Input", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0, "开关": Generate},
            "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }
        self.set_output_status(output_status)

    def __repr__(self) -> str:
        res = f"Logic_Input({self._position.x}, {self._position.y}, {self._position.z}, " \
              f"elementXYZ={self.is_elementXYZ}, " \
              f"output_status={bool(self.properties['开关'])})"

        return res

    @final
    def set_output_status(self, status: bool) -> Self:
        ''' 将逻辑输入的状态设置为1 '''
        if not isinstance(status, bool):
            raise TypeError

        self.properties["开关"] = int(status)
        return self

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
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Logic Output", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"状态": 0.0, "高电平": 3.0, "低电平": 0.0, "锁定": 1.0}, "Statistics": {},
            "Position": Generate,
            "Rotation": "0,180,0", "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "逻辑输出"

    @property
    def i(self) -> InputPin:
            return InputPin(self, 0)

class _2_Pin_Gate(_LogicBase):
    ''' 2引脚门电路基类 '''
    def __init__(self, x: num_type, y: num_type, z: num_type, /) -> None:
        self.data: CircuitElementData = {
            "ModelID": Generate, "Identifier": Generate,"IsBroken": False, "IsLocked": False,
            "Properties": {"高电平": 3.0, "低电平": 0.0, "最大电流": 0.1, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "No Gate"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "非门"

class _3_Pin_Gate(_LogicBase):
    ''' 3引脚门电路基类 '''
    def __init__(self, x: num_type, y: num_type, z: num_type, /) -> None:
        self.data: CircuitElementData = {
            "ModelID": "", "Identifier": Generate, "IsBroken": False, "IsLocked": False,
            "Properties": {"高电平": 3.0, "低电平": 0.0, "最大电流": 0.1, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Nimp Gate"

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "蕴含非门"

class _BigElement(_LogicBase):
    ''' 2体积元件父类 '''
    is_bigElement = True

    def __init__(self, x: num_type, y: num_type, z: num_type, /) -> None:
        self.data: CircuitElementData = {
            "ModelID": "", "Identifier": Generate, "IsBroken": False,
            "IsLocked": False, "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        plAR_version = plAR.get_plAR_version()
        if plAR_version is not None and plAR_version < (2, 5, 0):
            errors.warning("Physics-Lab-AR's version less than 2.5.0")

        super().__init__(x, y, z)
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
    ) -> None:
        plAR_version = plAR.get_plAR_version()
        if plAR_version is not None and plAR_version < (2, 5, 0):
            errors.warning("Physics-Lab-AR's version less than 2.5.0")

        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        super().__init__(x, y, z)
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
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "8bit Input", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"高电平": 3.0, "低电平": 0.0, "十进制": 0.0, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    def __repr__(self) -> str:
        res = f"eight_bit_Input({self._position.x}, {self._position.y}, {self._position.z}, " \
              f"elementXYZ={self.is_elementXYZ})"

        if self.data["Properties"]["十进制"] != 0:
            res += f".set_num({self.data['Properties']['十进制']})"
        return res

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
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "8bit Display", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"高电平": 3.0, "低电平": 0.0, "状态": 0.0, "锁定": 1.0},
            "Statistics": {"7": 0.0, "6": 0.0, "5": 0.0, "4": 0.0,
                            "3": 0.0, "2": 0.0, "1": 0.0, "0": 0.0, "十进制": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

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
        if low_level is None:
            low_level = min(high_level, 0)
        self.set_properties(high_level=high_level, low_level=low_level, inverted=inverted)

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "施密特触发器"

    def set_properties(
            self,
            *,
            high_level: Optional[num_type] = None,
            low_level: Optional[num_type] = None,
            inverted: Optional[bool] = None,
    ) -> Self:
        ''' 设置施密特触发器的属性
            @param high_level: 高电平电平
            @param low_level: 低电平电平
            @param inverted: 是否翻转
        '''
        if not isinstance(high_level, (int, float, type(None))) \
                or not isinstance(low_level, (int, float, type(None))) \
                or not isinstance(inverted, (bool, type(None))):
            raise TypeError

        if high_level is not None:
            self.properties["高电准位"] = high_level
        if low_level is not None:
            self.properties["低电准位"] = low_level
        if inverted is not None:
            self.properties["工作模式"] = float(inverted)

        if self.properties["高电准位"] < self.properties["低电准位"]:
            raise ValueError("The high level must be greater than the low level")

        return self

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
