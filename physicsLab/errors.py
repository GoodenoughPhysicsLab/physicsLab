# -*- coding: utf-8 -*-
import warnings
import inspect

from physicsLab import _colorUtils

class PhysicsLabWarning(Warning):
    ''' physicsLab抛出的警告的类型 '''

def _showwarning(message, category, filename, lineno, file=None, line=None):
    if category is PhysicsLabWarning:
        _colorUtils.color_print("Warning in", _colorUtils.COLOR.YELLOW)

        for frame_info in inspect.stack()[::-1]:
            module = inspect.getmodule(frame_info.frame)
            if module is None or module.__name__.startswith("physicsLab") or module.__name__.startswith("warnings"):
                continue
            print(f"  File \"{frame_info.filename}\", line {frame_info.lineno}, in {frame_info.function}")
            if frame_info.code_context is not None:
                print(f"    {frame_info.code_context[0].strip()}")
        _colorUtils.color_print(str(message), _colorUtils.COLOR.YELLOW)
    else:
        warnings.showwarning(message, category, filename, lineno, file, line)

warnings.showwarning = _showwarning

def warning(msg: str):
    assert isinstance(msg, str)
    warnings.warn(msg, PhysicsLabWarning)

# 导线颜色类型异常
class WireColorError(Exception):
    def __str__(self):
        return "illegal wire color."

# 未找到导线异常
class WireNotFoundError(Exception):
    def __str__(self):
        return "Unable to delete a nonexistent wire"

# 用于模块化元件的bitLength参数
class BitnumError(Exception):
    def __str__(self):
        return "illegal bitLength number"

class InternalError(Exception):
    ''' physicsLab内部错误 '''
    def __str__(self):
        return "internal error, please bug report"

class ExperimentHasOpenError(Exception):
    ''' 已打开实验 '''
    def __str__(self):
        return "The experiment has been opened"

class ExperimentNotOpenError(Exception):
    ''' 未打开实验 '''
    def __str__(self):
        return "The experiment has not been opened"

class ExperimentHasExistError(Exception):
    ''' 实验已存在 '''
    def __str__(self):
        return 'Duplicate name archives are forbidden'

class ExperimentNotExistError(Exception):
    ''' 实验不存在 '''
    err_msg = "The experiment does not exist"

    def __init__(self, err_msg = None) -> None:
        if err_msg is not None:
            self.err_msg = err_msg
    def __str__(self):
        return self.err_msg

class ExperimentHasCrtError(Exception):
    ''' 实验已创建 '''
    def __str__(self):
        return "The experiment has been created"

class ExperimentHasNotCrtError(Exception):
    ''' 实验未创建 '''
    def __str__(self):
        return "The experiment has not been created"

# 打开的实验与调用的元件不符
class ExperimentTypeError(Exception):
    def __str__(self):
        return "The type of experiment does not match the element"

# 用于get_Element 获取元件引用失败
class ElementNotFound(Exception):
    def __init__(self, err_msg: str = "Index out of range") -> None:
        self.err_msg: str = err_msg
    def __str__(self):
        return self.err_msg

# 类实例化异常 基类无法被实例化
class instantiateError(Exception):
    def __str__(self):
        return "This class cannot be instantiated"

class ExperimentError(Exception):
    def __init__(self, string: str = "") -> None:
        self.err_msg: str = string

    def __str__(self) -> str:
        return self.err_msg

class ElementNotExistError(Exception):
    pass

class ResponseFail(Exception):
    ''' 返回消息体失败 '''
    def __init__(self, err_msg: str):
        self.err_msg: str = err_msg
    def __str__(self):
        return self.err_msg

class MaxRetryError(Exception):
    ''' 重试次数过多 '''
    def __init__(self, err_msg: str):
        self.err_msg: str = err_msg

    def __str__(self):
        return self.err_msg
