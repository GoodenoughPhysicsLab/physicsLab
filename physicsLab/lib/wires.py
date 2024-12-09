# -*- coding: utf-8 -*-
from typing import Union, Callable, Tuple

from physicsLab import errors
from physicsLab.circuit.wire import crt_wire, del_wire, Pin

class UnitPin:
    ''' 模块化电路的"引脚", 输入输出都是数据 '''
    __slots__ = ("lib_self", "elementPins")
    def __init__(self, lib_self, *elementPins):
        self.lib_self = lib_self
        self.elementPins: Tuple[Pin] = tuple(elementPins)

    # 通过unionPin[num]来索引单个bit
    def __getitem__(self, item: Union[int, slice]) -> Pin:
        if isinstance(item, int):
            return self.elementPins[item]
        elif isinstance(item, slice):
            return UnitPin(self.lib_self, *self.elementPins[item])
        else:
            raise TypeError

    def __sub__(self, other: Union[Pin, "UnitPin"]):
        crt_wires(self, other)
        return other

    def __iter__(self):
        return iter(self.elementPins)

    def __next__(self):
        for i in self.elementPins:
            yield i

def check_TypeUnionPin(func: Callable):
    def result(
        sourcePin: Union[UnitPin, Pin],
        targetPin: Union[UnitPin, Pin],
        *args, **kwargs
    ) -> None:
        if isinstance(sourcePin, Pin):
            sourcePin = UnitPin(sourcePin.element_self, sourcePin)
        if isinstance(targetPin, Pin):
            targetPin = UnitPin(targetPin.element_self, targetPin)

        if not isinstance(sourcePin, UnitPin) or not isinstance(targetPin, UnitPin):
            raise TypeError

        if len(sourcePin.elementPins) != len(targetPin.elementPins):
            errors.warning(
                f"The number of {sourcePin.lib_self.__class__.__name__}'s output pin "
                f"is {len(sourcePin.elementPins)}, "
                f"but the number of {targetPin.lib_self.__class__.__name__}'s input pin "
                f"is {len(targetPin.elementPins)}."
            )

        func(sourcePin, targetPin, *args, **kwargs)
    return result

@check_TypeUnionPin
def crt_wires(sourcePin: Union[UnitPin, Pin],
              targetPin: Union[UnitPin, Pin],
              color="蓝"
              ) -> None:
    ''' 为unionPin连接导线, 相当于自动对数据进行连接导线 '''
    for i, o in zip(sourcePin.elementPins, targetPin.elementPins):
        crt_wire(i, o, color)

@check_TypeUnionPin
def del_wires(sourcePin: Union[UnitPin, Pin],
              targetPin: Union[UnitPin, Pin],
              ) -> None:
    ''' 删除unionPin的导线 '''
    for i, o in zip(sourcePin.elementPins, targetPin.elementPins):
        del_wire(i, o)
