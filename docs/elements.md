# 所有元件 elements
所有元件共有的基类：`ElementBase`

所有元件共有的`attribute`:
* .data: 元件的存档信息
* .experiment: 元件所在的实验

所有元件都有的`method`:
* set_position: 设置元件的位置
* get_position: 获取元件的位置
* get_index: 获取元件是第几个被创建的 (从1开始计数)

## 电学实验
电学实验元件的基类：`CircuitBase`

电学元件都有的`method`:
* set_rotation # 设置元件的角度
* rename # 重命名元件
* lock(status: bool): 更改元件锁定的状态

电学元件都有的`attribute`:
* .is_bigElement # 是否是大体积元件
* .is_elementXYZ # 是否是元件坐标系
* .modelID # 存档信息中的`ModelID`
* .properties # 存档信息中的`Properties`

### 逻辑电路

逻辑电路元件都有的`method`:
* set_high_level_value # 设置高电平的值
* get_high_level_value # 获取高电平的值
* set_low_level_value # 设置低电平的值
* get_low_level_value # 获取高电平的值

## 天体物理实验
天体物理元件的基类：`PlanetBase`

天体物理元件都有的`method`:
* set_velocity # 设置速度
* set_acceleration # 设置加速度

## 电与磁实验
电与磁元件的基类：`ElectromagnetismBase`

对每个元件的细致介绍，请[点这里](./docsgen/elements.md)查看
