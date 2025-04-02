# -*- coding: utf-8 -*-
import os
import ast
import inspect
import executing

from ._typing import NoReturn
from physicsLab import unwind
from physicsLab import _colorUtils
from physicsLab._typing import Optional, LiteralString

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
    os.abort()

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

    declare_frame = current_frame.f_back
    if declare_frame is None:
        unreachable()
    declare_node = executing.Source.executing(declare_frame).node
    declare_module = inspect.getmodule(declare_frame)
    if declare_module is None:
        unreachable()

    call_frame = declare_frame.f_back
    if call_frame is None:
        unreachable()
    call_node = executing.Source.executing(call_frame).node
    call_module = inspect.getmodule(call_frame)
    if call_module is None:
        unreachable()
    lineno = call_frame.f_lineno
    _colorUtils.cprint(
        "  File ",
        _colorUtils.Magenta(f"\"{call_frame.f_code.co_filename}\""),
        ", in ",
        _colorUtils.Magenta(call_frame.f_code.co_name),
        end='\n',
    )
    print(ast.get_source_segment(inspect.getsource(call_module), call_node, padded=True))

    while not isinstance(declare_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        declare_node = declare_node.parent
    func_declare = ast.get_source_segment(inspect.getsource(declare_module), declare_node, padded=True)
    if func_declare is None:
        unreachable()
    is_signature = False
    for char in func_declare:
        if char == '(':
            is_signature = True
        elif char == ')':
            is_signature = False
        elif char == ':' and not is_signature:
            print('\n', end='')
            break
        print(char, end='')

    _unrecoverable_error("TypeError", msg)

class InvalidWireError(Exception):
    def __init__(self, msg: str):
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
    def __init__(self, err_msg: LiteralString = "The experiment does not exist") -> None:
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
    def __init__(self, err_msg: LiteralString = "The type of experiment does not match the element") -> None:
        self.err_msg = err_msg

    def __str__(self) -> str:
        return self.err_msg

# 用于get_Element 获取元件引用失败
class ElementNotFound(Exception):
    def __init__(self, err_msg: LiteralString = "Can't find element") -> None:
        self.err_msg = err_msg
    def __str__(self) -> str:
        return self.err_msg

class ExperimentError(Exception):
    def __init__(self, string: str = "") -> None:
        self.err_msg: str = string

    def __str__(self) -> str:
        return self.err_msg

class ResponseFail(Exception):
    ''' 返回消息体失败 '''
    # TODO 获取对应的错误码
    def __init__(self, err_msg: LiteralString):
        self.err_msg: str = err_msg

    def __str__(self):
        return self.err_msg

class MaxRetryError(Exception):
    ''' 重试次数过多 '''
    def __init__(self, err_msg: LiteralString):
        self.err_msg = err_msg

    def __str__(self):
        return self.err_msg
