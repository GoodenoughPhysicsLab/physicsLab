# -*- coding: utf-8 -*-
import physicsLab.errors as errors

from .super_logic_gate import Const_NoGate, Super_AndGate
from .wires import UnitPin, crt_wires
from physicsLab._tools import round_data
from physicsLab.circuit import elements
from physicsLab.circuit._circuit_core import Pin, OutputPin
from physicsLab._core import get_current_experiment, native_to_elementXYZ
from physicsLab.enums import ExperimentType
from physicsLab._typing import num_type, Optional, Self, Union, Type, List

class TwoFour_Decoder:
    ''' 2-4译码器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
    ) -> None:
        if not isinstance(x, (int, float)) \
                or not isinstance(y, (int, float)) \
                or not isinstance(z, (int, float)) \
                or not isinstance(elementXYZ, (bool, type(None))):
            raise TypeError
        # 元件坐标系，如果输入坐标不是元件坐标系就强转为元件坐标系
        if elementXYZ is not True and not (get_current_experiment().is_elementXYZ is True and elementXYZ is None):
            x, y, z = native_to_elementXYZ(x, y, z)
        x, y, z = round_data(x), round_data(y), round_data(z)

        self.nor_gate = elements.Nor_Gate(x, y, z, elementXYZ=True)
        self.nimp_gate1 = elements.Nimp_Gate(x + 1, y, z, elementXYZ=True)
        self.nimp_gate2 = elements.Nimp_Gate(x + 1, y + 1, z, elementXYZ=True)
        self.and_gate = elements.And_Gate(x, y + 1, z, elementXYZ=True)
        crt_wires(self.nor_gate.i_up, self.nimp_gate1.i_low)
        crt_wires(self.nimp_gate1.i_low, self.nimp_gate2.i_up)
        crt_wires(self.nimp_gate2.i_up, self.and_gate.i_up)
        crt_wires(self.nor_gate.i_low, self.nimp_gate1.i_up)
        crt_wires(self.nimp_gate1.i_up, self.nimp_gate2.i_low)
        crt_wires(self.nimp_gate2.i_low, self.and_gate.i_low)

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

class Decoder:
    ''' 任意bit译码器 '''
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

        # 元件坐标系，如果输入坐标不是元件坐标系就强转为元件坐标系
        if elementXYZ is not True and not (get_current_experiment().is_elementXYZ is True and elementXYZ is None):
            x, y, z = native_to_elementXYZ(x, y, z)
        x, y, z = round_data(x), round_data(y), round_data(z)

        self.bitnum = bitnum
        if bitnum==1:
            m=elements.No_Gate(x,y,z,elementXYZ=True)
            self._inputs=[m.i]
            self._outputs=[m.i,m.o]
            return
        self._inputs = []
        self._outputs = []
        div_num,mod_num=divmod(bitnum,2)
        if mod_num==0:
            And_Gates=[[elements.And_Gate(x,y,z,elementXYZ=True) for a in range(2**div_num)] for b in range(2**div_num)]
            l1=Decoder(x,y,z,bitnum=div_num,elementXYZ=True)
            l2=Decoder(x,y,z,bitnum=div_num,elementXYZ=True)
            self._inputs=l1._inputs+l2._inputs
            for a in range(2**div_num):
                for b in range(2**div_num):
                    crt_wires(l1._outputs[a],And_Gates[a][b].i_low)
                    crt_wires(l2._outputs[b],And_Gates[a][b].i_up)
            self._outputs=[and_gate.o for and_gates in And_Gates for and_gate in and_gates] # Expand 2D list
        elif mod_num==1:
            And_Gates=[[elements.And_Gate(x,y,z,elementXYZ=True) for b in range(2**(div_num+1))] for a in range(2**div_num)]
            l1=Decoder(x,y,z,bitnum=div_num,elementXYZ=True)
            l2=Decoder(x,y,z,bitnum=div_num+1,elementXYZ=True)
            self._inputs=l1._inputs+l2._inputs
            for a in range(2**div_num):
                for b in range(2**(div_num+1)):
                    crt_wires(l1._outputs[a],And_Gates[a][b].i_low)
                    crt_wires(l2._outputs[b],And_Gates[a][b].i_up)
            self._outputs=[and_gate.o for and_gates in And_Gates for and_gate in and_gates] # Expand 2D list
        else:
            errors.unreachable()
    @property
    def inputs(self) -> UnitPin:
        return UnitPin(self, *self._inputs)

    @property
    def outputs(self) -> Pin:
        return self._outputs

class Switched_Register:
    ''' 可以在两列输入中切换的寄存器
    '''
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

        self.register = Register(x + 1, y, z, bitnum, elementXYZ=True, heading=False)
        self.switch_nogate = elements.No_Gate(x, y, z, elementXYZ=True)
        self.switches = []
        for delta_y in range(bitnum):
            m = elements.Multiplier(x, y + delta_y * 2, z, elementXYZ=True)
            crt_wires(m.o_lowmid, self.register.inputs[delta_y])
            crt_wires(m.i_up, self.switch_nogate.o)
            crt_wires(m.i_lowmid, self.switch_nogate.i)
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

class EqualTo:
    ''' 判断两个输入是否相等 (无需clk)
    '''
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

        self.xnorgates = []
        self.andgate = Super_AndGate(x, y, z, bitnum=bitnum, elementXYZ=True)
        for delta_y in range(bitnum):
            xnorgate = elements.Xnor_Gate(x, y + delta_y, z, elementXYZ=True)
            crt_wires(self.andgate.inputs[delta_y], xnorgate.o)
            self.xnorgates.append(xnorgate)

    @property
    def inputs1(self) -> UnitPin:
        return UnitPin(self, *[e.i_low for e in self.xnorgates])

    @property
    def inputs2(self) -> UnitPin:
        return UnitPin(self, *[e.i_up for e in self.xnorgates])

    @property
    def output(self) -> OutputPin:
        return self.andgate.output

class Signed_Sum:
    ''' 有符号数加法 (如果加法结果溢出则舍弃溢出值)
    '''
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

        self._inputs = AU_SumSub(x, y, z, bitnum=bitnum, elementXYZ=True)
        self._outputs = AU_SumSub(x + 2, y, z, bitnum=bitnum, elementXYZ=True)
        crt_wires(self._inputs.outputs[:-1], self._outputs.inputs2)
        self.xorgate = elements.Xor_Gate(x, y + bitnum * 2, z, elementXYZ=True)
        nimpgate = elements.Nimp_Gate(x + 1, y + bitnum * 2, z, elementXYZ=True)
        self.xorgate2 = elements.Xor_Gate(x + 2, y + bitnum * 2, z, elementXYZ=True)
        crt_wires(self.xorgate.o, self._inputs.switch)
        crt_wires(nimpgate.o, self._outputs.switch)
        crt_wires(self.xorgate.i_up, self.xorgate2.i_up)
        crt_wires(self.xorgate.o, nimpgate.i_up)
        crt_wires(nimpgate.i_low, self._inputs.outputs[-1])
        crt_wires(nimpgate.o, self.xorgate2.i_low)

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
                 x: num_type,
                 y: num_type,
                 z: num_type,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None,  # x, y, z是否为元件坐标系
                 heading: bool = False,  # False: 生成的元件为竖直方向，否则为横方向
                 fold: bool = False,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
                 foldMaxNum: int = 4,  # 达到foldMaxNum个元件数时即在z轴自动折叠
                 *args, **kwags
    ):
        self = cls.__new__(cls)
        _Expe = get_current_experiment()
        if _Expe.experiment_type != ExperimentType.Circuit:
            raise errors.ExperimentTypeError

        if not isinstance(x, (int, float)) \
                or not isinstance(y, (int, float)) \
                or not isinstance(z, (int, float)) \
                or not isinstance(elementXYZ, (bool, type(None))) \
                or not isinstance(heading, bool) \
                or not isinstance(fold, bool) \
                or not isinstance(foldMaxNum, int) \
                or not isinstance(bitnum, int):
            raise TypeError
        if foldMaxNum <= 0 or bitnum < 1:
            raise ValueError
        self.bitnum = bitnum

        # 元件坐标系，如果输入坐标不是元件坐标系就强转为元件坐标系
        if elementXYZ is not True and not (get_current_experiment().is_elementXYZ is True and elementXYZ is None):
            x, y, z = native_to_elementXYZ(x, y, z)
        x, y, z = round_data(x), round_data(y), round_data(z)

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

    def set_HighLevelValue(self, num: num_type) -> Self:
        ''' 设置高电平的值 '''
        for element in self._elements:
            element.set_HighLeaveValue(num)
        return self

    def set_LowLevelValue(self, num: num_type) -> Self:
        ''' 设置低电平的值 '''
        for element in self._elements:
            element.set_LowLeaveValue(num)
        return self

class Sum(_Base):
    ''' 模块化加法电路 '''
    def __init__(self,
                 x: num_type,
                 y: num_type,
                 z: num_type,
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
                    self._elements.append(elements.Full_Adder(x + i % foldMaxNum, y, zcor, elementXYZ=True))
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._elements.append(elements.Full_Adder(x + increase, y, z, elementXYZ=True))
        else:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._elements.append(
                        elements.Full_Adder(x, y + (i % foldMaxNum) * 2, zcor, elementXYZ=True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._elements.append(elements.Full_Adder(x, y + increase * 2, z, elementXYZ=True))

        # 连接导线
        for i in range(self._elements.__len__() - 1):
                crt_wires(self._elements[i].o_low, self._elements[i + 1].i_low)

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
    # TODO 使用物实2.5.0新增全减器与半减器
    def __init__(self,
                 x: num_type,
                 y: num_type,
                 z: num_type,
                 bitnum: int, # 减法器的最大计算比特数
                 elementXYZ: Optional[bool] = None,  # x, y, z是否为元件坐标系
                 heading: bool = False,  # False: 生成的元件为竖直方向，否则为横方向
                 fold: bool = False,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
                 foldMaxNum: int = 4  # 达到foldMaxNum个元件数时即在z轴自动折叠
                 ) -> None:
        self._elements: list = [Const_NoGate(x, y, z, elementXYZ=True)]
        self._noGates: list = []
        self._fullAdders: list = []

        if heading:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + i % foldMaxNum, y - 2, zcor, elementXYZ=True)
                    )
                    self._noGates.append(
                        elements.No_Gate(x + i % foldMaxNum, y, zcor, elementXYZ=True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + increase, y - 2, z, elementXYZ=True)
                    )
                    self._noGates.append(
                        elements.No_Gate(x + increase, y, z, elementXYZ=True)
                    )
        else:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + 1, y + (i % foldMaxNum) * 2, zcor, elementXYZ=True)
                    )
                    self._noGates.append(
                        elements.No_Gate(x, y + (i % foldMaxNum) * 2 + 1, zcor, elementXYZ=True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + 1, y + increase * 2, z, elementXYZ=True)
                    )
                    self._noGates.append(
                        elements.No_Gate(x, y + increase * 2 + 1, z, elementXYZ=True)
                    )

        crt_wires(self._elements[0].o, self._fullAdders[0].i_low)
        for i in range(self._fullAdders.__len__() - 1):
            crt_wires(self._fullAdders[i].o_low, self._fullAdders[i + 1].i_low)
            crt_wires(self._noGates[i].o, self._fullAdders[i].i_mid)
        crt_wires(self._noGates[-1].o, self._fullAdders[-1].i_mid)

        self._elements.extend(self._fullAdders + self._noGates)

    @property
    def minuend(self) -> UnitPin:
        ''' 被减数 '''
        return UnitPin(
            self,
            *(e.i_up for e in self._fullAdders)
        )

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
                 x: num_type,
                 y: num_type,
                 z: num_type,
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
                        elements.Full_Adder(x + i % foldMaxNum, y - 2, zcor, elementXYZ=True)
                    )
                    self._xorgates.append(
                        elements.Xor_Gate(x + i % foldMaxNum, y, zcor, elementXYZ=True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + increase, y - 2, z, elementXYZ=True)
                    )
                    self._xorgates.append(
                        elements.Xor_Gate(x + increase, y, z, elementXYZ=True)
                    )
        else:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + 1, y + (i % foldMaxNum) * 2, zcor, elementXYZ=True)
                    )
                    self._xorgates.append(
                        elements.Xor_Gate(x, y + (i % foldMaxNum) * 2 + 1, zcor, elementXYZ=True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._fullAdders.append(
                        elements.Full_Adder(x + 1, y + increase * 2, z, elementXYZ=True)
                    )
                    self._xorgates.append(
                        elements.Xor_Gate(x, y + increase * 2 + 1, z, elementXYZ=True)
                    )

        # 连接导线
        for i in range(self._fullAdders.__len__() - 1):
            crt_wires(self._fullAdders[i].o_low, self._fullAdders[i + 1].i_low)
            crt_wires(self._xorgates[i].o, self._fullAdders[i].i_mid)
            crt_wires(self._xorgates[i].i_low, self._xorgates[i + 1].i_low)
        crt_wires(self._xorgates[-1].o, self._fullAdders[-1].i_mid)
        crt_wires(self._xorgates[0].i_low, self._fullAdders[0].i_low)

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
                 x: num_type,
                 y: num_type,
                 z: num_type,
                 bitnum: int,
                 elementXYZ: Optional[bool] = None, # x, y, z是否为元件坐标系
                 heading: bool = False, # False: 生成的元件为竖直方向，否则为横方向
                 fold: bool = False, # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
                 foldMaxNum: int = 4, # 达到foldMaxNum个元件数时即在z轴自动折叠
                 is_loop: bool = True # 是否使流水灯循环
                 ) -> None:
        if bitnum < 2:
            raise ValueError

        if not isinstance(is_loop, bool):
            raise TypeError

        self.is_bitlen_equal_to_2: bool = False
        if bitnum == 2:
            self.is_bitlen_equal_to_2 = True
            self._elements = [elements.T_Flipflop(x, y, z, elementXYZ=True)]
            return

        self._elements: list = []

        if heading:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x + i % foldMaxNum, y, zcor, elementXYZ=True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x + increase, y, z, elementXYZ=True)
                    )
        else:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x, y + (i % foldMaxNum) * 2, zcor, elementXYZ=True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x, y + increase * 2, z, elementXYZ=True)
                    )

        # 连接clk
        for i in range(len(self._elements) - 1):
            crt_wires(self._elements[i].i_low, self._elements[i + 1].i_low)
        # 连接数据传输导线
        crt_wires(self._elements[0].o_low, self._elements[1].i_up)
        for i in range(1, len(self._elements) - 1):
            crt_wires(self._elements[i].o_up, self._elements[i + 1].i_up)
        # 流水灯循环导线
        if is_loop:
            crt_wires(self._elements[-1].o_low, self._elements[0].i_up)
        else:
            firstElement = self._elements[0]
            orGate = elements.Or_Gate(*firstElement.get_Position(), elementXYZ=True)
            crt_wires(orGate.i_up, orGate.o)
            crt_wires(orGate.o, firstElement.i_up)
            crt_wires(orGate.i_low, firstElement.i_low)

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
                 x: num_type,
                 y: num_type,
                 z: num_type,
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
                        elements.D_Flipflop(x + i % foldMaxNum, y, zcor, elementXYZ=True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x + increase, y, z, elementXYZ=True)
                    )
        else:
            if fold:
                zcor = z
                for i in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x, y + (i % foldMaxNum) * 2, zcor, elementXYZ=True)
                    )
                    if i == foldMaxNum - 1:
                        zcor += 1
            else:
                for increase in range(bitnum):
                    self._elements.append(
                        elements.D_Flipflop(x, y + increase * 2, z, elementXYZ=True)
                    )

        last_element = None
        for element in self._elements:
            if last_element is not None:
                crt_wires(element.i_low, last_element.i_low)
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
                 x: num_type,
                 y: num_type,
                 z: num_type,
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
                        element(x + plus, y, zcor, elementXYZ=True)
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
                        element(x + i, y, z, elementXYZ=True)
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
                        element(x, y + plus, zcor, elementXYZ=True)
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
                        element(x, y + plus, z, elementXYZ=True)
                    )

    def pins(self, pin: Pin) -> UnitPin:
        if not isinstance(pin, Pin):
            raise TypeError

        res = []
        for e in self._elements:
            for p_name in e._get_property():
                p = eval(f"e.{p_name}")
                if isinstance(p, Pin) and p._pin_label == pin._pin_label:
                    res.append(p)
        return UnitPin(self, *res)

class Outputs(MultiElements):
    def __init__(self,
                 x: num_type,
                 y: num_type,
                 z: num_type,
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
                 x: num_type,
                 y: num_type,
                 z: num_type,
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
