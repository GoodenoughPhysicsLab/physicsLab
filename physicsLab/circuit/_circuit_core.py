# -*- coding: utf-8 -*-
import inspect

from physicsLab import errors
from physicsLab import _tools

from physicsLab.enums import ExperimentType, WireColor
from physicsLab._tools import round_data
from physicsLab._core import _Experiment, get_current_experiment, ElementBase, elementXYZ_to_native
from physicsLab._typing import Optional, Self, num_type, NoReturn, Generate, override, final, List

class _PinMeta(type):
    ''' 该类仅仅用来实现以下效果:
        通过 isinstance(cls, type(Pin)) 判断cls是否是引脚的class
    '''

# 对于逻辑电路，应该使用`InputPin` 和 `OutputPin`
class Pin(metaclass=_PinMeta):
    ''' 电学元件引脚 '''
    __slots__ = ("element_self", "_pin_label")

    def __init__(self, input_self: "CircuitBase", _pin_label: int) -> None:
        self.element_self: "CircuitBase" = input_self
        self._pin_label: int = _pin_label

    def __eq__(self, other) -> bool:
        if not isinstance(other, Pin):
            return False

        return self.element_self == other.element_self and self._pin_label == other._pin_label

    def __hash__(self) -> int:
        return hash(self.element_self) + hash(self._pin_label)

    def export_str(self) -> str:
        ''' 将引脚转换为 a_element.a_pin 的形式
        '''
        pin_name = self.get_pin_name()
        return f"e{self.element_self.get_index()}.{pin_name}"

    def get_pin_name(self) -> str:
        ''' 获取该引脚在该元件中的名字
            @return: (e.g. i_up)
        '''
        for name, a_pin in self.element_self.get_all_pins_property():
            if a_pin.fget(self.element_self) == self:
                return name
        errors.unreachable()

    def get_wires(self) -> List["Wire"]:
        ''' 获取该引脚上连接的所有导线
        '''
        res = []
        for a_wire in self.element_self.experiment.Wires:
            if a_wire.Source == self or a_wire.Target == self:
                res.append(a_wire)
        return res

class InputPin(Pin):
    ''' 仅用于逻辑电路的输入引脚 '''
    def __init__(self, input_self, pinLabel: int) -> None:
        super().__init__(input_self, pinLabel)

class OutputPin(Pin):
    ''' 仅用于逻辑电路的输出引脚 '''
    def __init__(self, input_self, pinLabel: int) -> None:
        super().__init__(input_self, pinLabel)

class Wire:
    ''' 导线 '''
    __slots__ = ("Source", "Target", "color")

    def __init__(self, source_pin: Pin, target_pin: Pin, color: WireColor = WireColor.blue) -> None:
        if not isinstance(source_pin, Pin):
            errors.type_error(f"Parameter source_pin must be of type `Pin`, but got value {source_pin} of type `{type(source_pin).__name__}`")
        if not isinstance(target_pin, Pin):
            errors.type_error(f"Parameter target_pin must be of type `Pin`, but got value {target_pin} of type `{type(target_pin).__name__}`")
        if not isinstance(color, WireColor):
            errors.type_error(f"Parameter color must be of type `WireColor`, but got value {color} of type `{type(color).__name__}`")

        if source_pin.element_self.experiment is not target_pin.element_self.experiment:
            raise errors.InvalidWireError("can't link wire in two experiment")

        if source_pin == target_pin:
            raise errors.InvalidWireError("can't link wire to itself")

        self.Source: Pin = source_pin
        self.Target: Pin = target_pin
        self.color: WireColor = color

    def __hash__(self) -> int:
        return hash(self.Source) + hash(self.Target)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Wire):
            return False

        # 判断两个导线是否相等与导线的颜色无关
        if self.Source == other.Source and self.Target == other.Target \
                or self.Source == other.Target and self.Target == other.Source:
            return True
        else:
            return False

    def __repr__(self) -> str:
        return f"crt_wire({self.Source.export_str()}, {self.Target.export_str()}, color={self.color})"

    def release(self) -> dict:
        return {
            "Source": self.Source.element_self.data["Identifier"],
            "SourcePin": self.Source._pin_label,
            "Target": self.Target.element_self.data["Identifier"],
            "TargetPin": self.Target._pin_label,
            "ColorName": f"{self.color.value}色导线"
        }

def crt_wire(*pins: Pin, color: WireColor = WireColor.blue) -> List[Wire]:
    ''' 连接导线 '''
    if not all(isinstance(a_pin, Pin) for a_pin in pins):
            errors.type_error(f"Parameter pins must be of type `tuple[Pin]`")
    if not isinstance(color, WireColor):
            errors.type_error(f"Parameter color must be of type `WireColor`, but got value {color} of type `{type(color).__name__}`")
    if len(pins) <= 1:
        raise ValueError("pins must be more than 1")

    _expe = get_current_experiment()
    if _expe.experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError

    res: List[Wire] = []
    for i in range(len(pins) - 1):
        source_pin, target_pin = pins[i], pins[i + 1]
        a_wire = Wire(source_pin, target_pin, color)
        res.append(a_wire)
        _expe.Wires.add(a_wire)

    return res

def del_wire(source_pin: Pin, target_pin: Pin) -> None:
    ''' 删除导线'''
    if not isinstance(source_pin, Pin):
        errors.type_error(f"Parameter source_pin must be of type `Pin`, but got value {source_pin} of type `{type(source_pin).__name__}`")
    if not isinstance(target_pin, Pin):
        errors.type_error(f"Parameter target_pin must be of type `Pin`, but got value {target_pin} of type `{type(target_pin).__name__}`")

    _expe = get_current_experiment()
    if _expe.experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError

    _expe.Wires.remove(Wire(source_pin, target_pin))

# electricity class's metaClass
class _CircuitMeta(type):
    def __call__(
            cls,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            **kwargs,
    ):
        if not isinstance(x, (float, int)):
            errors.type_error(f"Parameter x must be of type `int | float`, but got value {x} of type {type(x).__name__}")
        if not isinstance(y, (float, int)):
            errors.type_error(f"Parameter y must be of type `int | float`, but got value {y} of type {type(y).__name__}")
        if not isinstance(z, (float, int)):
            errors.type_error(f"Parameter z must be of type `int | float`, but got value {z} of type {type(z).__name__}")
        if not isinstance(elementXYZ, (bool, type(None))):
            errors.type_error(f"Parameter elementXYZ must be of type `Optional[bool]`, but got value {elementXYZ} of type {type(elementXYZ).__name__}")
        if not isinstance(identifier, (str, type(None))):
            errors.type_error(f"Parameter identifier must be of type `Optional[str]`, but got value {identifier} of type {type(identifier).__name__}")
        if not isinstance(experiment, (_Experiment, type(None))):
            errors.type_error(f"Parameter experiment must be of type `Optional[Experiment]`, but got value {experiment} of type {type(experiment).__name__}")

        _Expe: _Experiment
        if experiment is None:
            _Expe = get_current_experiment()
        else:
            _Expe = experiment
        if _Expe.experiment_type != ExperimentType.Circuit:
            raise errors.ExperimentTypeError(f"Can't create {cls.__name__} because experiment_type is {_Expe.experiment_type}")

        self: "CircuitBase" = cls.__new__(cls)
        self.experiment = _Expe

        x, y, z = round_data(x), round_data(y), round_data(z)

        self.__init__(x, y, z, **kwargs)
        assert hasattr(self, "data") and isinstance(self.data, dict)

        self._set_identifier(identifier)
        self.set_position(x, y, z, elementXYZ)
        self.set_rotation()

        self.experiment.Elements.append(self)
        self.experiment._id2element[self.data["Identifier"]] = self

        return self

class CircuitBase(ElementBase, metaclass=_CircuitMeta):
    ''' 所有电学元件的父类 '''
    experiment: _Experiment # 元件所属的实验
    is_elementXYZ: bool
    is_bigElement = False # 该元件是否是逻辑电路的两体积元件

    def __init__(*args, **kwargs) -> NoReturn:
        raise NotImplementedError

    def __repr__(self) -> str:
        return  f"{self.__class__.__name__}" \
                f"({self._position.x}, {self._position.y}, {self._position.z}, " \
                f"elementXYZ={self.is_elementXYZ})"

    @property
    @final
    def properties(self) -> dict:
        ''' 返回元件的属性 '''
        return self.data["Properties"]

    @final
    def set_rotation(self, x_r: num_type = 0, y_r: num_type = 0, z_r: num_type = 180) -> Self:
        ''' 设置元件的角度 '''
        if not isinstance(x_r, (int, float)):
            errors.type_error(f"Parameter x_r must be of type `int | float`, but got value {x_r} of type `{type(x_r).__name__}`")
        if not isinstance(y_r, (int, float)):
            errors.type_error(f"Parameter y_r must be of type `int | float`, but got value {y_r} of type `{type(y_r).__name__}`")
        if not isinstance(z_r, (int, float)):
            errors.type_error(f"Parameter z_r must be of type `int | float`, but got value {z_r} of type `{type(z_r).__name__}`")

        x_r, y_r, z_r = round_data(x_r), round_data(y_r), round_data(z_r)
        self.data["Rotation"] = f"{x_r},{z_r},{y_r}"
        return self

    @override
    def set_position(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            elementXYZ: Optional[bool] = None,
    ) -> Self:
        ''' 设置元件的位置
        '''
        if not isinstance(x, (int, float)):
            errors.type_error(f"Parameter x must be of type `int | float`, but got value {x} of type `{type(x).__name__}`")
        if not isinstance(y, (int, float)):
            errors.type_error(f"Parameter y must be of type `int | float`, but got value {y} of type `{type(y).__name__}`")
        if not isinstance(z, (int, float)):
            errors.type_error(f"Parameter z must be of type `int | float`, but got value {z} of type `{type(z).__name__}`")
        if not isinstance(elementXYZ, (bool, type(None))):
            errors.type_error(f"Parameter elementXYZ must be of type `Optional[bool]`, but got value {elementXYZ} of type `{type(elementXYZ).__name__}`")

        x, y, z = round_data(x), round_data(y), round_data(z)
        self._position = _tools.position(x, y, z)

        # 元件坐标系
        if elementXYZ is True or self.experiment.is_elementXYZ is True and elementXYZ is None:
            x, y, z = elementXYZ_to_native(x, y, z, self.is_bigElement)
            self.is_elementXYZ = True
        else:
            self.is_elementXYZ = False

        return super().set_position(x, y, z)

    @property
    @final
    def lock(self) -> bool:
        return bool(self.properties["锁定"])

    @lock.setter
    @final
    def lock(self, status: bool):
        ''' 是否锁定元件 (位置不会受元件间碰撞的影响)
            @param status: 是否锁定元件
        '''
        if not isinstance(status, bool):
            errors.type_error(f"lock must be of type `bool`, but got value {status} of type {type(status).__name__}")

        self.properties["锁定"] = int(status)

    @property
    @final
    def modelID(self) -> str:
        ''' 存档的modelID '''
        assert not isinstance(self.data['ModelID'], type(Generate))
        return self.data['ModelID']

    @final
    @classmethod
    def get_all_pins_property(cls):
        ''' 获取该元件的所有引脚对应的property
        '''
        for name, obj in inspect.getmembers(cls):
            if isinstance(obj, property):
                property_type = obj.fget.__annotations__.get('return')
                if isinstance(property_type, type(Pin)):
                    yield name, obj

    @final
    def rename(self, name: str) -> Self:
        ''' 重命名元件
            @param name: 将元件重命名为name
        '''
        if not isinstance(name, str):
            errors.type_error(f"Parameter name must be of type `str`, but got value {name} of type `{type(name).__name__}`")

        self.data["Label"] = name
        return self

class _TwoPinMixIn(CircuitBase):
    ''' 双引脚模拟电路元件的基类 '''
    @property
    def red(self) -> Pin:
        return Pin(self, 0)

    @property
    def black(self) -> Pin:
        return Pin(self, 1)
