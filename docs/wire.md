# 导线 wire

## 连接导线
连接导线提供了2种方式  
1. 调用`crt_wire`函数
```Python
from physicsLab import *

with experiment(OpenMode.load_by_sav_name, "example"):
    _input = Logic_Input()
    _output = Logic_Output()

    crt_wire(_input.o, _putput.i, color="red") # 连接导线
# `o`是`_input`的引脚, 是output的缩写
# `i`是`_output`的引脚, 是input的缩写
# color暂时只支持中文的 "黑", "蓝", "红", "绿", "黄" 与 对应颜色的英文
# 不传入color参数的话，color默认为蓝色
```

2. 使用减号
之所以做了这个是因为我觉得`-`与导线很像

> Note: 有时候IDE会认为重载后的减法运算后没有变量去接受返回值, 因此会给出警告
```Python
element.o - element2.i
```
通过这种方法连接的导线只能为蓝色，但该用法还可以和`lib.Wires`的导线类型混合使用，因此功能更加强大

所有元件都定义得有自己的引脚名称，在[elements.md](elements.md)中记录得有所有引脚

## 删除导线
除了创建导线外，也可以删除导线：
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example"):
    element = Logic_Input()
    element2 = Logic_Output()

    del_wire(element.o, element2.i)
```
删除导线时不需要提供颜色参数
