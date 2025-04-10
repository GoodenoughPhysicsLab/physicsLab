# -*- coding: utf-8 -*-
''' 在命令行打印出有颜色的字
    为physicsLab最基础, 最底层的设施,
    所以不能依赖physicsLab的任何其他设施, 包括 errors.py

    Usage:
        >>> from physicsLab._colorUtils import *
        >>> cprint(Red("test")) # 输出红色字
        # 支持变参函数, 一次性打印多个不同颜色的Object
        # 但不像python的print一样支持sep参数 [设计如此]
        >>> cprint(Green("test"), "test", Yellow("test"), 1111, 3.14)
        >>> cprint(Blue("test")) # 还支持以下颜色
        >>> cprint(Magenta("test"))
        >>> cprint(Cyan("test"))
        >>> cprint(White("test"))
        >>> cprint(Black("test"))
        >>> cprint(Red("test"), file=sys.stderr) # 输出到stderr
        >>> cprint(Red("test"), end='') # 支持print那样指定end
        # 如果你不希望打印出颜色字 (即使使用了Red("xxx")之类的), 请使用python原生print
        >>> print(Green("test"), "test", Yellow("test")) # 此时打印无颜色
'''

import platform
from physicsLab._typing import final, Any

# 设置终端的编码为UTF-8
import io
import sys
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

import ctypes
if platform.system() == "Windows":
    from ctypes import wintypes

    class _CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes._COORD),
            ("dwCursorPosition", wintypes._COORD),
            ("wAttributes", wintypes.WORD),
            ("srWindow", wintypes.SMALL_RECT),
            ("dwMaximumWindowSize", wintypes._COORD),
        ]

    kernel32 = ctypes.windll.kernel32

    _GetStdHandle = ctypes.windll.kernel32.GetStdHandle
    _GetStdHandle.argtypes = [
        wintypes.DWORD,
    ]
    _GetStdHandle.restype = wintypes.HANDLE

    _GetConsoleScreenBufferInfo = ctypes.windll.kernel32.GetConsoleScreenBufferInfo
    _GetConsoleScreenBufferInfo.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(_CONSOLE_SCREEN_BUFFER_INFO),
    ]
    _GetConsoleScreenBufferInfo.restype = wintypes.BOOL

    _SetConsoleTextAttribute = ctypes.windll.kernel32.SetConsoleTextAttribute
    _SetConsoleTextAttribute.argtypes = [
        wintypes.HANDLE,
        wintypes.WORD,
    ]
    _SetConsoleTextAttribute.restype = wintypes.BOOL

    _stdout_handle = _GetStdHandle(-11) # STD_OUTPUT_HANDLE
    _stderr_handle = _GetStdHandle(-12) # STD_ERROR_HANDLE

class _Color:
    fore: int

    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __repr__(self) -> str:
        return self.msg

    @final
    def cprint(self, file):
        if platform.system() == "Windows":
            # 临时更改终端打印字符的属性
            csbi = _CONSOLE_SCREEN_BUFFER_INFO()
            if file is sys.stdout:
                _GetConsoleScreenBufferInfo(_stdout_handle, ctypes.byref(csbi))
                _SetConsoleTextAttribute(_stdout_handle, self.fore)
            elif file is sys.stderr:
                _GetConsoleScreenBufferInfo(_stderr_handle, ctypes.byref(csbi))
                _SetConsoleTextAttribute(_stderr_handle, self.fore)
            else:
                assert False
            print(self.msg, flush=True, end='', file=file)
            # 恢复终端打印字符的属性
            if file is sys.stdout:
                _SetConsoleTextAttribute(_stdout_handle, csbi.wAttributes)
            elif file is sys.stderr:
                _SetConsoleTextAttribute(_stderr_handle, csbi.wAttributes)
            else:
                assert False
        else:
            print(f"\033[{self.fore}m{self.msg}\033[39m", end='', file=file)

class Black(_Color):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

        if platform.system() == "Windows":
            self.fore = 0
        else:
            self.fore = 30

class Red(_Color):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

        if platform.system() == "Windows":
            self.fore = 4
        else:
            self.fore = 31

class Green(_Color):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

        if platform.system() == "Windows":
            self.fore = 2
        else:
            self.fore = 32

class Yellow(_Color):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

        if platform.system() == "Windows":
            self.fore = 6
        else:
            self.fore = 33


class Blue(_Color):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

        if platform.system() == "Windows":
            self.fore = 1
        else:
            self.fore = 34

class Magenta(_Color):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

        if platform.system() == "Windows":
            self.fore = 5
        else:
            self.fore = 35

class Cyan(_Color):
   def __init__(self, msg: str) -> None:
        super().__init__(msg)

        if platform.system() == "Windows":
            self.fore = 3
        else:
            self.fore = 36

class White(_Color):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

        if platform.system() == "Windows":
            self.fore = 7
        else:
            self.fore = 37

def cprint(*args, end='\n', file: Any = sys.stdout) -> None:
    # 先刷新再打印, 避免在Windows下打印缓冲区的内容还未输出就被改变了Attribute
    # e.g.
    # print("test")
    # _colorUtils.cprint("test")
    if file == sys.stdout:
        sys.stdout.flush()
    elif file == sys.stderr:
        sys.stderr.flush()
    else:
        assert False

    for arg in args:
        if isinstance(arg, _Color):
            arg.cprint(file=file)
        else:
            print(arg, end='', file=file)
    print(end, end='', file=file)
    # 再次刷新，确保终端的输出已经输出
    # e.g.
    # cprint(Green("test"), file=sys.stderr)
    # cprint(Red("ttt"), file=sys.stdout)
    if file == sys.stdout:
        sys.stdout.flush()
    elif file == sys.stderr:
        sys.stderr.flush()
    else:
        assert False
