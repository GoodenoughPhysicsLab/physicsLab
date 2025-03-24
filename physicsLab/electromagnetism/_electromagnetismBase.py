# -*- coding: utf-8 -*-
from physicsLab import _tools
from physicsLab import errors
from physicsLab.enums import ExperimentType
from physicsLab._core import get_current_experiment, _Experiment, ElementBase
from physicsLab._typing import num_type, Self, override, NoReturn, Optional

class _ElectromagnetismMeta(type):
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
            raise TypeError(f"Parameter x must be of type `int | float`, but got {type(x).__name__}")
        if not isinstance(y, (int, float)):
            raise TypeError(f"Parameter y must be of type `int | float`, but got {type(y).__name__}")
        if not isinstance(z, (int, float)):
            raise TypeError(f"Parameter z must be of type `int | float`, but got {type(z).__name__}")
        if not isinstance(identifier, (str, type(None))):
            raise TypeError(f"Parameter identifier must be of type `Optional[str]`, but got {type(identifier).__name__}")
        if not isinstance(experiment, (_Experiment, type(None))):
            raise TypeError(f"Parameter experiment must be of type `Optional[Experiment]`, but got {type(experiment).__name__}")

        _Expe: _Experiment
        if experiment is None:
            _Expe = get_current_experiment()
        else:
            _Expe = experiment
        if _Expe.experiment_type != ExperimentType.Electromagnetism:
            raise errors.ExperimentTypeError(f"Can't create {cls.__name__} because experiment_type is {_Expe.experiment_type}")

        self: "ElectromagnetismBase" = cls.__new__(cls)
        self.experiment = _Expe

        self.__init__(x, y, z, **kwargs)
        assert hasattr(self, "data") and isinstance(self.data, dict)

        self._set_identifier(identifier)
        self.set_position(x, y, z)
        self.set_rotation(0, 0, 0)

        self.experiment.Elements.append(self)
        self.experiment._id2element[self.data["Identifier"]] = self

        return self

class ElectromagnetismBase(ElementBase, metaclass=_ElectromagnetismMeta):
    ''' 所有电与磁元件的父类 '''
    experiment: _Experiment

    def __init__(*args, **kwargs) -> NoReturn:
        raise NotImplementedError

    @override
    def set_position(self, x: num_type, y: num_type, z: num_type) -> Self:
        if not isinstance(x, (int, float)) \
                or not isinstance(y, (int, float)) \
                or not isinstance(z, (int, float)):
            raise TypeError

        x, y, z= _tools.round_data(x), _tools.round_data(y), _tools.round_data(z)
        self._position = _tools.position(x, y, z)
        return super().set_position(x, y, z)

    def set_rotation(
            self,
            x_r: num_type,
            y_r: num_type,
            z_r: num_type,
    ) -> Self:
        ''' 设置元件的角度 '''
        if not isinstance(x_r, (int, float)) \
                or not isinstance(y_r, (int, float)) \
                or not isinstance(z_r, (int, float)):
            raise TypeError

        assert hasattr(self, "data")
        x_r, y_r, z_r = _tools.round_data(x_r), _tools.round_data(y_r), _tools.round_data(z_r)
        self.data["Rotation"] = f"{x_r},{z_r},{y_r}"
        return self
