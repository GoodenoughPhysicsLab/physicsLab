# -*- coding: utf-8 -*-
from enum import Enum, unique

import colorama
colorama.init(autoreset=True)

@unique
class COLOR(Enum):
    BLACK = colorama.Fore.BLACK
    RED = colorama.Fore.RED
    GREEN = colorama.Fore.GREEN
    YELLOW = colorama.Fore.YELLOW
    BLUE = colorama.Fore.BLUE
    MAGENTA = colorama.Fore.MAGENTA
    CYAN = colorama.Fore.CYAN
    WHITE = colorama.Fore.WHITE

# 打印write_Experiment的信息时是否使用彩色字
_ColorSupport = True

def color_print(msg: str, color: COLOR, end="\n") -> None:
    if not isinstance(color, COLOR) or not isinstance(msg, str):
        raise TypeError

    global _ColorSupport

    if _ColorSupport:
        print(color.value + msg, end=end)
    else:
        print(msg, end=end)

def close_color_print():
    ''' 关闭打印文字的颜色 '''
    global _ColorSupport
    _ColorSupport = False
