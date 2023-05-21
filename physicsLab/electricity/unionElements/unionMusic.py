#coding=utf-8
import math as _math
from typing import Union as _Union
import physicsLab._tools as _tools
import physicsLab.electricity.elementXYZ as _elementXYZ
import physicsLab.electricity.elementsClass as _elementsClass
from physicsLab.electricity.unionElements.unionLogic import d_WaterLamp
import physicsLab.electricity.unionElements._unionClassHead as _unionClassHead

# unionMusic音轨
class track(_unionClassHead.unionBase):
    def __init__(
            self,
            x: _tools.numType = 0,
            y: _tools.numType = 0,
            z: _tools.numType = 0,
            elementXYZ = None,
            musicArray: _Union[tuple, list, str] = ()
    ):
        if not (
            isinstance(x, (int, float)) or
            isinstance(y, (int, float)) or
            isinstance(z, (int, float)) or
            isinstance(musicArray, (tuple, list, str))
        ):
            raise TypeError

        isnt_elementXYZ = False
        if not (elementXYZ == True or (_elementXYZ.is_elementXYZ() == True and elementXYZ is None)):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)
            isnt_elementXYZ = True
            _elementXYZ.set_elementXYZ(True)

        # 计算音乐矩阵的宽
        side = None
        if len(musicArray) > 1:
            side = _math.ceil(_math.sqrt(musicArray.__len__()))
        else:
            side = 2

        tick = _elementsClass.Nimp_Gate(x + 1, y, z)
        _elementsClass.Logic_Input(x, y, z).o - tick.i_up
        tick.o - tick.i_low
        tick.o - _elementsClass.Counter(x, y + 1, z).i_up

        xPlayer = d_WaterLamp(x + 1, y + 1, z, unionHeading=True, bitLength=side)
        d_WaterLamp(x, y + 3, z, bitLength=side)
        xPlayer[0].o_low - _elementsClass.Yes_Gate(x + 1, y + 2, z + 1).i


        if isnt_elementXYZ:
            _elementXYZ.set_elementXYZ(False)
