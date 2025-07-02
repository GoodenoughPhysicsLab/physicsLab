# -*- coding: utf-8 -*-
from typing import *
from .vendor.typing_extensions import *

from physicsLab.savTemplate import Generate

num_type: TypeAlias = Union[int, float]

class CircuitElementData(TypedDict):
    ModelID: Union[str, Type[Generate]]
    IsBroken: bool
    IsLocked: bool
    Identifier: Union[str, Type[Generate]]
    Properties: dict
    Statistics: dict
    Position: Union[str, Type[Generate]]
    Rotation: Union[str, Type[Generate]]
    DiagramCached: bool
    DiagramPosition: dict
    DiagramRotation: int
