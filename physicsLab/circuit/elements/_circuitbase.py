# -*- coding: utf-8 -*-
import inspect

from physicsLab import errors
from physicsLab import _tools
from physicsLab.circuit import wire
import physicsLab.circuit.elementXYZ as _elementXYZ

from physicsLab.enums import ExperimentType
from physicsLab._tools import roundData, randString
from physicsLab._core import _Experiment, get_current_experiment, _ElementBase
from physicsLab.typehint import Optional, Self, num_type, NoReturn, Generate, override, final

# electricity class's metaClass
class _CircuitMeta(type):
    def __call__(cls,
                 x: num_type,
                 y: num_type,
                 z: num_type,
                 elementXYZ: Optional[bool] = None,
                 *args, **kwargs
                ):
        if not isinstance(x, (float, int)) or \
                not isinstance(y, (float, int)) or \
                not isinstance(z, (float, int)) or \
                not isinstance(elementXYZ, (bool, type(None))):
            raise TypeError

        _Expe: _Experiment = get_current_experiment()
        if _Expe.experiment_type != ExperimentType.Circuit:
            raise errors.ExperimentTypeError # TODO 更详尽的报错信息: 什么类型的实验不能创建什么元件

        self = cls.__new__(cls) # type: ignore -> create subclass
        self.experiment = _Expe

        self.is_elementXYZ = False # 元件坐标系

        x, y, z = roundData(x, y, z) # type: ignore -> result type: tuple

        self.__init__(x, y, z, elementXYZ, *args, **kwargs)
        assert hasattr(self, "data") and isinstance(self.data, dict)

        self.data["Identifier"] = randString(32)
        self.set_position(x, y, z, elementXYZ)
        self.set_rotation()

        _Expe.Elements.append(self)

        return self

class CircuitBase(_ElementBase, metaclass=_CircuitMeta):
    ''' 所有电学元件的父类 '''
    experiment: _Experiment # 元件所属的实验
    is_elementXYZ: bool
    is_bigElement = False # 该元件是否是逻辑电路的两体积元件

    def __init__(*args, **kwargs) -> NoReturn:
        raise NotImplementedError

    def __repr__(self) -> str:
        return  f"{self.__class__.__name__}" \
                f"({self._position.x}, {self._position.y}, {self._position.z}, " \
                f"elementXYZ={self.is_elementXYZ})"

    @final
    def set_rotation(self, x_r: num_type = 0, y_r: num_type = 0, z_r: num_type = 180) -> Self:
        ''' 设置原件的角度 '''
        if not isinstance(x_r, (int, float)) or \
                not isinstance(y_r, (int, float)) or \
                not isinstance(z_r, (int, float)):
            raise TypeError

        x_r, y_r, z_r = roundData(x_r, y_r, z_r) # type: ignore -> result type: tuple
        self.data["Rotation"] = f"{x_r},{z_r},{y_r}"
        return self

    @override
    def set_position(self, x: num_type, y: num_type, z: num_type, elementXYZ: Optional[bool] = None) -> Self:
        ''' 设置原件的位置
        '''
        if not isinstance(x, (int, float)) or \
                not isinstance(y, (int, float)) or \
                not isinstance(z, (int, float)) or \
                not isinstance(elementXYZ, (bool, type(None))):
            raise TypeError

        x, y, z = roundData(x, y, z) # type: ignore -> result type: tuple
        self._position = _tools.position(x, y, z)

        # 元件坐标系
        if elementXYZ is True or _elementXYZ.is_elementXYZ() is True and elementXYZ is None:
            x, y, z = _elementXYZ.xyzTranslate(x, y, z, self.is_bigElement)
            self.is_elementXYZ = True
        else:
            self.is_elementXYZ = False

        return super().set_position(x, y, z)

    @property
    @final
    def modelID(self) -> str:
        ''' 存档的modelID '''
        assert not isinstance(self.data['ModelID'], type(Generate))
        return self.data['ModelID']

    @classmethod
    @final
    def _get_property(cls) -> list:
        res: list = []
        for name, _ in inspect.getmembers(cls, lambda i: isinstance(i, property)):
            res.append(name)

        return res

    @final
    def rename(self, name: str) -> Self:
        ''' 重命名元件
            @param name: 将元件重命名为name
        '''
        if not isinstance(name, str):
            raise TypeError

        assert hasattr(self, "data")
        self.data["Label"] = name
        return self

class TwoPinMixIn(CircuitBase):
    ''' 双引脚模拟电路原件的基类 '''
    @property
    def red(self) -> wire.Pin:
        return wire.Pin(self, 0)

    @property
    def black(self) -> wire.Pin:
        return wire.Pin(self, 1)
