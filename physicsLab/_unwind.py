# -*- coding: utf-8 -*-
import sys
import math
import inspect
from physicsLab import _colorUtils
from physicsLab._typing import Callable


def print_code_block(print_title: Callable, line_number: int, source_code: str) -> None:
    ''' 打印错误信息
    '''
    digits = int(math.log10(line_number)) + 1
    print(' ', end='', file=sys.stderr)
    for _ in range(digits + 1):
        _colorUtils.cprint(_colorUtils.Cyan('-'), end='', file=sys.stderr)
    _colorUtils.cprint(_colorUtils.Cyan('+->'), end='', file=sys.stderr)
    print_title()
    for index, line in enumerate(source_code.splitlines()):
        _colorUtils.cprint(' ', _colorUtils.Cyan(str(line_number + index)), end='', file=sys.stderr)
        if int(math.log10(line_number + index)) + 1 == digits:
            print(' ', end='', file=sys.stderr)
        _colorUtils.cprint(_colorUtils.Cyan('|'), ' ', line, file=sys.stderr)


def print_stack(full: bool = False) -> None:
    for frame_info in inspect.stack()[::-1]:
        if not full:
            module = inspect.getmodule(frame_info.frame)
            if module is None or module.__name__.startswith("physicsLab") or module.__name__.startswith("warnings"):
                continue
        assert frame_info.code_context is not None
        print_code_block(
            lambda: _colorUtils.cprint(
                "  File ",
                _colorUtils.Magenta(f"\"{frame_info.filename}\""),
                ", in ",
                _colorUtils.Magenta(frame_info.function),
                file=sys.stderr,
           ),
            frame_info.lineno,
            frame_info.code_context[0].strip(),

        )
