# 异常 errors

## 警告 warning
默认情况下，警告会打印一条信息，但程序会继续运行。  
如果希望视警告为错误或者警告不打印信息，你可以设置警告状态，而这分为局部设置与全局设置两种。  
局部设置的优先级高于全局设置。  

全局设置需要使用`set_warning_status()`  
```Python
set_warning_status(False) # 不打印警告信息
set_warning_status(True) # 试警告为错误
```
example:
```Python
from physicsLab import *

set_warning_status(True)

a = Experiment().crt("example")
a.delete()
```

除了全局设置警告状态，还可以在一些会抛出警告的函数的参数中设置警告状态，这就是局部设置    
```Python
from physicsLab import *

a = Experiment().crt("example")
a.delete(warning_status=True)
```

如果使用`with experiment("example")`的形式打开存档，会默认局部设置不打印警告，以`Experiment.delete()`为例，此时设置状态需使用`delete_warning_status`参数
example:
```Python
from physicsLab import *

with experiment("example", write=False, delete=True, delete_warning_status=True) as exp:
    pass
```

## 异常

