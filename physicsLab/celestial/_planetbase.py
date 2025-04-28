# -*- coding: utf-8 -*-
from physicsLab import _tools
from physicsLab import errors
from physicsLab.enums import ExperimentType
from physicsLab._core import get_current_experiment, _Experiment, ElementBase
from physicsLab._typing import num_type, Self, override, final, NoReturn, Optional

class _PlanetMeta(type):
    def __call__(
            cls,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            identifier: Optional[str] = None,
            experiment: Optional[_Experiment] = None,
            **kwargs,
    ):
        if not isinstance(x, (int, float)):
            errors.type_error(f"Parameter x must be of type `int | float`, but got value `{x}` of type `{type(x).__name__}`")
        if not isinstance(y, (int, float)):
            errors.type_error(f"Parameter y must be of type `int | float`, but got value `{y}` of type `{type(y).__name__}`")
        if not isinstance(z, (int, float)):
            errors.type_error(f"Parameter z must be of type `int | float`, but got value `{z}` of type `{type(z).__name__}`")
        if not isinstance(identifier, (str, type(None))):
            errors.type_error(f"Parameter identifier must be of type `Optional[str]`, but got value `{identifier}` of type `{type(identifier).__name__}`")
        if not isinstance(experiment, (_Experiment, type(None))):
            errors.type_error(f"Parameter experiment must be of type `Optional[Experiment]`, but got value `{experiment}` of type `{type(experiment).__name__}`")

        _Expe: _Experiment
        if experiment is None:
            _Expe = get_current_experiment()
        else:
            _Expe = experiment
        if _Expe.experiment_type != ExperimentType.Celestial:
            raise errors.ExperimentTypeError(f"Can't create {cls.__name__} because experiment_type is {_Expe.experiment_type}")

        self: "PlanetBase" = cls.__new__(cls)
        self.experiment = _Expe

        x, y, z = _tools.round_data(x), _tools.round_data(y), _tools.round_data(z)

        self.__init__(x, y, z, **kwargs)
        assert isinstance(self.data, dict)

        self._set_identifier(identifier)
        self.set_position(x, y, z)
        self.set_velocity(0, 0, 0)
        self.set_acceleration(0, 0, 0)

        self.experiment.Elements.append(self)
        self.experiment._id2element[self.data["Identifier"]] = self

        return self

class PlanetBase(ElementBase, metaclass=_PlanetMeta):
    ''' 星球基类 '''
    experiment: _Experiment

    def __init__(*args, **kwargs) -> NoReturn:
        raise NotImplementedError

    @final
    @override
    def set_position(self, x: num_type, y: num_type, z: num_type) -> Self:
        ''' 设置位置坐标 '''
        if not isinstance(x, (int, float)):
            errors.type_error(f"Parameter x must be of type `int | float`, but got {type(x).__name__}")
        if not isinstance(y, (int, float)):
            errors.type_error(f"Parameter y must be of type `int | float`, but got {type(x).__name__}")
        if not isinstance(z, (int, float)):
            errors.type_error(f"Parameter z must be of type `int | float`, but got {type(x).__name__}")

        x, y, z = _tools.round_data(x), _tools.round_data(y), _tools.round_data(z)
        self._position = _tools.position(x, y, z)
        return super().set_position(x, y, z)

    def set_velocity(self, x_v: num_type, y_v: num_type, z_v: num_type) -> Self:
        ''' 设置速度
        '''
        if not isinstance(x_v, (int, float)) \
                or not isinstance(y_v, (int, float)) \
                or not isinstance(z_v, (int, float)):
            raise TypeError
        self.data["Velocity"] = f"{x_v},{z_v},{y_v}"
        return self

    def set_acceleration(self, x_a: num_type, y_a: num_type, z_a: num_type) -> Self:
        ''' 设置加速度
        '''
        if not isinstance(x_a, (int, float)) \
                or not isinstance(y_a, (int, float)) \
                or not isinstance(z_a, (int, float)):
            raise TypeError
        self.acceleration = _tools.position(x_a, y_a, z_a)
        self.data["Acceleration"] = f"{x_a},{z_a},{y_a}"
        return self
