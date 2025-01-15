# 模块化电路 unit

## Super_AndGate
支持任意大于1的正整数的输入引脚的与门
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    crt_wires(
        lib.Inputs(-1, 0, 0, bitnum=7).outputs,
        lib.Super_AndGate(0, 0, 0, bitnum=7).inputs
    )
```

## Super_OrGate
支持任意大于1的正整数的输入引脚的或门
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    crt_wires(
        lib.Inputs(-1, 0, 0, bitnum=7).outputs,
        lib.Super_OrGate(0, 0, 0, bitnum=7).inputs
    )
```

## Super_NorGate
支持任意大于1的正整数的输入引脚的或非门
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    crt_wires(
        lib.Inputs(-1, 0, 0, bitnum=7).outputs,
        lib.Super_NorGate(0, 0, 0, bitnum=7).inputs
    )
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
from physicsLab.union import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    a = D_WaterLamp(bitLength=8)
    b = Outputs(bigLength=8)
    crt_wires(a.data_Outputs, b.data_Inputs)
```

## 删除模块化电路的导线
调用`del_wires()`，同上