# 教程
大家好啊！虽然我在[functions.md](functions.md)介绍了一堆函数，但多少让人找不到主次。因此，我决定写下这个教程，以帮助各位更快速地上手physicsLab

## 第一个程序
元件浮空几乎成为了修改存档的代名词，因此，就让我们从创建一个悬空的逻辑输入开始吧：
```Python
from physicsLab import experiment, Logic_Input

with experiment("my experiment's name"):
    Logic_Input(0, 0, 0.1)
```
执行程序，打开物实，重新打开对应实验（my expeirment's name）查看奇迹  
<font color=green>注：该程序会首先检查本地是否存在实验“my experiment's name”，若存在则打开对应实验，若不存在则会自动创建一个名为"my experiment's name"的实验</font>

上面的方式是***最方便***也是我***最推荐***的  
  
更原始一些的方式是像下面这样写：
```python
from physicsLab import \
    crt_Experiment, write_Experiment, Logic_Input
# 这三个函数分别是：创建实验，写入试验，逻辑输入

crt_Experiment("myTest") # 创建一个名为"myTest"的实验
Logic_Input(0, 0, 0.1) # 创建一个逻辑输入
write_Experiment() # 写入试验（如果不写入的话将无法更新本地存档的状态
```
怎样，看起来还算简单吧  

<font color=red>请注意：若要创建的实验与已有实验的命名冲突，则会抛出错误</font>（报错信息源于physicsLab 1.3.0）
```
physicsLab.errors.crtExperimentFailError: Failed to create experiment, the experiment already exists
```

此时你需要将程序换为下面的样子

你可以选择到物实创建这个存档，也可以选择用程序创建这个存档：
```python
from physicsLab import \
    open_Experiment, write_Experiment, Logic_Input

# 这三个函数分别是：打开实验，写入试验，逻辑输入
open_Experiment("my experiment's name") # 注意，这里我们换成了创建这个实验
Logic_Input(0, 0, 0.1)
write_Experiment()
```
理论上此时就能正常运行了  

如果你不希望打开一个实验，如果实验不存在则创建实验的话，你可以这样写：
```python
from physicsLab import \
    open_or_crt_Experiment, write_Experiment, Logic_Input

open_or_crt_Experiment("my experiment's name")
Logic_Input(0, 0, 0.1)
write_Experiment()
```

## 创建元件
创建元件非常简单：
```Python
from physicsLab import *

with experiment("xxx"):
    Logic_Input(0.1, 0.2, 0) # 创建一个逻辑输入
```
更多的元件请在[所有元件.md](./%E6%89%80%E6%9C%89%E5%85%83%E4%BB%B6.md)中查看

除此之外还有一个通用的函数`crt_Element()`用来创建所有`physicsLab`支持的元件
```python
from physicsLab import *

crt_Element("NE555", 0.1, 0.2, 0) # 创建元件：555定时器
```
`name`参数不仅支持紫兰斋在存档中的`ModelID`对应的字符串，还支持`physicsLab`中类的名字

## 元件坐标系
物实已有的坐标表示方法往往稍大于一个元件的尺寸，而元件坐标系可以解决这个问题：
```Python
from physicsLab import experiment, Logic_Input

with experiment("my experiment's name"):
    Logic_Input(0, 0, 1, elementXYZ=True)
```
所有元件后面都有一个`elementXYZ`参数，当此参数为True时，该原件一定为元件坐标系  
你还可以全局设置为元件坐标系，此时`elementXYZ=False`会强行使该原件不为元件坐标系  
```Python
set_elementXYZ(True) # 将全局设置为元件坐标系
```

## 连接导线

## 模块化电路

## 在物实做音乐