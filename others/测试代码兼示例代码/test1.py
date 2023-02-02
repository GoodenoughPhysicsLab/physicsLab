from physicsLab import *

''' main '''
open_Experiment("be9e0b3f-e162-48cd-a379-ca1d6f308cf0.sav")
read_Experiment()
i = Xor_Gate(0,0,0.1)
crt_wire(i.i_low, i.o)
crt_wire(get_Element(0,0,0).o, i.i_up)
del_Element(get_Element(0,0,0))
write_Experiment()
''' end main '''
