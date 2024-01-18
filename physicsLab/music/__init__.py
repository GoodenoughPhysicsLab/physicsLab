# -*- coding: utf-8 -*-
try:
    from .unionMusic import *
except ImportError:
    import physicsLab.phy_errors as errors
    errors.warning("can not use physicsLab.music, type `pip install mido`")