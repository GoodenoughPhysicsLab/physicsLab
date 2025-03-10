# -*- coding: utf-8 -*-
from .wires import crt_wires, UnitPin
from physicsLab._tools import round_data
from physicsLab.circuit import elements, Pin, crt_wire, OutputPin, InputPin
from physicsLab._core import _Experiment, get_current_experiment, native_to_elementXYZ
from physicsLab._typing import num_type, Dict, Optional, List

class Const_NoGate:
    ''' 只用来提供高电平的非门，若没有则创建一个只读非门，若已存在则不会创建新的元件 '''
    __singleton: Dict[_Experiment, "Const_NoGate"] = {}
    __singleton_NoGate: elements.No_Gate

    def __new__(
            cls,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
    ):
        _Expe: _Experiment = get_current_experiment()
        if _Expe in cls.__singleton:
            return cls.__singleton[_Expe]

        self = super().__new__(cls)
        self.__singleton_NoGate = elements.No_Gate(x, y, z, elementXYZ=elementXYZ)
        self.__singleton[_Expe] = self
        return self

    @property
    def o(self):
        return self.__singleton_NoGate.o

class Super_AndGate:
    ''' 多引脚与门 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            bitnum: int,
            elementXYZ: Optional[bool] = None,
    ) -> None:
        ''' @param: bitnum: 输入引脚的数量
        '''
        if not isinstance(x, (int, float))\
                or not isinstance(y, (int, float)) \
                or not isinstance(z, (int, float)) \
                or not isinstance(elementXYZ, (bool, type(None))) \
                or not isinstance(bitnum, int):
            raise TypeError
        if bitnum <= 1:
            raise ValueError

        if elementXYZ is not True and not (get_current_experiment().is_elementXYZ is True and elementXYZ is None):
            x, y, z = native_to_elementXYZ(x, y, z)
        x, y, z = round_data(x), round_data(y), round_data(z)
        self.bitnum = bitnum

        if bitnum == 2:
            m = elements.And_Gate(x, y, z, elementXYZ=True)
            self._inputs = [m.i_low, m.i_up]
            self._outputs = m.o
            return
        elif bitnum == 3:
            m = elements.Multiplier(x, y, z, elementXYZ=True)
            self._inputs = [m.i_low, m.i_lowmid, m.i_upmid]
            self._outputs = m.o_up
            crt_wire(m.i_up, m.i_upmid)
            return
        elif bitnum == 4:
            m = elements.Multiplier(x, y, z, elementXYZ=True)
            self._inputs = [m.i_low, m.i_lowmid, m.i_upmid, m.i_up]
            self._outputs = m.o_up
            return

        div_num, mod_num = divmod(bitnum, 4)
        _muls: List[elements.Multiplier] = [elements.Multiplier(x, y, z, elementXYZ=True) for _ in range(div_num)]
        self._inputs = []
        for a_mul in _muls:
            self._inputs += [a_mul.i_low, a_mul.i_lowmid, a_mul.i_upmid, a_mul.i_up]

        if mod_num == 0:
            sub_super_and_gate = Super_AndGate(x, y, z, bitnum=div_num, elementXYZ=True)
            # 构造了一个临时的 UnitPin 对象来批量连接导线
            crt_wires(UnitPin(None, *[a_mul.o_up for a_mul in _muls]), sub_super_and_gate.inputs)
        elif mod_num == 1:
            sub_super_and_gate = Super_AndGate(x, y, z, bitnum=div_num + 1, elementXYZ=True)
            self._inputs.append(sub_super_and_gate._inputs[-1])
            crt_wires(UnitPin(None, *[a_mul.o_up for a_mul in _muls]), sub_super_and_gate.inputs[:-1])
        elif mod_num == 2:
            sub_super_and_gate = Super_AndGate(x, y, z, bitnum=div_num + 1, elementXYZ=True)
            _and_gate = elements.And_Gate(x, y, z, elementXYZ=True)
            self._inputs += [_and_gate.i_low, _and_gate.i_up]
            crt_wires(UnitPin(None, *[a_mul.o_up for a_mul in _muls], _and_gate.o), sub_super_and_gate.inputs)
        elif mod_num == 3:
            sub_super_and_gate = Super_AndGate(x, y, z, bitnum=div_num + 1, elementXYZ=True)
            _mul = elements.Multiplier(x, y, z, elementXYZ=True)
            crt_wire(_mul.i_upmid, _mul.i_up)
            self._inputs += [_mul.i_low, _mul.i_lowmid, _mul.i_upmid]
            crt_wires(UnitPin(None, *[a_mul.o_up for a_mul in _muls], _mul.o_up), sub_super_and_gate.inputs)
        else:
            errors.unreachable()

        self._outputs = sub_super_and_gate.output

    @property
    def inputs(self) -> UnitPin:
        return UnitPin(self, *self._inputs)

    @property
    def output(self) -> OutputPin:
        return self._outputs

class Super_OrGate:
    ''' 多引脚或门, 引脚数为num '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            bitnum: int,
            elementXYZ: Optional[bool] = None,
    ) -> None:
        if not isinstance(x, (int, float)) \
                or not isinstance(y, (int, float)) \
                or not isinstance(z, (int, float)) \
                or not isinstance(elementXYZ, (bool, type(None))) \
                or not isinstance(bitnum, int):
            raise TypeError
        if bitnum <= 1:
            raise ValueError

        if elementXYZ is not True and not (get_current_experiment().is_elementXYZ is True and elementXYZ is None):
            x, y, z = native_to_elementXYZ(x, y, z)
        x, y, z = round_data(x), round_data(y), round_data(z)
        self.bitnum = bitnum

        if bitnum == 2:
            tmp = elements.Or_Gate(x, y, z, elementXYZ=True)
            self._inputs = [tmp.i_low, tmp.i_up]
            self._outputs = [tmp.o]
            self._output = tmp.o
            return

        self._inputs = []
        self._outputs = []
        if bitnum % 2 == 0:
            num_copy = bitnum
            while num_copy != 0:
                tmp = elements.Or_Gate(x, y + (bitnum - num_copy) / 2, z, elementXYZ=True)
                self._inputs += [tmp.i_low, tmp.i_up]
                self._outputs.append(tmp.o)
                num_copy -= 2
            next_orgates = Super_OrGate(x, y, z, bitnum=len(self._outputs), elementXYZ=True)
            self._output = next_orgates._output
            for input_, output_ in zip(self._outputs, next_orgates._inputs):
                crt_wires(input_, output_)
        elif bitnum % 2 == 1:
            num_copy = bitnum
            while num_copy != 1:
                tmp = elements.Or_Gate(x, y + (bitnum - num_copy) / 2, z, elementXYZ=True)
                self._inputs += [tmp.i_low, tmp.i_up]
                self._outputs.append(tmp.o)
                num_copy -= 2
            next_orgates = Super_OrGate(x, y, z, bitnum=len(self._outputs) + 1, elementXYZ=True)
            self._inputs.append(next_orgates._inputs[-1])
            self._output = next_orgates._output
            for input_, output_ in zip(self._outputs, next_orgates._inputs):
                crt_wires(input_, output_)
        else:
            errors.unreachable()

    @property
    def inputs(self) -> UnitPin:
        return UnitPin(self, *self._inputs)

    @property
    def output(self) -> Pin:
        return self._output

class Super_NorGate:
    ''' 多引脚或非门, 引脚数为num '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            bitnum: int,
            elementXYZ: Optional[bool] = None,
    ) -> None:
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)) or \
           not isinstance(z, (int, float)) or \
           elementXYZ is not None and not isinstance(elementXYZ, bool) or \
           not isinstance(bitnum, int) or bitnum <= 1:
            raise TypeError

        if elementXYZ is not True and not (get_current_experiment().is_elementXYZ is True and elementXYZ is None):
            x, y, z = native_to_elementXYZ(x, y, z)
        x, y, z = round_data(x), round_data(y), round_data(z)
        self.bitnum = bitnum

        if bitnum == 2:
            tmp = elements.Nor_Gate(x, y, z, elementXYZ=True)
            self._inputs = [tmp.i_low, tmp.i_up]
            self._outputs = [tmp.o]
            self._output = tmp.o
            return

        self._inputs = []
        self._outputs = []
        if bitnum % 2 == 0:
            num_copy = bitnum
            while num_copy != 0:
                tmp = elements.Or_Gate(x, y + (bitnum - num_copy) / 2, z, elementXYZ=True)
                self._inputs += [tmp.i_low, tmp.i_up]
                self._outputs.append(tmp.o)
                num_copy -= 2
            next_orgates = Super_NorGate(x, y, z, bitnum=len(self._outputs), elementXYZ=True)
            self._output = next_orgates._output
            for input_, output_ in zip(self._outputs, next_orgates._inputs):
                crt_wires(input_, output_)
        elif bitnum % 2 == 1:
            num_copy = bitnum
            while num_copy != 1:
                tmp = elements.Or_Gate(x, y + (bitnum - num_copy) / 2, z, elementXYZ=True)
                self._inputs += [tmp.i_low, tmp.i_up]
                self._outputs.append(tmp.o)
                num_copy -= 2
            next_orgates = Super_NorGate(x, y, z, bitnum=len(self._outputs) + 1, elementXYZ=True)
            self._inputs.append(next_orgates._inputs[-1])
            self._output = next_orgates._output
            for input_, output_ in zip(self._outputs, next_orgates._inputs):
                crt_wires(input_, output_)
        else:
            errors.unreachable()

    @property
    def inputs(self) -> UnitPin:
        return UnitPin(
            self,
            *self._inputs
        )

    @property
    def output(self) -> Pin:
        return self._output

class Tick_Counter:
    ''' 当 逻辑输入 输入了num次, 就输出为1, 否则为0
        如果输出为1, 则进入下一个周期, 在下一次输入了num次时输出为1, 否则为0
    '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            num: int,
            elementXYZ: Optional[bool] = None,
    ) -> None:
        if not isinstance(x, (int, float)) \
                or not isinstance(y, (int, float)) \
                or not isinstance(z, (int, float)) \
                or not isinstance(elementXYZ, (bool, type(None))) \
                or not isinstance(num, int):
            raise TypeError
        if num <= 1:
            raise ValueError

        if elementXYZ is not True and not (get_current_experiment().is_elementXYZ is True and elementXYZ is None):
            x, y, z = native_to_elementXYZ(x, y, z)
        x, y, z = round_data(x), round_data(y), round_data(z)
        self.bitnum = num

        if num == 2:
            self._output = elements.T_Flipflop(x, y, z, elementXYZ=True)
        else:
            if num >= 16:
                raise Exception("Do not support num >= 16 in this version")

            self._output = elements.Counter(x + 1, y, z, elementXYZ=True)

            bitlist = []
            num -= 1
            for _ in range(4):
                bitlist.append(num & 1)
                num >>= 1

            output_pins = []
            for i, a_bit in enumerate(bitlist):
                if a_bit:
                    self._o = [self._output.o_low, self._output.o_lowmid, self._output.o_upmid, self._output.o_up][i]
                    output_pins.append(self._o)

            if len(output_pins) >= 2:
                sa = Super_AndGate(x + 1, y, z, bitnum=len(output_pins), elementXYZ=True)
                self._o = sa.output
                crt_wires(UnitPin(None, *output_pins), sa.inputs)

            imp = elements.Imp_Gate(x, y + 1, z, elementXYZ=True)
            or_gate = elements.Or_Gate(x, y, z, elementXYZ=True)
            crt_wires(or_gate.i_low, or_gate.o)
            crt_wires(or_gate.o, imp.i_up)
            crt_wires(or_gate.i_up, self._output.i_up)
            crt_wires(imp.o, self._output.i_low)
            crt_wires(self._o, imp.i_low)

    @property
    def i(self) -> InputPin:
        if isinstance(self._output, elements.T_Flipflop):
            return self._output.i_low
        elif isinstance(self._output, elements.Counter):
            return self._output.i_up
        else:
            errors.unreachable()

    @property
    def o(self) -> OutputPin:
        if isinstance(self._output, elements.T_Flipflop):
            return self._output.o_low
        elif isinstance(self._output, elements.Counter):
            return self._o
        else:
            errors.unreachable()
