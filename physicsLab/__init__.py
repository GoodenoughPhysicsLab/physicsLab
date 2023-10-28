#coding=utf-8

# Win: 若存档对应文件夹不存在直接报错
import physicsLab._fileGlobals as _fileGlobals
from os import path as _path, mkdir as _mkdir

# 检测操作系统
from sys import platform as _platform
if _platform == "win32":
    if not _path.exists(_fileGlobals.FILE_HEAD):
        raise WindowsError("The folder does not exist, try launching Physics-Lab-AR and try it out")
else:
    if not _path.exists("physicsLabSav"):
        _mkdir("physicsLabSav")

# 颜色打印
from physicsLab._colorUtils import close_color_print
# 操作实验
from physicsLab.experiment import *
# 电学实验
from physicsLab.electricity import *
# 天体物理实验
from physicsLab.astrophysics import *
# 电与磁实验
from physicsLab.electromagnetism.elementsClass import *
# 操作元件
from physicsLab.element import *
# 自定义异常类
from physicsLab.errors import *
# 获取存档类型与整个存档文件
from physicsLab._fileGlobals import get_Sav, get_experimentType, experimentType
# 模块化电路
import physicsLab.electricity.unionElements.unionLogic as union
import physicsLab.electricity.unionElements.unionMusic as music

# 在import了physicsLab的程序的第一行加上#coding=utf-8
try: # 在cmd或者shell上无法执行该功能
    import sys
    s = ""
    with open(sys.argv[0], encoding='utf-8') as f:
        s = f.read()
    if not s.replace('\n', '').startswith("#coding=utf-8"):
        with open(sys.argv[0], 'w', encoding='utf-8') as f:
            if s.startswith('\n'):
                f.write(f'#coding=utf-8{s}')
            else:
                f.write(f'#coding=utf-8\n{s}')
    del sys
except FileNotFoundError:
    close_color_print()

__all__ = [
    # _colorUtils.py
    "close_color_print",
    # _fileGlobals.py
    "_fileGlobals", "get_Sav", "get_experimentType", "experimentType",

    # errors.py
    "openExperimentError", "wireColorError", "wireNotFoundError", "bitLengthError",
    "experimentExistError", "experimentTypeError", "getElementError", "crtExperimentFailError",

    # experiment.py
    "experiment", "open_Experiment", "crt_Experiment", "read_Experiment", "write_Experiment",
    "rename_Experiment", "show_Experiment", "del_Experiment", "yield_Experiment", "exist_Experiment",
    "open_or_crt_Experiment",

    # element.py
    "crt_Element", "del_Element", "count_Elements", "get_Element", "clear_Elements", "print_Elements",

    # wire.py
    "crt_Wire", "del_Wire", "count_Wires", "clear_Wires", "print_Wires",

    # elementsClass
    "NE555", "Basic_Capacitor", 'Ground_Component', "Operational_Amplifier", "Relay_Component",
    "N_MOSFET", "Sinewave_Source", "Square_Source", "Triangle_Source", "Sawtooth_Source", "Pulse_Source",
    "Simple_Switch", "SPDT_Switch", "DPDT_Switch", "Push_Switch", "Battery_Source", "Student_Source",
    "Resistor", "Fuse_Component", "Slide_Rheostat", "Logic_Input", "Logic_Output", "Yes_Gate", "No_Gate",
    "Or_Gate", "And_Gate", "Nor_Gate", "Nand_Gate", "Xor_Gate", "Xnor_Gate", "Imp_Gate", "Nimp_Gate",
    "Half_Adder", "Full_Adder", "Multiplier", "D_Flipflop", "T_Flipflop", "JK_Flipflop", "Counter",
    "Random_Generator", "eight_bit_Input", "eight_bit_Display", "Electric_Fan", "Simple_Instrument",
    "P_MOSFET",

    # unionElements
    "union", "music",

    # wires.py
    "crt_Wires", "del_Wires",

    # elementXYZ.py
    "set_elementXYZ", "is_elementXYZ", "xyzTranslate", "translateXYZ", "set_O", "get_OriginPosition", "get_xyzUnit",

    # electromagnetism
    "Negative_Charge", "Positive_Charge"
]
