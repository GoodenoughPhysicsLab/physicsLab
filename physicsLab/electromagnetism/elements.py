# coding=utf-8
from physicsLab import _tools
from physicsLab import errors

from physicsLab.experiment import stack_Experiment
from physicsLab.experimentType import experimentType
from physicsLab.typehint import Callable, Optional, numType

# 所有电与磁元件的父类
class _elementBase:
    # 设置原件的角度
    def set_Rotation(self, xRotation: numType = 0, yRotation: numType = 0,
                     zRotation: numType = 180):
        if not (
                isinstance(xRotation, (int, float)) and
                isinstance(yRotation, (int, float)) and
                isinstance(zRotation, (int, float))
        ):
            raise RuntimeError('illegal argument')

        self._arguments["Rotation"] = \
            f"{_tools.roundData(xRotation)},{_tools.roundData(zRotation)},{_tools.roundData(yRotation)}"
        return self

    # 重新设置元件的坐标
    def set_Position(self, x: numType, y: numType, z: numType):
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
            raise RuntimeError('illegal argument')
        x, y, z = _tools.roundData(x, y, z)
        del stack_Experiment.top().elements_Position[self._position]
        self._position = (x, y, z)
        self._arguments['Position'] = f"{x},{z},{y}"
        stack_Experiment.top().elements_Position[self._position] = self
        return self

    # 格式化坐标参数，主要避免浮点误差
    def format_Position(self) -> tuple:
        if not isinstance(self._position, tuple) or self._position.__len__() != 3:
            raise RuntimeError("Position must be a tuple of length three but gets some other value")
        self._position = _tools.roundData(self._position[0], self._position[1], self._position[2])
        return self._position


# __init__ 装饰器
_index = 1


def _element_Init_HEAD(func: Callable) -> Callable:
    def result(
            self,
            x: numType = 0,
            y: numType = 0,
            z: numType = 0,
            elementXYZ: Optional[bool] = None
    ) -> None:
        if not (
                isinstance(x, (float, int)) and
                isinstance(y, (float, int)) and
                isinstance(z, (float, int))
        ):
            raise TypeError('illegal argument')
        if stack_Experiment.top().ExperimentType != experimentType.Electromagnetism:
            raise errors.ExperimentTypeError

        _Expe = stack_Experiment.top()

        # 初始化全局变量
        global is_big_Element
        is_big_Element = False

        x, y, z = _tools.roundData(x, y, z) # type: ignore
        self._position = (x, y, z)

        func(self, x, y, z)

        self._arguments["Identifier"] = _tools.randString(32)
        # x, z, y 物实采用欧拉坐标系
        self._arguments["Position"] = f"{x},{z},{y}"

        # 该坐标是否已存在，则存入列表
        if self._position in _Expe.elements_Position.keys():
            _Expe.elements_Position[self._position]['self'].append(self)
        else:
            elementDict: dict = {
                'self': [self],
                'elementXYZ': None,  # 电与磁实验不支持元件坐标系
                'originPosition': None
            }
            _Expe.elements_Position[self._position] = elementDict
        self.set_Rotation()
        # 通过元件生成顺序来索引元件
        global _index
        self._index = _index
        _Expe.Elements.append(self)
        # 元件index索引加1
        _index += 1

    return result


# 负电荷
class Negative_Charge(_elementBase):
    @_element_Init_HEAD
    def __init__(self, x: numType, y: numType, z: numType):
        self._arguments = {'ModelID': 'Negative Charge', 'Identifier': '',
                           'Properties': {'锁定': 1.0, '强度': -1e-07, '质量': 0.1},
                           'Position': '', 'Rotation': '', 'Velocity': '0,0,0',
                           'AngularVelocity': '0,0,0'}


class Positive_Charge(_elementBase):
    @_element_Init_HEAD
    def __init__(self, x: numType, y: numType, z: numType):
        self._arguments = {'ModelID': 'Positive Charge', 'Identifier': '',
                           'Properties': {'锁定': 1.0, '强度': 1e-07, '质量': 0.1},
                           'Position': '', 'Rotation': '', 'Velocity': '0,0,0',
                           'AngularVelocity': '0,0,0'}