# -*- coding: utf-8 -*-
import physicsLab.circuit.elementXYZ as _elementXYZ

from physicsLab.circuit import elements
from physicsLab.circuit.wire import InputPin, OutputPin
from physicsLab.typehint import numType, Optional, Self

class _TriggerMeta(type):
    def __call__(cls, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None) -> Self:
        self = cls.__new__(cls)
        if not (
                isinstance(x, (float, int)) and
                isinstance(y, (float, int)) and
                isinstance(z, (float, int)) and
                (elementXYZ is None or isinstance(elementXYZ, bool))
        ):
            raise TypeError

        if not (elementXYZ is True or _elementXYZ.is_elementXYZ() is True and elementXYZ is None):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)

        self.__init__(x, y, z, elementXYZ)

        return self

class Rising_edge_trigger(metaclass=_TriggerMeta):
    ''' 上升沿触发器 '''
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None) -> None:
        self.no_gate = elements.No_Gate(x, y, z, True)
        self.and_gate = elements.And_Gate(x, y + 1, z, True)
        self.no_gate.o - self.and_gate.i_low
        self.no_gate.i - self.and_gate.i_up

    @property
    def i(self) -> InputPin:
        return self.no_gate.i

    @property
    def o(self) -> OutputPin:
        return self.and_gate.o

class Falling_edge_trigger(metaclass=_TriggerMeta):
    ''' 下降沿触发器 '''
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None) -> None:
        self.yes_gate = elements.Yes_Gate(x, y, z, True)
        self.nimp_gate = elements.Nimp_Gate(x, y + 1, z, True)
        self.yes_gate.o - self.nimp_gate.i_up
        self.yes_gate.i - self.nimp_gate.i_low

    @property
    def i(self) -> InputPin:
        return self.yes_gate.i

    @property
    def o(self) -> OutputPin:
        return self.nimp_gate.o

class Edge_trigger(metaclass=_TriggerMeta):
    ''' 边沿触发器 (同时可以在上升沿与下降沿触发) '''
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None) -> None:
        self.yes_gate = elements.Yes_Gate(x, y, z, True)
        self.xor_gate = elements.Xor_Gate(x, y + 1, z, True)
        self.yes_gate.o - self.xor_gate.i_up
        self.yes_gate.i - self.xor_gate.i_low

    @property
    def i(self) -> InputPin:
        return self.yes_gate.i

    @property
    def o(self) -> OutputPin:
        return self.xor_gate.o
