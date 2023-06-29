#coding=utf-8
# 用于存放自定义错误类
# 由于有时在package外需要异常处理，故不为文件私有变量
import physicsLab._colorUtils as _colorUtils

def warning(msg: str) -> None:
    _colorUtils.printf("Warning: " + msg, _colorUtils.YELLOW)

# 打开实验异常
class openExperimentError(Exception):
    def __str__(self):
        return "open a experiment but find nothing(must open a experiment)."

class wireColorError(Exception):
    def __str__(self):
        return "illegal wire color."

class wireNotFoundError(Exception):
    def __str__(self):
        return "Unable to delete a nonexistent wire"

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
class experimentTypeError(Exception):
    def __str__(self):
        return "The type of experiment does not match the element"

class getElementError(Exception):
    def __str__(self):
        return "Index out of range"

class instantiateError(Exception):
    def __str__(self):
        return "This class cannot be instantiated"