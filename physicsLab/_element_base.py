# -*- coding: utf-8 -*-
import copy

from physicsLab.typehint import numType, Self, final
from physicsLab import _tools

class ElementBase:
    def __init__(self) -> None:
        raise NotImplementedError

    def set_position(self, x: numType, y: numType, z: numType) -> Self:
        ''' 设置原件的位置 '''
        if not isinstance(x, (int, float)) or \
                not isinstance(y, (int, float)) or \
                not isinstance(z, (int, float)):
            raise TypeError

        x, y, z = _tools.roundData(x, y, z) # type: ignore -> result type: tuple
        assert hasattr(self, 'experiment')
        _Expe = self.experiment

        for self_list in _Expe._elements_position.values():
            if self in self_list:
                self_list.remove(self)

        assert hasattr(self, 'data')
        self.data['Position'] = f"{x},{z},{y}" # type: ignore -> has attr .data

        assert hasattr(self, '_position')
        if self._position in _Expe._elements_position.keys():
            _Expe._elements_position[self._position].append(self)
        else:
            _Expe._elements_position[self._position] = [self]

        return self

    @final
    def get_position(self) -> tuple:
        ''' 获取原件的坐标 '''
        assert hasattr(self, '_position')
        return copy.deepcopy(self._position)
