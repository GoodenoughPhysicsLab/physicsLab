#coding=utf-8
import typing as _typing
import physicsLab.electricity.elementPin as elementPin
from physicsLab.electricity.unionElements.wires import crt_Wires
import physicsLab.electricity.unionElements._unionClassHead as _unionClassHead

# 模块化电路的“引脚”，输入输出都是数据
class union_Pin:
    __slots__ = ("union_self", "elementPins")
    def __init__(self, union_self: _unionClassHead.unionBase, *elementPins):
        self.union_self = union_self
        self.elementPins: _typing.Tuple[elementPin.element_Pin] = tuple(elementPins)

    # 通过unionPin[num]来索引单个bit
    def __getitem__(self, item):
        return self.elementPins[item]

    def __sub__(self, other: "union_Pin"):
        crt_Wires(self, other)