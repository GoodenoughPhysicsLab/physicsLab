# -*- coding: utf-8 -*-
import physicsLab.phy_errors as phy_errors

from physicsLab.experiment import stack_Experiment
from physicsLab.experimentType import experimentType

# 电学元件引脚类, 模电元件引脚无明确的输入输出之分, 因此用这个
class Pin:
    __slots__ = ("element_self", "pinLabel")
    is_input = False
    is_output = False
    def __init__(self, input_self, pinLabel: int) -> None:
        self.element_self = input_self
        self.pinLabel: int = pinLabel

    # 重载减法运算符作为连接导线的语法
    def __sub__(self, obj: "Pin") -> "Pin":
        crt_Wire(self, obj)
        return obj

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

# 检查函数参数是否是导线
def _check_typeWire(func):
    def result(SourcePin: Pin, TargetPin: Pin, color: str = '蓝') -> None:
        if (
                isinstance(SourcePin, Pin) and
                isinstance(TargetPin, Pin)
        ):
            # 将英文的color转换为中文
            if color in ("black", "blue", "red", "green", "yellow"):
                color = {"black": "黑", "blue": "蓝", "red": "红", "green": "绿", "yellow": "黄"}[color]

            if (color not in ("黑", "蓝", "红", "绿", "黄")):
                raise phy_errors.WireColorError

            if stack_Experiment.top().ExperimentType != experimentType.Circuit:
                raise phy_errors.ExperimentTypeError

            func(SourcePin, TargetPin, color)

    return result

# 新版连接导线
@_check_typeWire
def crt_Wire(SourcePin: Pin, TargetPin: Pin, color: str = '蓝') -> None:
    stack_Experiment.top().Wires.append({"Source": SourcePin.element_self._arguments["Identifier"], "SourcePin": SourcePin.pinLabel,
                   "Target": TargetPin.element_self._arguments["Identifier"], "TargetPin": TargetPin.pinLabel,
                   "ColorName": f"{color}色导线"})

# 删除导线
@_check_typeWire
def del_Wire(SourcePin: Pin, TargetPin: Pin, color: str = '蓝') -> None:
    a_wire = {
        "Source": SourcePin.element_self._arguments["Identifier"], "SourcePin": SourcePin.pinLabel,
        "Target": TargetPin.element_self._arguments["Identifier"], "TargetPin": TargetPin.pinLabel,
        "ColorName": f"{color}色导线"
    }
    _Expe = stack_Experiment.top()

    if a_wire in _Expe.Wires:
        _Expe.Wires.remove(a_wire)
    else:
        a_wire = {
            "Source": TargetPin.element_self._arguments["Identifier"], "SourcePin": TargetPin.pinLabel,
            "Target": SourcePin.element_self._arguments["Identifier"], "TargetPin": SourcePin.pinLabel,
            "ColorName": f"{color}色导线"
        }
        if a_wire in _Expe.Wires:
            _Expe.Wires.remove(a_wire)
        else:
            raise phy_errors.WireNotFoundError

# 删除所有导线
def clear_Wires() -> None:
    if stack_Experiment.top().ExperimentType != experimentType.Circuit:
        raise phy_errors.ExperimentTypeError
    stack_Experiment.top().Wires.clear()

# 获取当前导线数
def count_Wires() -> int:
    if stack_Experiment.top().ExperimentType != experimentType.Circuit:
        raise phy_errors.ExperimentTypeError
    return len(stack_Experiment.top().Wires)