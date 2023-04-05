#coding=utf-8
from physicsLab.electricity.wire import crt_Wire

# 电学元件引脚类
class element_Pin:
    def __init__(self, input_self,  pinLabel : int):
        self.element_self = input_self
        self.pinLabel = pinLabel

    # 重载减法运算符作为连接导线的语法
    def __sub__(self, obj):
        crt_Wire(self, obj)
        return obj

    # 返回一个字符串形式的类型
    def type(self) -> str:
        return 'element Pin'