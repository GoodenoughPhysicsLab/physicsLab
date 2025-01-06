# -*- coding: utf-8 -*-
from physicsLab import errors
from physicsLab._core import get_current_experiment
from physicsLab.enums import ExperimentType, WireColor
from physicsLab.typehint import Optional, Callable, Union

# 对于逻辑电路，应该使用`InputPin` 和 `OutputPin`
class Pin:
    ''' 电学元件引脚 '''
    __slots__ = ("element_self", "pinLabel")

    def __init__(self, input_self, pinLabel: int) -> None:
        self.element_self = input_self
        self.pinLabel: int = pinLabel

    # 重载减法运算符作为连接导线的语法
    def __sub__(self, obj: Union["Pin", "UnitPin"]) -> Union["Pin", "UnitPin"]:
        from physicsLab.lib.wires import UnitPin, crt_wires
        if isinstance(obj, Pin):
            crt_wire(self, obj)
        elif isinstance(obj, UnitPin):
            crt_wires(self, obj)
        else:
            raise TypeError
        return obj

    def __eq__(self, other) -> bool:
        if not isinstance(other, Pin):
            return False

        return self.element_self == other.element_self and self.pinLabel == other.pinLabel

    # 将self转换为 CircuitBase.a_pin的形式
    def export_str(self) -> str:
        pin_name = self._get_pin_name_of_class()
        if pin_name is None:
            raise errors.ExperimentError("Pin is not belong to any element")
        return f"e{self.element_self.get_index()}.{pin_name}"

    def _get_pin_name_of_class(self) -> Optional[str]:
        for method in self.element_self._get_property():
            if eval(f"self.element_self.{method}") == self:
                return method
        return None

class InputPin(Pin):
    ''' 仅用于逻辑电路的输入引脚 '''
    def __init__(self, input_self, pinLabel: int) -> None:
        super().__init__(input_self, pinLabel)

class OutputPin(Pin):
    ''' 仅用于逻辑电路的输出引脚 '''
    def __init__(self, input_self, pinLabel: int) -> None:
        super().__init__(input_self, pinLabel)

class _Wire:
    ''' 导线 '''
    __slots__ = ("Source", "Target", "color")

    def __init__(self, source_pin: Pin, target_pin: Pin, color: WireColor = WireColor.blue) -> None:
        if not isinstance(source_pin, Pin) \
                or not isinstance(target_pin, Pin) \
                or not isinstance(color, WireColor):
            raise TypeError

        if source_pin.element_self.experiment is not target_pin.element_self.experiment:
            raise errors.InvalidWireError("can't link wire in two experiment")

        if source_pin == target_pin:
            raise errors.InvalidWireError("can't link wire to itself")

        self.Source: Pin = source_pin
        self.Target: Pin = target_pin
        self.color: WireColor = color

    def __hash__(self) -> int:
        return hash(
            (self.Source.element_self, self.Source.pinLabel, self.Target.element_self, self.Target.pinLabel)
        ) + hash(
            (self.Target.element_self, self.Target.pinLabel, self.Source.element_self, self.Source.pinLabel)
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, _Wire):
            return False

        # 判断两个导线是否相等与导线的颜色无关
        if self.Source == other.Source and self.Target == other.Target \
                or self.Source == other.Target and self.Target == other.Source:
            return True
        else:
            return False

    def __repr__(self) -> str:
        return f"crt_wire({self.Source.export_str()}, {self.Target.export_str()}, '{self.color}')"

    def release(self) -> dict:
        return {
            "Source": self.Source.element_self.data["Identifier"],
            "SourcePin": self.Source.pinLabel,
            "Target": self.Target.element_self.data["Identifier"],
            "TargetPin": self.Target.pinLabel,
            "ColorName": f"{self.color.value}色导线"
        }

def crt_wire(*pins: Pin, color: WireColor = WireColor.blue) -> None:
    ''' 连接导线 '''
    if not all(isinstance(a_pin, Pin) for a_pin in pins) or not isinstance(color, WireColor):
        raise TypeError

    _expe = get_current_experiment()
    if _expe.experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError

    for i in range(len(pins) - 1):
        source_pin, target_pin = pins[i], pins[i + 1]
        _expe.Wires.add(_Wire(source_pin, target_pin, color))

def del_wire(source_pin: Pin, target_pin: Pin) -> None:
    ''' 删除导线'''
    if not isinstance(source_pin, Pin) or not isinstance(target_pin, Pin):
        raise TypeError

    _expe = get_current_experiment()
    if _expe.experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError

    _expe.Wires.remove(_Wire(source_pin, target_pin))
