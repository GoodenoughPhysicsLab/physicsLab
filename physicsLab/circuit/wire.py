# -*- coding: utf-8 -*-
from physicsLab import errors
from physicsLab.Experiment import Experiment, get_current_experiment
from physicsLab.enums import ExperimentType
from physicsLab.typehint import Optional, Callable, Union

# 电学元件引脚类, 模电元件引脚无明确的输入输出之分, 因此用这个
class Pin:
    __slots__ = ("element_self", "pinLabel")
    is_input = False
    is_output = False
    def __init__(self, input_self, pinLabel: int) -> None:
        self.element_self = input_self # CircuitBase
        self.pinLabel: int = pinLabel

    # 重载减法运算符作为连接导线的语法
    def __sub__(self, obj: Union["Pin", "UnitPin"]) -> Union["Pin", "UnitPin"]: # type: ignore UnitPin
        from physicsLab.lib.wires import UnitPin, crt_wires
        if isinstance(obj, Pin):
            crt_wire(self, obj)
        elif isinstance(obj, UnitPin):
            crt_wires(self, obj)
        else:
            raise TypeError
        return obj

    def __eq__(self, other: "Pin") -> bool:
        if not isinstance(other, Pin):
            return False

        return self.element_self == other.element_self and self.pinLabel == other.pinLabel

    # 将self转换为 CircuitBase.a_pin的形式
    def export_str(self) -> str:
        pin_name = self._get_pin_name_of_class()
        if pin_name is None:
            raise errors.ExperimentError("Pin is not belong to any element")
        return f"e{self.element_self.get_Index()}.{pin_name}"

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

        if Source.element_self.experiment is not Target.element_self.experiment:
            raise errors.ExperimentError("can't link wire in two experiment")

        if Source == Target:
            raise errors.ExperimentError()

        if color in ("black", "blue", "red", "green", "yellow"):
            color = {"black": "黑", "blue": "蓝", "red": "红", "green": "绿", "yellow": "黄"}[color]
        if color not in ('蓝', '绿', '黄', '红', '黑'):
            raise errors.WireColorError

        self.Source: Pin = Source
        self.Target: Pin = Target
        self.color: str = color

    def __hash__(self) -> int:
        return hash(
            (self.Source.element_self, self.Source.pinLabel, self.Target.element_self, self.Target.pinLabel)
        ) + hash(
            (self.Target.element_self, self.Target.pinLabel, self.Source.element_self, self.Source.pinLabel)
        )

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

    def release(self) -> dict:
        return {
            "Source": self.Source.element_self.data["Identifier"],
            "SourcePin": self.Source.pinLabel,
            "Target": self.Target.element_self.data["Identifier"],
            "TargetPin": self.Target.pinLabel,
            "ColorName": f"{self.color}色导线"
        }

# 检查函数参数是否是导线
def _check(func: Callable):
    def result(SourcePin: Pin, TargetPin: Pin, *args, **kwargs) -> None:
        if not (
                isinstance(SourcePin, Pin) and
                isinstance(TargetPin, Pin)
        ):
            raise TypeError

        if get_current_experiment().experiment_type != ExperimentType.Circuit:
            raise errors.ExperimentTypeError

        func(SourcePin, TargetPin, *args, **kwargs)

    return result

# 连接导线
@_check
def crt_wire(SourcePin: Pin, TargetPin: Pin, color: str = "blue") -> None:
    get_current_experiment().Wires.add(Wire(SourcePin, TargetPin, color))

# 删除导线
@_check
def del_wire(SourcePin: Pin, TargetPin: Pin) -> None:
    temp = Wire(SourcePin, TargetPin)
    if temp in get_current_experiment().Wires:
        get_current_experiment().Wires.remove(temp)
    else:
        get_current_experiment().Wires.remove(Wire(TargetPin, SourcePin))

# 删除所有导线
def clear_wires() -> None:
    if get_current_experiment().experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError
    get_current_experiment().Wires.clear()

# 获取当前导线数
def count_wires() -> int:
    if get_current_experiment().experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError
    return len(get_current_experiment().Wires)

def _read_wires(experiment: Experiment, _wires: list) -> None:
    assert experiment.experiment_type == ExperimentType.Circuit

    for wire_dict in _wires:
        experiment.Wires.add(
            Wire(
                Pin(experiment.get_element_from_identifier(wire_dict["Source"]), wire_dict["SourcePin"]),
                Pin(experiment.get_element_from_identifier(wire_dict["Target"]), wire_dict["TargetPin"]),
                wire_dict["ColorName"][0] # e.g. "蓝"
            )
        )
