#coding=utf-8
import physicsLab._tools as _tools
import physicsLab.electricity.elementXYZ as _elementXYZ
# Union class的基类
class unionObject:
    # 设置坐标
    def set_Position(self, x, y, z):
        pass

# union class __init__装饰器
def union_Init_HEAD(func):
    def result(
            self,
            x: _tools.numType,
            y: _tools.numType,
            z: _tools.numType,
            elementXYZ: bool = None, # x, y, z是否为元件坐标系
            unionHeading: bool = False, # False: 生成的元件为竖直方向，否则为横方向
            fold: bool = False # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
    ):
        # 元件坐标系
        if elementXYZ == True or (_elementXYZ.is_elementXYZ() == True and elementXYZ is None):
            x, y, z = _elementXYZ.xyzTranslate(x, y, z)

        func(self, x, y, z, elementXYZ, unionHeading, fold)
    return result