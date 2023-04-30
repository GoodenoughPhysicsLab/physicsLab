#coding=utf-8
# 模块化电路
import typing as _typing
import physicsLab._tools as _tools
import physicsLab.electricity as electricity
import physicsLab.electricity.elementXYZ as _elementXYZ
import physicsLab.electricity.elementsClass as _elementsClass
from physicsLab.electricity.unionElements.unionPin import unionPin
import physicsLab.electricity.unionElements._unionClassHead as _unionClassHead

# 任意引脚加法电路
class union_Sum:
    def __init__(self, x : _tools.numType = 0, y : _tools.numType = 0, z : _tools.numType = 0, bitCount : int = 1):
        if not (
                isinstance(x, (float, int)) and isinstance(y, (float, int)) and
                isinstance(z, (float, int)) and isinstance(bitCount, int) and bitCount > 0
        ):
            raise RuntimeError('Error in input parameters')
        x, y, z = _tools.roundData(x), _tools.roundData(y), _tools.roundData(z)
        electricity.Full_Adder(x, y, z)
        for count in range(1, bitCount):
            if count % 8 != 0:
                y = _tools.roundData(y + 0.2)
                electricity.crt_Wire(
                    electricity.Full_Adder(x, y, z).i_low,
                    electricity.get_Element(x, y - 0.2, z).o_low
                )
            else:
                y -= 1.4
                z = _tools.roundData(z + 0.1)
                electricity.crt_Wire(
                    electricity.Full_Adder(x, y, z).i_low,
                    electricity.get_Element(x, y + 1.4, z - 0.1).o_low
                )

# 任意引脚减法电路
class union_Sub:
    pass

# 2-4译码器
class union_2_4_Decoder:
    def __init__(self, x : _tools.numType = 0, y : _tools.numType = 0, z : _tools.numType = 0):
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
class union_4_16_Decoder:
    def __init__(self, x : _tools.numType = 0, y : _tools.numType = 0, z : _tools.numType = 0):
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
        return unionPin(
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

# 多个逻辑输入（暂不支持m * n矩阵排列元件的方式）
class inputs(_unionClassHead.unionBase):
    def __init__(
            self,
            x: _tools.numType = 0,
            y: _tools.numType = 0,
            z: _tools.numType = 0,
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
                self.__elements.append(
                    electricity.Logic_Input(x + i % foldMaxNum, y, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func2():
            for i in range(bitLength):
                self.__elements.append(
                    _elementsClass.Logic_Input(x + i, y, z, True)
                )

        def func3():
            zcor = z
            for i in range(bitLength):
                self.__elements.append(
                    electricity.Logic_Input(x, y + i % foldMaxNum, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func4():
            for i in range(bitLength):
                self.__elements.append(
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

        self.__elements: _typing.List[_elementsClass.Logic_Input] = []
        _unionHeading_fold(
            func1, func2, func3, func4, unionHeading, fold
        )

    @property
    def data_Output(self) -> unionPin:
        return unionPin(element.o for element in self.__elements)

# 多个逻辑输入（暂不支持m * n矩阵排列元件的方式）
class outputs(_unionClassHead.unionBase):
    def __init__(
            self,
            x: _tools.numType = 0,
            y: _tools.numType = 0,
            z: _tools.numType = 0,
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
                self.__elements.append(
                    electricity.Logic_Output(x + i % foldMaxNum, y, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func2():
            for i in range(bitLength):
                self.__elements.append(
                    _elementsClass.Logic_Output(x + i, y, z, True)
                )

        def func3():
            zcor = z
            for i in range(bitLength):
                self.__elements.append(
                    electricity.Logic_Output(x, y + i % foldMaxNum, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func4():
            for i in range(bitLength):
                self.__elements.append(
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

        self.__elements: _typing.List[_elementsClass.Logic_Output] = []
        _unionHeading_fold(
            func1, func2, func3, func4, unionHeading, fold
        )

    @property
    def data_Output(self) -> unionPin:
        return unionPin(element.i for element in self.__elements)

# D触发器流水灯
class d_WaterLamp(_unionClassHead.unionBase):
    def __init__(
            self,
            x: _tools.numType = 0,
            y: _tools.numType = 0,
            z: _tools.numType = 0,
            bitLength: int = None,
            elementXYZ: bool = None, # x, y, z是否为元件坐标系
            unionHeading: bool = False, # False: 生成的元件为竖直方向，否则为横方向
            fold: bool = False, # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
            foldMaxNum: int = 4 # 达到foldMaxNum个元件数时即在z轴自动折叠
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
            elements[-1].o_low - elements[0].i_up

        def func1():
            zcor = z
            for i in range(bitLength):
                self.__elements.append(
                    electricity.D_Flipflop(x + i % foldMaxNum, y, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func2():
            for increase in range(bitLength):
                self.__elements.append(
                    electricity.D_Flipflop(x + increase, y, z, True)
                )

        def func3():
            zcor = z
            for i in range(bitLength):
                self.__elements.append(
                    electricity.D_Flipflop(x, y + (i % foldMaxNum) * 2, zcor, True)
                )
                if i == foldMaxNum - 1:
                    zcor += 1

        def func4():
            for increase in range(bitLength):
                self.__elements.append(
                    electricity.D_Flipflop(x, y + increase * 2, z, True)
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

        self.__elements: _typing.List[_elementsClass.D_Flipflop] = []
        _unionHeading_fold(
            func1, func2, func3, func4, unionHeading, fold
        )
        link_D_Flipflop(self.__elements)

    @property
    def data_Input(self) -> unionPin:
        return unionPin(self.__elements[0].i_low)

    @property
    def data_Output(self) -> unionPin:
        return unionPin(
            self.__elements[0].i_low,
            *(element.o_up for element in self.__elements[1:])
        )