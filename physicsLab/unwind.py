# -*- coding: utf-8 -*-
import inspect
from physicsLab import _colorUtils

def print_stack() -> None:
    for frame_info in inspect.stack()[::-1]:
        module = inspect.getmodule(frame_info.frame)
        if module is None or module.__name__.startswith("physicsLab") or module.__name__.startswith("warnings"):
            continue
        _colorUtils.cprint(
            "  File ",
            _colorUtils.Magenta(f"\"{frame_info.filename}\""),
            ", line ",
            _colorUtils.Magenta(str(frame_info.lineno)),
            ", in ",
            _colorUtils.Magenta(frame_info.function),
        )
        if frame_info.code_context is not None:
            print(f"    {frame_info.code_context[0].strip()}")
