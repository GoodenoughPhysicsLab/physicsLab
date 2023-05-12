#coding=utf-8
# 操作实验
from physicsLab.experiment import *
# 电学实验
from physicsLab.electricity import *
# 天体物理实验
import physicsLab.astrophysics as astrophysics
# 电与磁实验
from physicsLab.electromagnetism.elementsClass import *
# 操作元件
from physicsLab.element import *
# 自定义异常类
from physicsLab.errors import *
# 获取存档类型与整个存档文件
from physicsLab._fileGlobals import get_experimentType, get_Sav


# __all__ = [
#     "get_Sav", "get_experimentType",
#
#     "openExperimentError", "wireColorError", "wireNotFoundError", "bitLengthError",
#     "experimentExistError", "experimentTypeError",
#
#     "experiment", "open_Experiment", "crt_Experiment", "read_Experiment", "write_Experiment",
#     "rename_Experiment", "show_Experiment", "del_Experiment", "rollBack_Experiment",
#     "introduce_Experiment", "title_Experiment",
#
#     "crt_Element", "del_Element", "count_Elements", "get_Element", "clear_Elements",
#
#     "crt_Wire", "del_Wire", "count_Wires", "clear_Wires",
#
#     "NE555", "Basic_Capacitor", 'Ground_Component', "Operational_Amplifier", "Relay_Component",
#     "N_MOSFET", "Sinewave_Source", "Square_Source", "Triangle_Source", "Sawtooth_Source", "Pulse_Source",
#     "Simple_Switch", "SPDT_Switch", "DPDT_Switch", "Push_Switch", "Battery_Source", "Student_Source",
#     "Resistor", "Fuse_Component", "Slide_Rheostat", "Logic_Input", "Logic_Output", "Yes_Gate", "No_Gate",
#     "Or_Gate", "And_Gate", "Nor_Gate", "Nand_Gate", "Xor_Gate", "Xnor_Gate", "Imp_Gate", "Nimp_Gate",
#     "Half_Adder", "Full_Adder", "Multiplier", "D_Flipflop", "T_Flipflop", "JK_Flipflop", "Counter",
#     "Random_Generator", "eight_bit_Input", "eight_bit_Display", "Electric_Fan", "Simple_Instrument",
#
#     "union_Inputs", "union_Outputs", "union_Sum", "union_Sub", "union_2_4_Decoder", "union_4_16_Decoder", "d_WaterLamp",
#
#     "crt_Wires", "del_Wires",
#
#     "set_elementXYZ", "is_elementXYZ", "set_O", "get_OriginPosition", "get_xyzUnit",
#
#     "Negative_Charge", "Positive_Charge"
# ]
