#coding=utf-8
from electricity.elementsClass._elementClassHead import *

# 小电扇
@two_pin_ArtificialCircuit_Pin
class Electric_Fan(elementObject):
    @element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
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
class Simple_Instrument(elementObject):
    @element_Init_HEAD
    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0, z: Union[int, float] = 0):
        self._arguments = {'ModelID': 'Simple Instrument', 'Identifier': '', 'IsBroken': False, 'IsLocked': False,
                           'Properties': {'额定电压': 3.0, '额定功率': 0.3, '音量': 1.0, '音高': 60.0, '节拍': 70.0, '锁定': 1.0,
                                          '乐器': 1.0},
                           'Statistics': {'瞬间功率': 0, '瞬间电流': 0, '瞬间电压': 0, '功率': 0, '电压': 0, '电流': 0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

    @property
    def i(self):
        return element_Pin(self, 0)

    @property
    def o(self):
        return element_Pin(self, 1)

    # 设置音高
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
    def set_Tonality(self, tonality: Union[int, str]) -> None:
        if isinstance(tonality, int):
            if 0 < tonality < 8:
                raise RuntimeError('Input data error')
            tonality = str(tonality)
        elif isinstance(tonality, str):
            tonality.strip()
            for char in tonality:
                if char not in digits[1:8] and char not in '.#b':
                    raise RuntimeError('Input data error')
        else:
            raise RuntimeError('The entered data type is incorrect')

        pitch, pitchIndex = None, None
        for char in tonality:
            if char in digits[1:8]:
                pitch = [60, 62, 64, 65, 67, 69, 71][int(char) - 1]
                pitchIndex = tonality.find(char)
        if pitch == None:
            raise RuntimeError('Input data error')
        for charIndex in range(tonality.__len__()):
            char = tonality[charIndex]
            if char == '.':
                if charIndex < pitchIndex:
                    pitch -= 12
                else:
                    pitch += 12
            elif char in digits:
                continue
            elif char == '#':
                if charIndex != pitchIndex + 1:
                    raise RuntimeError('Input data error')
                pitch += 1
            elif char == 'b':
                if charIndex != pitchIndex + 1:
                    raise RuntimeError('Input data error')
                pitch -= 1
            else:
                raise RuntimeError('Input data error')
        self._arguments['Properties']['音高'] = pitch