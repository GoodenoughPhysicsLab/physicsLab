# 模块化电路 lib

## RisingEdgeTrigger

上升沿触发器

引脚：

* i: 输入引脚
* o: 输出引脚

## FallingEdgeTrigger

下降沿触发器

引脚：

* i: 输入引脚
* o: 输出引脚

## EdgeTrigger

上升沿和下降沿触发器

引脚：

* i: 输入引脚
* o: 输出引脚

## Super_AndGate

支持任意大于1的正整数的输入引脚的与门

```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    lib.crt_wires(
        lib.Inputs(-1, 0, 0, bitnum=7).outputs,
        lib.Super_AndGate(0, 0, 0, bitnum=7).inputs
    )
```

## Super_OrGate

支持任意大于1的正整数的输入引脚的或门

```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    lib.crt_wires(
        lib.Inputs(-1, 0, 0, bitnum=7).outputs,
        lib.Super_OrGate(0, 0, 0, bitnum=7).inputs
    )
```

## Super_NorGate

支持任意大于1的正整数的输入引脚的或非门

```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    lib.crt_wires(
        lib.Inputs(-1, 0, 0, bitnum=7).outputs,
        lib.Super_NorGate(0, 0, 0, bitnum=7).inputs
    )
```

## Tick_Counter

当 逻辑输入 输入了num次, 就输出为1, 否则为0, 如果输出为1, 则进入下一个周期, 在下一次输入了num次时输出为1, 否则为0

引脚：

* i: 输入引脚
* o: 输出引脚

```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    logic_input = Logic_Input(0, 0, 0)
    tick_counter = lib.Tick_Counter(0, 0, 0, num=i)
    crt_wire(logic_input.o, tick_counter.i)
    crt_wire(tick_counter.o, Logic_Output(0, 0, 0).i)
```

## TowFour_Decoder

2-4译码器

引脚:

* inputs
* outputs

```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    i = lib.Inputs(-1, 0, 0, bitnum=2)
    decoder = lib.TwoFour_Decoder(0, 0, 0)
    o = lib.Outputs(1, 0, 0, bitnum=4)
    lib.crt_wires(i.outputs, decoder.inputs)
    lib.crt_wires(decoder.outputs, o.inputs)
```

## Switched_Register

可以在两列输入中切换的寄存器

```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    i1 = lib.Inputs(-1, 0, 0, bitnum=6)
    i2 = lib.Inputs(-0.5, 0, 0, bitnum=6)
    clk = Logic_Input(-1, -1, 0)
    switch = Logic_Input(-0.5, -1, 0)
    decoder = lib.Switched_Register(0, 0, 0, bitnum=6)
    o = lib.Outputs(1, 0, 0, bitnum=6)
    lib.crt_wires(i1.outputs, decoder.inputs1)
    lib.crt_wires(i2.outputs, decoder.inputs2)
    crt_wire(clk.o, decoder.clk)
    crt_wire(switch.o, decoder.switch)
    lib.crt_wires(decoder.outputs, o.inputs)
```

## EqualTo

判断两个输入是否相等

```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    i1 = lib.Inputs(-1, 0, 0, bitnum=6)
    i2 = lib.Inputs(-0.5, 0, 0, bitnum=6)
    compute = lib.EqualTo(0, 0, 0, bitnum=6)
    o = Logic_Output(0.5, 0, 0)
    lib.crt_wires(i1.outputs, compute.inputs1)
    lib.crt_wires(i2.outputs, compute.inputs2)
    crt_wire(compute.output, o.i)
```

## Sum

```Sum()```用于创建模块化加法电路  
含有3个数据引脚：`data_Input1`, `data_Input2`, `data_Output`

## Sub

`Sub()`用于创建模块化减法电路
含有3个引脚：`minuend`, `subtrahend`, `outputs`

## Const_NoGate

只读非门类  
当没有只读非门时会创建该非门  
当存在时会获取已存在的非门而非创建  
含有一个引脚：`o`

## Inputs

逻辑输入模块  
引脚：`data_Output`

## Outputs

逻辑输出模块
引脚：`data_Input`

## D触流水灯

创建由d触发器组成的流水灯电路  
引脚：`data_Input`（即为clk），`data_Output`， `neg_data_Output`

## 导线 wires

## 连接模块化电路的导线

调用`crt_wires()`，参数支持传入元件/模块化电路的引脚

```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    a = lib.D_WaterLamp(bitLength=8)
    b = lib.Outputs(bigLength=8)
    lib.crt_wires(a.data_Outputs, b.data_Inputs)
```

## 删除模块化电路的导线

调用`del_wires()`，同上
