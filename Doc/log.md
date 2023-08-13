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

## coming soon
1.  实装Midi类（与piece类的转换与导出midi，播放midi）
2.  Track类增加append方法
3.  优化了乐器矩阵的基础架构
4.  `self.set_Position`增加了对元件坐标系的支持
5.  增加了`Midi.set_tempo`方法