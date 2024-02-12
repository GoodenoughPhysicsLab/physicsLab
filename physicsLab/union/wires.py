# -*- coding: utf-8 -*-
from typing import Union, Callable, Tuple
from physicsLab import errors
from ._unionClassHead import UnionBase
from physicsLab.circuit.wire import crt_Wire, del_Wire, Pin

# 模块化电路的“引脚”，输入输出都是数据
class union_Pin:
    __slots__ = ("union_self", "elementPins")
    def __init__(self, union_self: UnionBase, *elementPins):
        self.union_self = union_self
        self.elementPins: Tuple[Pin] = tuple(elementPins)

    # 通过unionPin[num]来索引单个bit
    def __getitem__(self, item):
        return self.elementPins[item]

    def __sub__(self, other: Union[Pin, "union_Pin"]):
        crt_Wires(self, other)
        return other

def check_TypeUnionPin(func: Callable):
    def result(
        sourcePin: Union[union_Pin, Pin],
        targetPin: Union[union_Pin, Pin],
        *args, **kwargs
    ) -> None:
        if isinstance(sourcePin, Pin):
            sourcePin = union_Pin(sourcePin.element_self, sourcePin)
        if isinstance(targetPin, Pin):
            targetPin = union_Pin(targetPin.element_self, targetPin)

        if not (
                isinstance(sourcePin, union_Pin)
                and isinstance(targetPin, union_Pin)
        ):
            raise TypeError

        if len(sourcePin.elementPins) != len(targetPin.elementPins):
            errors.warning(
                f"The number of {sourcePin.union_self.__class__.__name__}'s output pin "
                f"are not equal to {targetPin.union_self.__class__.__name__}'s input pin."
            )

        func(sourcePin, targetPin, *args, **kwargs)
    return result

# 为unionPin连接导线，相当于自动对数据进行连接导线
@check_TypeUnionPin
def crt_Wires(
        sourcePin: Union[union_Pin, Pin],
        targetPin: Union[union_Pin, Pin],
        color="蓝"
) -> None:
    for i, o in zip(sourcePin.elementPins, targetPin.elementPins):
        crt_Wire(i, o, color)

# 删除unionPin的导线
@check_TypeUnionPin
def del_Wires(
        sourcePin: Union[union_Pin, Pin],
        targetPin: Union[union_Pin, Pin],
) -> None:
    for i, o in zip(sourcePin.elementPins, targetPin.elementPins):
        del_Wire(i, o)