# -*- coding: utf-8 -*-
try:
    from typing import Self
except ImportError:
    try:
        from typing_extensions import Self
    except ImportError:
        from .typing_extensions import Self

from typing import *

if TYPE_CHECKING:
    class WireDict(TypedDict):
        Source: str
        SourcePin: str
        Target: str
        TargetPin: str
        ColorName: str
else:
    WireDict = dict

numType = Union[int, float]