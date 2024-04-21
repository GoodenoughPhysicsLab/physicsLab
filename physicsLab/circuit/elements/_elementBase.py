# coding=utf-8
import inspect

from physicsLab import errors
from physicsLab import _tools
from physicsLab.circuit import wire
from physicsLab.elementBase import ElementBase
import physicsLab.circuit.elementXYZ as _elementXYZ

from physicsLab.experimentType import experimentType
from physicsLab.typehint import Optional, Self, numType
from physicsLab._tools import roundData, randString
from physicsLab.experiment import Experiment, stack_Experiment

# electricity class's metaClass
class CircuitMeta(type):
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
        self.experiment = _Expe

        if _Expe.ExperimentType != experimentType.Circuit:
            raise errors.ExperimentTypeError

        self.is_elementXYZ = False # 元件坐标系
        if not hasattr(cls, "is_bigElement"):
            cls.is_bigElement = property(lambda self: False) # 2体积元件

        x, y, z = roundData(x, y, z) # type: ignore -> result type: tuple
        self._position = _tools.position(x, y, z) # type: ignore -> define _arguments in metaclass
        # 元件坐标系
        if elementXYZ is True or _elementXYZ.is_elementXYZ() is True and elementXYZ is None:
            x, y, z = _elementXYZ.xyzTranslate(x, y, z)
            self.is_elementXYZ = True

        self.__init__(x, y, z, elementXYZ, *args, **kwargs)
        # 若是big_Element，则修正坐标
        if self.is_elementXYZ and self.is_bigElement:
            x, y, z = _elementXYZ.amend_big_Element(x, y, z)

        self._arguments["Identifier"] = randString(32)
        # x, z, y 物实采用欧拉坐标系
        self._arguments["Position"] = f"{x},{z},{y}"

        # 该坐标是否已存在，则存入列表
        if self._position in _Expe.elements_Position.keys():
            _Expe.elements_Position[self._position].append(self)
        else:
            _Expe.elements_Position[self._position] = [self]
        self.set_Rotation()

        _Expe.Elements.append(self)

        return self

# 所有电学元件的父类
class CircuitBase(ElementBase, metaclass=CircuitMeta):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}" \
               f"({self._position.x}, {self._position.y}, {self._position.z}, {self.is_elementXYZ})"

    # 设置原件的角度
    def set_Rotation(self, xRotation: numType = 0, yRotation: numType = 0, zRotation: numType = 180) -> Self:
        if not (
                isinstance(xRotation, (int, float)) and
                isinstance(yRotation, (int, float)) and
                isinstance(zRotation, (int, float))
        ):
            raise TypeError

        self._arguments["Rotation"] = f"{roundData(xRotation)},{roundData(zRotation)},{roundData(yRotation)}"
        return self

    # 重新设置元件的坐标
    def set_Position(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> Self:
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
            raise TypeError
        x, y, z = roundData(x, y, z) # type: ignore -> result type: tuple

        self._position = _tools.position(x, y, z)

        #元件坐标系
        if elementXYZ is True or _elementXYZ.is_elementXYZ() is True and elementXYZ is None:
            x, y, z = _elementXYZ.xyzTranslate(x, y, z, self.is_bigElement)
            self.is_elementXYZ = True
            # if self.is_bigElement:
            #     x, y, z = _elementXYZ.amend_big_Element(x, y, z)

        for _, self_list in stack_Experiment.top().elements_Position.items():
            if self in self_list:
                self_list.remove(self)

        self._arguments['Position'] = f"{x},{z},{y}" # type: ignore -> define _arguments in metaclass

        _Expe = stack_Experiment.top()
        if self._position in _Expe.elements_Position.keys():
            _Expe.elements_Position[self._position].append(self)
        else:
            _Expe.elements_Position[self._position] = [self]

        return self

    # 获取原件的坐标
    def get_Position(self) -> tuple:
        return self._position

    # 获取元件的index（每创建一个元件，index就加1）
    def get_Index(self) -> int:
        return self.experiment.Elements.index(self) + 1

    # 获取子类的类型（也就是ModelID）
    @property
    def modelID(self) -> str:
        return self._arguments['ModelID'] # type: ignore -> define _arguments in metaclass

    # 打印参数
    def print_arguments(self) -> None:
        print(self._arguments) # type: ignore

    @classmethod
    def _get_property(cls) -> list:
        res: list = []
        for name, _ in inspect.getmembers(cls, lambda i: isinstance(i, property)):
            res.append(name)

        return res

# 双引脚模拟电路原件的基类
class TwoPinMixIn(CircuitBase):
    @property
    def red(self) -> wire.Pin:
        return wire.Pin(self, 0)

    @property
    def black(self) -> wire.Pin:
        return wire.Pin(self, 1)