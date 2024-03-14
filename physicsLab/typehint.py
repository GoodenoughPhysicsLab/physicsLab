# -*- coding: utf-8 -*-
from typing import *
from typing_extensions import *

class WireDict(TypedDict):
    Source: str
    SourcePin: str
    Target: str
    TargetPin: str
    ColorName: str

numType: TypeAlias = Union[int, float]