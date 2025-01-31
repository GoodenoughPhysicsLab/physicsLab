# quick start

## 第一个程序
元件浮空几乎成为了修改存档的代名词，因此，就让我们从创建一个悬空的逻辑输入开始吧：
```Python
from physicsLab import *

with Experiment(OpenMode.crt, "example", ExperimentType.Circuit, force_crt=True):
    Logic_Input(0, 0, 0.1)
```
执行程序，打开物实，打开名为example的实验查看奇迹

这个程序会首先检查本地是否存在实验“example”，若不存在则创建，否则会覆盖已有的`example`存档的状态，强行创建一个名为"example"的实验

`with`对应的缩进内写的代码会被视为是对实验`example`的操作，比如`Logic_Input(0, 0, 0.1)`对应着创建一个坐标为`x=0, y=0, z=0.1`的逻辑输入

除此之外也可以只创建实验(若实验存在则抛出异常), 只打开实验(若实验不存在则抛出异常)，通过捕获异常开可以实现打开的实验不存在就创建实验
`class Experiment`一共有4种打开存档的方式，请查看[experiment.md](experiment.md)

## 创建元件
创建元件非常简单：
```Python
from physicsLab import *

with Experiment(OpenMode.crt, "example", ExperimentType.Circuit, force_crt=True):
    Logic_Output(0.1, 0.2, 0) # 创建一个逻辑输出
```
更多的元件请在[elements.md](./elements.md)中查看

更多的对元件进行操作的方式请查看[elements.md](./elements.md)

## 元件坐标系
物实已有的坐标表示方法往往稍大于一个元件的尺寸，而元件坐标系可以解决这个问题：
```Python
from physicsLab import *

with Experiment(OpenMode.crt, "example", ExperimentType.Circuit, force_crt=True):
    Logic_Input(0, 0, 1, elementXYZ=True)
```
也可以在全局设置使用元件坐标系, 更多用法请查看[elements.md](./elements.md)

## 连接导线
```Python
from physicsLab import *

with Experiment(OpenMode.crt, "example", ExperimentType.Circuit, force_crt=True):
    a = Logic_Input(-1, 0, 0, elementXYZ=True)
    b = Logic_Output(1, 0, 0, elementXYZ=True)
    crt_wire(a.o, b.i) # a的输出引脚 与 b的输入引脚 连接导线
```
更多引脚的信息请查看[elements.md](./elements.md)
更多用法请查看[wire.md](./wire.md)

## 通过网络api与物实交互
仿照客户端的行为，向物实服务器发送请求，获取物实服务器的响应
```Python
from physicsLab import *

# 登录物实账号
user = web.User(YOUR_EMAIL, YOUR_PASSWORD)
# 或者，使用token & authcode登录
# user = web.User(token=YOUR_TOKEN, auth_code=YOUR_AUTHCODE)

print(user.get_messages()) # 获取收件箱的消息
```
更多用法请查看[web.md](./web.md)
