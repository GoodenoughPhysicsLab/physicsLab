# -*- coding: utf-8 -*-
from physicsLab import errors
from physicsLab.experiment import get_Experiment
from physicsLab.experimentType import experimentType
from physicsLab.typehint import WireDict, Optional

# 电学元件引脚类, 模电元件引脚无明确的输入输出之分, 因此用这个
class Pin:
    __slots__ = ("element_self", "pinLabel")
    is_input = False
    is_output = False
    def __init__(self, input_self, pinLabel: int) -> None:
        self.element_self = input_self # CircuitBase
        self.pinLabel: int = pinLabel

    # 重载减法运算符作为连接导线的语法
    def __sub__(self, obj: "Pin") -> "Pin":
        crt_Wire(self, obj)
        return obj

    def __eq__(self, other: "Pin") -> bool:
        if not isinstance(other, Pin):
            return False

        return self.element_self == other.element_self and self.pinLabel == other.pinLabel

    # 将self转换为 CircuitBase.a_pin的形式
    def export_str(self) -> str:
        pin_name = self._get_pin_name_of_class()
        if pin_name is None:
            raise RuntimeError("Pin is not belong to any element")
        return f"{self.element_self._arguments['Identifier']}.{pin_name}"

    def _get_pin_name_of_class(self) -> Optional[str]:
        for method in self.element_self._get_property():
            if eval(f"self.element_self.{method}") == self:
                return method
        return None

# 只用于输入的引脚
class InputPin(Pin):
    is_input = True
    def __init__(self, input_self, pinLabel: int) -> None:
        super().__init__(input_self, pinLabel)

# 只用于输出的引脚
class OutputPin(Pin):
    is_output = True
    def __init__(self, input_self, pinLabel: int) -> None:
        super().__init__(input_self, pinLabel)

# 导线类
class Wire:
    __slots__ = ("Source", "Target", "color")
    def __init__(self, Source: Pin, Target: Pin, color: str = '蓝') -> None:
        if not isinstance(Source, Pin) or not isinstance(Target, Pin):
            raise TypeError
        if color not in ('蓝', '绿', '黄', '红', '紫'):
            raise errors.WireColorError

        self.Source: Pin = Source
        self.Target: Pin = Target
        self.color: str = color

    def __eq__(self, other: "Wire") -> bool:
        if not isinstance(other, Wire):
            return False

        if ((self.Source == other.Source and self.Target == other.Target)
           or (self.Source == other.Target and self.Target == other.Source)):
            return True
        else:
            return False

    def __repr__(self) -> str:
        if self.color == "蓝":
            return f"{self.Source.export_str()} - {self.Target.export_str()}"
        else:
            return f"crt_Wire({self.Source.export_str()}, {self.Target.export_str()}, '{self.color}')"

    def release(self) -> WireDict:
        return {
            "Source": self.Source.element_self._arguments["Identifier"],
            "SourcePin": self.Source.pinLabel,
            "Target": self.Target.element_self._arguments["Identifier"],
            "TargetPin": self.Target.pinLabel,
            "ColorName": f"{self.color}色导线"
        }

# 检查函数参数是否是导线
def _check_typeWire(func: callable):
    def result(SourcePin: Pin, TargetPin: Pin, *args, **kwargs) -> None:
        if not (
                isinstance(SourcePin, Pin) and
                isinstance(TargetPin, Pin)
        ):
            raise TypeError

        if get_Experiment().ExperimentType != experimentType.Circuit:
            raise errors.ExperimentTypeError

        func(SourcePin, TargetPin, *args, **kwargs)

    return result

# 连接导线
@_check_typeWire
def crt_Wire(SourcePin: Pin, TargetPin: Pin, color: str = "blue") -> None:
    if color in ("black", "blue", "red", "green", "yellow"):
        color = {"black": "黑", "blue": "蓝", "red": "红", "green": "绿", "yellow": "黄"}[color]

    if color not in ("黑", "蓝", "红", "绿", "黄"):
        raise errors.WireColorError

    get_Experiment().Wires.append(Wire(SourcePin, TargetPin, color))

# 删除导线
@_check_typeWire
def del_Wire(SourcePin: Pin, TargetPin: Pin) -> None:
    i: int = 0
    while i < len(get_Experiment().Wires):
        if Wire(SourcePin, TargetPin) == get_Experiment().Wires[i]:
            get_Experiment().Wires.pop(i)
        else:
            i += 1

# 删除所有导线
def clear_Wires() -> None:
    if get_Experiment().ExperimentType != experimentType.Circuit:
        raise errors.ExperimentTypeError
    get_Experiment().Wires.clear()

# 获取当前导线数
def count_Wires() -> int:
    if get_Experiment().ExperimentType != experimentType.Circuit:
        raise errors.ExperimentTypeError
    return len(get_Experiment().Wires)