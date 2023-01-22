from physicsLab import *

''' main '''
open_Experiment("be9e0b3f-e162-48cd-a379-ca1d6f308cf0.sav")
m=Logic_Input(-0.2,0,0)
n=Logic_Input(-0.2,0.1,0)
p=Logic_Input(-0.2,0.2,0)
q=Logic_Input(-0.2,0.3,0)
b = union_4_16_Decoder()
crt_wire(m.o, b.i_low)
crt_wire(n.o, b.i_lowmid)
crt_wire(p.o, b.i_upmid)
crt_wire(q.o, b.i_up)
a = Logic_Output(1,0,0)
crt_wire(b.o1, a.i)
write_Experiment()
''' end main '''
