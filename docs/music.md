# music

`physicsLab.music`本来是`physicsLab`的模块化电路的其中一个组成部分，不过由于其引入了`mido`这个依赖，所以我单独将其分离出来。  
正常情况下，下载physicsLab时会自动下载mido。如果无法使用mido的话只会无法使用`physicsLab.music`，此时你需要输入该命令下载mido这个依赖：
```bash
pip install mido
```

## 快速使用
通常来说，music模块使用得最多的功能是将一个`midi`文件转化为一个对应的可以在物实运行的音乐电路。  

下面给出代码模板：
```Python
from physicsLab import *

with experiment("example"):
    music.Midi("/your/path/of/midi.mid").to_piece(max_notes=2000).release(-1, -1, 0)
```

上面的示例代码打开或创建了一个名为`example`的存档  
`max_notes`用来控制音乐电路的音符的数量，当`max_notes=None`时，physicsLab会将整首midi乐曲都给处理完。  
`to_piece`还有一些其他的参数: 
* `div_time`: 用来调控生成的音乐电路的节奏。其原理大概是这样的：一个midi文件的时长是固定的，physicsLab以div_time的时长为最小的单位，如果有一堆音符的播放时长在div_time内，那么这些音符会被处理为一个和弦；后面的音符会以同样的原理被处理为下一个音符/和弦，或者下下个，下下下个音符/和弦...  
因此，div_time的值越小，对midi的处理就越精细，但随之而来的影响是乐曲的播放速度变慢。  
* `is_optimize`: 为`False`时将不会把多个音符优化为和弦  
* `fix_strange_note`: 用来优化一些midi中的奇怪的，不符合和弦的，而且总是钢琴音色的，音量贼大的音符  
`release`对应的三个参数分别是x, y, z，个人感觉这`-1, -1, 0`就已经很好用了，没必要修改。  

## class Midi
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

### Midi.sound() # 播放midi
我最推荐使用我为physicsLab专门写的二进制拓展：`plmidi`  
下载plmidi:
```shell
pip install plmidi
```
但`pygame`也有播放midi的功能，你也可以下载pygame：
```shell
pip install pygame
```
如果上述两个package都不存在，那么physicsLab会尝试系统调用播放midi。  

通过调用Midi的sound方法来播放midi：
```python
from physicsLab import *

music.Midi("/your/path/of/midi").sound()
```

> Note: 参数的作用之类的在源码的注释中可以找到  
请注意，`Note`, `Chord`, `Piece`为数据类（只用来存储数据），要转变为物实对应的电路结构需要使用`Piece.release()`方法
## class Note
`Note`是音符类  
其中的`time`参数的含义是***距离播放该音符需要等待多少时间***

注意`time`参数需要大于0  
在midi的表示方法中，time=0表示和弦，但这在physicsLab中是非法的
如果你要表示和弦，请使用`Chord`类

## class Chord
`Chord(self, *notes: Note, time: int)`
* `notes`: 一个音符的列表，列表中的音符将共同构成这个和弦
* `time`: 和弦的time，其对Chord的作用与Note的time一致

## class Piece
```Piece```是乐曲类
这是一个只用来保存数据的类，想要往里面存储音符必须是`Note`，如果是休止符则用`Rest_symbol`表示  
初始化时支持传入`list`，但也支持`append`方法  
将Piece类转换为可以在物实播放的电路，除了使用`Player(piece, x, y, z, elementXYZ)`的方法，也可以使用`piece.release(x, y, z, elementXYZ)`的方法，两者是等价的。  
在`midi`中最容易碰到的是播放速度过慢或过快的问题，你可以调用`Piece().set_tempo(num)`来重新设置播放速度，`num`参数的含义是将原有的播放速度乘以num倍。
```Python
from physicsLab import *

with experiment("example"):
    p = Piece([Note(time=1), Note(time=2)])

    p.release() # 转化为物实的音乐电路
```