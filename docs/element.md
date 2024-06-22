# 元件 element

## 创建元件
物实中所有的元件都被封装为`physicsLab`中对应的类（暂未支持物实中的全部元件）  
物实元件与其相应的类名在[所有元件.md](elements.md)中查看  
例：
```python
with experiment("example"):
    Logic_Input()  # 创建一个逻辑输入
    Logic_Output() # 创建一个逻辑输出
    b = Or_Gate()  # 创建一个或门
```

除此之外还有一个通用的函数`crt_Element()`用来创建所有`physicsLab`支持的元件
```python
def crt_Element(name: str, x=0, y=0, z=0, elementXYZ: Optional[bool] = None) -> CircuitBase
```
`name`参数不仅支持紫兰斋在存档中的`ModelID`对应的字符串，还支持`physicsLab`中类的名字  


## 获取元件
`在物理实验室( Physics-Lab-AR )`, 我们要操作一个元件只需要点击就行了。但要在`physicsLab`中操作元件, 我们只能操作类的实例。  
但当我们通过`read_Experiment`获取一些类的时候，我们难以获取其引用，此时需要知道元件的坐标或者那个元件是第多少个被创建的( 这个数字即是index )，然后使用`get_Element()`：  

`get_Element`有两种获取元件的方式：  
1.  通过元件的坐标进行索引
2.  通过元件在物实中生成的先后顺序进行索引（即`index`）  

`get_Element`的返回值是这个坐标对应的元件的引用，若不存在抛出Error  
```python
get_Element(0, 0, 0) # x, y, z
get_Element(index=1) # 通过元件是第多少个被创建的来获取
```

> Note:   
> 1.  当元件的坐标重叠时，此时会返回一个含所有位于该坐标的元件的list  
> 2.  `get_Element`并不会区分索引的坐标是不是元件坐标系( elementXYZ )  
>     但你可以通过元件的`is_elementXYZ`属性来获取是否是元件坐标系

元件的`index`会从1开始，每生成一个元件就会加1
```Python
from physicsLab import *

with experiment("example"):
    No_Gate() # index = 1
    Or_Gate(0, 0, 0.1) # index = 2
``` 

> Note: `get_Element`用来索引的坐标为创建元件时对应的坐标, 与是否为元件坐标系无关

用一个简单的例子来说明:
```Python
from physicsLab import *

with experiment("example"):
   Logic_Input(1, 0, 0, elementXYZ=True)
   Logic_Output(1, 0, 0)
   print(get_Element(1, 0, 0))

with experiment("example", read=True):
   Logic_Input(1, 0, 0, elementXYZ=True)
   Logic_Output(1, 0, 0)
   print(get_Element(1, 0, 0))
```
输出结果:
```
[Logic_Input(1, 0, 0, elementXYZ=True), Logic_Output(1, 0, 0, elementXYZ=False)]
Successfully create experiment "example"! 2 elements, 0 wires.
[Logic_Output(1, 0, 0, elementXYZ=False), Logic_Input(1, 0, 0, elementXYZ=True), Logic_Output(1, 0, 0, elementXYZ=False)]
Successfully update experiment "example"! 4 elements, 0 wires.
```

你能理解为什么第二次打印时输出的列表长度为3吗?  
因为在上一次写入的时候会将元件坐标系自动转化为物实坐标系, 在第二次read的时候会直接读取存档内的物实坐标系, 那么上一次创建时的`Logic_Input(1, 0, 0elementXYZ=True)`自然就不会在后面read这次的坐标索引中被找到了  
如果要索引第一次创建的元件坐标系的元件, 需要这样写`get_Element(xyzTranslate(1, 0, 0))`  
详见`元件坐标系`  
当`get_Element`索引元件失败时，会抛出`ElementNotFound`的Error  
如果你想在索引失败时不抛出error，需要使用default参数
```Python
from physicsLab import *

with experiment("example"):
    get_Element(1, 0, 0, default=None)
```

## 删除元件
我们也可以删除元件：
```python
from physicsLab import *

a = Logic_Input()
del_Element(a) # input: element's self, output: None
```
`del_Element`需要传入元件的引用，所以必要时也需要用`get_Element`。

## 元件坐标系 elementXYZ
`物实坐标系`即为物实默认的坐标系  
物实坐标系的单位长度与元件尺寸出入较大，因此physicsLab提供了专门为元件尺寸定制的`元件坐标系`。  
元件坐标系的x, y单位长度为1个是门的长、宽，z的单位长度为物实坐标系的0.1  
### 设置为元件坐标系
此函数将从调用该函数之后到打开下一个存档之前的作用域的坐标系设置为元件坐标系
```Python
from physicsLab import *
set_elementXYZ(True)
```
当你只希望某个元件是元件坐标系，而其他元件不受影响时，你可以在创建元件时传入对应参数
```Python
And_Gate(0, 0, 0.1) # 这个或门的坐标为物实坐标系
Or_Gate(0, 1, 0, elementXYZ=True) # 这个或门的坐标为元件坐标系，其他元件也一样
```
### 判断是否为元件坐标系
你也可以使用该函数获取当前作用域下是否为元件坐标系：
```python
from physicsLab import *
is_elementXYZ() # return a bool
```
如果你想查看某个元件是否为元件坐标系，可以通过元件属性`is_elementXYZ`查看：
```Python
from physicsLab import *

with experiment("example"):
  a = Logic_Input()
  print(a.is_elementXYZ)
```

### 设置元件坐标系的坐标原点
元件坐标系原点默认为物实坐标系的元件：`(0, 0, 0)`，但这是可以动态设置的
```Python

with experiment("example"):
    set_O(0.2, 0.2, 0.1)
    print(get_OriginPosition()) # 获取坐标原点
```
> Note: set_O只认为传进来的x, y, z为物实默认坐标系下的坐标而非元件坐标系

### 获取坐标原点
如上面的例子所示，可以使用`get_OriginPosition()`来获取坐标原点

### 获取物实坐标系单位长度
`get_xyzUnit()`用于此功能
```Python
get_xyzUnit("x") # result: 0.16
get_xyzUnit("y", "z") # result: 0.08, 0.1
```

### 与物实坐标系的转换
`translateXYZ`将物实坐标系转换为元件坐标系（包括2体积元件坐标修正）  
`xyzTranslate`将元件坐标系转换为物实坐标系（默认不支持2体积元件坐标修正）, 但你可以通过传入元件的`is_bigElement`属性来进行2体积元件修正


## methods & attributes
所有的元件都有一些方法来操作
```python
from physicsLab import *

with experiment("example"):
    a = Logic_Input()

    # methods
    a.set_highLevel() # 将逻辑输入设置为输出为1（仅对逻辑输入有效）
    a.get_Position() # 获取元件坐标
    a.set_Position() # 设置元件坐标（暂时只支持元件坐标系）
    a.get_Index() # 获取元件的Index（元件生成顺序）
    a.set_HighLeaveValue() # 设置高电平的值，仅逻辑电路元件有效
    a.set_LowLeaveValue() # 设置低电平的值，仅逻辑电路元件有效
    a.get_HighLeaveValue() # 获取高电平的值，仅逻辑电路元件有效
    a.get_LowLeaveValue() # 获取低电平的值，仅逻辑电路元件有效
    # attributes
    a.data # 获取元件在物实对应的dict
    a.modelID # 获取元件的ModelID
    a.experiment # 获取元件对应的实验
```
在[所有元件 elements](elements.md)中也介绍得有元件的方法


## hook
`physicsLab`暂未支持定义元件的`hook`
```Python
from physicsLab import *

def f():
    pass

with experiment("example"):
    set_hook(f) # 初始化元件的hook
```
