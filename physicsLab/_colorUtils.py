# -*- coding: utf-8 -*-
import sys
from enum import Enum, unique

@unique
class COLOR(Enum):
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    _DEFAULT = '\033[39m'

# 打印write_Experiment的信息时是否使用彩色字
colorSupport = True

if colorSupport and sys.platform == "win32":
    try:
        # https://stackoverflow.com/questions/36760127/...
        # how-to-use-the-new-support-for-ansi-escape-sequences-in-the-windows-10-console
        from ctypes import windll
        kernel32 = windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except ImportError:
        colorSupport = False

# 打印颜色字
def color_print(msg: str, color: COLOR) -> None:
    if not isinstance(color, COLOR):
        raise TypeError

    global colorSupport

    if not isinstance(msg, str):
        raise TypeError
    if colorSupport:
        print(f"{color.value}{msg}{COLOR._DEFAULT.value}")
    else:
        print(msg)

# 关闭打印时的color
def close_color_print():
    global colorSupport
    colorSupport = False