# 元件 element

## 创建元件
物实中所有的元件都被封装为`physicsLab`中对应的类，详见[所有元件.md](elements.md)

创建元件对应的类的实例，就会在存档中创建该元件
```python
with Experiment(OpenMode.load_by_sav_name, "example"):
    Logic_Input()  # 创建一个逻辑输入
    Logic_Output() # 创建一个逻辑输出
    b = Or_Gate()  # 创建一个或门
```

除此之外还有`crt_element`函数
```python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    expe.crt_element("Logic Input", 0, 0, 0) # Model ID
    expe.crt_element("Logic_Input", 0, 0, 0) # class name
```
`name`参数不仅支持物实存档中的`ModelID`对应的字符串，还支持`physicsLab`中类的名字

## 获取元件
在物实, 我们要操作一个元件只需要点击就行了。但要在`physicsLab`中操作元件, 我们只能操作元件类的实例。  
这意味着，当我们导入已有的实验的时候，只能通过一些间接的方法来获取元件的引用

`physicsLab`提供以下间接获取元件的引用的方式：
* 通过元件的坐标
* 通过元件在物实中生成的先后顺序进行索引（这个生成的顺序被称为`index`）
* 通过元件的`Identifier`

若未能找到符合条件的元件的话, 会抛出`ElementNotFound`

```python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    expe.get_element_from_position(0, 0, 0) # x, y, z
    expe.get_element_from_index(index=1) # 通过元件是第多少个被创建的来获取
    expe.get_element_from_identifier("fe089d7e37114de394918a261c53df00") # 通过元件的Identifier来获取
```

> Note:
> 1.  当元件的坐标重叠时，此时会返回一个含所有位于该坐标的元件的list
> 2.  对于电学实验而言，`get_element_*`并不会区分索引的坐标是不是元件坐标系 (elementXYZ)
>     但你可以通过元件的`is_elementXYZ`属性来获取是否是元件坐标系

元件的`index`会从1开始，每生成一个元件就会加1
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    No_Gate(0, 0, 0) # index = 1
    Or_Gate(0, 0, 0.1) # index = 2
```

> Note: `get_element_*`用来索引的坐标为创建元件时对应的坐标, 与是否为元件坐标系无关

用一个简单的例子来说明:
```Python
from physicsLab import *

with Experiment(OpenMode.crt, "example", ExperimentType.Circuit, force_crt=True) as expe:
   Logic_Input(1, 0, 0, elementXYZ=True)
   Logic_Output(1, 0, 0)
   print(expe.get_element_from_position(1, 0, 0))

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
   Logic_Input(1, 0, 0, elementXYZ=True)
   Logic_Output(1, 0, 0)
   print(expe.get_element_from_position(1, 0, 0))
```
输出结果:
```
[Logic_Input(1, 0, 0, elementXYZ=True), Logic_Output(1, 0, 0, elementXYZ=False)]
Successfully update experiment "example"! 2 elements, 0 wires.
[Logic_Output(1, 0, 0, elementXYZ=False), Logic_Input(1, 0, 0, elementXYZ=True), Logic_Output(1, 0, 0, elementXYZ=False)]
Successfully update experiment "example"! 4 elements, 0 wires.
```

你能理解为什么第二次打印时输出的列表长度为3吗?  
因为在上一次写入的时候会将元件坐标系自动转化为物实坐标系, 在第二次read的时候会直接读取存档内的物实坐标系, 那么上一次创建时的`Logic_Input(1, 0, 0elementXYZ=True)`自然就不会在后面read这次的坐标索引中被找到了  
如果要索引第一次创建的元件坐标系的元件, 需要用`xyzTranslate(1, 0, 0)`来执行元件坐标系与物实坐标系之间的转换
详见[元件坐标系](#元件坐标系-elementXYZ)

## 删除元件
我们也可以删除元件：
```python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    a = Logic_Input(0, 0, 0)
    expe.del_element(a) # input: element's self, output: None
```
`del_element`需要传入元件的引用，所以必要时也需要配合`get_element_*`使用。

## 获取元件的数量

physicsLab提供了`get_elements_count`来获取元件的数量：

```python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    print(self.get_elements_count())
```

## 清空实验的元件

physicsLab提供了`clear_elements`来清空实验的元件：

```python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    expe.clear_elements()
```

## 元件坐标系 elementXYZ
`物实坐标系`即为物实默认的坐标系  
物实坐标系的单位长度与元件尺寸出入较大，因此physicsLab提供了专门为元件尺寸定制的`元件坐标系`。  
元件坐标系的x, y单位长度为1个是门的长、宽，z的单位长度为物实坐标系的0.1

### 设置为元件坐标系
此函数将从调用该函数之后到打开下一个存档之前的作用域的坐标系设置为元件坐标系
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
  set_elementXYZ(True) # 将expe设置为元件坐标系
  # do something
```

当你只希望某个元件是元件坐标系，而其他元件不受影响时，你可以在创建元件时传入对应参数
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    And_Gate(0, 0, 0.1) # 这个或门的坐标为物实坐标系
    Or_Gate(0, 1, 0, elementXYZ=True) # 这个或门的坐标为元件坐标系
```

### 判断是否为元件坐标系
你也可以使用该函数获取当前作用域下是否为元件坐标系：
```python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    print(expe.is_elementXYZ)
```
如果你想查看某个元件是否为元件坐标系，可以通过元件属性`is_elementXYZ`查看：
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
  a = Logic_Input()
  print(a.is_elementXYZ)
```

### 获取物实坐标系单位长度
`get_xyzUnit()`用于获取元件坐标系下的单位长度对应着物实坐标系下的值
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    print(get_xyzUnit())
```

### 与物实坐标系的转换
`translateXYZ`将物实坐标系转换为元件坐标系（包括2体积元件坐标修正）  
`xyzTranslate`将元件坐标系转换为物实坐标系（默认不支持2体积元件坐标修正）, 但你可以通过传入元件的`is_bigElement`属性来进行2体积元件修正

## methods & attributes
所有的元件都有一些方法来操作
```python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    a = Logic_Input()

    # methods
    a.set_highLevel() # 将逻辑输入设置为输出为1（仅对逻辑输入有效）
    a.set_position() # 设置元件坐标
    a.get_index() # 获取元件的Index（index为元件生成顺序的计数器）
    a.set_HighLeaveValue() # 设置高电平的值，仅逻辑电路元件有效
    # attributes
    a.data # 获取元件在物实对应的dict
    a.properties # 获取元件的属性（相当于a.data["Properties"]）
    a.experiment # 获取元件对应的实验
```
在[所有元件 elements](elements.md)中介绍得更全面
