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
1. 增加android的支持
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
1.  完成`Midi.write_plm`的主要逻辑

## 1.3.4
1.  进一步完善了Midi类（translate_to_piece）
2.  优化了plmidi的播放效果（使用pybind11代替了Python.h）

## 1.3.5
1.  改进`Midi.sound`的播放机制,使`plmidi`与`pygame`的播放效果相同

## 1.3.6
1.  使用了物实`v2.4.7`的特性优化模块化音乐电路，这也意味着旧版本物实不支持`physicsLab`生成的电路
2.  修复了颜色打印的Bug，增加了`close_color_print()`以关闭颜色打印
3.  更改了在`Android`上创建存档的行为，同时理论上支持了其他操作系统
4.  更新了`write_Experiment`的`extra_filepath`
5.  更新了`Piece.write_midi`, `Piece.traslate_to_midi`
6.  更新了简单乐器播放多个音符的机制:`Simple_Instrument.add_note`与获取简单乐器的和弦:`Simple_Instrument.get_chord()`
7.  实装了`Chord`类，同时禁止了旧有的和弦表示方式

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
2.  一些bugfix

# 1.4.4
1.  与`plmidi`兼容性更好的调用方式
2.  部分优化了和弦的音量生成规则, 但更好的音量生成需等待物实增加单独控制简单乐器中的每个音符的音量的支持
3.  删除导线不再需要提供颜色信息
4.  全局设置警告状态
5.  `Simple_Instrument`新增在init时设置和弦的方法

# 1.4.5
1.  增加了更多的元件
2.  重复连接的导线将不会被连接
3.  删除旧式函数调用的`xxx_Experiment`等api (不兼容更新)
4.  删除自动增加`# -*- coding: utf-8 -*-`的机制

# 1.4.6
1.  修复重复连接导线时的bug
2.  将`music.Midi`的`read_midopy`移动到`__init__`中
3.  修复`export`的bug
4.  将`Piece.translate_to_midi`改名为`Piece.to_midi`，`Midi.translate_to_piece`改名为`Midi.to_piece`（不兼容更新）

# 1.4.7
1.  新增`Experiment.merge`
2.  元件新增`experiment`属性
3.  `get_Element`增加`default`参数
4.  重命名`unit`为`lib` （不兼容更新）
5.  `crt_Element`新增`*args`与`**kwargs`用来传递创建一些元件需要的额外的参数

# 1.4.8
1.  删除`Piece`类的冗余参数
2.  新增休止符类`Rest_symbol`
3.  `to_piece`新增`is_optimize`参数，用来控制是否优化为和弦
4.  `to_piece`新增`is_fix_strange_note`参数，用来控制是否修正一些midi中奇怪的音符
5.  新增设置环境变量`PHYSICSLAB_HOME_PATH`
6.  增加`crt_Wire`自连接导线的检查

# 1.4.9
1.  重命名`Midi.to_piece`的`is_fix_strange_note`参数为`fix_strange_note`（不兼容更新）
2.  更智能的`Midi`的`div_time`参数的自动推测

# 1.4.10
1.  `Midi`类支持直接导入文件对象(io.IOBase)
2.  `Midi.to_piece`与`Midi.write_plpy`新增`notes_filter`参数，该参数要求传入一个2个参数（第一个为instrument, 第二个为velocity），输出为bool的函数，用来过滤音符
3.  `Note`支持`C3`这种风格的构造
4.  增加`lib.Rising_edge_trigger`, `lib.Falling_edge_trigger`, `lib.Edge_trigger`
5.  增加`Experiment.paused`
6.  增加对`web-api`的操作的更高级api
7.  增加`Tag`(enum class)
8.  增加`Category`
9.  增加`lib.Super_AndGate`, `lib.Tick_Counter`

# 1.4.11
1.  更多`web`api
2.  增加`Experiment.read_from_web`
3.  增加`Experiment.upload`, `Experiment.update`

# 1.4.12
1.  增加`lib.MultiElements`等等
2.  增强了减号连接导线的功能(`Pin` - `unitPin`)
3.  修复`CircuitBase.is_bigElement`
4.  新增`Experiment.edit_tags`
5.  新增对`sensor`的支持

## 1.4.13
1.  `web.get_comments`增加`take`与`skip`参数

## 1.4.14
1.  公开了`id_to_time`
2.  新增`get_warned_messages`, `get_banned_messages`

# 1.4.15
1.  重命名`set_Position`为`set_position`, `set_Rotation`为`set_rotation`, `get_Position`为`get_position`, `get_Index`为`get_index` (不兼容更新)
2.  实装部分对天体物理实验的支持
3.  电学元件新增`.rename`方法
4.  电阻与电阻箱增加`set_resistor`
5.  修复了`music`的鼓点生成规则的bug
6.  新增`web.CommentsIter`

# 1.4.16
1.  完善了`web.CommentsIter`
2.  新增了电与磁实验的支持

# 1.4.17
1.  新增`web.get_avatar`, `get_avatars`
2.  `Experiment.write`新增`no_print_info`参数
3.  新增`User.get_relations`与`User.get_user`新增`name`参数

# 1.4.18
1.  新增`RelationsIter`

# 1.4.19
1.  优化了`RelationsIter`

# 1.4.20
1.  改`get_avatars`为`AvatarsIter`, `get_banned_messages`为`BannedMsgIter`, `get_warned_messages`为`WarnedMsgIter` (不兼容更新)
2.  优化`RelationsIter`

# 1.4.21
1.  新增`User.recive_bonus`, `User.rename`, `User.star_content`

# 1.5.0
1. 新增`web.ManageMsgIter`
2. `web/api.py`几乎都增加了以`async_`开头的支持协程的风格的api
3. 重命名`get_Experiment`为`get_current_experiment`
4. 重命名`search_Experiment`为`search_experiment`
5. 删除`get_Element`, `crt_Element`, `del_Element`, `count_Element`, `clear_Element`
6. 新增`Experiment.get_element`, `Experiment.crt_element`, `Experiment.del_element`, `Experiment.count_element`, `Experiment.clear_element`
7. 删除`music.Player`，其功能完全由`music.Piece.release`代替
8. 重命名`*_Wire`为`*_wire`, `*_Wires`为`*_wires`
9. 重命名`set_HighLevelValue`为`set_high_level_value`, `set_HighLevel`为`set_high_level`, 对lowLevel也同理

## 1.5.1
1. 修复`User.async_*`的阻塞问题
2. 修复`webutils.py`的大多数迭代器在ctrl+c时无法退出的问题
3. 废弃`warning_status`, 改为支持`built-in warnings module`
4. `get_plAR_version`改为返回`Tuple[int, int, int]`
5. 为检测到安装物实时改为警告
6. `User.post_comment`的自动探测回复增加多语言支持
7. `User.get_experiment`现在可以自动执行`get_summary`
8. 新增`User.remove_comment`, `User.modify_info`

## 1.6.0
1.  重命名`web.ManageMsgIter`为`web.NotificationsMsgIter`
2.  移除`web.Bot`
3.  新增`add_graph_to`函数， 移除`Experiment.graph`
4.  新增`crt_element`函数, 移除`Experiment.crt_element`
5.  新增`del_element`函数, 移除`Experiment.del_element`
6.  新增`count_elements`函数, 移除`Experiment.count_elements`
7.  新增`clear_elements`函数, 移除`Experiment.clear_elements`
8.  新增`read_plsav`函数, 移除`Experiment.read`
9.  新增`read_plsav_from_web`函数, 移除`Experiment.read_from_web`
10. 废弃`get_element`, 新增`get_element_from_positon`, `get_element_from_index`

## 1.6.1
1.  `web`的部分迭代器增加`async for`支持
2.  some bug-fix

## 1.6.2
1.  修复test_pl被意外打包进pip的问题
2.  修复由于Python更新导致_async_wrapper报错的问题

## 1.6.3
1.  不再需要从pip中下载`mido`依赖
2.  修复`read_plsav_from_web`无法读取天体实验与电与磁实验的问题

## 2.0.0
1.  移除`Experiment.show`
2.  废弃`read_plsav_from_web`, `Experiment.open`, `Experiment.open_or_crt`, `Experiment.crt`, 相似功能直接由`Experiment`提供
3.  新增`enum class OpenMode`
4.  重命名`Experiment.write`为`Experiment.save`
5.  重命名`read_plsav`为`load_elements`
6.  移除`Experiment.save`的`no_pop`参数
7.  移除`Experiment.delete`, `Experiment.exit`增加`delete`参数
8.  移除`Experiment.get_element_from_identifier`，新增`get_element_from_identifier`函数
9.  将`Experiment.save`的`extra_filepath`改为`target_path`
10. 移除`Experiment.save`的`ln`参数
11. 支持`with Experiment`，废弃`with experiment`
12. `class Experiment` 实验性地加入`stable`支持, 未来`class Experiment`会更加谨慎地做出不兼容更新
13. `class Experiment`的构造函数支持默认导入元件了，`load_elements`函数被废弃
14. `clear_elements`, `del_element`, `count_elements`, `get_element_from_position`, `get_element_from_index`, `get_element_from_identifier`, `crt_element`改为`Experiment.clear_elements`, `Experiment.del_element`, `Experiment.get_elements_count`, `Experiment.get_element_from_position`, `Experiment.get_element_from_index`, `Experiment.get_element_from_identifier`, `Experiment.crt_element`
15. `pin1 - pin2`被废弃，`crt_wire`现在支持多个参数了
16. `class experiment`被废弃
17. 一些元件增加了`set_properties`方法，并且支持在构造函数中传入这些属性
18. 现在可以通过修改Simple_Instruments.pitches来修改和弦
19. 电学元件新增lock方法
20. 移除元件坐标系`set_O`
21. 元件新增`identifier`参数用于指定元件的id
22. 废弃`elementXYZ.is_elementXYZ()`
23. 重命名`Experiment.exit`为`Experiment.close`

## 2.0.1
1.  不再默认省略`crt_wires`的命名空间`lib`
2.  重命名`Translatexyz`， `XYZTranslate`为`native_to_elementXYZ`, `elementXYZ_to_native`, 新增`ElementXYZ`
3.  重命名`lib.Equal_to`为`lib.EqualTo`
4.  移除`Category.BlackHole`, `User.get_user`的`positional-argument`
5.  `Experiment.get_element_from_position`现在只会返回list (不兼容更新)

## 2.0.2
1. 新增`web.User.remove_experiment`
2. 新增`lib.analog_circuit`

## 2.0.3
1. 元件增加`zh_name()`方法
2. 增加对匿名存档的支持(Experiment.is_anonymous_sav)
3. 修复windows locale导致的bug
4. 改进报错信息

## 2.0.4
1. `Experiment`增加`.delete`方法
2. `class User`的构造函数被破坏性更新
3. 新增`GetUserMode`
4. 移除`close_color_print`, _colorUtils为内部模块, 在外部请谨慎使用

# 2.0.5
