# -*- coding: utf-8 -*-
''' Python API for Physics-Lab-AR '''
import os
import platform

# 颜色打印
from ._colorUtils import close_color_print
# 操作实验
from .element import *
from .Experiment import Experiment, search_experiment, get_current_experiment
# 实验, 标签类型
from .enums import *
# 电学实验
from .circuit import *
# 天体物理实验
from .celestial import *
# 电与磁实验
from .electromagnetism import *
# `physicsLab`自定义异常类
from .errors import *

from .lib.wires import crt_wires, del_wires

from physicsLab.plAR import *
from physicsLab.utils import *

from physicsLab import web
from physicsLab import lib
from physicsLab import music

if not os.path.exists(Experiment.SAV_ROOT_DIR):
    if platform.system() == "Windows":
        warning("Have you installed Physics-Lab-AR?")
    os.makedirs(Experiment.SAV_ROOT_DIR)

del os
del platform
