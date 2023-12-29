# -*- coding: utf-8 -*-
try:
    from typing import Self
except ImportError:
    try:
        from typing_extensions import Self
    except ImportError:
        from .typing_extensions import Self

from typing import *