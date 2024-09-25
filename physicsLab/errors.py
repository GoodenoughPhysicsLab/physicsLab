# -*- coding: utf-8 -*-
# 用于存放自定义错误类
# 由于有时在package外需要异常处理，故不为文件私有变量
import inspect

from physicsLab import _colorUtils
from typing import Optional

_warning_status: Optional[bool] = None

def set_warning_status(warning_status: bool) -> None:
    ''' 设置警告状态
        False: 不打印警告
        None: 打印警告
        True: 视警告为错误
    '''
    if not isinstance(warning_status, bool):
        raise TypeError

    global _warning_status
    _warning_status = warning_status

# 抛出警告, 当warning_status==None
def warning(msg: str, warning_status: Optional[bool] = None) -> None:
    if not isinstance(warning_status, (bool, type(None))):
        raise TypeError

    if _warning_status is not None:
        warning_status = _warning_status

    if warning_status is False:
        return
    if warning_status is True:
        raise WarningError

    # if warning_status is None:
    _colorUtils.color_print("Warning in", _colorUtils.COLOR.YELLOW)

    for frame_info in inspect.stack()[::-1]:
        module = inspect.getmodule(frame_info.frame)
        if module is None or module.__name__.startswith("physicsLab"):
            continue
        print(f"  File \"{frame_info.filename}\", line {frame_info.lineno}, in {frame_info.function}")
        if frame_info.code_context is not None:
            print(f"    {frame_info.code_context[0].strip()}")
    _colorUtils.color_print(msg, _colorUtils.COLOR.YELLOW)

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

class WarningError(Exception):
    def __str__(self) -> str:
        return "see warning as error"

class ElementNotExistError(Exception):
    pass

class ResponseFail(Exception):
    ''' 返回消息体失败 '''
    def __init__(self, err_msg: str):
        self.err_msg: str = err_msg
    def __str__(self):
        return self.err_msg
