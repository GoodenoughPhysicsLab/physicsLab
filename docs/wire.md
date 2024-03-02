# 导线 wire

## 连接导线
连接导线提供了2种方式  
第一种 :  
```Python
from physicsLab import *

with experiment("example"):
    _input = Logic_Input()
    _output = Logic_Output()

    crt_Wire(_input.o, _putput.i, color='红') # 连接导线
# `o`是`_input`的引脚, 是output的缩写
# `i`是`_output`的引脚, 是input的缩写
# color暂时只支持中文的 "黑", "蓝", "红", "绿", "黄" 与 对应颜色的英文
# 不传入color参数的话，color默认为蓝色
```

另一种方法 :  
之所以做了这个是因为我觉得`-`与导线很像  
> <font color=red>Note: </font>有时候IDE会认为重载后的减法运算后没有变量去接受返回值, 因此会给出黄色波浪线
```Python
element.o - element2.i
```
但通过这种方法连接的导线只能为蓝色  

所有元件都定义得有自己的引脚名称，这里举个例子：  
```python
from physicsLab import *
a = Or_Gate(0.1, 0.1, 0)
crt_Wire(a.o, a.i_up)
```

引脚也可以在[所有元件.md](elements.md)中找到

## 删除导线
除了创建导线外，也可以删除导线：  
```Python
from physicsLab import *

with experiment("example"):
    element = Logic_Input()
    element2 = Logic_Output()

    del_Wire(element.o, element2.i, color="red")
```
使用方法与crt_Wire一模一样  
> <font color=red>Note: </font>目前删除导线时仍然需要提供绝对准确的颜色参数, 未来可能会考虑只需用提供两个引脚就行了

## others
尽管我尽量避免讲一些实现, 但这个我还是忍不住想讲一下这个  
在以前有另一个更原始的函数用来连接导线( 在`physicsLab v1.2.2`之后，该函数被移除 ) :
```Python
old_crt_wire(SourceLabel, SourcePin: int, TargetLabel, TargetPin: int, color = "蓝") -> None
```
连接导线的方式是更偏于物实存档的原始方案，即用数字来表示某个引脚  
下面呈现部分元件引脚图（第一种其实就是对这个老函数更方便的封装）：  
```
D触发器：     两引脚门电路：    比较器:     三引脚门电路：     全加器：     继电器：
2    0         0     1       1            0                2    0      0    4
                                   2            2          3             1
3    1                       0            1                4    1      2    3

逻辑输入、逻辑输出：
0  
  
二位乘法器：  
4  0  
5  1  
6  2  
7  3  
```
很明显比第一种更麻烦  