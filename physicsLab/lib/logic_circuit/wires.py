# -*- coding: utf-8 -*-
from typing import Union, Callable, Tuple

from physicsLab import errors
from physicsLab.enums import WireColor
from physicsLab.circuit._circuit_core import crt_wire, del_wire, Pin
from physicsLab._typing import overload

class UnitPin:
    ''' 模块化电路的"引脚", 是对多个Pin进行组合的封装
    '''
    __slots__ = ("lib_self", "pins")
    def __init__(self, lib_self, *pins):
        self.lib_self = lib_self
        self.pins: Tuple[Pin] = tuple(pins)

    @overload
    def __getitem__(self, item: int) -> Pin:
        ...

    @overload
    def __getitem__(self, item: slice) -> "UnitPin":
        ...

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.pins[item]
        elif isinstance(item, slice):
            return UnitPin(self.lib_self, *self.pins[item])
        else:
            raise TypeError

    def __iter__(self):
        return iter(self.pins)

    def __next__(self):
        for i in self.pins:
            yield i

def _check_union_pin_type(func: Callable):
    def result(
            source_pin: Union[UnitPin, Pin],
            target_pin: Union[UnitPin, Pin],
            *args, **kwargs
    ) -> None:
        if isinstance(source_pin, Pin):
            source_pin = UnitPin(source_pin.element_self, source_pin)
        if isinstance(target_pin, Pin):
            target_pin = UnitPin(target_pin.element_self, target_pin)

        if not isinstance(source_pin, UnitPin) or not isinstance(target_pin, UnitPin):
            raise TypeError

        if len(source_pin.pins) != len(target_pin.pins):
            # TODO 警告信息里把具体的是哪个变量给显示出来
            errors.warning(
                f"The number of {source_pin.lib_self.__class__.__name__}'s output pin "
                f"is {len(source_pin.pins)}, "
                f"but the number of {target_pin.lib_self.__class__.__name__}'s input pin "
                f"is {len(target_pin.pins)}."
            )

        func(source_pin, target_pin, *args, **kwargs)
    return result

# TODO 支持传入多个 Pin / UnitPin
@_check_union_pin_type
def crt_wires(
        source_pin: Union[UnitPin, Pin],
        target_pin: Union[UnitPin, Pin],
        color: WireColor = WireColor.blue,
) -> None:
    ''' 为unionPin连接导线, 相当于自动对数据进行连接导线 '''
    assert isinstance(source_pin, UnitPin) and isinstance(target_pin, UnitPin)
    for i, o in zip(source_pin.pins, target_pin.pins):
        crt_wire(i, o, color=color)

@_check_union_pin_type
def del_wires(
        source_pin: Union[UnitPin, Pin],
        target_pin: Union[UnitPin, Pin],
) -> None:
    ''' 删除unionPin的导线 '''
    assert isinstance(source_pin, UnitPin) and isinstance(target_pin, UnitPin)
    for i, o in zip(source_pin.pins, target_pin.pins):
        del_wire(i, o)
