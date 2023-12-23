# -*- coding: utf-8 -*-
# 用于存放自定义错误类
# 由于有时在package外需要异常处理，故不为文件私有变量
import physicsLab._colorUtils as _colorUtils

def warning(msg: str) -> None:
    _colorUtils.color_print("Warning: " + msg, _colorUtils.COLOR.YELLOW)

# 打开实验异常
class OpenExperimentError(Exception):
    def __str__(self):
        return "open a experiment but find nothing(must open a experiment)."

# 导线颜色类型异常
class WireColorError(Exception):
    def __str__(self):
        return "illegal wire color."

# 未找到导线异常
class WireNotFoundError(Exception):
    def __str__(self):
        return "Unable to delete a nonexistent wire"

# 用于模块化元件的bitLength参数
class bitLengthError(Exception):
    def __str__(self):
        return "illegal bitLength number"

# 创建实验已存在
class experimentExistError(Exception):
    def __str__(self):
        return 'Duplicate name archives are forbidden'

class crtExperimentFailError(Exception):
    def __str__(self):
        return "Failed to create experiment, the experiment already exists"

# 打开的实验与调用的元件不符
class ExperimentTypeError(Exception):
    def __str__(self):
        return "The type of experiment does not match the element"

# 用于get_Element 获取元件引用失败
class getElementError(Exception):
    def __str__(self):
        return "Index out of range"

# 类实例化异常 基类无法被实例化
class instantiateError(Exception):
    def __str__(self):
        return "This class cannot be instantiated"

class ExperimentError(Exception):
    def __init__(self, string: str) -> None:
        self.err_msg: str = string

    def __str__(self) -> str:
        return self.err_msg