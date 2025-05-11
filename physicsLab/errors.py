# -*- coding: utf-8 -*-
''' physicsLab的异常系统
    有2个主要的组成部分: 可恢复的异常, 不可恢复的错误

    * 可恢复的异常: 基于Python的Exception自定义的一系列错误类

    * 不可恢复的错误:
        当某些错误发生的时候, physicsLab认为程序抽象机已经崩溃, 无法继续运行
        也就是说, 当该错误发生时, 仅表明程序出现了bug, 因此坚决不给用户捕获异常的可能
        因此一旦这些错误发生, physicsLab会调用os.abort来终止程序, 而不是抛出一个异常
        被视为 不可恢复的错误 的有:
        * assertion_error: 断言错误, physicsLab认为其为不可恢复的错误, 因此请不要使用 AssertionError
        * type_error: 断言错误, physicsLab认为其为不可恢复的错误, 因此请不要使用 TypeError
        除此之外, physicsLab自定义了不可恢复错误发生时的打印输出格式
        这些格式比Python自带的traceback可读性更好
'''

import os
import sys
import ast
import math
import inspect
import threading
import executing

from ._typing import NoReturn
from physicsLab import _unwind
from physicsLab import _colorUtils
from physicsLab._typing import Optional, LiteralString

BUG_REPORT: str = "please send a bug-report at " \
                "https://github.com/GoodenoughPhysicsLab/physicsLab/issues or " \
                "https://gitee.com/script2000/physicsLab/issues " \
                "with your code, *.sav and traceback / coredump for Python"

def _unrecoverable_error(err_type: str, msg: Optional[str]) -> NoReturn:
    ''' 不可恢复的错误, 表明程序抽象机已崩溃
        会打印的错误信息并退出程序
    '''
    _colorUtils.cprint(_colorUtils.Red(err_type), end='', file=sys.stderr)
    if msg is None:
        print('\n', file=sys.stderr)
    else:
        _colorUtils.cprint(": ", _colorUtils.Red(msg), file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()
    os.abort()

_unrecoverable_error_lock = threading.Lock()

def assertion_error(msg: str) -> NoReturn:
    ''' 断言错误, physicsLab认为其为不可恢复的错误
    '''
    _unrecoverable_error_lock.acquire()
    _unwind.print_stack(full=True)
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
    _unrecoverable_error_lock.acquire()
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
    call_module = inspect.getmodule(call_frame)
    call_executing = executing.Source.executing(call_frame)
    call_node = call_executing.node
    if call_node is None:
        # executing 的原理是通过解析字节码`__code__`来获取对应的节点
        # 但executing支持的字节码有限, 比如await有关的字节码就不支持, 无法获取对应的node
        # 此时只好用inspect.stack来反射获取相对原始的源代码信息
        call_frame_info = inspect.stack()[2]
        if call_frame_info is None or call_frame_info.code_context is None:
            unreachable()
        _unwind.print_code_block(
            lambda: _colorUtils.cprint(
                " File ",
                _colorUtils.Magenta(f"\"{call_frame.f_code.co_filename}\""),
                ", in ",
                _colorUtils.Magenta(call_executing.code_qualname()),
                file=sys.stderr
            ),
            call_frame_info.lineno,
            call_frame_info.code_context[0].strip(),
        )
    else:
        if call_module is None:
            unreachable()
        call_src = ast.get_source_segment(inspect.getsource(call_module), call_node, padded=True)
        if call_src is None:
            unreachable()
        _unwind.print_code_block(
            lambda: _colorUtils.cprint(
                " File ",
                _colorUtils.Magenta(f"\"{call_frame.f_code.co_filename}\""),
                ", in ",
                _colorUtils.Magenta(call_executing.code_qualname()),
                file=sys.stderr
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

        _unwind.print_code_block(
            lambda: _colorUtils.cprint(
                _colorUtils.Yellow(" Note"), ": function defined here:",
                file=sys.stderr,
            ),
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
