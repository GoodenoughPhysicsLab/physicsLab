# -*- coding: utf-8 -*-
try:
    from .unionMusic import *
except ImportError:
    from physicsLab.errors import warning
    warning("can not use physicsLab.music, type `pip install mido`")