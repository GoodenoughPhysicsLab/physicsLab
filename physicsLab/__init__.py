# -*- coding: utf-8 -*-

# 颜色打印
from ._colorUtils import close_color_print
# 操作实验
from .experiment import *
# 实验类型
from .experimentType import *
# 电学实验
from .circuit import *
# 天体物理实验
from .celestial import *
# 电与磁实验
from .electromagnetism import *
# 操作元件
from .element import *
# `physicsLab`自定义异常类
from .errors import *
# 模块化电路
from .unit.wires import *
from physicsLab import unit
from physicsLab import music

# 检测操作系统
# Win: 若存档对应文件夹不存在直接报错
import os
import platform
if platform.system() == "Windows":
    if not os.path.exists(Experiment.FILE_HEAD):
        raise RuntimeError("The folder does not exist, try launching Physics-Lab-AR and try it out")
else:
    if not os.path.exists("physicsLabSav"):
        os.mkdir("physicsLabSav")

__all__ = [
    # _colorUtils.py
    "close_color_print",

    # experimentType.py
    "experimentType",

    # errors.py
    "OpenExperimentError", "WireColorError", "WireNotFoundError", "bitLengthError",
    "experimentExistError", "ExperimentTypeError", "getElementError", "crtExperimentFailError",
    "ExperimentError", "set_warning_status", "WarningError", "ElementNotExistError",

    # experiment.py
    "Experiment", "experiment", "search_Experiment", "get_Experiment",

    # element.py
    "crt_Element", "del_Element", "count_Elements", "get_Element", "clear_Elements",

    # wire.py
    "crt_Wire", "del_Wire", "count_Wires", "clear_Wires",

    # elementsClass
    "NE555", "Basic_Capacitor", 'Ground_Component', "Operational_Amplifier", "Relay_Component",
    "N_MOSFET", "Sinewave_Source", "Square_Source", "Triangle_Source", "Sawtooth_Source", "Pulse_Source",
    "Simple_Switch", "SPDT_Switch", "DPDT_Switch", "Push_Switch", "Battery_Source", "Student_Source",
    "Resistor", "Fuse_Component", "Slide_Rheostat", "Logic_Input", "Logic_Output", "Yes_Gate", "No_Gate",
    "Or_Gate", "And_Gate", "Nor_Gate", "Nand_Gate", "Xor_Gate", "Xnor_Gate", "Imp_Gate", "Nimp_Gate",
    "Half_Adder", "Full_Adder", "Multiplier", "D_Flipflop", "T_Flipflop", "JK_Flipflop", "Counter",
    "Random_Generator", "eight_bit_Input", "eight_bit_Display", "Electric_Fan", "Simple_Instrument",
    "P_MOSFET", "Incandescent_Lamp", "Buzzer", "Multimeter", "Galvanometer", "Microammeter",
    "Electricity_Meter", "Resistance_Box", "Simple_Ammeter", "Simple_Voltmeter", "Basic_Inductor",
    "Basic_Diode", "Light_Emitting_Diode", "Transformer", "Tapped_Transformer", "Mutual_Inductor",
    "Rectifier", "Transistor", "Comparator", "Air_Switch", "Schmitt_Trigger", "Spark_Gap", "Tesla_Coil",
    "Color_Light_Emitting_Diode", "Dual_Light_Emitting_Diode", "Electric_Bell", "Musical_Box",
    "Resistance_Law", "Solenoid",

    # unionElements
    "unit", "music",

    # wires.py
    "crt_Wires", "del_Wires",

    # elementXYZ.py
    "set_elementXYZ", "is_elementXYZ", "xyzTranslate", "translateXYZ", "set_O", "get_OriginPosition",
    "get_xyzUnit",

    # electromagnetism
    "Negative_Charge", "Positive_Charge"
]