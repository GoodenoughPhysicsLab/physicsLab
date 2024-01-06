# coding=utf-8
import physicsLab.phy_errors as phy_errors
import physicsLab.circuit.wire as _elementPin
import physicsLab.circuit.elementXYZ as _elementXYZ

from physicsLab.experimentType import experimentType
from physicsLab.typehint import Optional, NoReturn, Self
from physicsLab.experiment import Experiment, stack_Experiment
from physicsLab._tools import numType, roundData, randString, position

# electricity class's metaClass
class CircuitMeta(type):
    # element index
    __index = 1

    def __call__(cls,
                 x: numType = 0,
                 y: numType = 0,
                 z: numType = 0,
                 elementXYZ: Optional[bool] = None,
                 *args, **kwargs
    ) -> Self:
        self = cls.__new__(cls) # type: ignore -> create subclass of electricityBase
        if not (
                isinstance(x, (float, int)) and
                isinstance(y, (float, int)) and
                isinstance(z, (float, int))
        ):
            raise TypeError('illegal argument')
        _Expe: Experiment = stack_Experiment.top()

        if _Expe.ExperimentType != experimentType.Circuit:
            raise phy_errors.ExperimentTypeError

        self.is_elementXYZ = False # 元件坐标系
        if not hasattr(cls, "is_bigElement"):
            cls.is_bigElement = property(lambda self: False) # 2体积元件

        x, y, z = roundData(x, y, z) # type: ignore -> result type: tuple
        self._position = position(x, y, z) # type: ignore -> define _arguments in metaclass
        # 元件坐标系
        if elementXYZ == True or (_elementXYZ.is_elementXYZ() == True and elementXYZ is None):
            x, y, z = _elementXYZ.xyzTranslate(x, y, z)
            self.is_elementXYZ = True

        self.__init__(x, y, z, elementXYZ, *args, **kwargs)
        # 若是big_Element，则修正坐标
        if self.is_elementXYZ and self.is_bigElement:
            x, y, z = _elementXYZ.amend_big_Element(x, y, z)

        self._arguments["Identifier"] = randString(32)
        # x, z, y 物实采用欧拉坐标系
        self._arguments["Position"] = f"{x},{z},{y}"
        _Expe.Elements.append(self._arguments)

        # 该坐标是否已存在，则存入列表
        if self._position in _Expe.elements_Position.keys():
            _Expe.elements_Position[self._position].append(self)
        else:
            _Expe.elements_Position[self._position] = [self]
        self.set_Rotation()
        # 通过元件生成顺序来索引元件
        self._index = CircuitMeta.__index
        _Expe.elements_Index.append(self)
        # 元件index索引加1
        CircuitMeta.__index += 1
        return self


# 所有电学元件的父类
class CircuitBase(metaclass=CircuitMeta):
    # 类无法被实例化
    def __init__(self, *args, **kwargs) -> NoReturn:
        raise phy_errors.instantiateError

    # 设置原件的角度
    def set_Rotation(self, xRotation: numType = 0, yRotation: numType = 0, zRotation: numType = 180) -> Self:
        if not (
                isinstance(xRotation, (int, float)) and
                isinstance(yRotation, (int, float)) and
                isinstance(zRotation, (int, float))
        ):
            raise RuntimeError('illegal argument')

        self._arguments["Rotation"] = f"{roundData(xRotation)},{roundData(zRotation)},{roundData(yRotation)}" # type: ignore -> define _arguments in metaclass
        return self

    # 重新设置元件的坐标
    def set_Position(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> Self:
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
            raise RuntimeError('illegal argument')
        x, y, z = roundData(x, y, z) # type: ignore -> result type: tuple

        #元件坐标系
        if elementXYZ == True or (_elementXYZ.is_elementXYZ() == True and elementXYZ is None):
            x, y, z = _elementXYZ.xyzTranslate(x, y, z)
            self.is_elementXYZ = True
        
        del stack_Experiment.top().elements_Position[self._position]
        self._position = position(x, y, z) # type: ignore -> define _arguments in metaclass
        self._arguments['Position'] = f"{x},{z},{y}" # type: ignore -> define _arguments in metaclass
        stack_Experiment.top().elements_Position[self._position] = self
        return self

    # 格式化坐标参数，主要避免浮点误差
    def format_Position(self) -> tuple:
        if not isinstance(self._position, tuple) or self._position.__len__() != 3:
            raise RuntimeError("Position must be a tuple of length three but gets some other value")
        self._position = position(*roundData(self._position.x, self._position.y, self._position.z)) # type: ignore -> result type: tuple
        return self._position

    # 获取原件的坐标
    def get_Position(self) -> tuple:
        return self._position

    # 获取元件的index（每创建一个元件，index就加1）
    def get_Index(self) -> int:
        return self._index # type: ignore -> define self._index in metaclass

    # 获取子类的类型（也就是ModelID）
    @property
    def modelID(self) -> str:
        return self._arguments['ModelID'] # type: ignore -> define _arguments in metaclass

    # 打印参数
    def print_arguments(self) -> None:
        print(self._arguments) # type: ignore

# 双引脚模拟电路原件的引脚
def two_pin_ArtificialCircuit_Pin(cls):
    @property
    def red(self) -> _elementPin.Pin:
        return _elementPin.Pin(self, 0)

    cls.red, cls.l = red, red

    @property
    def black(self) -> _elementPin.Pin:
        return _elementPin.Pin(self, 1)

    cls.black, cls.r = black, black

    return cls