# physicsLab

## 操作本地实验（存档） experiment

### 更优雅的写法
你可以用with语句打开一个存档，且读写存档等重复工作无须手动重复编写
```python
with experiment(
    'name',
    read=False, # 读取存档，默认为False
    write=True, # 写入实验，默认为True
    type=expermentType.Circuit # 指定创建存档的类型（只在创建存档时有效）
):
    # to do something
    # 该方式会自动打开存档
    # 若打开失败会自动创建存档
    # 执行完代码之后会自动写入存档
    pass
```

### 打开存档
你必须指明你要打开的是哪个存档：
```Python
open_Experiment('xxx.sav') # 存档的文件名，不推荐使用
open_Experiment('blabla') # 通过在物实保存的本地实验的名字打开存档
```
<font color=red>请注意，你可以多次调用</font>`open_Experiment()`<font color=red>或</font>`crt_Experiment()`<font color=red>，但只有你最后一次调用该函数打开或创建的存档会被操作</font>  

### 创建存档
如果你想要创建一个实验：
```python
crt_Experiment('存档的名字')
crt_Experiment("xxx", experimentType=4)
```
<font color=red>请注意，你可以多次调用</font>`open_Experiment()`<font color=red>或</font>`crt_Experiment()`<font color=red>，但只有你最后一次调用该函数打开或创建的存档会被操作</font>  
```type```参数用于指定创建存档的类型，详情请查看```指定创建实验类型```  

如果你希望打开存档失败不报错而是创建存档，除了使用`with experiment(...)`，你还可以使用
```Python
open_or_crt_Experiment(savName: str, experimentType) -> None
```
该函数与`crt_Experiment`传参相同，但`experimentType`参数仅在尝试创建存档时有效

### 判断存档是否存在
调用`exist_Experiment()`判断存档是否存在  
如果存档已经存档，则会返回存档的文件名  
如果存档不存在，则返回`None`


### 读取存档的内容
被打开的存档不会读取原实验的状态。如果你不希望原实验的状态被覆盖，需要调用该函数：  
```Python
read_Experiment()
```

### 向存档中写入
最后你需要调用该函数往存档里写入程序运行之后的结果：  
```Python
write_Experiment()
```

### 用记事本打开存档文件
你也可以打开存档查看：
```Python
show_Experiment()
```
仅`Windows`上有效

### 删除存档
除了创建存档，你也可以删除存档：
```Python
del_Experiment()
```

## 元件 element
### 创建元件
物实中所有的元件都被封装为`physicsLab`中对应的类（暂未支持全部元件）  
物实元件与其相应的类名在[所有元件.md](./%E6%89%80%E6%9C%89%E5%85%83%E4%BB%B6.md)中查看  
例：
```python
Logic_Input()  # 创建一个逻辑输入
Logic_Output() # 创建一个逻辑输出
b = Or_Gate()  # 创建一个或门，b保存的是Or_Gate的self
# 千万要注意的是：两个元件的坐标不能重叠！
```

除此之外还有一个通用的函数`crt_Element()`用来创建所有`physicsLab`支持的元件
```python
crt_Element(name: str, x = 0, y = 0, z = 0)
```
`name`参数不仅支持紫兰斋在存档中的`ModelID`对应的字符串，还支持`physicsLab`中类的名字  


### 获取元件
要在`physicsLab`中对元件进行操作，我们需要有变量引用着类并由我们调用。但当我们通过`read_Experiment`获取一些类的时候，我们难以获取其引用，此时我们可以用`get_Element()`：
```python
get_Element(x=0, y=0, z=0)
get_Element(index=1)
get_Element(0, 0, 0) # 依然是坐标索引，对应xyz
get_Element(1) # 依然是index索引
```
`get_Element`有两种获取元件的方式：  
  1.  通过元件的坐标进行索引
  2.  通过元件在物实中生成的先后顺序进行索引（即`index`）  

注：当元件的坐标重叠时，此时会返回一个含所有位于该坐标的元件的list  

元件的`index`会从1开始，每生成一个元件就会加1
```Python
from physicsLab import *

No_Gate() # index = 1
Or_Gate(0, 0, 0.1) # index = 2
```
返回值是这个坐标对应的元件的引用，若不存在抛出Error  

### 删除元件
我们也可以删除元件：
```python
from physicsLab import *

a = Logic_Input()
del_Element(a) # input: element's self, output: None
```
`del_Element`需要传入元件的引用，所以必要时也需要用`get_Element`。

### 元件坐标系 elementXYZ
`物实坐标系`即为物实默认的坐标系  
物实坐标系的单位长度与元件尺寸出入较大，因此physicsLab提供了专门为元件尺寸定制的`元件坐标系`。  
元件坐标系的x, y单位长度为1个是门的长、宽，z的单位长度为物实坐标系的0.1  
#### 设置为元件坐标系
此函数将从调用该函数之后到打开下一个存档之前的作用域的坐标系设置为元件坐标系
```Python
from physicsLab import *
set_elementXYZ(True)
```
当你只希望某个元件是元件坐标系，而其他元件不受影响时，你可以在创建元件时传入对应参数
```Python
from physicsLab import *
And_Gate(0, 0, 0.1) # 这个或门的坐标为物实坐标系
Or_Gate(0, 1, 0, elementXYZ=True) # 这个或门的坐标为元件坐标系，其他元件也一样
```
#### 判断是否为元件坐标系
你也可以使用该函数获取当前作用域下是否为元件坐标系：
```python
from physicsLab import *
is_elementXYZ() # return a bool
```
如果你想查看某个元件是否为元件坐标系，可以通过元件属性`is_elementXYZ`查看：
```Python
from physicsLab import *

with experiment("xxx"):
  a = Logic_Input()
  print(a.is_elementXYZ)
```

#### 设置元件坐标系的元件
元件坐标系原点默认为物实坐标系的元件：`(0, 0, 0)`，但这是可以动态设置的
```Python

with experiment("xxx"):
    set_O(0.2, 0.2, 0.1)
    print(get_OriginPosition()) # 获取坐标原点
```
<font color=red>注意：set_O只认为传进来的x, y, z为物实默认坐标系下的坐标</font>

#### 获取坐标原点
如上面的例子所示，可以使用`get_OriginPosition()`来获取坐标原点

#### 获取物实坐标系单位长度
`get_xyzUnit()`用于此功能
```Python
get_xyzUnit("x") # result: 0.16
get_xyzUnit("y", "z") # result: 0.08, 0.1
```

#### 与物实坐标系的转换
`translateXYZ`将物实坐标系转换为元件坐标系（包括2体积元件坐标转换）   
`xyzTranslate`将元件坐标系转换为物实坐标系（默认不支持2体积元件坐标转换）


### Methods
所有的元件都有一些方法来操作
```python
from physicsLab import *
a = Logic_Input()

a.set_highLevel() # 将逻辑输入设置为输出为1（仅对逻辑输入有效）
a.get_Position() # 获取元件坐标
a.set_Position() # 设置元件坐标（暂时只支持元件坐标系）
a.get_Index() # 获取元件的Index（元件生成顺序）
a.set_HighLeaveValue(3) # 设置高电平的值，仅逻辑电路元件有效
a.set_LowLeaveValue(0) # 设置低电平的值，仅逻辑电路元件有效
a.get_HighLeaveValue() # 获取高电平的值，仅逻辑电路元件有效
a.get_LowLeaveValue() # 获取低电平的值，仅逻辑电路元件有效
a.print_arguments() # 打印元件对应的存档信息
a.modelID # 获取元件的ModelID
a.format_Position() # 舍去坐标的浮点精度（因为物实的浮点运算误差）
```

## 导线 wire
连接导线提供了2种方式  
第一种：  
```Python
from physicsLab import *
element = Logic_Input()
element2 = Logic_Output()

crt_Wire(element.o, element2.i, color='红')
# color暂时只支持中文的 "黑", "蓝", "红", "绿", "黄" 与 英文
# 不传入color参数的话，color默认为蓝色
```

上面连接导线的代码也等价于：
```Python
element.o - element2.i
```

所有元件都定义得有自己的引脚名称，这里举个例子：  
```python
from physicsLab import *
a = Or_Gate(0.1, 0.1, 0)
crt_Wire(a.o, a.i_up)
```

引脚也可以在[所有元件.md](./%E6%89%80%E6%9C%89%E5%85%83%E4%BB%B6.md)中找到

另一种连接引脚的方式是不推荐使用的老函数（已移除）：  
```Python
old_crt_wire(SourceLabel, SourcePin: int, TargetLabel, TargetPin: int, color = "蓝") -> None
```
连接导线的方式是更偏于物实存档的原始方案，即用数字来表示某个引脚  
下面呈现部分元件引脚图（第一种其实就是对这个老函数更方便的封装）：  
```
D触发器：          
2    0                  
                             
3    1                          

是门、非门： 
0 1 

比较器:
1
    2
0  

逻辑输入、逻辑输出：
0  

三引脚门电路：   
0             
    2         
1             

全加器：  
2    0  
3  
4    1  

继电器pin  
0   4  
  1    
2   3  
  
二位乘法器：  
4  0  
5  1  
6  2  
7  3  
很明显比第一种更麻烦  
```
在physicsLab 1.2.2之后，该函数被永久弃用（移除）
  
除了创建导线外，也可以删除导线：  
```Python
from physicsLab import *
element = Logic_Input()
element2 = Logic_Output()

del_Wire(element.o, element2.i)
```
使用方法与crt_Wire一模一样  
  
（这篇readme应该介绍了大部分常用功能）

## 模块化电路 union

### Sum
```Sum()```用于创建模块化加法电路  
含有3个数据引脚：`data_Input1`, `data_Input2`, `data_Output`

### Sub
`Sub()`用于创建模块化减法电路
含有3个引脚：`minuend`, `subtrahend`, `outputs`

### Const_NoGate
只读非门类  
当没有只读非门时会创建该非门  
当存在时会获取已存在的非门而非创建  
含有一个引脚：`o`

### Inputs
逻辑输入模块  
引脚：`data_Output`

### Outputs
逻辑输出模块
引脚：`data_Input`

### D触流水灯
创建由d触发器组成的流水灯电路  
引脚：`data_Input`（即为clk），`data_Output`， `neg_data_Output`

### 导线 wires
#### 连接模块化电路的导线
调用`crt_Wires()`，参数支持传入元件/模块化电路的引脚
```Python
from physicsLab import *
from physicsLab.union import *

with experiment("测逝"):
    a = D_WaterLamp(bitLength=8)
    b = Outputs(bigLength=8)
    crt_Wires(a.data_Outputs, b.data_Inputs)
```

#### 删除模块化电路的导线
调用`del_Wires()`，同上

### 音乐拓展 music extension
参数的作用之类的都在源码的注释当中，时间原因文档只好简写了
#### Note
`Note`是音符类  
其中的`time`参数的含义是***距离播放该音符需要等待多少时间***

#### Piece
```Piece```是乐曲类
这是一个只用来保存数据的类，想要往里面存储音符必须是`Note`，如果是休止符则用`None`表示  
初始化时支持传入`list`，但也支持`append`方法  
将Piece类转换为可以在物实播放的电路，除了使用`Player(piece, x, y, z, elementXYZ)`的方法，也可以使用`piece.play(x, y, z, elementXYZ)`的方法，两者是等价的。  
在`midi`中最容易碰到的是播放速度的问题，你可以调用`Piece().set_tempo(num)`来重新设置播放速度，`num`参数的含义是将原有的播放速度乘以num倍。

#### Player
```player```将```piece```转换为能够在物实播放的电路

#### Midi
`Midi` 类是`Piece`与 *midi文件* 之间的桥梁  
```Python
for physicsLab import *

m = music.Midi("temp.mid")
m.sound() # 播放该midi，此方法会尝试使用plmidi, pygame与系统调用来播放
m.sound(player=music.Midi.PLAYER.PYGAME) # 指定使用pygame播放midi
# 共有PLAYER.plmidi, PLAYER.pygame, PLAYER.os三个参数

m.translate_to_piece() # 将Midi类转换为Piece类

# Midi类有一种特殊的存储数据的类型: .mido.py
# 这个文件导出的音符信息可以方便的进行修改，播放
m.read_midopy("path") # 读取指定path的 .mido.py
m.write_midopy("path") # 导出 .mido.py到指定路径

m.write_midi("path") # 导出midi到指定路径
# 为啥没有read_midi的方法呢? 因为创建一个Midi类的时候就可以读取Midi

# .plm.py: 生成一种可以运行后可以易于编辑, 且运行后就可以生成在物实对应的电路的文件结构
m.write_plm() # 将文件以.plm.py的格式导出
```

## 创建其他类型的实验
创建其他类型的实验主要通过`experiment`或`crt_Experiment`或```open_Experiment```的type参数指定  
type支持的参数如下：  
```Python
type = experimentType.Circuit # 电学实验
type = experimentType.Celestial # 天体物理实验
type = experimentType.Electromagnetism # 电与磁实验
type = experimentType.电学实验
type = experimentType.天体物理实验
type = experimentType.电与磁实验
```
`type`可以什么都不传，此时默认为电学实验

# 物实程序化3  
我也曾试过xuzhengx的物实程序化3，发现爆了文件错误  
与原作者（xuzhegnx）沟通之后了解到：xuzhengx直接把冰如冷的教程拿来索引元件  
这是个大坑，对感兴趣的同学应该有帮助  
[点击查看物实程序化3](https://gitee.com/script2000/temp/blob/master/other%20physicsLab/%E7%89%A9%E5%AE%9E%E7%A8%8B%E5%BA%8F%E5%8C%963.py)