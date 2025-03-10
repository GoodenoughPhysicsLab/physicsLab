# -*- coding: utf-8 -*-
''' 在命令行打印出有颜色的字 '''
import platform
from enum import Enum, unique

# import colorama
# colorama.init(autoreset=True)

if platform.system() == "Windows":
    import io
    import sys
    # 设置终端的编码为UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# @unique
# class COLOR(Enum):
#     BLACK = colorama.Fore.BLACK
#     RED = colorama.Fore.RED
#     GREEN = colorama.Fore.GREEN
#     YELLOW = colorama.Fore.YELLOW
#     BLUE = colorama.Fore.BLUE
#     MAGENTA = colorama.Fore.MAGENTA
#     CYAN = colorama.Fore.CYAN
#     WHITE = colorama.Fore.WHITE

@unique
class COLOR(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7

_ColorSupport = True

def color_print(msg: str, color: COLOR, end='\n') -> None:
    if not isinstance(color, COLOR) or not isinstance(msg, str):
        raise TypeError

    global _ColorSupport

    # if _ColorSupport:
    #     print(color.value + msg, end=end)
    # else:
    #     print(msg, end=end)
    print(msg, end=end)
    # print(msg.encode("utf-8").decode("utf-8"), end=end)

def close_color_print():
    ''' 关闭打印的文字是有颜色的功能 '''
    global _ColorSupport
    _ColorSupport = False
