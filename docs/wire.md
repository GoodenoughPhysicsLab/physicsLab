# 导线 & 引脚

## class Wire
导线

Wire的实例有以下属性：
* Source: 一个引脚
* Target: 另一个引脚

> 之所以叫`Source`, `Target`, 是因为在物实连接导线都是点击一个引脚，然后点击或者拖向另一个引脚。第一个引脚就是`Source`，第二个引脚即为`Target`。

## class Pin
引脚

Pin的实例有以下属性：
*  element_self: 该引脚所属的元件

## enum class WireColor
导线颜色:
* red
* blue
* green
* yellow
* black

## 连接导线
通过`crt_wire`，可以连接导线
```Python
from physicsLab import *

with experiment(OpenMode.load_by_sav_name, "example"):
    e1 = Yes_Gate() # 是门
    e2 = Yes_Gate()

    crt_wire(e1.o, e2.i, color=WireColor.red) # 连接导线
    crt_wire(e1.i, e2.o) # color默认为蓝色
```
`i, o`都是引脚的名字。元件的引脚的名字详见[elements.md](elements.md)

> Note:
> * `color`参数为`Keyword-Only argument`
> * 连接的导线必须是在同一个实验中的两个不同的引脚，否则会抛出`InvalidWireError`异常
> * 重复连接的导线会被忽略

```python
from physicsLab import *

with experiment(OpenMode.load_by_sav_name, "example"):
    e1 = Yes_Gate() # 是门
    e2 = Yes_Gate()

    crt_wire(e1.o, e2.i)
    crt_wire(e1.i, e2.o) # 重复连接, 该导线会被忽略
    crt_wire(e1.o, e2.i, color=WireColor.red) # 虽然导线颜色不同，但还是重复连接的导线，会被忽略
```

## 删除导线
除了创建导线外，也可以删除导线：
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    element = Logic_Input()
    element2 = Logic_Output()

    del_wire(element.o, element2.i)
```
删除导线时不需要提供颜色参数

## 清空导线
```python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    expe.clear_wires()
```

## 导线的数量
```python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    print(expe.get_wires_count())
```
