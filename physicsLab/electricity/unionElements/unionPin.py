#coding=utf-8
import typing as _typing
import physicsLab.electricity.elementPin as elementPin

# 模块化电路的“引脚”，输入输出都是数据
class unionPin:
    def __init__(
            self,
            *elementPins: elementPin,
    ):
        self.elementPins: _typing.Tuple[elementPin] = elementPins

    # 通过unionPin[num]来索引单个bit
    def __getitem__(self, item):
        pass