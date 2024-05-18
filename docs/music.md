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

## class Note

## class Chord

## class Piece

## class Player