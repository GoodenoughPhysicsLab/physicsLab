# 操作本地实验（存档） experiment


## 更优雅的写法
你可以用with语句打开一个存档，且读写存档等重复工作无须手动重复编写
```python
# example
with experiment('name'):
    # to do something
    # 该方式会自动打开存档
    # 若打开失败会自动创建存档
    # 执行完代码之后会自动写入存档
    ...
```
`experiment`还有很多其他参数：  
1.  `read`: 是否读取存档已有状态

## 打开存档
你必须指明你要打开的是哪个存档：
```Python
Experiment.open('example.sav')
Experiment.open('example')
open_Experiment('example.sav') # 存档的文件名，不推荐使用
open_Experiment('example') # 通过在物实保存的本地实验的名字打开存档
```
>Note: 你可以多次调用`open_Experiment()`或`crt_Experiment()`, 但只有你最后一次调用该函数打开或创建的存档会被操作

## 创建存档
如果你想要创建一个实验：
```python
Experiment.crt('example')
crt_Experiment('example')
crt_Experiment("example", experimentType=experimentType.Circuit) # 指定实验类型
```
> Note: 你可以多次调用`open_Experiment()`或`crt_Experiment()`, 但只有你最后一次调用该函数打开或创建的存档会被操作

```type```参数用于指定创建存档的类型，详情请查看```指定创建实验类型```  

如果你希望打开存档失败不报错而是创建存档，除了使用`with experiment(...)`，你还可以使用
```Python
Experiment("example")
Experiment.open_or_crt("example")
open_or_crt_Experiment(savName: str, experimentType) -> None
```
该函数与`crt_Experiment`传参相同，但`experimentType`参数仅在尝试创建存档时有效

## 判断存档是否存在
调用`search_Experiment()`判断存档是否存在  
如果存档已经存档，则会返回存档的文件名  
如果存档不存在，则返回`None`


## 读取存档的内容
被打开的存档不会读取原实验的状态。如果你不希望原实验的状态被覆盖，需要调用该函数：  
```Python
Experiment.read()
read_Experiment()
```

## 向存档中写入
最后你需要调用该函数往存档里写入程序运行之后的结果：  
```Python
Experiment.write()
write_Experiment()
```

## 删除存档
除了创建存档，你也可以删除存档：
```Python
Experiment.delete()
del_Experiment()
```

## 停止操作存档
`Experiment.write()`与`Experiment.delete()`都会停止操作存档，但如果你只想停止操作该存档而不想将当前的实验状态保存或者书删除实验的话，你可以调用: 
```Python
Experiment.exit()
exit_Experiment()
```

## 用记事本打开存档文件
你也可以打开存档查看：
```Python
Experiment.read()
show_Experiment()
```
仅`Windows`上有效

## 多存档操作
获取当前正在操作的存档:
```Python
get_Experiment()
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

## 以physicsLab代码的形式导出
```Python
Experiment.export()
```