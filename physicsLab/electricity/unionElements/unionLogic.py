#coding=utf-8
# 模块化电路
import typing as _typing
from physicsLab._tools import numType
import physicsLab.errors as _errors
import physicsLab.electricity as electricity
import physicsLab.electricity.elementsClass as _elementsClass
from physicsLab.electricity.unionElements.unionPin import union_Pin
import physicsLab.electricity.unionElements._unionClassHead as _unionClassHead

# unionHeading与fold的判断的代码
def _unionHeading_fold(
        func1: _typing.Callable,
        func2: _typing.Callable,
        func3: _typing.Callable,
        func4: _typing.Callable,
        unionHeading: bool,
        fold: bool
):
    if unionHeading: # 生成元件为横方向
        if fold: # z轴折叠
            func1()
        else:
            func2()
    else: # 竖方向
        if fold:
            func3()
        else:
            func4()

# 用metaClass检查是否有self._elements
class _union_LogicMeta(type):
    pass

# 模块化电路逻辑电路基类
class Union_LogicBase(_unionClassHead.UnionBase):
    # 设置高电平的值
    def set_HighLeaveValue(self, num: numType) -> "Union_LogicBase":
        for element in self._elements:
            element.set_HighLeaveValue(num)
        return self

    def set_LowLeaveValue(self, num: numType) -> "Union_LogicBase":
        for element in self._elements:
            element.set_LowLeaveValue(num)
        return self

# 任意引脚加法电路
class Sum(Union_LogicBase):
    def __init__(
            self,
            bitLength: int,
            x: numType = 0,
            y: numType = 0,
            z: numType = 0,
            elementXYZ: bool = None,  # x, y, z是否为元件坐标系
            unionHeading: bool = False,  # False: 生成的元件为竖直方向，否则为横方向
            fold: bool = False,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
            foldMaxNum: int = 4  # 达到foldMaxNum个元件数时即在z轴自动折叠
    ) -> None:
        def link_union_Sum(elements: _typing.List[_elementsClass.Full_Adder]) -> None:
            for i in range(elements.__len__() - 1):
                elements[i].o_low - elements[i + 1].i_low

        def func1():
            zcor = z
            for i in range(bitLength):
                self._elements.append(
                    electricity.Full_Adder(x + i % foldMaxNum, y, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func2():
            for increase in range(bitLength):
                self._elements.append(
                    electricity.Full_Adder(x + increase, y, z, True)
                )

        def func3():
            zcor = z
            for i in range(bitLength):
                self._elements.append(
                    electricity.Full_Adder(x, y + (i % foldMaxNum) * 2, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func4():
            for increase in range(bitLength):
                self._elements.append(
                    electricity.Full_Adder(x, y + increase * 2, z, True)
                )

        # main
        # if bitLength < 2:
        #     raise errors.bitLengthError

        x, y, z = _unionClassHead.union_Init_HEAD(
            x, y, z,
            bitLength,
            elementXYZ,
            unionHeading,
            fold,
            foldMaxNum
        )

        self._elements: _typing.List[_elementsClass.Full_Adder] = []
        _unionHeading_fold(
            func1, func2, func3, func4, unionHeading, fold
        )
        link_union_Sum(self._elements)

    @property
    def data_Input1(self) -> union_Pin:
        return union_Pin(
            self,
            *(element.i_mid for element in self._elements)
        )

    @property
    def data_Input2(self) -> union_Pin:
        return union_Pin(
            self,
            *(element.i_up for element in self._elements)
        )

    @property
    def data_Output(self) -> union_Pin:
        return union_Pin(
            self,
            *(element.o_up for element in self._elements),
            self._elements[-1].o_low
        )

# 只读非门，若没有则创建一个只读非门，若已存在则不会创建新的元件
class Const_NoGate:
    __singleton_NoGate: electricity.No_Gate = None
    def __init__(self,
                x: numType = 0,
                y: numType = 0,
                z: numType = 0,
                elementXYZ: bool = None
    ):
        if Const_NoGate.__singleton_NoGate is None:
            Const_NoGate.__singleton_NoGate = electricity.No_Gate(x, y, z, elementXYZ)

    @property
    def o(self):
        return Const_NoGate.__singleton_NoGate.o

# 任意引脚减法电路
class Sub(Union_LogicBase):
    def __init__(
            self,
            bitLength: int, # 减法器的最大计算比特数
            x: numType = 0,
            y: numType = 0,
            z: numType = 0,
            elementXYZ: bool = None,  # x, y, z是否为元件坐标系
            unionHeading: bool = False,  # False: 生成的元件为竖直方向，否则为横方向
            fold: bool = False,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
            foldMaxNum: int = 4  # 达到foldMaxNum个元件数时即在z轴自动折叠
    ) -> None:
        def link_union_Sub(
                fullAdders: _typing.List[_elementsClass.Full_Adder],
                noGates: _typing.List[_elementsClass.No_Gate]
        ) -> None:
            self._elements[0].o - fullAdders[0].i_low
            for i in range(fullAdders.__len__() - 1):
                fullAdders[i].o_low - fullAdders[i + 1].i_low
                noGates[i].o - fullAdders[i].i_mid
            noGates[-1].o - fullAdders[-1].i_mid

        def func1():
            zcor = z
            for i in range(bitLength):
                self._fullAdders.append(
                    electricity.Full_Adder(x + i % foldMaxNum, y - 2, zcor, True)
                )
                self._noGates.append(
                    electricity.No_Gate(x + i % foldMaxNum, y, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func2():
            for increase in range(bitLength):
                self._fullAdders.append(
                    electricity.Full_Adder(x + increase, y - 2, z, True)
                )
                self._noGates.append(
                    electricity.No_Gate(x + increase, y, z, True)
                )

        def func3():
            zcor = z
            for i in range(bitLength):
                self._fullAdders.append(
                    electricity.Full_Adder(x + 1, y + (i % foldMaxNum) * 2, zcor, True)
                )
                self._noGates.append(
                    electricity.No_Gate(x, y + (i % foldMaxNum) * 2 + 1, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func4():
            for increase in range(bitLength):
                self._fullAdders.append(
                    electricity.Full_Adder(x + 1, y + increase * 2, z, True)
                )
                self._noGates.append(
                    electricity.No_Gate(x, y + increase * 2 + 1, z, True)
                )

        x, y, z = _unionClassHead.union_Init_HEAD(
            x, y, z,
            bitLength,
            elementXYZ,
            unionHeading,
            fold,
            foldMaxNum
        )

        self._elements: _typing.List[_typing.Union[_elementsClass.Full_Adder, _elementsClass.No_Gate]] = [
            Const_NoGate(x, y, z, True)
        ]

        self._noGates: _typing.List[_elementsClass.No_Gate] = []
        self._fullAdders: _typing.List[_elementsClass.Full_Adder] = []

        _unionHeading_fold(
            func1, func2, func3, func4, unionHeading, fold
        )
        link_union_Sub(self._fullAdders, self._noGates)
        self._elements.extend(self._fullAdders + self._noGates)

    # 被减数
    @property
    def minuend(self) -> union_Pin:
        return union_Pin(
            self,
            *(e.i_up for e in self._fullAdders)
        )

    # 减数
    @property
    def subtrahend(self):
        return union_Pin(
            self,
            *(e.i for e in self._noGates)
        )

    @property
    def outputs(self):
        return union_Pin(
            self,
            *(e.o_up for e in self._fullAdders),
            self._fullAdders[-1].o_low
        )

# 2-4译码器
class _two_four_Decoder:
    def __init__(self, x : numType = 0, y : numType = 0, z : numType = 0):
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
            raise RuntimeError('illegal argument')
        self.x = x
        self.y = y
        self.z = z
        obj1 = electricity.Nor_Gate(x, y, z)
        obj2 = electricity.Nimp_Gate(x, y + 0.1, z)
        obj3 = electricity.Nimp_Gate(x, y + 0.2, z)
        obj4 = electricity.And_Gate(x, y + 0.3, z)
        electricity.crt_Wire(obj1.i_up, obj2.i_low), electricity.crt_Wire(obj2.i_low, obj3.i_up), electricity.crt_Wire(obj3.i_up, obj4.i_up)
        electricity.crt_Wire(obj1.i_low, obj2.i_up), electricity.crt_Wire(obj2.i_up, obj3.i_low), electricity.crt_Wire(obj3.i_low, obj4.i_low)

    @property
    def i_up(self):
        return electricity.element_Pin(electricity.get_Element(self.x, self.y + 0.3, self.z), 0)

    @property
    def i_low(self):
        return electricity.element_Pin(electricity.get_Element(self.x, self.y + 0.3, self.z), 1)

# 4-16译码器
class _four_sixteen_Decoder:
    def __init__(self, x : numType = 0, y : numType = 0, z : numType = 0):
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
            raise RuntimeError('illegal argument')
        self.x = x
        self.y = y
        self.z = z
        obj1 = electricity.Nor_Gate(x, y, z); obj2 = electricity.Nimp_Gate(x, y + 0.1, z)
        obj3 = electricity.Nimp_Gate(x, y + 0.2, z); obj4 = electricity.And_Gate(x, y + 0.3, z)
        obj5 = electricity.Nor_Gate(x + 0.15, y, z); obj6 = electricity.Nimp_Gate(x + 0.15, y + 0.1, z)
        obj7 = electricity.Nimp_Gate(x + 0.15, y + 0.2, z); obj8 = electricity.And_Gate(x + 0.15, y + 0.3, z)
        electricity.crt_Wire(obj1.i_up, obj2.i_low), electricity.crt_Wire(obj2.i_low, obj3.i_up), electricity.crt_Wire(obj3.i_up, obj4.i_up)
        electricity.crt_Wire(obj5.i_up, obj6.i_low), electricity.crt_Wire(obj6.i_low, obj7.i_up), electricity.crt_Wire(obj7.i_up, obj8.i_up)
        electricity.crt_Wire(obj1.i_low, obj2.i_up), electricity.crt_Wire(obj2.i_up, obj3.i_low), electricity.crt_Wire(obj3.i_low, obj4.i_low)
        electricity.crt_Wire(obj5.i_low, obj6.i_up), electricity.crt_Wire(obj6.i_up, obj7.i_low), electricity.crt_Wire(obj7.i_low, obj8.i_low)
        for i in [0.3, 0.45, 0.6, 0.75]:
            for j in [0.05, 0.25]:
                obj = electricity.Multiplier(x + i, y + j, z)
                if j == 0.05:
                    electricity.crt_Wire(obj1.o, obj.i_low)
                    electricity.crt_Wire(obj2.o, obj.i_up)
                else:
                    electricity.crt_Wire(obj3.o, obj.i_low)
                    electricity.crt_Wire(obj4.o, obj.i_up)
                eval(f'crt_Wire(obj{round((i - 0.3) / 0.15) + 5}.o, obj.i_upmid)')
                eval(f'crt_Wire(obj{round((i - 0.3) / 0.15) + 5}.o, obj.i_lowmid)')

    # 输入译码器的数据
    @property
    def inputData(self):
        return union_Pin(
            electricity.element_Pin(electricity.get_Element(self.x + 0.15, self.y + 0.3, self.z), 0),
            electricity.element_Pin(electricity.get_Element(self.x + 0.15, self.y + 0.3, self.z), 1),
            electricity.element_Pin(electricity.get_Element(self.x, self.y + 0.3, self.z), 0),
            electricity.element_Pin(electricity.get_Element(self.x, self.y + 0.3, self.z), 1)
        )

    # 输出译码器的数据
    def outputData(self):
        pass

    @property
    def i_up(self):
        return electricity.element_Pin(electricity.get_Element(self.x + 0.15, self.y + 0.3, self.z), 0)

    @property
    def i_upmid(self):
        return electricity.element_Pin(electricity.get_Element(self.x + 0.15, self.y + 0.3, self.z), 1)

    @property
    def i_lowmid(self):
        return electricity.element_Pin(electricity.get_Element(self.x, self.y + 0.3, self.z), 0)

    @property
    def i_low(self):
        return electricity.element_Pin(electricity.get_Element(self.x, self.y + 0.3, self.z), 1)

    @property
    def o0(self):
        return electricity.get_Element(self.x + 0.3, self.y + 0.05, self.z).o_lowmid

    @property
    def o1(self):
        return electricity.get_Element(self.x + 0.3, self.y + 0.05, self.z).o_upmid

    @property
    def o2(self):
        return electricity.get_Element(self.x + 0.3, self.y + 0.25, self.z).o_lowmid

    @property
    def o3(self):
        return electricity.get_Element(self.x + 0.45, self.y + 0.25, self.z).o_upmid

    @property
    def o4(self):
        return electricity.get_Element(self.x + 0.45, self.y + 0.05, self.z).o_lowmid

    @property
    def o5(self):
        return electricity.get_Element(self.x + 0.45, self.y + 0.05, self.z).o_upmid

    @property
    def o6(self):
        return electricity.get_Element(self.x + 0.45, self.y + 0.25, self.z).o_lowmid

    @property
    def o7(self):
        return electricity.get_Element(self.x + 0.45, self.y + 0.25, self.z).o_upmid

    @property
    def o8(self):
        return electricity.get_Element(self.x + 0.6, self.y + 0.05, self.z).o_lowmid

    @property
    def o9(self):
        return electricity.get_Element(self.x + 0.6, self.y + 0.05, self.z).o_upmid

    @property
    def o10(self):
        return electricity.get_Element(self.x + 0.6, self.y + 0.25, self.z).o_lowmid

    @property
    def o11(self):
        return electricity.get_Element(self.x + 0.6, self.y + 0.25, self.z).o_upmid

    @property
    def o12(self):
        return electricity.get_Element(self.x + 0.3, self.y + 0.05, self.z).o_lowmid

    @property
    def o13(self):
        return electricity.get_Element(self.x + 0.3, self.y + 0.05, self.z).o_upmid

    @property
    def o14(self):
        return electricity.get_Element(self.x + 0.3, self.y + 0.25, self.z).o_lowmid

    @property
    def o15(self):
        return electricity.get_Element(self.x + 0.3, self.y + 0.25, self.z).o_upmid

# 多个逻辑输入（暂不支持m * n矩阵排列元件的方式）
class Inputs(Union_LogicBase):
    def __init__(
            self,
            x: numType = 0,
            y: numType = 0,
            z: numType = 0,
            bitLength: int = None,
            elementXYZ: bool = None,  # x, y, z是否为元件坐标系
            unionHeading: bool = False,  # False: 生成的元件为竖直方向，否则为横方向
            fold: bool = False,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
            foldMaxNum: int = 8  # 达到foldMaxNum个元件数时即在z轴自动折叠
    ) -> None:
        # 搭配_unionHeading_fold使用
        def func1():
            zcor = z
            for i in range(bitLength):
                self._elements.append(
                    electricity.Logic_Input(x + i % foldMaxNum, y, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func2():
            for i in range(bitLength):
                self._elements.append(
                    _elementsClass.Logic_Input(x + i, y, z, True)
                )

        def func3():
            zcor = z
            for i in range(bitLength):
                self._elements.append(
                    electricity.Logic_Input(x, y + i % foldMaxNum, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func4():
            for i in range(bitLength):
                self._elements.append(
                    _elementsClass.Logic_Input(x, y + i, z, True)
                )

        # main
        x, y, z = _unionClassHead.union_Init_HEAD(
            x, y, z,
            bitLength,
            elementXYZ,
            unionHeading,
            fold,
            foldMaxNum
        )

        self._elements: _typing.List[_elementsClass.Logic_Input] = []
        _unionHeading_fold(
            func1, func2, func3, func4, unionHeading, fold
        )

    @property
    def data_Output(self) -> union_Pin:
        return union_Pin(
            self,
            *(element.o for element in self._elements)
        )

# 多个逻辑输入（暂不支持m * n矩阵排列元件的方式）
class Outputs(Union_LogicBase):
    def __init__(
            self,
            x: numType = 0,
            y: numType = 0,
            z: numType = 0,
            bitLength: int = None,
            elementXYZ: bool = None,  # x, y, z是否为元件坐标系
            unionHeading: bool = False,  # False: 生成的元件为竖直方向，否则为横方向
            fold: bool = False,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
            foldMaxNum: int = 8  # 达到foldMaxNum个元件数时即在z轴自动折叠
    ) -> None:
        # 搭配_unionHeading_fold使用
        def func1():
            zcor = z
            for i in range(bitLength):
                self._elements.append(
                    electricity.Logic_Output(x + i % foldMaxNum, y, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func2():
            for i in range(bitLength):
                self._elements.append(
                    _elementsClass.Logic_Output(x + i, y, z, True)
                )

        def func3():
            zcor = z
            for i in range(bitLength):
                self._elements.append(
                    electricity.Logic_Output(x, y + i % foldMaxNum, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func4():
            for i in range(bitLength):
                self._elements.append(
                    _elementsClass.Logic_Output(x, y + i, z, True)
                )

        # main
        x, y, z = _unionClassHead.union_Init_HEAD(
            x, y, z,
            bitLength,
            elementXYZ,
            unionHeading,
            fold,
            foldMaxNum
        )

        self._elements: _typing.List[_elementsClass.Logic_Output] = []
        _unionHeading_fold(
            func1, func2, func3, func4, unionHeading, fold
        )

    @property
    def data_Input(self) -> union_Pin:
        return union_Pin(
            self,
            *(element.i for element in self._elements)
        )

# D触发器流水灯
class D_WaterLamp(Union_LogicBase):
    def __init__(
            self,
            x: numType = 0,
            y: numType = 0,
            z: numType = 0,
            bitLength: int = None,
            elementXYZ: bool = None, # x, y, z是否为元件坐标系
            unionHeading: bool = False, # False: 生成的元件为竖直方向，否则为横方向
            fold: bool = False, # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
            foldMaxNum: int = 4, # 达到foldMaxNum个元件数时即在z轴自动折叠
            is_loop: bool = True # 是否使流水灯循环
    ) -> None:
        # D触流水灯导线连接方式
        def link_D_Flipflop(elements: _typing.List[_elementsClass.D_Flipflop]) -> None:
            # 连接clk
            for i in range(len(elements) - 1):
                elements[i].i_low - elements[i + 1].i_low
            # 连接数据传输导线
            elements[0].o_low - elements[1].i_up
            for i in range(1, len(elements) - 1):
                elements[i].o_up - elements[i + 1].i_up
            # 流水灯循环导线
            if is_loop:
                elements[-1].o_low - elements[0].i_up
            else:
                firstElement = elements[0]
                orGate = _elementsClass.Or_Gate(*firstElement.get_Position(), True)
                orGate.i_up - orGate.o
                orGate.o - firstElement.i_up
                orGate.i_low - firstElement.i_low

        def func1():
            zcor = z
            for i in range(bitLength):
                self._elements.append(
                    electricity.D_Flipflop(x + i % foldMaxNum, y, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func2():
            for increase in range(bitLength):
                self._elements.append(
                    electricity.D_Flipflop(x + increase, y, z, True)
                )

        def func3():
            zcor = z
            for i in range(bitLength):
                self._elements.append(
                    electricity.D_Flipflop(x, y + (i % foldMaxNum) * 2, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func4():
            for increase in range(bitLength):
                self._elements.append(
                    electricity.D_Flipflop(x, y + increase * 2, z, True)
                )

        # main
        if bitLength < 2:
            raise _errors.bitLengthError

        x, y, z = _unionClassHead.union_Init_HEAD(
            x, y, z,
            bitLength,
            elementXYZ,
            unionHeading,
            fold,
            foldMaxNum
        )

        if not isinstance(is_loop, bool):
            raise TypeError

        self._elements: _typing.List[_elementsClass.D_Flipflop] = []
        _unionHeading_fold(
            func1, func2, func3, func4, unionHeading, fold
        )
        link_D_Flipflop(self._elements)

    @property
    def data_Input(self) -> union_Pin:
        return union_Pin(
            self,
            self._elements[0].i_low
        )

    @property
    def data_Output(self) -> union_Pin:
        return union_Pin(
            self,
            self._elements[0].o_low,
            *(element.o_up for element in self._elements[1:])
        )

    # 与data_Output相反的引脚
    @property
    def neg_data_Output(self) -> union_Pin:
        return union_Pin(
            self,
            self._elements[0].o_up,
            *(element.o_low for element in self._elements[1:])
        )