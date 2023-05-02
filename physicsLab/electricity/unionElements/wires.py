#coding=utf-8
from typing import Union, Callable
import physicsLab.errors as errors
import physicsLab.electricity.elementPin as _elementPin
from physicsLab.electricity.wire import crt_Wire, del_Wire
import physicsLab.electricity.unionElements.union_Pin as _unionPin

def check_TypeUnionPin(func: Callable):
    def result(
        sourcePin: Union["_unionPin.union_Pin", "_elementPin.element_Pin"],
        targetPin: Union["_unionPin.union_Pin", "_elementPin.element_Pin"],
        color="蓝"
    ) -> None:
        if isinstance(sourcePin, _elementPin.element_Pin):
            sourcePin = _unionPin.union_Pin(sourcePin)
        if isinstance(targetPin, _elementPin.element_Pin):
            targetPin = _unionPin.union_Pin(targetPin)

        if not (
                isinstance(sourcePin, _unionPin.union_Pin) or
                isinstance(targetPin, _unionPin.union_Pin)
        ):
            raise TypeError

        if len(sourcePin.elementPins) != len(targetPin.elementPins):
            errors.warning(
                f"The number of {sourcePin.union_self.__class__.__name__}'s output pin "
                f"are not equal to {targetPin.union_self.__class__.__name__}'s input pin."
            )

        func(sourcePin, targetPin, color)
    return result

# 为unionPin连接导线，相当于自动对数据进行连接导线
@check_TypeUnionPin
def crt_Wires(
        sourcePin: Union["_unionPin.union_Pin", "_elementPin.element_Pin"],
        targetPin: Union["_unionPin.union_Pin", "_elementPin.element_Pin"],
        color="蓝"
) -> None:
    for i, o in zip(sourcePin.elementPins, targetPin.elementPins):
        crt_Wire(i, o, color)

# 删除unionPin的导线
@check_TypeUnionPin
def del_Wires(
        sourcePin: Union["_unionPin.union_Pin", "_elementPin.element_Pin"],
        targetPin: Union["_unionPin.union_Pin", "_elementPin.element_Pin"],
        color="蓝"
) -> None:
    for i, o in zip(sourcePin.elementPins, targetPin.elementPins):
        del_Wire(i, o, color)