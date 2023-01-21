#coding: UTF-8
import sys, json
sys.path.append("C:/Users/Administrator/AppData/LocalLow/CIVITAS/Quantum Physics/Circuit/python/include")
from physicsLab import *

''' main '''
open_Experiment("be9e0b3f-e162-48cd-a379-ca1d6f308cf0.sav")
Sawtooth_Source(0,0,0)
Square_Source(0,0,0.1)
Pulse_Source(0,0,0.2)
Triangle_Source(0,0,0.3)
Sinewave_Source(0,0,0.4)
crt_wire(get_Element(0,0,0.4).i, get_Element(0,0,0.3).o)
write_Experiment()
''' end main '''
