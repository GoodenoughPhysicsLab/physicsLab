# physicsLab

*  [操作本地实验（存档） experiment](experiment.md)
*  [元件 element](element.md) & [所有元件 elements](elements.md)
*  [导线 wire](wire.md)

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
参数的作用之类的在源码的注释中可以找到
请注意，`Note`, `Chord`, `Piece`为数据类（只用来存储数据），要转变为物实对应的电路结构需要使用`release()`方法，但通常来说你只需用调用`Piece.release()`或者`Player`

#### Note
`Note`是音符类  
其中的`time`参数的含义是***距离播放该音符需要等待多少时间***

#### Piece
```Piece```是乐曲类
这是一个只用来保存数据的类，想要往里面存储音符必须是`Note`，如果是休止符则用`None`表示  
初始化时支持传入`list`，但也支持`append`方法  
将Piece类转换为可以在物实播放的电路，除了使用`Player(piece, x, y, z, elementXYZ)`的方法，也可以使用`piece.release(x, y, z, elementXYZ)`的方法，两者是等价的。  
在`midi`中最容易碰到的是播放速度的问题，你可以调用`Piece().set_tempo(num)`来重新设置播放速度，`num`参数的含义是将原有的播放速度乘以num倍。
```Python
from physicsLab import *
from physicsLab.union import * # from import所有的模块化电路

with experiment("测逝"):
    p = Piece([Note(time=1)])
    p.append(Note(time=2))

    p.release()
```

#### Player
`player`将`piece`转换为能够在物实播放的电路

#### Midi
`Midi` 类是`Piece`与 *midi文件* 之间的桥梁  
```Python
from physicsLab import *

m = music.Midi("example.mid")
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

# .pl.py: 生成一种可以运行后可以易于编辑, 且运行后就可以生成在物实对应的电路的文件结构
m.write_plpy() # 将文件以.pl.py的格式导出
```

## 创建其他类型的实验
创建其他类型的实验主要通过`experiment`或`crt_Experiment`或```open_Experiment```的type参数指定  
type支持的参数如下：  
```Python
type = experimentType.Circuit # 电学实验
type = experimentType.Celestial # 天体物理实验
type = experimentType.Electromagnetism # 电与磁实验
```
`type`可以什么都不传，此时默认为电学实验

## 其他
### 关闭打印的颜色
因为`windows`的颜色打印很容易出问题，因此提供了关闭颜色打印的函数：`close_color_print()`  

# 物实程序化3  
我也曾试过xuzhengx的物实程序化3，发现爆了文件错误  
与原作者（xuzhegnx）沟通之后了解到：xuzhengx直接把冰如冷的教程拿来索引元件  
这是个大坑，对感兴趣的同学应该有帮助  
[点击查看物实程序化3](https://gitee.com/script2000/temp/blob/master/other%20physicsLab/%E7%89%A9%E5%AE%9E%E7%A8%8B%E5%BA%8F%E5%8C%963.py)