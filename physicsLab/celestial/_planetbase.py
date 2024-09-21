from physicsLab import _tools
from physicsLab import errors
from physicsLab.elementBase import ElementBase
from physicsLab.typehint import numType, Self
from physicsLab.enums import ExperimentType
from physicsLab.experiment import get_Experiment

class _PlanetMeta(type):
    def __call__(cls, x:numType, y: numType, z:numType, *args, **kwargs):
        if not isinstance(x, (int, float)) or \
                not isinstance(y, (int, float)) or \
                not isinstance(z, (int, float)):
            raise TypeError

        self = cls.__new__(cls) # type: ignore -> create subclass
        _Expe = get_Experiment()
        self.experiment = _Expe

        if _Expe.experiment_type != ExperimentType.Celestial:
            raise errors.ExperimentTypeError

        x, y, z = _tools.roundData(x, y, z) # type: ignore -> return Tuple[numType, numType, numType]

        self.__init__(x, y, z, *args, **kwargs)
        assert hasattr(self, "data")

        self.data["Identifier"] = _tools.randString(32)
        self.set_position(x, y, z)
        self.set_velocity(0, 0, 0)
        self.set_acceleration(0, 0, 0)

        if self._position in _Expe.elements_Position.keys():
            _Expe.elements_Position[self._position].append(self)
        else:
            _Expe.elements_Position[self._position] = [self]

        _Expe.Elements.append(self)

        return self

class PlanetBase(ElementBase, metaclass=_PlanetMeta):
    ''' 星球基类 '''
    def __init__(self) -> None:
        raise AssertionError(f"internal error, can't initial {self.__class__.__name__}, please bug report")

    def __define_virtual_var_to_let_ide_show(
            self, data: dict,
    ):
        ''' useless
            这些变量的定义在CircuitMeta中
        '''
        self.data: dict = data

    def set_position(self, x_p: numType, y_p: numType, z_p: numType) -> Self:
        ''' 设置位置
        '''
        if not isinstance(x_p, (int, float)) or \
                not isinstance(y_p, (int, float)) or \
                not isinstance(z_p, (int, float)):
            raise TypeError
        self._position = _tools.position(x_p, y_p, z_p)
        self.data["Position"] = f"{self._position.x},{self._position.z},{self._position.y}"
        return self

    def get_position(self) -> _tools.position:
        return self._position

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
