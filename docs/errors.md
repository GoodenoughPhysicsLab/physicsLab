`physicsLab`也提供了一些自定义的异常类型

# 警告

`physicsLab`抛出的警告类型都是`PhysicsLabWarning`，并且为该警告客制化了打印输出的格式

如果希望更精细地控制警告的行为 (比如忽略警告，将警告视为错误等等), 请参阅python内置[warnings](https://docs.python.org/3/library/warnings.html)模块

## 异常

### ExperimentOpenedError

尝试打开一个已经有某个`Experiment`的实例打开过的实验时，会抛出此异常

### ExperimentClosedError

尝试在调用了`Experiment.close`之后使用该实例的方法时，会抛出此异常

### ExperimentExistError

尝试创建一个已经存在的实验时，会抛出此异常, 除非`force_crt=True`

### ExperimentNotExistError

尝试导入一个不存在的实验时，会抛出此异常
