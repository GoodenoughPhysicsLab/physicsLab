# -*- coding: utf-8 -*-
''' 在命令行打印出有颜色的字 '''

# 设置终端的编码为UTF-8
import io
import sys
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import colorama
from physicsLab import errors

_color_support = True

def close_color_print():
    ''' 关闭打印的文字是有颜色的功能 '''
    global _color_support
    _color_support = False

class Color:
    def __init__(self, msg: str) -> None:
        errors.assert_true(isinstance(msg, str))
        self.msg = msg

class Black(Color):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class Red(Color):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class Green(Color):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class Yellow(Color):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class Blue(Color):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class Magenta(Color):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class Cyan(Color):
   def __init__(self, msg: str) -> None:
       super().__init__(msg)

class White(Color):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

def cprint(*args, end='\n'):
    global _color_support
    for arg in args:
        if _color_support:
            if isinstance(arg, Black):
                print(colorama.Fore.BLACK + arg.msg + colorama.Fore.RESET, end='')
            elif isinstance(arg, Red):
                print(colorama.Fore.RED + arg.msg + colorama.Fore.RESET, end='')
            elif isinstance(arg, Green):
                print(colorama.Fore.GREEN + arg.msg + colorama.Fore.RESET, end='')
            elif isinstance(arg, Yellow):
                print(colorama.Fore.YELLOW + arg.msg + colorama.Fore.RESET, end='')
            elif isinstance(arg, Blue):
                print(colorama.Fore.BLUE + arg.msg + colorama.Fore.RESET, end='')
            elif isinstance(arg, Magenta):
                print(colorama.Fore.MAGENTA + arg.msg + colorama.Fore.RESET, end='')
            elif isinstance(arg, Cyan):
                print(colorama.Fore.CYAN + arg.msg + colorama.Fore.RESET, end='')
            elif isinstance(arg, White):
                print(colorama.Fore.WHITE + arg.msg + colorama.Fore.RESET, end='')
            else:
                print(arg, end='')
        else:
            if isinstance(arg, Color):
                print(arg.msg, end='')
            else:
                print(arg, end='')
    print(end, end='')
