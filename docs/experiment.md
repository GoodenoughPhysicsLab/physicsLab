# 操作本地实验（存档） experiment

## class Experiment
`Experiment`类的实例有一些attr:
* `PlSav`: 物实存档json对应的dict

1个Experiment类的实例仅用于操作1个实验存档,  无法同时创建2个对应同一个实验的Experiment实例。
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

## enum class OpenMode
用Experiment打开存档的模式
*   load_by_sav_name : 存档的名字 (在物实内给存档取的名字)
*   load_by_filepath : 用户自己提供的存档的完整路径
*   load_by_plar_app : 通过网络请求从物实读取的存档
*   crt : 新建存档

## 打开存档
这是***最推荐的方式***。你可以用with语句打开一个存档
```python
# 参数含义: 打开模式为打开已经存在的存档，存档名为example
with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    # 使用with Experiment会自动导入元件信息 (也就是默认调用 load_elements)
    # 执行完代码之后会自动保存存档并使expe退出对存档的操作（无法再操作存档）
    ''' do something '''
```
`expe`是一个`Experiment`类的实例，因此你可以通过`expe`来轻易地使用`Experiment`类的所有方法来操作存档

> Note: 当你使用`Experiment`导入一个实验而不调用`load_elements`时，你仅仅只会损失实验所有原件的信息，而`force_crt`则会覆盖掉实验的所有信息

> Note: 任何尝试重复导入实验（不论是读取实验还是创建实验）都会导致抛出错误

更底层的使用方式是，你必须指明你要打开的是哪个存档：
```Python
from physicsLab import *
Experiment(OpenMode.load_by_filepath, "/your/path/of/sav") # 根据存档的文件名（也就是xxxx.sav）进行导入
                               #（e.g. e229d7fe-7fa3-4efa-9190-dcb4558a385a.sav）
Experiment(OpenMode.load_by_sav_name, "example") # 根据存档的实验名（也就是你在物实导入本地实验时看到的实验的名字）进行导入实验
Experiment(OpenMode.load_by_plar_app, "642cf37a494746375aae306a", Category.Discussion)
```

但该方法支持读取字符串的形式最完善, 共支持3种:
1.  存档名（在物实保存的实验的名字）
2.  自定义存档的路径
3.  读取物实服务器上的实验

> Note: 当open的实验不存在，会抛出错误；

> Note: 该低级api不会导入元件信息，需要手动调用`load_elements`

## 创建存档
***低级api***

如果你想要创建一个实验：
```python
# 参数含义: 打开模式为创建新存档；存档名为example；实验的类型为电学实验；如果要创建的实验已经存在，将会抛出异常
with Experiment(OpenMode.crt, "example", ExperimentType.Circuit, force_crt=False) as expe:
    # 使用with Experiment的话，执行完代码之后会自动保存存档并使expe退出对存档的操作（无法再操作存档）
    ...
```
上面代码等价于:
```python
from physicsLab import *
expe = Experiment(OpenMode.crt, "example", ExperimentType.Circuit, force_crt=False)
# do something
expe.save()
expe.exit()
```

* `experiment_type`参数用于指定创建实验的类型
* `force_crt` (默认为`False`)：
  * `True`时，如果要创建的实验已经存在，则会删除那个实验并创建一个新实验
  * `False`时，如果要创建的实验已经存在，将会抛出异常

如果你希望打开存档失败后创建存档，你可以使用
```Python
try:
    expe = Experiment(OpenMode.load_by_sav_name, "example")
except ExperimentNotExistError:
    expe = Experiment(OpenMode.crt, "example", ExperimentType.Circuit)
```

## 搜索存档&判断存档是否存在
***低级api***

调用`search_Experiment()`判断存档是否存在  
如果存档存在，则会返回存档的文件名  
如果存档不存在，则返回`None`

## 读取存档的内容
被打开的存档不会读取实验的元件与导线的状态。如果你不希望原实验的状态被覆盖，需要调用该方法：
```Python
from physicsLab import *

expe = Experiment(OpenMode.load_by_sav_name, "example")
load_elements(expe)
# do something
expe.save()
expe.exit()
```

> Note: with Experiment()默认会导入存档的元件信息, 因此更加方便好用

## 向物实发布新的实验
如果需要修改实验的tag, 可以使用`Experiment.edit_tags`
```Python
from physicsLab import *

user = web.User(YOUR_UESRNAME, YOUR_PASSWORD)
# 也可使用 web.User(token=YOUR_TOKEN, auth_code=YOUR_AUTH_CODE)

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    # do something
    # 参数含义：上传该实验到物实的哪个用户, 是实验区还是讨论区, 封面图片的路径
    expe.upload(user, Category.Discussion, YOUR_IMAGE_PATH)
```

## 向物实上传已发布的实验
```Python
from physicsLab import *

user = web.User(YOUR_UESRNAME, YOUR_PASSWORD)

with Experiment(OpenMode.load_by_plar_app, "642cf37a494746375aae306a", Category.Discussion) as expe:
  expe.update(user, YOUR_IMAGE_PATH)
  expe.exit() # 这里手动调用了expe.exit()之后, `with Experiment`在退出的时候就不会执行默认的保存存档并退出的操作了
              # 也就是说，这样写，Experiment.save() 不会被调用
```

## 对存档名进行重命名
该方法会同时修改存档名与发布后的标题
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    expe.entitle("new_name")
```

## 保存存档的状态
如果你使用的是`with Experiment`的话，你通常不需要自己操心这一步骤

```Python
from physicsLab import *

exp = Experiment(OpenMode.load_by_sav_name, "example")
# do something
exp.save()
exp.exit()
```
`Experiment.save`也有一些参数：
*  `target_path`: 将存档写入自己指定的路径
*  `ln`: 输出存档的元件字符串是否换行
*  `no_print_info`: 是否打印写入存档的元件数, 导线数(如果是电学实验的话)

不过请注意，`with Experiment`支持自定义退出的方式:
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    # do something
    expe.exit() # expe已经退出对存档的操作了, 就不会再在退出with的时候调用expe.save()了
```

## 删除存档
除了创建存档，你也可以删除存档：
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    # maybe do something
    expe.exit(delete=True) # 在退出操作存档的时候执行删除存档的操作
    # 并且由于已经手动调用了expe.exit(), 在退出with的时候不会调用expe.save()了
```

更原始的方式是：
```Python
from physicsLab import *

expe = Experiment(OpenMode.load_by_sav_name, "example")
# maybe do something
expe.exit(delete=True)
```

## 停止操作存档
***低级api***
`Experiment.exit`会立刻停止对存档的操作:
```Python
from physicsLab import *

exp = Experiment(OpenMode.load_by_sav_name, "example")
# do something, 但未调用Experiment.save
exp.exit()
# 对exp的所有修改都丢失了
```

注意:
``` python
from physicsLab import *

exp = Experiment(OpenMode.load_by_sav_name, "example")
# do something
exp.exit()

Logic_Input() # error: 不可以在没有实验打开的情况下创建元件
```

``` python
from physicsLab import *

expe = Experiment(OpenMode.load_by_sav_name, "example")
# do something
expe.exit()
# expe.save() # 无法对已经退出操作的存档调用任何Experiment的方法进行操作
# expe.exit() # 无法重复调用.exit
```

## 编辑存档的发布信息
使用`edit_publish_info`方法, `title`参数修改发布标题，`description`参数定义发布描述，`wx`参数为是否续写`description`的内容
```python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    expe.edit_publish_info(title="new_title", description="new_description", wx=True)
```

## 多存档操作
获取当前正在操作的存档:
```Python
get_current_experiment()
```

使用`with Experiment`也在多存档操作中被推荐：
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as exp1:
    # do something in example
    with Experiment(OpenMode.load_by_sav_name, "example2") as exp2:
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

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    # do something
    eexp.export()
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
with Experiment(OpenMode.load_by_sav_name, "example1") as expe:
    Logic_Input().o - Logic_Output(1, 0, 0, elementXYZ=True).i

    with Experiment(OpenMode.load_by_sav_name, "example2") as exp2:
        Logic_Output(0, 0, 0.1)
        exp2.merge(expe, 1, 0, 0, elementXYZ=True)
```

## 手动设置输出路径
你可以使用`os.environ["PHYSICSLAB_HOME_PATH"] = "xxx"`来设置`physicsLab`读写存档的默认文件夹

该功能主要为非`Windows`系统设计, 虽然`Windows`上也可以用

该方法也是另一种导入任意路径的存档的一种方法(另一种是直接调用`load_by_filepath`)

## 暂停实验
你可以使用`Experiment.paused(status: bool)`来暂停实验
```Python
from physicsLab import *

with Experiment(OpenMode.load_by_sav_name, "example") as expe:
    expe.paused()
    # 如果要解除暂停实验，请使用exp.paused(False)
    ...
```

## 通过用户/实验的id获取时间
```python
from physicsLab import *

print(id_to_time("62d3fd092f3a2a60cc8ccc9e"))
```