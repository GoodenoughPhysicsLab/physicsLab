# 操作本地实验（存档） experiment

## class Experiment
> Note: 该类不要与`experiment`混淆，`class experiment`仅仅提供了用with操作存档的更好用的api，本质上还是对Experiment类的封装  

`Experiment`类的实例有一些attr:
* `PlSav`: 物实存档json对应的dict
* `is_crt`: 存档本来不存在, 是被创建的
* `is_open`: 存档存在, 是被打开的

1个Experiment类的实例用于操作1个实验存档  
Experiment类的方法会在后面依次介绍

## enum class ExperimentType
ExperimentType是枚举类，用于指定实验类型。目前支持三种类型：
* Circuit 电学实验
* Celestial 天体物理
* Electromagnetism 电与磁

## enum class Category
* Experiment 实验区
* Discussion 讨论区(黑洞区)
* BlackHole 讨论区(黑洞区)

## 打开存档
这是***最推荐的方式***。你可以用with语句打开一个存档
```python
with experiment('example') as exp:
    # to do something
    # 该方式会自动打开存档
    # 若打开失败会自动创建存档
    # 执行完代码之后会自动写入存档
    ...
```
`exp`是一个`Experiment`类的实例，因此你可以是使用exp来轻易地使用`Experiment`类的所有方法

`experiment`还有很多其他参数：  
*  `read`: 是否读取存档已有状态
*  `delete`: 是否删除实验存档
*  `write`: 是否写入存档
*  `elementXYZ`: 是否将该实验设定为元件坐标系
*  `experiment_type`: 若创建实验，支持传入指定实验类型
*  `extra_filepath`: 将存档写入额外的路径
*  `force_crt`: 强制创建一个实验, 若已存在则覆盖已有实验
*  `is_exit`: 是否调用`Experiment.exit`退出实验而不是调用`Experiment.write`或者`Experiment.delete`

> Note: 当你使用`Experiment`导入一个实验而不调用`read`时，你仅仅只会损失实验所有原件的信息，而`force_crt`则会覆盖掉实验的所有信息

> Note: 任何尝试重复导入实验（不论是读取实验还是创建实验）都会导致抛出错误
## 打开存档
***低级api***

你必须指明你要打开的是哪个存档：
```Python
Experiment().open('example.sav') # 根据存档的文件名（也就是xxxx.sav）进行导入
                               #（e.g. e229d7fe-7fa3-4efa-9190-dcb4558a385a.sav）
Experiment().open('example') # 根据存档的实验名（也就是你在物实导入本地实验时看到的实验的名字）进行导入实验
```
但该方法支持读取字符串的形式最完善, 共支持3种:
1.  存档名（在物实保存的实验的名字）
2.  文件名 (默认的存档所在的路径)
3.  自定义存档的路径
> Note: 当open的实验不存在，会抛出错误；

## 创建存档
***低级api***

如果你想要创建一个实验：
```python
Experiment.crt('example')
Experiment.crt("example", experiment_type=ExperimentType.Circuit) # 指定实验类型
```

`experiment_type`参数用于指定创建实验的类型  
如果要创建的实验已经存在，那么该函数会抛出错误  

如果你希望打开存档失败不报错而是创建存档，你可以使用
```Python
Experiment("example") # 该写法等价于下面的写法
Experiment.open_or_crt("example")
```
该函数与`crt_Experiment`传参相同，但`ExperimentType`参数仅在尝试创建存档时有效

***但使用这些api的效果都不如使用`with experiment()`方便***

## 搜索存档&判断存档是否存在
***低级api***

调用`search_Experiment()`判断存档是否存在  
如果存档存在，则会返回存档的文件名  
如果存档不存在，则返回`None`

## 读取存档的内容
被打开的存档不会读取实验的元件与导线的状态。如果你不希望原实验的状态被覆盖，需要调用该方法：  
```Python
from physicsLab import *

with experiment("example", read=True):
    # do something
    ...
```
你也可以这么写：
```Python
from physicsLab import *

with experiment("example") as exp:
    read_plsav(exp)
    # do something
```

## 读取已发布到物实的实验
你可以使用`read_plsav_from_web()`获取已发布到物实上的实验
```Python
from physicsLab import *

with experiment("example") as exp:
    read_plsav_from_web(exp, "642cf37a494746375aae306a", Category.Discussion)
```

## 向物实发布新的实验
如果需要修改实验的tag, 需要手动改`Experiment().PlSav["Summary"]["Tags"]`
```Python
from physicsLab import *

user = web.User(YOUR_UESRNAME, YOUR_PASSWORD)
# 也可使用 web.User(token=YOUR_TOKEN, auth_code=YOUR_AUTH_CODE)

with experiment("example") as exp:
    # do something
    exp.upload(user, Category.Discussion, YOUR_IMAGE_PATH)
```

## 向物实上传已发布的实验
```Python
from physicsLab import *

user = web.User(YOUR_UESRNAME, YOUR_PASSWORD)

with experiment("example") as exp:
    read_plsav_from_web(exp, "642cf37a494746375aae306a", Category.Discussion)
    # do something
    exp.update(user, YOUR_IMAGE_PATH)
```

## 对存档名进行重命名
该方法会同时修改存档名与发布后的标题
```Python
from physicsLab import *

with experiment("example") as exp:
    exp.entitle("new_name")
```

## 保存程序修改后的存档
如果你使用的是`with experiment()`的话，你不需要自己操心这一步骤  
如果你使用的是低级api的话，最后你需要调用该函数往存档里写入程序运行之后的结果：  
```Python
from physicsLab import *

exp = Experiment("example")
# do something
exp.write()
```
`Experiment.write`也有一些参数：
*  `extra_filepath`: 将存档写入额外的路径
*  `ln`: 输出存档的元件字符串是否换行
*  `no_pop`: Experiment在write执行完了之后是否不再操作该存档

我将用一个例子解释`no_pop`的作用：
```Python
from physicsLab import *

exp = Experiment("example")
# do something
exp.write(no_pop=True)

Logic_Input() # ok, create a Logic_Input in experiment "example"
exp.write()
```
``` python
from physicsLab import *

exp = Experiment("example")
# do something
exp.write()

Logic_Input() # error: 不可以在没有实验打开的情况下创建元件
```

## 删除存档
除了创建存档，你也可以删除存档：
```Python
from physicsLab import *

with experiment("example", delete=True):
    # maybe do something
```
你也可以加上`write=False`，不过没必要

更原始的方式是：
```Python
from physicsLab import *

exp = Experiment("example")
# maybe do something
exp.delete()
```

## 停止操作存档
`Experiment.write()`与`Experiment.delete()`都会停止操作存档，但如果你只想放弃本次用程序操作存档(所有对存档的修改都放弃)，你可以调用`Experiment.exit`:
```Python
from physicsLab import *

with experiment("example", is_exit=True):
    # do something
    ...
```

```Python
from physicsLab import *

exp = Experiment("example")
# do something, 但不会改变存档的状态
exp.exit()
```

## 编辑存档的发布信息
使用`edit_publish_info`方法, `title`参数修改发布标题，`description`参数定义发布描述，`wx`参数为是否续写`description`的内容
```python
from physicsLab import *

with experiment("example") as exp:
    exp.edit_publish_info(title="new_title", description="new_description", wx=True)
```

## 用记事本打开存档文件
你也可以打开存档查看：
```Python
with experiment("example") as exp:
    exp.show()
```
仅`Windows`上有效

## 多存档操作
获取当前正在操作的存档:
```Python
get_current_experiment()
```
使用`with experiment`也在多存档操作中被推荐：
```Python
from physicsLab import *

with experiment("example") as exp1:
    # do something in example
    with experiment("example2") as exp2:
        # do something in example2
```

## 设置实验者的观察视角
```Python
Experiment.observe(
    self,
    x: Optional[numType] = None,
    y: Optional[numType] = None,
    z: Optional[numType] = None,
    distance: Optional[numType] = None,
    rotation_x: Optional[numType] = None,
    rotation_y: Optional[numType] = None,
    rotation_z: Optional[numType] = None
):
```
x, y, z为观察者位置
distance为观察者距离物实实验室中心的距离
rotation_x, rotation_y, rotation_z为观察者的角度

## 以physicsLab代码的形式导出实验
```Python
from physicslab import *

with experiment("example") as exp:
    # do something
    exp.export()
```
export有2个参数：
* `output_path`: 导出的文件路径
* `sav_name`: 导出的存档名（即在物实可以直接看到的存档的名字）

## 合并其他实验
```
Experiment.merge(other: Experiment, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None)
```
`other`为要合并的实验  
`x, y, z, elementXYZ`为重新设置要合并的实验的坐标系原点在self的坐标系的位置  
```Python
with experiment("example1") as exp:
    Logic_Input().o - Logic_Output(1, 0, 0, elementXYZ=True).i

    with experiment("example2") as exp2:
        Logic_Output(0, 0, 0.1)
        exp2.merge(exp, 1, 0, 0, elementXYZ=True)
```

## 手动设置输出路径
你可以使用`os.environ["PHYSICSLAB_HOME_PATH"] = "xxx"`来设置`physicsLab`读写存档的默认文件夹

该功能主要为非`Windows`系统设计, 虽然`Windows`上也可以用

该方法也是另一种导入任意路径的存档的一种方法(另一种是直接调用`read_plsav`)

## 暂停实验
你可以使用`Experiment.paused(status: bool)`来暂停实验
```Python
from physicsLab import *

with experiment("example") as exp:
    exp.paused()
    # 如果要解除暂停实验，请使用exp.paused(False)
    ...
```

## 通过用户/实验的id获取时间
```python
from physicsLab import *

print(id_to_time("62d3fd092f3a2a60cc8ccc9e"))
```