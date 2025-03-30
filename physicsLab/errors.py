# -*- coding: utf-8 -*-
import inspect
from ._typing import NoReturn
from physicsLab import unwind
from physicsLab import _colorUtils
from physicsLab._typing import Optional

BUG_REPORT: str = "please send a bug-report at " \
                "https://github.com/GoodenoughPhysicsLab/physicsLab/issues or " \
                "https://gitee.com/script2000/physicsLab/issues " \
                "with your code, *.sav and traceback"

def _unrecoverable_error(err_type: str, msg: Optional[str]) -> NoReturn:
    ''' 不可恢复的错误, 表明程序抽象机已崩溃
        会打印的错误信息并退出程序
    '''
    _colorUtils.cprint(_colorUtils.Red(err_type), end='')
    if msg is None:
        print('\n')
    else:
        _colorUtils.cprint(": ", _colorUtils.Red(msg))
    exit(1)

def assertion_error(msg: str) -> NoReturn:
    ''' 断言错误, physicsLab认为其为不可恢复的错误
    '''
    unwind.print_stack()
    _unrecoverable_error("AssertionError", msg)

def assert_true(
        condition: bool,
        msg: str = BUG_REPORT,
) -> None:
    if not condition:
        assertion_error(msg)

def unreachable() -> NoReturn:
    assertion_error(f"Unreachable touched, {BUG_REPORT}")

def type_error(msg: Optional[str] = None) -> NoReturn:
    ''' 类型错误, physicsLab认为其为不可恢复的错误
    '''
    current_frame = inspect.currentframe()
    if current_frame is None:
        unreachable()
    declared_frame = current_frame.f_back
    if declared_frame is None:
        unreachable()
    func_obj = declared_frame.f_globals.get(declared_frame.f_code.co_name)
    if func_obj is None:
        unreachable()
    print(func_obj)
    _unrecoverable_error("TypeError", msg)

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

class ExperimentTypeError(Exception):
    ''' 打开的实验与调用的元件不符 '''
    def __init__(self, err_msg: str = "The type of experiment does not match the element"):
        self.err_msg = err_msg

    def __str__(self):
        return self.err_msg

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
