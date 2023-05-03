#coding=utf-8
import physicsLab._tools as _tools
import physicsLab.errors as _errors
import physicsLab._fileGlobals as _fileGlobals
import physicsLab.electricity.elementXYZ as _elementXYZ
import physicsLab.electricity.elementsClass as _elementsClass
# Union class的基类
class unionBase:
    # 获取以模块化电路生成顺序为item的原件的self
    def __getitem__(self, item: int) -> "_elementsClass.elementBase":
        if not isinstance(item, int):
            raise TypeError
        return self._elements[item]
    # 设置坐标
    def set_Position(self, x, y, z):
        pass

# union class __init__装饰器
def union_Init_HEAD(
        x: _tools.numType,
        y: _tools.numType,
        z: _tools.numType,
        bitLength: int,
        elementXYZ: bool,  # x, y, z是否为元件坐标系
        unionHeading: bool,  # False: 生成的元件为竖直方向，否则为横方向
        fold: bool,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
        foldMaxNum: int  # 达到foldMaxNum个元件数时即在z轴自动折叠
):
    _fileGlobals.check_ExperimentType(0)
        # input type check
    if foldMaxNum <= 0 or not(
        isinstance(x, (int, float)) or
        isinstance(y, (int, float)) or
        isinstance(z, (int, float)) or
        isinstance(elementXYZ, bool) or
        isinstance(unionHeading, bool) or
        isinstance(fold, bool) or
        isinstance(foldMaxNum, int)
    ):
        raise TypeError
    if not isinstance(bitLength, int) or bitLength < 1:
        raise _errors.bitLengthError("bitLength must get a integer")

    # 元件坐标系，如果输入坐标不是元件坐标系就强转为元件坐标系
    if not (elementXYZ == True or (_elementXYZ.is_elementXYZ() == True and elementXYZ is None)):
        x, y, z = _elementXYZ.translateXYZ(x, y, z)

    return _tools.roundData(x, y, z)
