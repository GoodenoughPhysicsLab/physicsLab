#coding=utf-8
from typing import Union
from string import digits as _digits
from physicsLab._tools import numType
import physicsLab.electricity.elementPin as _elementPin
import physicsLab.electricity.elementsClass._elementClassHead as _elementClassHead

# 小电扇
@_elementClassHead.two_pin_ArtificialCircuit_Pin
class Electric_Fan(_elementClassHead.electricityBase):
    @_elementClassHead.element_Init_HEAD
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ = None):
        self._arguments = {'ModelID': 'Electric Fan', 'Identifier': '',
                           'IsBroken': False, 'IsLocked': False,
                           'Properties': {'额定电阻': 1.0, '马达常数': 0.1, '转动惯量': 0.01, '电感': 5e-05, '负荷扭矩': 0.01,
                                          '反电动势系数': 0.001, '粘性摩擦系数': 0.01, '角速度': 0, '锁定': 1.0},
                           'Statistics': {'瞬间功率': 0, '瞬间电流': 0, '瞬间电压': 0, '功率': 0,
                                          '电压': 0, '电流': 0, '摩擦扭矩': 0, '角速度': 0,
                                          '反电动势': 0, '转速': 0, '输入功率': 0, '输出功率': 0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

# 简单乐器（更多功能的源代码在union_music）
class Simple_Instrument(_elementClassHead.electricityBase):
    @_elementClassHead.element_Init_HEAD
    def __init__(
            self,
            x: numType = 0,
            y: numType = 0,
            z: numType = 0,
            elementXYZ = None,
            instrument = 0, # 演奏的乐器，暂时只支持传入数字
            pitch = 60, # 音高/音调
            bpm = 100, # 节奏
            volume = 1.0 # 音量/响度
    ) -> None:
        if not (
            (isinstance(instrument, int) and 0 <= instrument <= 128) and
            (isinstance(pitch, int) and 20 < pitch < 128) and
            (isinstance(bpm, int) and 20 <= bpm <= 240) and
            (isinstance(volume, float) and 0 <= volume <= 1)
        ):
            raise TypeError

        self._arguments = {'ModelID': 'Simple Instrument', 'Identifier': '', 'IsBroken': False, 'IsLocked': False,
                           'Properties': {'额定电压': 3.0, '额定功率': 0.3, '音量': volume, '音高': pitch, '节拍': bpm, '锁定': 1.0,
                                          '乐器': instrument},
                           'Statistics': {'瞬间功率': 0, '瞬间电流': 0, '瞬间电压': 0, '功率': 0, '电压': 0, '电流': 0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i(self) -> _elementPin.element_Pin:
        return _elementPin.element_Pin(self, 0)

    @property
    def o(self) -> _elementPin.element_Pin:
        return _elementPin.element_Pin(self, 1)

    # 设置音高
    def set_Tonality(self, *inputs) -> "Simple_Instrument":
        '''
        输入格式：
            中音区：
                (funcInput -> 音调)
                '1' -> do,
                '1#' or '2b' -> do#,
                '2' -> ri
                ...
                7 -> xi
            低1个八度： '.1', '.1#', '.2' ...
            低2个八度： '..1', '..1#', '..2' ...
            升1个八度： '1.', '1#.', '2' ...
            以此类推即可
        '''
        def mySet_Tonality(self, tonality: numType) -> "Simple_Instrument":
            if isinstance(tonality, int):
                if 0 < tonality < 8:
                    raise TypeError('Input data error')
                tonality = str(tonality)
            elif isinstance(tonality, str):
                tonality.strip()
                for char in tonality:
                    if char not in _digits[1:8] and char not in '.#b':
                        raise TypeError('Input data error')
            else:
                raise TypeError('The entered data type is incorrect')

            pitch, pitchIndex = None, None
            for char in tonality:
                if char in _digits[1:8]:
                    pitch = [60, 62, 64, 65, 67, 69, 71][int(char) - 1]
                    pitchIndex = tonality.find(char)
            if pitch == None:
                raise TypeError('Input data error')
            for charIndex in range(tonality.__len__()):
                char = tonality[charIndex]
                if char == '.':
                    if charIndex < pitchIndex:
                        pitch -= 12
                    else:
                        pitch += 12
                elif char in _digits:
                    continue
                elif char == '#':
                    if charIndex != pitchIndex + 1:
                        raise TypeError('Input data error')
                    pitch += 1
                elif char == 'b':
                    if charIndex != pitchIndex + 1:
                        raise TypeError('Input data error')
                    pitch -= 1
                else:
                    raise TypeError('Input data error')
            self._arguments['Properties']['音高'] = pitch
            return self

        '''
        输入格式：
            tonality: C4, A5 ...
            rising_falling = True 时，为升调，为 False 时降调
            
        输入范围：
            C0 ~ C8
            注: C0: 24, C1: 36, C2: 48, C3: 60, ..., C8: 120
            
        '''
        def majorSet_Tonality(self, tonality: str = "C3", rising_falling: bool = None) -> "Simple_Instrument":
            if (not isinstance(tonality, str) or
                len(tonality) != 2 or
                tonality.upper()[0] not in "ABCDEFG" or
                tonality[1] not in "012345678" or
                not (isinstance(rising_falling, bool) or rising_falling is None)
            ):
                raise TypeError

            var = 1 if rising_falling == True else 0 if rising_falling is None else -1

            pitch = {
                'A': 22,
                'B': 23,
                'C': 24,
                'D': 25,
                'E': 26,
                'F': 27,
                'G': 28
            }[tonality.upper()[0]] + 12 * int(tonality[1]) + var

            self._arguments["Properties"]["音高"] = pitch
            return self

        try:
            return majorSet_Tonality(self, *inputs)
        except TypeError:
            try:
                return mySet_Tonality(self, *inputs)
            except TypeError:
                raise TypeError
