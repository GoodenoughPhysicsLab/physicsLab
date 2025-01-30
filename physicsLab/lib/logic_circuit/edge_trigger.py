# -*- coding: utf-8 -*-
from physicsLab._core import get_current_experiment
from physicsLab.circuit import elements
from physicsLab.circuit._circuit_core import InputPin, OutputPin, crt_wire
from physicsLab._typing import num_type, Optional
from physicsLab._core import native_to_elementXYZ

class _TriggerMeta(type):
    def __call__(
            cls,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
    ):
        self = cls.__new__(cls)
        if not isinstance(x, (float, int)) \
                or not isinstance(y, (float, int)) \
                or not isinstance(z, (float, int)) \
                or not isinstance(elementXYZ, (bool, type(None))):
            raise TypeError

        if not (elementXYZ is True or get_current_experiment().is_elementXYZ is True and elementXYZ is None):
            x, y, z = native_to_elementXYZ(x, y, z)

        self.__init__(x, y, z, elementXYZ=elementXYZ)

        return self

class RisingEdgeTrigger(metaclass=_TriggerMeta):
    ''' 上升沿触发器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
    ) -> None:
        self.no_gate = elements.No_Gate(x, y, z, elementXYZ=True)
        self.and_gate = elements.And_Gate(x, y + 1, z, elementXYZ=True)
        crt_wire(self.no_gate.o, self.and_gate.i_low)
        crt_wire(self.no_gate.i, self.and_gate.i_up)

    @property
    def i(self) -> InputPin:
        return self.no_gate.i

    @property
    def o(self) -> OutputPin:
        return self.and_gate.o

class FallingEdgeTrigger(metaclass=_TriggerMeta):
    ''' 下降沿触发器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
    ) -> None:
        self.yes_gate = elements.Yes_Gate(x, y, z, elementXYZ=True)
        self.nimp_gate = elements.Nimp_Gate(x, y + 1, z, elementXYZ=True)
        crt_wire(self.yes_gate.o, self.nimp_gate.i_up)
        crt_wire(self.yes_gate.i, self.nimp_gate.i_low)

    @property
    def i(self) -> InputPin:
        return self.yes_gate.i

    @property
    def o(self) -> OutputPin:
        return self.nimp_gate.o

class EdgeTrigger(metaclass=_TriggerMeta):
    ''' 边沿触发器 (同时可以在上升沿与下降沿触发) '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
    ) -> None:
        self.yes_gate = elements.Yes_Gate(x, y, z, elementXYZ=True)
        self.xor_gate = elements.Xor_Gate(x, y + 1, z, elementXYZ=True)
        crt_wire(self.yes_gate.o, self.xor_gate.i_up)
        crt_wire(self.yes_gate.i, self.xor_gate.i_low)

    @property
    def i(self) -> InputPin:
        return self.yes_gate.i

    @property
    def o(self) -> OutputPin:
        return self.xor_gate.o
