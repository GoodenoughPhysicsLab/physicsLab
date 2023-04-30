#coding=utf-8
import typing as _typing
import physicsLab.electricity.elementPin as elementPin
from physicsLab.electricity.unionElements.wires import crt_Wires

# 模块化电路的“引脚”，输入输出都是数据
class unionPin:
    __slots__ = ("elementPins")
    def __init__(
            self,
            *elementPins,
    ):
        self.elementPins: _typing.Tuple[elementPin.element_Pin] = tuple(elementPins)

    # 通过unionPin[num]来索引单个bit
    def __getitem__(self, item):
        pass

    def __sub__(self, other: "unionPin"):
        crt_Wires(self, other)