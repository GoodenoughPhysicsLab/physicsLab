# -*- coding: utf-8 -*-
''' Python API for Physics-Lab-AR '''

from ._colorUtils import close_color_print
# 操作实验
from .element import search_experiment, Experiment
from ._core import (
    ElementBase,
    get_current_experiment,
    elementXYZ_to_native,
    native_to_elementXYZ,
    ElementXYZ,
)
# 实验, 标签类型
from .enums import ExperimentType, Category, Tag, OpenMode, WireColor
# 电学实验
from .circuit import *
# 天体物理实验
from .celestial import *
# 电与磁实验
from .electromagnetism import *
# `physicsLab`自定义异常类
from .errors import *

from physicsLab.plAR import *
from physicsLab.utils import *

from physicsLab import web
from physicsLab import lib
from physicsLab import music

import os
import platform

if not os.path.exists(Experiment.SAV_PATH_DIR):
    if platform.system() == "Windows":
        warning("Have you installed Physics-Lab-AR?")
    os.makedirs(Experiment.SAV_PATH_DIR)

del os
del platform
