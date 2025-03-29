# -*- coding: utf-8 -*-
''' 在命令行打印出有颜色的字
    为最基础, 最底层的设施
'''

import platform
from physicsLab._typing import final

# 设置终端的编码为UTF-8
import io
import sys
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

if platform.system() == "Windows":
    import ctypes
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
    _stderr_handle = _GetStdHandle(-12)

_color_support = True

def close_color_print():
    ''' 关闭打印的文字是有颜色的功能 '''
    global _color_support
    _color_support = False

class _Color:
    fore: int

    def __init__(self, msg: str) -> None:
        self.msg = msg

    @final
    def cprint(self):
        if platform.system() == "Windows":
            # 先刷新再打印, 避免以下的bug
            # print("test")
            # _colorUtils.cprint("test")
            sys.stdout.flush()
            csbi = _CONSOLE_SCREEN_BUFFER_INFO()
            _GetConsoleScreenBufferInfo(_stdout_handle, ctypes.byref(csbi))
            _SetConsoleTextAttribute(_stdout_handle, self.fore)
            print(self.msg, flush=True, end='')
            _SetConsoleTextAttribute(_stdout_handle, csbi.wAttributes)
        else:
            print(f"\033[{self.fore}m{self.msg}\033[39m", end='')

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

def cprint(*args, end='\n'):
    global _color_support
    for arg in args:
        if _color_support and isinstance(arg, _Color):
            arg.cprint()
        else:
            print(arg, end='')
    print(end, end='')
