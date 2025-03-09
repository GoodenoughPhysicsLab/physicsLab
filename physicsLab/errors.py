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
            print("  File ", end='')
            _colorUtils.color_print(f"\"{frame_info.filename}\"", _colorUtils.COLOR.MAGENTA, end='')
            print(", line ", end='')
            _colorUtils.color_print(str(frame_info.lineno), _colorUtils.COLOR.MAGENTA, end='')
            print(", in ", end='')
            _colorUtils.color_print(frame_info.function, _colorUtils.COLOR.MAGENTA)
            if frame_info.code_context is not None:
                print(f"    {frame_info.code_context[0].strip()}")
        _colorUtils.color_print(str(message), _colorUtils.COLOR.YELLOW)
    else:
        warnings.showwarning(message, category, filename, lineno, file, line)

warnings.showwarning = _showwarning

def warning(msg: str):
    assert isinstance(msg, str)
    warnings.warn(msg, PhysicsLabWarning)

BUG_REPORT: str = "please send a bug-report at " \
                "https://github.com/GoodenoughPhysicsLab/physicsLab/issues or " \
                "https://gitee.com/script2000/physicsLab/issues " \
                "with your code, *.sav and traceback"

def assert_true(
        condition: bool,
        msg: str = BUG_REPORT,
) -> None:
    if not condition:
        raise AssertionError(msg)

def unreachable():
    raise AssertionError(f"Unreachable touched, {BUG_REPORT}")

class InvalidWireError(Exception):
    def __init__(self, msg: str):
        assert isinstance(msg, str)
        self.msg = msg

    def __str__(self):
        return self.msg

class InvalidSavError(Exception):
    ''' 存档文件错误 '''
    def __str__(self):
        return "The archive file is incorrect"

class ExperimentOpenedError(Exception):
    ''' 已打开实验 '''
    def __str__(self):
        return "The experiment has been opened"

class ExperimentClosedError(Exception):
    ''' 未打开实验 '''
    def __str__(self):
        return "The experiment has been closed"

# TODO 强化报错信息：将实验的具体信息也打印出来
class ExperimentExistError(Exception):
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
    def __init__(self, err_msg: str = "") -> None:
        self.err_msg: str = err_msg
    def __str__(self):
        return self.err_msg

class ExperimentError(Exception):
    def __init__(self, string: str = "") -> None:
        self.err_msg: str = string

    def __str__(self) -> str:
        return self.err_msg

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
