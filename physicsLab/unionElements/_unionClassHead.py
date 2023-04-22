#coding=utf-8
import physicsLab.electricity.elementXYZ as _elementXYZ
# Union class的基类
class unionObject:
    # 设置坐标
    def set_Position(self, x, y, z):
        pass

# union class __init__装饰器
def union_Init_HEAD(func):
    def result(*args, **kwargs):
        func(*args, **kwargs)
    return result