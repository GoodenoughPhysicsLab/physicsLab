## 历史重大成就
1. 2023-1-5 改存档实验成功
2. 2023-1-12 physicsLab上传至gitee
3. 2023-2-25 引入git管理physicsLab
4. 2023-3-17 physicsLab上传至pypi（不可使用）
5. 2023-3-19 physicsLab上传至pypi的版本可以使用
6. 2023-4-8 physicsLab上传至github
7. 2023-4-15 python调用dll实验成功
8. 2023-4-30 增加模块化电路：D触流水灯
9. 2023-5-4 ```python build``` c拓展实验成功
10. 2023-6-18 将```@element_Init_HEAD```改为metaclass: ```electricityMeta```
11. 2023-6-18 c/cpp调用Python实验成功

## 1.3.0
1. 增加android的支持 2023-6-22
2. 增加对电与磁实验的简单支持
3. 增加了模块化电路命名空间union
4. 增加了模块化电路音乐电路与music命名空间
5. experiment()新增write参数

## 1.3.0.1 & 1.3.1
1.  增加对`P-MOSFET`元件的支持
2.  增加`from physicsLab.union import *`来省略union命名空间的书写
3.  增加单个元件判断是否为元件坐标系的方法：`self.is_elementXYZ`
4.  新增只读非门`Const_NoGate`
5.  `crt_Wire`支持传入英文color参数
6.  新增`_fileGlobals`命名空间（不推荐访问）

## 1.3.2
1.  实装Midi类（与piece类的转换与导出midi，播放midi）
2.  Track类增加append方法
3.  优化了乐器矩阵的基础架构
4.  `self.set_Position`增加了对元件坐标系的支持
5.  增加了`Midi.set_tempo`方法

## 1.3.3
1.  完成Midi.write_plm的主要逻辑

## 1.3.4
1.  进一步完善了Midi类（translate_to_piece）
2.  优化了plmidi的播放效果（使用pybind11代替了Python.h）

## 1.3.5
1.  改进`Midi.sound`的播放机制,使`plmidi`与`pygame`的播放效果相同

## 1.3.6
1.  元件类增加`hook`
2.  使用了物实`v2.4.7`的特性优化模块化音乐电路，这也意味着旧版本物实不支持`physicsLab`生成的电路
3.  修复了颜色打印的Bug，增加了`close_color_print()`以关闭颜色打印
4.  更改了在`Android`上创建存档的行为，同时理论上支持了其他操作系统
5.  更新了`write_Experiment`的`extra_filepath`
6.  更新了`Piece.write_midi`, `Piece.traslate_to_midi`
7.  更新了简单乐器播放多个音符的机制:`Simple_Instrument.add_note`与获取简单乐器的和弦:`Simple_Instrument.get_chord()`
8.  实装了`Chord`类，同时禁止了旧有的和弦表示方式

## 1.3.7
1.  修复了由`typing`导致的问题
2.  实装了支持`Chord`的`Piece.write_midi`

# 1.4.0
1. `traslate_to_midi`增加了对音量的支持
2. 移除了`Note.time=0`的表示方式
3. 将`.plm.py`更名为`.pl.py`
4. 将传统的函数式实验存档读写改为了`class Experiment`的形式
5. 在一些小的行为上进行了优化, 使编写更加直观

# 1.4.1
1. 优化了`Experiment.delete()`的行为
2. 优化了`Player`生成音符的音量的效果

# 1.4.2
1.  新增了`get_Experiment`
2.  修复了`Experiment.read`的bug

# 1.4.3
1.  `plmidi`新增播放进度条