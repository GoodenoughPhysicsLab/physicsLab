# -*- coding: utf-8 -*-
import physicsLab.errors as errors
import physicsLab.circuit.elementXYZ as _elementXYZ

from .wires import UnitPin, crt_wires
from physicsLab._tools import roundData
from physicsLab.circuit import elements
from physicsLab.circuit.wire import crt_wire, Pin
from physicsLab.Experiment import get_current_experiment
from physicsLab.enums import ExperimentType
from physicsLab.typehint import numType, Optional, Self, Union, Type, List

class Const_NoGate:
    ''' 只读非门，若没有则创建一个只读非门，若已存在则不会创建新的元件 '''
    __singleton: Optional["Const_NoGate"]  = None
    __singleton_NoGate = None

    def __new__(cls,
                x: numType,
                y: numType,
                z: numType,
                elementXYZ: Optional[bool] = None,
                ):
        if Const_NoGate.__singleton_NoGate is None:
            Const_NoGate.__singleton = object.__new__(cls)
            Const_NoGate.__singleton_NoGate = elements.No_Gate(x, y, z, elementXYZ)

        assert Const_NoGate.__singleton is not None
        return Const_NoGate.__singleton

    @property
    def o(self):
        assert Const_NoGate.__singleton_NoGate is not None
        return Const_NoGate.__singleton_NoGate.o

class Super_AndGate:
    ''' 多引脚与门, 引脚数为num '''
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None,
                 ) -> None:
        if not isinstance(x, (int, float)) or \
           not isinstance(y, (int, float)) or \
           not isinstance(z, (int, float)) or \
           elementXYZ is not None and not isinstance(elementXYZ, bool) or \
           not isinstance(bitnum, int) or bitnum <= 1:
            raise TypeError

        if not (elementXYZ is True or (_elementXYZ.is_elementXYZ() is True and elementXYZ is None)):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)
        x, y, z = roundData(x, y, z)
        self.bitnum = bitnum

        if bitnum == 2:
            m = elements.And_Gate(x, y, z, elementXYZ=True)
            self._inputs = [m.i_low, m.i_up]
            self._outputs = m.o
            return
        elif bitnum == 3 or bitnum == 4:
            m = elements.Multiplier(x, y, z, elementXYZ=True)
            self._inputs = [m.i_low, m.i_lowmid, m.i_upmid, m.i_up]
            self._outputs = m.o_up
            if bitnum == 3:
                m.i_up - m.i_upmid
            return
        if bitnum == 5:
            m = elements.Multiplier(x, y, z, elementXYZ=True)
            a = elements.And_Gate(x, y, z, elementXYZ=True)
            m.o_up - a.i_low
            self._inputs = [m.i_low, m.i_lowmid, m.i_upmid, m.i_up, a.i_up]
            self._outputs = a.o
            return

        muls, mod_num = divmod(bitnum, 4)
        self._inputs = []

        if mod_num == 2 or mod_num == 3:
            muls = [elements.Multiplier(x, y, z, elementXYZ=True) for _ in range(muls)]
            tmp = Super_AndGate(x, y, z, len(muls) + 1, True)
        elif mod_num == 1:
            muls = [elements.Multiplier(x, y, z, elementXYZ=True) for _ in range(muls - 1)]
            tmp = Super_AndGate(x, y, z, len(muls) + 5, True)
        else: # end_num == 0
            muls = [elements.Multiplier(x, y, z, elementXYZ=True) for _ in range(muls)]
            tmp = Super_AndGate(x, y, z, len(muls), True)

        if mod_num == 3:
            end_element = elements.Multiplier(x, y, z, elementXYZ=True)
            end_element.i_up - end_element.i_upmid
            crt_wires(UnitPin(None, *(mul.o_up for mul in muls), end_element.o_up), tmp.inputs)
            for mul in muls:
                self._inputs += [mul.i_low, mul.i_lowmid, mul.i_upmid, mul.i_up]
            self._inputs += [end_element.i_low, end_element.i_lowmid, end_element.i_upmid, end_element.i_up]

        elif mod_num == 2:
            end_element = elements.And_Gate(x, y, z, elementXYZ=True)
            crt_wires(UnitPin(None, *(mul.o_up for mul in muls), end_element.o), tmp.inputs)
            for mul in muls:
                self._inputs += [mul.i_low, mul.i_lowmid, mul.i_upmid, mul.i_up]
            self._inputs += [end_element.i_low, end_element.i_up]

        elif mod_num == 1:
            for mul, i in zip(muls, tmp._inputs):
                mul.o_up - i
            for mul in muls:
                self._inputs += [mul.i_low, mul.i_lowmid, mul.i_upmid, mul.i_up]
            self._inputs += tmp._inputs[len(muls):]

        else: # end_num == 0
            crt_wires(UnitPin(None, *(mul.o_up for mul in muls)), tmp.inputs)
            for mul in muls:
                self._inputs += [mul.i_low, mul.i_lowmid, mul.i_upmid, mul.i_up]

        self._outputs = tmp.output

    @property
    def inputs(self) -> UnitPin:
        return UnitPin(
            self,
            *self._inputs
        )

    @property
    def output(self) -> Pin:
        return self._outputs

class Super_OrGate:
    ''' 多引脚或门, 引脚数为num '''
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None,
                 ) -> None:
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)) or \
           not isinstance(z, (int, float)) or \
           not isinstance(elementXYZ, (bool, type(None))) or \
           not isinstance(bitnum, int) or bitnum <= 1:
            raise TypeError

        if not (elementXYZ is True or (_elementXYZ.is_elementXYZ() is True and elementXYZ is None)):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)
        x, y, z = roundData(x, y, z)
        self.bitnum = bitnum

        if bitnum == 2:
            tmp = elements.Or_Gate(x, y, z, True)
            self._inputs = [tmp.i_low, tmp.i_up]
            self._outputs = [tmp.o]
            self._output = tmp.o
            return
        elif bitnum == 3:
            tmp = elements.Or_Gate(x, y, z, True)
            tmp2 = elements.Or_Gate(x, y + 1, z, True)
            tmp2.o - tmp.i_up
            self._inputs = [tmp.i_low, tmp2.i_low, tmp2.i_up]
            self._outputs = [tmp.o]
            self._output = tmp.o
            return

        self._inputs = []
        self._outputs = []
        if bitnum % 2 == 0:
            num_copy = bitnum
            while num_copy != 0:
                tmp = elements.Or_Gate(x, y + (bitnum - num_copy) / 2, z, True)
                self._inputs += [tmp.i_low, tmp.i_up]
                self._outputs.append(tmp.o)
                num_copy -= 2
            next_orgates = Super_OrGate(x, y, z, len(self._outputs), True)
            self._output = next_orgates._output
            for input_, output_ in zip(self._outputs, next_orgates._inputs):
                crt_wire(input_, output_)
        else: # num % 2 == 1
            num_copy = bitnum
            while num_copy != 1:
                tmp = elements.Or_Gate(x, y + (bitnum - num_copy) / 2, z, True)
                self._inputs += [tmp.i_low, tmp.i_up]
                self._outputs.append(tmp.o)
                num_copy -= 2
            next_orgates = Super_OrGate(x, y, z, len(self._outputs) + 1, True)
            self._inputs.append(next_orgates._inputs[-1])
            self._output = next_orgates._output
            for input_, output_ in zip(self._outputs, next_orgates._inputs):
                crt_wire(input_, output_)

    @property
    def inputs(self) -> UnitPin:
        return UnitPin(
            self,
            *self._inputs
        )

    @property
    def output(self) -> Pin:
        return self._output

class Super_NorGate:
    ''' 多引脚或非门, 引脚数为num '''
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None,
                 ) -> None:
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)) or \
           not isinstance(z, (int, float)) or \
           elementXYZ is not None and not isinstance(elementXYZ, bool) or \
           not isinstance(bitnum, int) or bitnum <= 1:
            raise TypeError

        if not (elementXYZ is True or (_elementXYZ.is_elementXYZ() is True and elementXYZ is None)):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)
        x, y, z = roundData(x, y, z)
        self.bitnum = bitnum

        if bitnum == 2:
            tmp = elements.Nor_Gate(x, y, z, True)
            self._inputs = [tmp.i_low, tmp.i_up]
            self._outputs = [tmp.o]
            self._output = tmp.o
            return
        elif bitnum == 3:
            tmp = elements.Nor_Gate(x, y, z, True)
            tmp2 = elements.Or_Gate(x, y + 1, z, True)
            tmp2.o - tmp.i_up
            self._inputs = [tmp.i_low, tmp2.i_low, tmp2.i_up]
            self._outputs = [tmp.o]
            self._output = tmp.o
            return

        self._inputs = []
        self._outputs = []
        if bitnum % 2 == 0:
            num_copy = bitnum
            while num_copy != 0:
                tmp = elements.Or_Gate(x, y + (bitnum - num_copy) / 2, z, True)
                self._inputs += [tmp.i_low, tmp.i_up]
                self._outputs.append(tmp.o)
                num_copy -= 2
            next_orgates = Super_NorGate(x, y, z, True, len(self._outputs))
            self._output = next_orgates._output
            for input_, output_ in zip(self._outputs, next_orgates._inputs):
                crt_wire(input_, output_)
        else: # num % 2 == 1
            num_copy = bitnum
            while num_copy != 1:
                tmp = elements.Or_Gate(x, y + (bitnum - num_copy) / 2, z, True)
                self._inputs += [tmp.i_low, tmp.i_up]
                self._outputs.append(tmp.o)
                num_copy -= 2
            next_orgates = Super_NorGate(x, y, z, True, len(self._outputs) + 1)
            self._inputs.append(next_orgates._inputs[-1])
            self._output = next_orgates._output
            for input_, output_ in zip(self._outputs, next_orgates._inputs):
                crt_wire(input_, output_)

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
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None,
                 ) -> None:
        if not isinstance(x, (int, float)) or \
            not isinstance(y, (int, float)) or \
            not isinstance(z, (int, float)) or \
            not isinstance(elementXYZ, (bool, type(None))) or \
            not isinstance(bitnum, int) or bitnum <= 1:
            raise TypeError

        if not (elementXYZ is True or (_elementXYZ.is_elementXYZ() is True and elementXYZ is None)):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)
        x, y, z = roundData(x, y, z)
        self.bitnum = bitnum

        if bitnum == 2:
            self._output = elements.T_Flipflop(x, y, z, True)
        else:
            if bitnum >= 16:
                raise Exception("Do not support num >= 16 in this version")

            self._output = elements.Counter(x + 1, y, z, True)

            bitlist = []
            bitnum -= 1
            for _ in range(4):
                bitlist.append(bitnum & 1)
                bitnum >>= 1

            output_pins = []
            for i, a_bit in enumerate(bitlist):
                if a_bit:
                    _p = [self._output.o_low, self._output.o_lowmid, self._output.o_upmid, self._output.o_up][i]
                    output_pins.append(_p)
                    self._o = UnitPin(self, _p)

            if len(output_pins) >= 2:
                sa = Super_AndGate(x + 1, y, z, True, len(output_pins))
                self._o = sa.output
                crt_wires(UnitPin(None, *output_pins), sa.inputs)

            imp = elements.Imp_Gate(x, y + 1, z, True)
            or_gate = elements.Or_Gate(x, y, z, True)
            or_gate.i_low - or_gate.o
            or_gate.o - imp.i_up
            or_gate.i_up - self._output.i_up
            imp.o - self._output.i_low
            crt_wires(self._o, imp.i_low)

    @property
    def input(self) -> UnitPin:
        if isinstance(self._output, elements.T_Flipflop):
            return UnitPin(self, self._output.i_low)
        else: # isinstance(self._output, elements.Counter)
            return UnitPin(self, self._output.i_up)

    @property
    def output(self) -> UnitPin:
        if isinstance(self._output, elements.T_Flipflop):
            return UnitPin(self, self._output.o_low)
        else: # isinstance(self._output, elements.Counter)
            return self._o

class Two_four_Decoder:
    ''' 2-4译码器 '''
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 elementXYZ: Optional[bool] = None,
                 ) -> None:
        if not isinstance(x, (int, float)) or \
            not isinstance(y, (int, float)) or \
            not isinstance(z, (int, float)) or \
            not isinstance(elementXYZ, (bool, type(None))):
            raise TypeError
        # 元件坐标系，如果输入坐标不是元件坐标系就强转为元件坐标系
        if not (elementXYZ is True or (_elementXYZ.is_elementXYZ() is True and elementXYZ is None)):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)
        x, y, z = roundData(x, y, z)

        self.nor_gate = elements.Nor_Gate(x, y, z, True)
        self.nimp_gate1 = elements.Nimp_Gate(x + 1, y, z, True)
        self.nimp_gate2 = elements.Nimp_Gate(x + 1, y + 1, z, True)
        self.and_gate = elements.And_Gate(x, y + 1, z, True)
        self.nor_gate.i_up - self.nimp_gate1.i_low
        self.nimp_gate1.i_low - self.nimp_gate2.i_up
        self.nimp_gate2.i_up - self.and_gate.i_up
        self.nor_gate.i_low - self.nimp_gate1.i_up
        self.nimp_gate1.i_up - self.nimp_gate2.i_low
        self.nimp_gate2.i_low - self.and_gate.i_low

    @property
    def inputs(self) -> UnitPin:
        return UnitPin(
            self,
            self.nor_gate.i_low,
            self.and_gate.i_up,
        )

    @property
    def outputs(self) -> UnitPin:
        return UnitPin(
            self,
            self.nor_gate.o,
            self.nimp_gate1.o,
            self.nimp_gate2.o,
            self.and_gate.o,
        )

class Switched_Register:
    ''' 可以切换输入的寄存器
    '''
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None,  # x, y, z是否为元件坐标系
                 ) -> None:
        if not isinstance(x, (int, float)) or \
            not isinstance(y, (int, float)) or \
            not isinstance(z, (int, float)) or \
            not isinstance(elementXYZ, (bool, type(None))) or \
            not isinstance(bitnum, int) or bitnum <= 1:
            raise TypeError

        if not (elementXYZ is True or (_elementXYZ.is_elementXYZ() is True and elementXYZ is None)):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)
        x, y, z = roundData(x, y, z)
        self.bitnum = bitnum

        self.register = Register(x + 1, y, z, bitnum, elementXYZ=True, heading=False)
        self.switch_nogate = elements.No_Gate(x, y, z, True)
        self.switches = []
        for delta_y in range(bitnum):
            m = elements.Multiplier(x, y + delta_y * 2, z, True)
            m.o_lowmid - self.register.inputs[delta_y]
            m.i_up - self.switch_nogate.o
            m.i_lowmid - self.switch_nogate.i
            self.switches.append(m)

    @property
    def switch(self) -> Pin:
        return self.switch_nogate.i

    @property
    def clk(self) -> Pin:
        return self.register.clk

    @property
    def inputs1(self) -> UnitPin:
        return UnitPin(
            self,
            *[e.i_low for e in self.switches]
        )

    @property
    def inputs2(self) -> UnitPin:
        return UnitPin(
            self,
            *[e.i_upmid for e in self.switches]
        )

    @property
    def outputs(self):
        return self.register.outputs

class Equal_to:
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None,  # x, y, z是否为元件坐标系
                 ) -> None:
        if not isinstance(x, (int, float)) or \
            not isinstance(y, (int, float)) or \
            not isinstance(z, (int, float)) or \
            not isinstance(elementXYZ, (bool, type(None))) or \
            not isinstance(bitnum, int) or bitnum <= 1:
            raise TypeError

        if not (elementXYZ is True or (_elementXYZ.is_elementXYZ() is True and elementXYZ is None)):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)
        x, y, z = roundData(x, y, z)
        self.bitnum = bitnum

        self.xnorgates = []
        self.andgate = Super_AndGate(x, y, z, bitnum=bitnum, elementXYZ=True)
        for delta_y in range(bitnum):
            xnorgate = elements.Xnor_Gate(x, y + delta_y, z, True)
            self.andgate.inputs[delta_y] - xnorgate.o
            self.xnorgates.append(xnorgate)

    @property
    def inputs1(self) -> UnitPin:
        return UnitPin(self, *[e.i_low for e in self.xnorgates])

    @property
    def inputs2(self) -> UnitPin:
        return UnitPin(self, *[e.i_up for e in self.xnorgates])

    @property
    def output(self) -> Pin:
        return self.andgate.output

class Signed_Sum:
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None,  # x, y, z是否为元件坐标系
                 ) -> None:
        if not isinstance(x, (int, float)) or \
            not isinstance(y, (int, float)) or \
            not isinstance(z, (int, float)) or \
            not isinstance(elementXYZ, (bool, type(None))) or \
            not isinstance(bitnum, int) or bitnum <= 1:
            raise TypeError

        if not (elementXYZ is True or (_elementXYZ.is_elementXYZ() is True and elementXYZ is None)):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)
        x, y, z = roundData(x, y, z)
        self.bitnum = bitnum

        self._inputs = AU_SumSub(x, y, z, bitnum=bitnum, elementXYZ=True)
        self._outputs = AU_SumSub(x + 2, y, z, bitnum=bitnum, elementXYZ=True)
        self._inputs.outputs[:-1] - self._outputs.inputs2
        self.xorgate = elements.Xor_Gate(x, y + bitnum * 2, z, True)
        nimpgate = elements.Nimp_Gate(x + 1, y + bitnum * 2, z, True)
        self.xorgate2 = elements.Xor_Gate(x + 2, y + bitnum * 2, z, True)
        self.xorgate.o - self._inputs.switch
        nimpgate.o - self._outputs.switch
        self.xorgate.i_up - self.xorgate2.i_up
        self.xorgate.o - nimpgate.i_up
        nimpgate.i_low - self._inputs.outputs[-1]
        nimpgate.o - self.xorgate2.i_low

    @property
    def inputs1(self) -> UnitPin:
        return self._inputs.inputs1

    @property
    def inputs2(self) -> UnitPin:
        return self._inputs.inputs2

    @property
    def inputs1_sign(self) -> Pin:
        return self.xorgate.i_up

    @property
    def inputs2_sign(self) -> Pin:
        return self.xorgate.i_low

    @property
    def outputs(self) -> UnitPin:
        return self._outputs.outputs[0:-1]

    @property
    def outputs_sign(self) -> Pin:
        return self.xorgate2.o

class _Simple_Logic_Meta(type):
    def __call__(cls,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None,  # x, y, z是否为元件坐标系
                 heading: bool = False,  # False: 生成的元件为竖直方向，否则为横方向
                 fold: bool = False,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
                 foldMaxNum: int = 4,  # 达到foldMaxNum个元件数时即在z轴自动折叠
                 *args, **kwags
    ):
        self = cls.__new__(cls)
        if get_current_experiment().experiment_type != ExperimentType.Circuit:
            raise errors.ExperimentTypeError

        if foldMaxNum <= 0 or \
            not isinstance(x, (int, float)) or \
            not isinstance(y, (int, float)) or \
            not isinstance(z, (int, float)) or \
            not isinstance(elementXYZ, (bool, type(None))) or \
            not isinstance(heading, bool) or \
            not isinstance(fold, bool) or \
            not isinstance(foldMaxNum, int):
            raise TypeError
        if not isinstance(bitnum, int) or bitnum < 1:
            raise errors.BitnumError("bitnum must get a integer")
        self.bitnum = bitnum

        # 元件坐标系，如果输入坐标不是元件坐标系就强转为元件坐标系
        if not (elementXYZ is True or (_elementXYZ.is_elementXYZ() is True and elementXYZ is None)):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)
        x, y, z = roundData(x, y, z) # type: ignore -> result type: tuple

        self.__init__(x=x,
                      y=y,
                      z=z,
                      elementXYZ=elementXYZ,
                      bitnum=bitnum,
                      heading=heading,
                      fold=fold,
                      foldMaxNum=foldMaxNum,
                      *args, **kwags)
        assert hasattr(self, "_elements")

        return self

class _Base(metaclass=_Simple_Logic_Meta):
    def __getitem__(self, item: Union[int, slice]):
        if not isinstance(item, (int, slice)):
            raise TypeError

        return self._elements[item]

    def set_HighLevelValue(self, num: numType) -> Self:
        ''' 设置高电平的值 '''
        for element in self._elements:
            element.set_HighLeaveValue(num)
        return self

    def set_LowLevelValue(self, num: numType) -> Self:
        ''' 设置低电平的值 '''
        for element in self._elements:
            element.set_LowLeaveValue(num)
        return self

class Sum(_Base):
    ''' 模块化加法电路 '''
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None,  # x, y, z是否为元件坐标系
                 heading: bool = False,  # False: 生成的元件为竖直方向，否则为横方向
                 fold: bool = False,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
                 foldMaxNum: int = 4  # 达到foldMaxNum个元件数时即在z轴自动折叠
                 ) -> None:
        self._elements: list = []

        if heading:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._elements.append(elements.Full_Adder(x + i % foldMaxNum, y, zcor, True))
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._elements.append(elements.Full_Adder(x + increase, y, z, True))
        else:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._elements.append(
                        elements.Full_Adder(x, y + (i % foldMaxNum) * 2, zcor, True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._elements.append(elements.Full_Adder(x, y + increase * 2, z, True))

        # 连接导线
        for i in range(self._elements.__len__() - 1):
                self._elements[i].o_low - self._elements[i + 1].i_low

    @property
    def inputs1(self) -> UnitPin:
        ''' 加数1 '''
        return UnitPin(
            self,
            *(element.i_mid for element in self._elements)
        )

    @property
    def inputs2(self) -> UnitPin:
        ''' 加数2 '''
        return UnitPin(
            self,
            *(element.i_up for element in self._elements)
        )

    @property
    def outputs(self) -> UnitPin:
        ''' 加法的结果 '''
        return UnitPin(
            self,
            *(element.o_up for element in self._elements),
            self._elements[-1].o_low
        )

class Sub(_Base):
    ''' 模块化减法电路 '''
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int, # 减法器的最大计算比特数
                 elementXYZ: Optional[bool] = None,  # x, y, z是否为元件坐标系
                 heading: bool = False,  # False: 生成的元件为竖直方向，否则为横方向
                 fold: bool = False,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
                 foldMaxNum: int = 4  # 达到foldMaxNum个元件数时即在z轴自动折叠
                 ) -> None:
        self._elements: list = [Const_NoGate(x, y, z, True)]
        self._noGates: list = []
        self._fullAdders: list = []

        if heading:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + i % foldMaxNum, y - 2, zcor, True)
                    )
                    self._noGates.append(
                        elements.No_Gate(x + i % foldMaxNum, y, zcor, True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + increase, y - 2, z, True)
                    )
                    self._noGates.append(
                        elements.No_Gate(x + increase, y, z, True)
                    )
        else:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + 1, y + (i % foldMaxNum) * 2, zcor, True)
                    )
                    self._noGates.append(
                        elements.No_Gate(x, y + (i % foldMaxNum) * 2 + 1, zcor, True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + 1, y + increase * 2, z, True)
                    )
                    self._noGates.append(
                        elements.No_Gate(x, y + increase * 2 + 1, z, True)
                    )

        # 连接导线
        self._elements[0].o - self._fullAdders[0].i_low
        for i in range(self._fullAdders.__len__() - 1):
            self._fullAdders[i].o_low - self._fullAdders[i + 1].i_low
            self._noGates[i].o - self._fullAdders[i].i_mid
        self._noGates[-1].o - self._fullAdders[-1].i_mid

        self._elements.extend(self._fullAdders + self._noGates)

    @property
    def minuend(self) -> UnitPin:
        ''' 被减数 '''
        return UnitPin(
            self,
            *(e.i_up for e in self._fullAdders)
        )

    # 减数
    @property
    def subtrahend(self):
        ''' 减数 '''
        return UnitPin(
            self,
            *(e.i for e in self._noGates)
        )

    @property
    def outputs(self):
        ''' 减法的结果 '''
        return UnitPin(
            self,
            *(e.o_up for e in self._fullAdders),
            self._fullAdders[-1].o_low
        )

class AU_SumSub(_Base):
    ''' 无符号加减器 '''
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None,  # x, y, z是否为元件坐标系
                 heading: bool = False,  # False: 生成的元件为竖直方向，否则为横方向
                 fold: bool = False,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
                 foldMaxNum: int = 4  # 达到foldMaxNum个元件数时即在z轴自动折叠
                 ) -> None:
        self._elements: list = []
        self._xorgates: List[elements.Xor_Gate] = []
        self._fullAdders: List[elements.Full_Adder] = []

        if heading:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + i % foldMaxNum, y - 2, zcor, True)
                    )
                    self._xorgates.append(
                        elements.Xor_Gate(x + i % foldMaxNum, y, zcor, True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + increase, y - 2, z, True)
                    )
                    self._xorgates.append(
                        elements.Xor_Gate(x + increase, y, z, True)
                    )
        else:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + 1, y + (i % foldMaxNum) * 2, zcor, True)
                    )
                    self._xorgates.append(
                        elements.Xor_Gate(x, y + (i % foldMaxNum) * 2 + 1, zcor, True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + 1, y + increase * 2, z, True)
                    )
                    self._xorgates.append(
                        elements.Xor_Gate(x, y + increase * 2 + 1, z, True)
                    )

        # 连接导线
        for i in range(self._fullAdders.__len__() - 1):
            self._fullAdders[i].o_low - self._fullAdders[i + 1].i_low
            self._xorgates[i].o - self._fullAdders[i].i_mid
            self._xorgates[i].i_low - self._xorgates[i + 1].i_low
        self._xorgates[-1].o - self._fullAdders[-1].i_mid
        self._xorgates[0].i_low - self._fullAdders[0].i_low

        self._elements.extend(self._fullAdders + self._xorgates)

    @property
    def inputs1(self) -> UnitPin:
        ''' 加数1 or 被减数 '''
        return UnitPin(
            self,
            *(e.i_up for e in self._fullAdders)
        )

    @property
    def inputs2(self) -> UnitPin:
        ''' 加数2 or 减数 '''
        return UnitPin(
            self,
            *(e.i_up for e in self._xorgates)
        )

    @property
    def outputs(self) -> UnitPin:
        ''' 加法器的结果 '''
        return UnitPin(
            self,
            *(e.o_up for e in self._fullAdders),
            self._fullAdders[-1].o_low
        )

    @property
    def switch(self) -> Pin:
        ''' 切换加法与减法 '''
        return self._xorgates[0].i_low

class D_WaterLamp(_Base):
    ''' D触发器流水灯 '''
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None, # x, y, z是否为元件坐标系
                 heading: bool = False, # False: 生成的元件为竖直方向，否则为横方向
                 fold: bool = False, # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
                 foldMaxNum: int = 4, # 达到foldMaxNum个元件数时即在z轴自动折叠
                 is_loop: bool = True # 是否使流水灯循环
                 ) -> None:
        if bitnum < 2:
            raise errors.BitnumError

        if not isinstance(is_loop, bool):
            raise TypeError

        self.is_bitlen_equal_to_2: bool = False
        if bitnum == 2:
            self.is_bitlen_equal_to_2 = True
            self._elements = [elements.T_Flipflop(x, y, z, True)]
            return

        self._elements: list = []

        if heading:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x + i % foldMaxNum, y, zcor, True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x + increase, y, z, True)
                    )
        else:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x, y + (i % foldMaxNum) * 2, zcor, True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x, y + increase * 2, z, True)
                    )

        # 连接clk
        for i in range(len(self._elements) - 1):
            self._elements[i].i_low - self._elements[i + 1].i_low
        # 连接数据传输导线
        self._elements[0].o_low - self._elements[1].i_up
        for i in range(1, len(self._elements) - 1):
            self._elements[i].o_up - self._elements[i + 1].i_up
        # 流水灯循环导线
        if is_loop:
            self._elements[-1].o_low - self._elements[0].i_up
        else:
            firstElement = self._elements[0]
            orGate = elements.Or_Gate(*firstElement.get_Position(), True)
            orGate.i_up - orGate.o
            orGate.o - firstElement.i_up
            orGate.i_low - firstElement.i_low

    @property
    def inputs(self) -> UnitPin:
        return UnitPin(
            self,
            self._elements[0].i_low
        )

    @property
    def outputs(self) -> UnitPin:
        if not self.is_bitlen_equal_to_2:
            return UnitPin(
                self,
                self._elements[0].o_low,
                *(element.o_up for element in self._elements[1:])
            )
        else:
            return UnitPin(
                self,
                self._elements[0].o_up,
                self._elements[0].o_low
            )

    # 与data_Output相反的引脚
    @property
    def neg_outputs(self) -> UnitPin:
        return UnitPin(
            self,
            self._elements[0].o_up,
            *(element.o_low for element in self._elements[1:])
        )

class Register(_Base):
    ''' 寄存器 '''
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None, # x, y, z是否为元件坐标系
                 heading: bool = False, # False: 生成的元件为竖直方向，否则为横方向
                 fold: bool = False, # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
                 foldMaxNum: int = 4, # 达到foldMaxNum个元件数时即在z轴自动折叠
                 ) -> None:
        self._elements: list = []

        if heading:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x + i % foldMaxNum, y, zcor, True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x + increase, y, z, True)
                    )
        else:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x, y + (i % foldMaxNum) * 2, zcor, True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x, y + increase * 2, z, True)
                    )

        last_element = None
        for element in self._elements:
            if last_element is not None:
                element.i_low - last_element.i_low
            last_element = element

    @property
    def clk(self) -> Pin:
        return self._elements[0].i_low

    @property
    def inputs(self) -> UnitPin:
        return UnitPin(
            self,
            *(element.i_up for element in self._elements)
        )

    @property
    def outputs(self) -> UnitPin:
        return UnitPin(
            self,
            *(element.o_up for element in self._elements)
        )

    @property
    def neg_outputs(self) -> UnitPin:
        return UnitPin(
            self,
            *(element.o_low for element in self._elements)
        )

class MultiElements(_Base):
    ''' 创建多个元件 '''
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None,  # x, y, z是否为元件坐标系
                 heading: bool = False,  # False: 生成的元件为竖直方向，否则为横方向
                 fold: bool = False,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
                 foldMaxNum: int = 8,  # 达到foldMaxNum个元件数时即在z轴自动折叠
                 element: Optional[Type[elements.CircuitBase]] = None,  # 元件类型
                 ) -> None:
        if element is None or not issubclass(element, elements.CircuitBase):
            raise TypeError

        self._elements: list = []
        if heading:
            if fold:
                zcor = z
                for i in range(bitnum):
                    if element.is_bigElement:
                        plus = 2 * i % foldMaxNum
                    else:
                        plus = i % foldMaxNum
                    self._elements.append(
                        element(x + plus, y, zcor, True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for i in range(bitnum):
                    if element.is_bigElement:
                        plus = 2 * i
                    else:
                        plus = i
                    self._elements.append(
                        element(x + i, y, z, True)
                    )
        else:
            if fold:
                zcor = z
                for i in range(bitnum):
                    if element.is_bigElement:
                        plus = 2 * i % foldMaxNum
                    else:
                        plus = i % foldMaxNum
                    self._elements.append(
                        element(x, y + plus, zcor, True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for i in range(bitnum):
                    if element.is_bigElement:
                        plus = 2 * i
                    else:
                        plus = i
                    self._elements.append(
                        element(x, y + plus, z, True)
                    )

    def pins(self, pin: Pin) -> UnitPin:
        if not isinstance(pin, Pin):
            raise TypeError

        res = []
        for e in self._elements:
            for p_name in e._get_property():
                p = eval(f"e.{p_name}")
                if isinstance(p, Pin) and p.pinLabel == pin.pinLabel:
                    res.append(p)
        return UnitPin(self, *res)

class Outputs(MultiElements):
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None,  # x, y, z是否为元件坐标系
                 heading: bool = False,  # False: 生成的元件为竖直方向，否则为横方向
                 fold: bool = False,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
                 foldMaxNum: int = 8,  # 达到foldMaxNum个元件数时即在z轴自动折叠
                ) -> None:
        super().__init__(x=x,
                         y=y,
                         z=z,
                         bitnum=bitnum,
                         elementXYZ=elementXYZ,
                         heading=heading,
                         fold=fold,
                         foldMaxNum=foldMaxNum,
                         element=elements.Logic_Output)

    @property
    def inputs(self) -> UnitPin:
        return UnitPin(
            self,
            *(element.i for element in self._elements)
        )

class Inputs(MultiElements):
    def __init__(self,
                 x: numType,
                 y: numType,
                 z: numType,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None,  # x, y, z是否为元件坐标系
                 heading: bool = False,  # False: 生成的元件为竖直方向，否则为横方向
                 fold: bool = False,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
                 foldMaxNum: int = 8,  # 达到foldMaxNum个元件数时即在z轴自动折叠
                 ) -> None:
        super().__init__(x, y, z, bitnum, elementXYZ, heading, fold, foldMaxNum, elements.Logic_Input)

    @property
    def outputs(self) -> UnitPin:
        return UnitPin(
            self,
            *(element.o for element in self._elements)
        )
