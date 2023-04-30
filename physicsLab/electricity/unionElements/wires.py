#coding=utf-8
from typing import Union, Callable
import physicsLab.errors as errors
import physicsLab.electricity.elementPin as _elementPin
from physicsLab.electricity.wire import crt_Wire, del_Wire
import physicsLab.electricity.unionElements.unionPin as _unionPin

def check_TypeUnionPin(func: Callable):
    def result(
        sourcePin: Union["_unionPin.unionPin", "_elementPin.element_Pin"],
        targetPin: Union["_unionPin.unionPin", "_elementPin.element_Pin"],
        color="蓝"
    ) -> None:
        if isinstance(sourcePin, _elementPin.element_Pin):
            sourcePin = _unionPin.unionPin(sourcePin)
        if isinstance(targetPin, _elementPin.element_Pin):
            targetPin = _unionPin.unionPin(targetPin)

        if not (
            isinstance(sourcePin, _unionPin.unionPin) or
            isinstance(targetPin, _unionPin.unionPin)
        ):
            raise TypeError

        if len(sourcePin.elementPins) != len(targetPin.elementPins):
            errors.warning("The number of input and output pins is not equal")

        func(sourcePin, targetPin, color)
    return result

# 为unionPin连接导线，相当于自动对数据进行连接导线
@check_TypeUnionPin
def crt_Wires(
        sourcePin: Union["_unionPin.unionPin", "_elementPin.element_Pin"],
        targetPin: Union["_unionPin.unionPin", "_elementPin.element_Pin"],
        color="蓝"
) -> None:
    for i, o in zip(sourcePin.elementPins, targetPin.elementPins):
        crt_Wire(i, o, color)

# 删除unionPin的导线
@check_TypeUnionPin
def del_Wires(
        sourcePin: Union["_unionPin.unionPin", "_elementPin.element_Pin"],
        targetPin: Union["_unionPin.unionPin", "_elementPin.element_Pin"],
        color="蓝"
) -> None:
    for i, o in zip(sourcePin.elementPins, targetPin.elementPins):
        del_Wire(i, o, color)