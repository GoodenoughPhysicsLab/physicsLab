# -*- coding: utf-8 -*-
from physicsLab.typehint import num_type, Self, override
from physicsLab import _tools
from physicsLab import errors
from physicsLab._experiment import get_current_experiment, _Experiment, _ElementBase
from physicsLab.enums import ExperimentType

class _ElectromagnetismMeta(type):
    def __call__(cls,
                 x: num_type,
                 y: num_type,
                 z: num_type,
                 *args,
                 **kwargs
                 ):
        if not isinstance(x, (int, float)) or \
                not isinstance(y, (int, float)) or \
                not isinstance(z, (int, float)):
            raise TypeError

        _Expe = get_current_experiment()
        if _Expe.experiment_type != ExperimentType.Electromagnetism:
            raise errors.ExperimentTypeError

        self = cls.__new__(cls) # type: ignore -> create subclass
        self.experiment = _Expe

        self.__init__(x, y, z, *args, **kwargs)
        assert hasattr(self, "data") and isinstance(self.data, dict)

        self.data["Identifier"] = _tools.randString(32)
        self.set_position(x, y, z)
        self.set_rotation(0, 0, 0)

        _Expe.Elements.append(self)

        return self

class ElectromagnetismBase(_ElementBase, metaclass=_ElectromagnetismMeta):
    ''' 所有电与磁元件的父类 '''
    experiment: _Experiment

    def __init__(self) -> None:
        raise NotImplementedError

    @override
    def set_position(self, x: num_type, y: num_type, z: num_type) -> Self:
        if not isinstance(x, (int, float)) or \
                not isinstance(y, (int, float)) or \
                not isinstance(z, (int, float)):
            raise TypeError

        x, y, z= _tools.roundData(x, y, z) # type: ignore
        self._position = _tools.position(x, y, z)
        return super().set_position(x, y, z)

    def set_rotation(
            self,
            x_r: num_type,
            y_r: num_type,
            z_r: num_type,
    ) -> Self:
        ''' 设置原件的角度 '''
        if not isinstance(x_r, (int, float)) or \
                not isinstance(y_r, (int, float)) or \
                not isinstance(z_r, (int, float)):
            raise TypeError

        assert hasattr(self, "data")
        x_r, y_r, z_r = _tools.roundData(x_r, y_r, z_r) # type: ignore -> return tuple
        self.data["Rotation"] = f"{x_r},{z_r},{y_r}"
        return self
