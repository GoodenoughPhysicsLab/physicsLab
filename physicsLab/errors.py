# -*- coding: utf-8 -*-
import os
import ast
import math
import inspect
import threading
import executing

from ._typing import NoReturn, Callable
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

def _print_err_msg(print_title: Callable, line_number: int, source_code: str) -> None:
    ''' 打印错误信息
    '''
    digits = int(math.log10(line_number)) + 1
    print(' ', end='')
    for _ in range(digits + 1):
        _colorUtils.cprint(_colorUtils.Cyan('-'), end='')
    _colorUtils.cprint(_colorUtils.Cyan('+->'), end='')
    print_title()
    for index, line in enumerate(source_code.splitlines()):
        _colorUtils.cprint(' ', _colorUtils.Cyan(str(line_number + index)), end='')
        if int(math.log10(line_number + index)) + 1 == digits:
            print(' ', end='')
        _colorUtils.cprint(_colorUtils.Cyan('|'), line)

_type_error_lock = threading.Lock()

def type_error(msg: Optional[str] = None) -> NoReturn:
    ''' 类型错误, physicsLab认为其为不可恢复的错误
    '''
    _type_error_lock.acquire()
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
    call_executing = executing.Source.executing(call_frame)
    call_node = call_executing.node
    call_module = inspect.getmodule(call_frame)
    if call_module is None:
        unreachable()
    call_src = ast.get_source_segment(inspect.getsource(call_module), call_node, padded=True)
    if call_src is None:
        unreachable()
    _print_err_msg(
        lambda: _colorUtils.cprint(
            " File ",
            _colorUtils.Magenta(f"\"{call_frame.f_code.co_filename}\""),
            ", in ",
            _colorUtils.Magenta(call_executing.code_qualname()),
        ),
        call_frame.f_lineno,
        call_src,
    )

    while not isinstance(declare_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        declare_node = declare_node.parent
    func_declare = ast.get_source_segment(inspect.getsource(declare_module), declare_node, padded=True)
    if func_declare is None:
        unreachable()
    is_signature = 0
    declare_output: str = ""
    for char in func_declare:
        if char == '(':
            is_signature += 1
        elif char == ')':
            is_signature -= 1
        elif char == ':' and is_signature == 0:
            declare_output += '\n'
            break
        declare_output += char

    _print_err_msg(
        lambda: _colorUtils.cprint(_colorUtils.Yellow(" Note"), ": function defined here:"),
        declare_node.lineno,
        declare_output,
    )

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
