# -*- coding: utf-8 -*-
from physicsLab import _tools
from physicsLab import errors
from physicsLab.typehint import num_type, Self, override, final
from physicsLab.enums import ExperimentType
from physicsLab._experiment import get_current_experiment, _Experiment, _ElementBase

class _PlanetMeta(type):
    def __call__(cls, x:num_type, y: num_type, z:num_type, *args, **kwargs):
        if not isinstance(x, (int, float)) or \
                not isinstance(y, (int, float)) or \
                not isinstance(z, (int, float)):
            raise TypeError

        _Expe = get_current_experiment()
        if _Expe.experiment_type != ExperimentType.Celestial:
            raise errors.ExperimentTypeError

        self: "PlanetBase" = cls.__new__(cls) # type: ignore -> create subclass
        self.experiment = _Expe

        x, y, z = _tools.roundData(x, y, z) # type: ignore -> return Tuple[numType, numType, numType]

        self.__init__(x, y, z, *args, **kwargs)
        assert isinstance(self.data, dict)

        self.data["Identifier"] = _tools.randString(32)
        self.set_position(x, y, z)
        self.set_velocity(0, 0, 0)
        self.set_acceleration(0, 0, 0)

        _Expe.Elements.append(self)

        return self

class PlanetBase(_ElementBase, metaclass=_PlanetMeta):
    ''' 星球基类 '''
    experiment: _Experiment

    def __init__(self) -> None:
        raise NotImplementedError

    @final
    @override
    def set_position(self, x: num_type, y: num_type, z: num_type) -> Self:
        ''' 设置位置坐标 '''
        if not isinstance(x, (int, float)) or \
                not isinstance(y, (int, float)) or \
                not isinstance(z, (int, float)):
            raise TypeError

        x, y, z = _tools.roundData(x, y, z) # type: ignore -> return Tuple[numType, numType, numType]
        self._position = _tools.position(x, y, z)
        return super().set_position(x, y, z)

    def set_velocity(self, x_v: num_type, y_v: num_type, z_v: num_type) -> Self:
        ''' 设置速度
        '''
        if not isinstance(x_v, (int, float)) or \
                not isinstance(y_v, (int, float)) or \
                not isinstance(z_v, (int, float)):
            raise TypeError
        self.data["Velocity"] = f"{x_v},{z_v},{y_v}"
        return self

    def set_acceleration(self, x_a: num_type, y_a: num_type, z_a: num_type) -> Self:
        ''' 设置加速度
        '''
        if not isinstance(x_a, (int, float)) or \
                not isinstance(y_a, (int, float)) or \
                not isinstance(z_a, (int, float)):
            raise TypeError
        self.acceleration = _tools.position(x_a, y_a, z_a)
        self.data["Acceleration"] = f"{x_a},{z_a},{y_a}"
        return self
