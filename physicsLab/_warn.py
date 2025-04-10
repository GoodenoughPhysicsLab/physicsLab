# -*- coding: utf-8 -*-
import warnings

from physicsLab import _colorUtils
from physicsLab import _unwind

class PhysicsLabWarning(Warning):
    ''' physicsLab抛出的警告的类型 '''

def _showwarning(message, category, filename, lineno, file=None, line=None):
    if category is PhysicsLabWarning:
        _colorUtils.cprint(_colorUtils.Yellow("Warning in"))
        _unwind.print_stack()
        _colorUtils.cprint(_colorUtils.Yellow(str(message)))
    else:
        warnings.showwarning(message, category, filename, lineno, file, line)

warnings.showwarning = _showwarning

def warning(msg: str):
    warnings.warn(msg, PhysicsLabWarning)
