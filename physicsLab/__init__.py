# -*- coding: utf-8 -*-
''' Python API for Physics-Lab-AR '''
import os
import platform

# 颜色打印
from ._colorUtils import close_color_print
# 操作实验
from .experiment import Experiment, experiment, search_Experiment, get_Experiment, id_to_time
# 实验, 标签类型
from .enums import *
# 电学实验
from .circuit import *
# 天体物理实验
from .celestial import *
# 电与磁实验
from .electromagnetism import *
# 操作元件
from .element import crt_Element, del_Element, count_Elements, get_Element, clear_Elements
# `physicsLab`自定义异常类
from .errors import *

from .lib.wires import crt_Wires, del_Wires

from physicsLab.plAR import *

from physicsLab import web
from physicsLab import lib
from physicsLab import music

# 检测操作系统
# Win: 若存档对应文件夹不存在直接报错
if platform.system() == "Windows":
    if not os.path.exists(Experiment.SAV_ROOT_DIR):
        raise RuntimeError("The folder does not exist, try launching Physics-Lab-AR and try it out")
else:
    if not os.path.exists(Experiment.SAV_ROOT_DIR):
        os.mkdir(Experiment.SAV_ROOT_DIR)

plAR_version = get_plAR_version()
if plAR_version is not None:
    _, mid, small = eval(f"({plAR_version.replace('.', ',')})")
    if mid < 4 or mid == 4 and small < 7:
        warning("the version of Physics-Lab-AR is less than v2.4.7")

del os
del platform
