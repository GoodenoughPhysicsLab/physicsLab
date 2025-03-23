# -*- coding: utf-8 -*-
import warnings
import inspect

from physicsLab import _colorUtils

class PhysicsLabWarning(Warning):
    ''' physicsLab抛出的警告的类型 '''

def _showwarning(message, category, filename, lineno, file=None, line=None):
    if category is PhysicsLabWarning:
        _colorUtils.cprint(_colorUtils.Yellow("Warning in"))

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
        _colorUtils.cprint(_colorUtils.Yellow(str(message)))
    else:
        warnings.showwarning(message, category, filename, lineno, file, line)

warnings.showwarning = _showwarning

def warning(msg: str):
    if not isinstance(msg, str):
        raise TypeError(f"Parameter msg must be of `str`, but got {type(msg)}")
    warnings.warn(msg, PhysicsLabWarning)
