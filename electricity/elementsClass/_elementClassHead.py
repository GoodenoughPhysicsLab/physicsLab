#coding=utf-8
import random as _random
import string as _string
from typing import Callable, Union
import _fileGlobals
import electricity._elementPin as _elementPin
import electricity._elementPosition as _elementPosition

# 所有元件的父类
class elementObject:
    # 用来避免IDE报太多错的函数，无实际作用
    def __define(self):
        self._arguments = {'ModelID': '', 'Identifier': "", 'IsBroken': False, 'IsLocked': False, 'Properties': {},
                           'Statistics': {}, 'Position': "", 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {}, 'DiagramRotation': 0}
        self._index = None

    # 设置原件的角度
    def set_Rotation(self, xRotation: Union[int, float] = 0, yRotation: Union[int, float] = 0, zRotation: Union[int, float] = 180):
        if not (isinstance(xRotation, (int, float)) and isinstance(yRotation, (int, float)) and isinstance(zRotation, (int, float))):
            raise RuntimeError('illegal argument')
        self._arguments["Rotation"] = f"{_fileGlobals.myRound(xRotation)},{_fileGlobals.myRound(zRotation)},{_fileGlobals.myRound(yRotation)}"
        return self

    # 重新设置元件的坐标
    def set_Position(self, x: Union[int, float], y: Union[int, float], z: Union[int, float]):
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
            raise RuntimeError('illegal argument')
        x, y, z = _fileGlobals.myRound(x), _fileGlobals.myRound(y), _fileGlobals.myRound(z)
        del _fileGlobals.elements_Address[self._position]
        self._position = (x, y, z)
        self._arguments['Position'] = f"{x},{z},{y}"
        _fileGlobals.elements_Address[self._position] = self
        return self

    # 格式化坐标参数，主要避免浮点误差
    def format_Position(self) -> tuple:
        if not isinstance(self._position, tuple) or self._position.__len__() != 3:
            raise RuntimeError("Position must be a tuple of length three but gets some other value")
        self._position = (_fileGlobals.myRound(self._position[0]), _fileGlobals.myRound(self._position[1]), _fileGlobals.myRound(self._position[2]))
        return self._position

    # 获取原件的坐标
    def get_Position(self) -> tuple:
        return self._position

    # 获取父类的类型
    def father_type(self) -> str:
        return 'element'

    # 获取元件的index（每创建一个元件，index就加1）
    def get_Index(self) -> int:
        return self._index

    # 获取子类的类型（也就是ModelID）
    def type(self) -> str:
        return self._arguments['ModelID']

    # 打印参数
    def print_arguments(self) -> None:
        print(self._arguments)

# __init__ 装饰器
_index = 1
def element_Init_HEAD(isBigElement = False) -> Callable:
    def resultdec(func : Callable) -> Callable:
        def result(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0, elementXYZ: bool = None) -> None:
            if not isinstance(x, (float, int)) and isinstance(y, (float, int)) and isinstance(z, (float, int)):
                raise TypeError('illegal argument')
            x, y, z = _fileGlobals.myRound(x), _fileGlobals.myRound(y), _fileGlobals.myRound(z)
            # 元件坐标系
            if elementXYZ == True or (_elementPosition.elementXYZ == True and elementXYZ is None):
                x, y, z = _elementPosition.translate(x, y, z, bool(isBigElement))
            self._position = (x, y, z)
            if self._position in _fileGlobals.elements_Address.keys():
                raise RuntimeError("The position already exists")
            func(self, x, y, z)
            self._arguments["Identifier"] = ''.join(_random.choice(_string.ascii_letters + _string.digits) for _ in range(32))
            self._arguments["Position"] = f"{self._position[0]},{self._position[2]},{self._position[1]}"
            _fileGlobals.Elements.append(self._arguments)
            _fileGlobals.elements_Address[self._position] = self
            self.set_Rotation()
            # 通过元件生成顺序来索引元件
            global _index
            self._index = _index
            _fileGlobals.elements_Index[self._index] = self
            # 元件index索引加1
            _index += 1
        return result
    return resultdec

# 双引脚模拟电路原件的引脚
def two_pin_ArtificialCircuit_Pin(cls):
    @property
    def red(self):
        return _elementPin.element_Pin(self, 0)
    cls.red, cls.l = red, red

    @property
    def black(self):
        return _elementPin.element_Pin(self, 1)
    cls.black, cls.r = black, black

    return cls
