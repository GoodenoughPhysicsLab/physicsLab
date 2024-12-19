# -*- coding: utf-8 -*-
from physicsLab import _tools
from physicsLab import errors
from physicsLab._element_base import ElementBase
from physicsLab.typehint import numType, Self, override, final
from physicsLab.enums import ExperimentType
from physicsLab.Experiment import get_current_experiment

class _PlanetMeta(type):
    def __call__(cls, x:numType, y: numType, z:numType, *args, **kwargs):
        if not isinstance(x, (int, float)) or \
                not isinstance(y, (int, float)) or \
                not isinstance(z, (int, float)):
            raise TypeError

        _Expe = get_current_experiment()
        if _Expe.experiment_type != ExperimentType.Celestial:
            raise errors.ExperimentTypeError

        self = cls.__new__(cls) # type: ignore -> create subclass
        self.experiment = _Expe

        x, y, z = _tools.roundData(x, y, z) # type: ignore -> return Tuple[numType, numType, numType]

        self.__init__(x, y, z, *args, **kwargs)
        assert hasattr(self, "data") and isinstance(self.data, dict)

        self.data["Identifier"] = _tools.randString(32)
        self.set_position(x, y, z)
        self.set_velocity(0, 0, 0)
        self.set_acceleration(0, 0, 0)

        _Expe.Elements.append(self)

        return self

class PlanetBase(ElementBase, metaclass=_PlanetMeta):
    ''' 星球基类 '''
    def __init__(self) -> None:
        raise NotImplementedError

    def __define_virtual_var_to_let_ide_show(
            self, data: dict,
    ):
        ''' useless
            这些变量的定义在CircuitMeta中
        '''
        self.data: dict = data

    @final
    @override
    def set_position(self, x: numType, y: numType, z: numType) -> Self:
        ''' 设置位置坐标 '''
        if not isinstance(x, (int, float)) or \
                not isinstance(y, (int, float)) or \
                not isinstance(z, (int, float)):
            raise TypeError

        x, y, z = _tools.roundData(x, y, z) # type: ignore -> return Tuple[numType, numType, numType]
        self._position = _tools.position(x, y, z)
        return super().set_position(x, y, z)

    def set_velocity(self, x_v: numType, y_v: numType, z_v: numType) -> Self:
        ''' 设置速度
        '''
        if not isinstance(x_v, (int, float)) or \
                not isinstance(y_v, (int, float)) or \
                not isinstance(z_v, (int, float)):
            raise TypeError
        self.data["Velocity"] = f"{x_v},{z_v},{y_v}"
        return self

    def set_acceleration(self, x_a: numType, y_a: numType, z_a: numType) -> Self:
        ''' 设置加速度
        '''
        if not isinstance(x_a, (int, float)) or \
                not isinstance(y_a, (int, float)) or \
                not isinstance(z_a, (int, float)):
            raise TypeError
        self.acceleration = _tools.position(x_a, y_a, z_a)
        self.data["Acceleration"] = f"{x_a},{z_a},{y_a}"
        return self
