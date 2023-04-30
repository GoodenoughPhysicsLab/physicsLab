### 更详细的说明（使用方法）

# physicsLab
## 操作本地实验（存档）
### 打开存档
你必须指明你要打开的是哪个存档：
```Python
open_Experiment('xxx.sav') # 打开存档的文件名
open_Experiment('blabla') # 通过在物实保存的本地实验的名字打开存档
```
请注意，即使你多次调用上述函数，只有被最新打开的存档会被操作  

### 创建存档
如果你想要创建一个实验：
```python
crt_Experiment('存档的名字')
```
请注意，这个函数和```open_Experiment()```一起，只有被最新打开的存档会被操作  

### 读取存档的内容
打开的文件不会读取原实验的状态，如果你不希望原实验的状态被覆盖，需要调用该函数：  
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
os_Experiment()
```

### 删除存档
除了创建存档，你也可以删除存档：
```Python
del_Experiment()
```

### 更优雅的语法
你可以用with语句打开一个存档，且读写存档等重复工作无须手动重复编写
```python
with experiment(
    'physics Lab save name',
    read=True # 读取存档
):
    # do something
    # 该方式会自动打开存档
    # 若打开失败会自动创建存档
    # 执行完代码之后会自动写入存档
    pass
```

## 原件
### 创建元件
所有的原件都被写成了一个类（不过我还在施工，无法支持全部原件）  
你可以调用  
```python
crt_Element(name: str, x = 0, y = 0, z = 0)
```
name可以支持紫兰斋的ModelID的命名方式，也可以支持类的名字  

实际上，physicsLab支持的每一个元件背后都是一个类，因此你也可以用类的实例化来创建原件：  
```python
Logic_Input()  # 创建一个逻辑输入
Logic_Output() # 创建一个逻辑输出
b = Or_Gate()  # 创建一个或门，b保存的是Or_Gate的self
# 千万要注意的是：两个原件的坐标不能重叠！
```

部分原件的ModelID与类的名字：  
<table border="1">
    <tr>
        <th>物实元件的中文名</th>
        <th>物实元件的类名</th>
        <th>物实元件的ModelID</th>
    </tr>
    <tr>
        <td>逻辑输入</td>
        <td>Logic_Input</td>
        <td>logic Input</td>
    </tr>
    <tr>
        <td>逻辑输出</td>
        <td>Logic_Output</td>
        <td>Logic Output</td>
    </tr>
    <tr>
        <td>是门</td>
        <td>Yes_Gate</td>
        <td>Yes Gate</td>
    </tr>
    <tr>
        <td>非门</td>
        <td>No_Gate</td>
        <td>No Gate</td>
    </tr>
    <tr>
        <td>或门</td>
        <td>Or_Gate</td>
        <td>Or Gate</td>
    </tr>
    <tr>
        <td>与门</td>
        <td>And_Gate</td>
        <td>And Gate</td>
    </tr>
    <tr>
        <td>或非门</td>
        <td>Nor_Gate</td>
        <td>Nor Gate</td>
    </tr>
    <tr>
        <td>与非门</td>
        <td>Nand_Gate</td>
        <td>Nand Gate</td>
    </tr>
    <tr>
        <td>异或门</td>
        <td>Xor_Gate</td>
        <td>Xor Gate</td>
    </tr>
    <tr>
        <td>同或门</td>
        <td>Xnor_Gate</td>
        <td>Xnor Gate</td>
    </tr>
    <tr>
        <td>蕴含门</td>
        <td>Imp_Gate</td>
        <td>Imp Gate</td>
    </tr>
    <tr>
        <td>蕴含非门</td>
        <td>Nimp_Gate</td>
        <td>Nimp Gate</td>
    </tr>
    <tr>
        <td>半加器</td>
        <td>Half_Adder</td>
        <td>Half Adder</td>
    </tr>
    <tr>
        <td>全加器</td>
        <td>Full_Adder</td>
        <td>Full Adder</td>
    </tr>
    <tr>
        <td>二位乘法器</td>
        <td>Multiplier</td>
        <td>Multiplier</td>
    </tr>
</table>
未完待续……  
（如果你着急想看某个原件对应的名字的话，可以直接在源代码的```eletricity\elementClass```中查看所有的元件类）  


### 获取元件
我们往往难以获取一些元件的self，此时我们就可以用```get_Element()```：
```python
get_Element(x=0, y=0, z=0)
get_Element(index=1)
get_Element(0, 0, 0) # 依然是坐标索引，对应xyz
get_Element(1) # 依然是index索引
```
当原件的坐标重叠时，此时会返回一个含所有坐标重叠的原件的list  

元件的```index```会从1开始，每生成一个元件就会加1
```Python
No_Gate() # index = 1
Or_Gate(0, 0, 0.1) # index = 2
```
返回值是这个坐标对应原件的self，若不存在抛出Error  

### 删除元件
我们也可以删除原件：
```python
from physicsLab import *
a = Logic_Input()
del_Element(a) # input: element's self, output: None
```
因为传入参数为self，所以必要时也需要用get_Element。

### 元件坐标系
物实提供的坐标系的单位长度与元件尺寸出入较大，因此physicsLab提供了专门为元件尺寸定制的原件坐标系。  
元件坐标系的x, y单位长度为1个是门的长、宽，z的单位长度为物实坐标系的0.1  
此函数将x, y, z的大小设置为原件坐标系
```Python
from physicsLab import *
set_elementXYZ(True)
```
当你只希望某个元件是元件坐标系，而其他元件不受影响时，physicsLab也提供了对应的机制
```Python
from physicsLab import *
And_Gate(0, 0, 0.1) # 这个或门的坐标为物实坐标系
Or_Gate(0, 1, 0, elementXYZ=True) # 这个或门的坐标为元件坐标系，其他元件也一样
```
你也可以使用该函数获取是否为元件坐标系：
```python
from physicsLab import *
is_elementXYZ() # return a bool
```

### Methods
所有的元件都有一些方法来操作
```python
from physicsLab import *
a = Logic_Input()

a.set_highLevel() # 将逻辑输入设置为输出为1
a.get_Position()
a.type()
a.father_type()
a.get_Index()
a.set_HighLeaveValue(3)
a.set_LowLeaveValue(0)
a.print_arguments()
```

## 导线
连接导线提供了2种方式  
第一种：  
```Python
from physicsLab import *
element = Logic_Input()
element2 = Logic_Output()

crt_Wire(element.o, element2.i, color='红') 
# color暂时只支持中文的 "黑", "蓝", "红", "绿", "黄"
# 不传入color参数的话，color默认为蓝色
```
所有原件都定义得有自己的引脚名称，这里举个例子：  
```python
from physicsLab import *
a = Or_Gate(0.1, 0.1, 0)
crt_Wire(a.o, a.i_up)
```
引脚的命名规范：（适用于逻电）  
1个输入引脚：i  
2个输入引脚：i_up, i_low  
3个输入引脚：i_up, i_mid, i_low  
4个输入引脚：i_up, i_upmid, i_lowmid, i_low  
输出是一样的，仅仅换成了o_xxx罢了。  
模电的命名可能是根据左右引脚来区分的，也就是l_up, r_low之类的，也可能是根据物实的引脚名  
如果以后有时间的话，也会打个表  

另一种连接引脚的方式是不推荐使用的老函数：  
```Python
old_crt_wire(SourceLabel, SourcePin: int, TargetLabel, TargetPin: int, color = "蓝") -> None
```
连接导线的方式是更偏于物实存档的原始方案，即用数字来表示某个引脚  
下面呈现部分原件引脚图（第一种其实就是对这个老函数更方便的封装）：  
```diff
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
  
除了创建导线外，也可以删除导线：  
```Python
from physicsLab import *
element = Logic_Input()
element2 = Logic_Output()

del_Wire(element.o, element2.i)
```
使用方法与crt_Wire一模一样  
  
（这篇readme应该介绍了大部分常用功能）

## 模块化电路

# 物实程序化3  
我也曾试过物实程序化3，发现爆了文件错误  
与原作者（xuzhegnx）沟通之后了解到：xuzhengx直接把冰如冷的教程拿来索引原件  
这是个大坑，对感兴趣的同学应该有帮助