# quick start
## 第一个程序
元件浮空几乎成为了修改存档的代名词，因此，就让我们从创建一个悬空的逻辑输入开始吧：
```Python
from physicsLab import experiment, Logic_Input

with experiment("example"):
    Logic_Input(0, 0, 0.1)
```
执行程序，打开物实，打开名为example的实验查看奇迹  

`experiment("example")`会首先检查本地是否存在实验“example”，若存在则打开，若不存在则会自动创建一个名为"example"的实验

`with`对应的缩进内写的代码会被视为是对实验`example`的操作，比如`Logic_Input(0, 0, 0.1)`对应着创建一个坐标为`x=0, y=0, z=0.1`的逻辑输入

上面的方式是***最方便***也是我***最推荐***的  

## 创建元件
创建元件非常简单：
```Python
from physicsLab import *

with experiment("example"):
    Logic_Output(0.1, 0.2, 0) # 创建一个逻辑输出
```
更多的元件请在[elements.md](./elements.md)中查看

除此之外还有另一个函数`crt_Element()`用来创建所有`physicsLab`支持的元件
```python
from physicsLab import *

with experiment("example"):
    crt_Element("NE555", 0.1, 0.2, 0) # 创建元件：555定时器
```
`name`参数不仅支持紫兰斋在存档中的`ModelID`对应的字符串，还支持`physicsLab`中类的名字

## 元件坐标系
物实已有的坐标表示方法往往稍大于一个元件的尺寸，而元件坐标系可以解决这个问题：
```Python
from physicsLab import experiment, Logic_Input

with experiment("example"):
    Logic_Input(0, 0, 1, elementXYZ=True)
```
所有元件后面都有一个`elementXYZ`参数，当此参数为True时，该原件一定为元件坐标系  
你还可以全局设置为元件坐标系，此时`elementXYZ=False`会强行使该原件不为元件坐标系  
```Python
from physicsLab import *

with experiment("example", elementXYZ=True):
    Logic_Input(0, 0, 1) # 此时也是元件坐标系为True的效果
    Logic_Input(0, 0, 1, elementXYZ=False) # 该False只对该原件有效，且优先级大于全局为True的优先级
```