# -*- coding: utf-8 -*-
from ..wire import Pin
from physicsLab.typehint import Optional, Self, List, Union, numType
from ._elementBase import CircuitBase, two_pin_ArtificialCircuit_Pin

# 小电扇
@two_pin_ArtificialCircuit_Pin
class Electric_Fan(CircuitBase):
    def __init__(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None):
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
class Simple_Instrument(CircuitBase):
    def __init__(
            self,
            x: numType = 0,
            y: numType = 0,
            z: numType = 0,
            elementXYZ: Optional[bool] = None,
            instrument: Union[int, str] = 0, # 演奏的乐器，暂时只支持传入数字
            pitch: Union[int, str] = 60, # 音高/音调: 20 ~ 128
            bpm: int = 100, # 节奏
            velocity: numType = 1.0, # 音量/响度
            rated_oltage: numType = 3.0, # 额定电压
            is_ideal_model: bool = False, # 是否为理想模式
            is_single: bool = True, # 简单乐器是否只响一次
            other_chord_notes: list = [], # 其他和弦音
    ) -> None:
        if not (
            (isinstance(instrument, int) and 0 <= instrument <= 128) and
            (isinstance(bpm, int) and 20 <= bpm <= 240) and
            (isinstance(velocity, (int, float)) and 0 <= velocity <= 1)
        ):
            raise TypeError

        self._arguments = {'ModelID': 'Simple Instrument', 'Identifier': '', 'IsBroken': False, 'IsLocked': False,
                           'Properties': {'额定电压': rated_oltage, '额定功率': 0.3, '音量': velocity, '音高': None, '节拍': bpm, '锁定': 1.0,
                                          "和弦": 1.0, '乐器': instrument, "理想模式": int(is_ideal_model), "脉冲": int(is_single), "电平": 0.0},
                           'Statistics': {'瞬间功率': 0, '瞬间电流': 0, '瞬间电压': 0, '功率': 0, '电压': 0, '电流': 0},
                           'Position': '', 'Rotation': '', 'DiagramCached': False,
                           'DiagramPosition': {'X': 0, 'Y': 0, 'Magnitude': 0.0}, 'DiagramRotation': 0}

        self.set_Tonality(pitch)
        self.notes: List[int] = [self._arguments["Properties"]["音高"]] # 仅用于记录self已有的音符
        for a_note in other_chord_notes:
            self.add_note(a_note)

    @property
    def i(self) -> Pin:
        return Pin(self, 0)

    @property
    def o(self) -> Pin:
        return Pin(self, 1)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._position.x}, {self._position.y}, {self._position.z}, " \
               f"elementXYZ={self.is_elementXYZ}, instrument={self._arguments['Properties']['乐器']}, " \
               f"pitch={self._arguments['Properties']['音高']}, bpm={self._arguments['Properties']['节拍']}, " \
               f"velocity={self._arguments['Properties']['音量']}, rated_oltage={self._arguments['Properties']['额定电压']}, " \
               f"is_ideal_model={self._arguments['Properties']['理想模式']}, is_single={bool(self._arguments['Properties']['脉冲'])}, " \
               f"other_chord_notes={self.notes})"

    # 物实v2.4.7新功能: 简单乐器同时播放多个音符
    def add_note(self, *pitchs: int) -> Self:
        if not all(isinstance(a_pitch, int) and 0 <= a_pitch < 128 for a_pitch in pitchs):
            raise TypeError

        for a_pitch in pitchs:
            if a_pitch not in self.notes:
                amount: int = int(self._arguments["Properties"]["和弦"])
                self._arguments["Properties"][f"音高{amount}"] = a_pitch
                self._arguments["Properties"]["和弦"] += 1
                self.notes.append(a_pitch)

        return self

    # 获取简单乐器已有的和弦
    def get_chord(self) -> tuple:
        return tuple(self.notes)

    # 获取简单乐器的和弦
    def get_instrument(self) -> int:
        return self._arguments["Properties"]["乐器"]

    # 设置音高
    def set_Tonality(self, pitch: Union[int, str], tone: Optional[bool] = None) -> "Simple_Instrument":
        '''
        输入格式：
            中音区：
                (funcInput -> 音调)
                '1' -> do,
                '1#' or '2b' -> do#,
                '2' -> ri
                ...
                7 -> xi
            低1个八度: '.1', '.1#', '.2' ...
            低2个八度: '..1', '..1#', '..2' ...
            升1个八度: '1.', '1#.', '2' ...
            以此类推即可
        '''
        # def mySet_Tonality(self, tonality: numType) -> "Simple_Instrument":
        #
        #     if isinstance(tonality, str):
        #         tonality.strip()
        #         for char in tonality:
        #             if char not in _digits[1:8] and char not in '.#b':
        #                 raise TypeError('Input data error')
        #     else:
        #         raise TypeError('The entered data type is incorrect')
        #
        #     pitch, pitchIndex = None, None
        #     for char in tonality:
        #         if char in _digits[1:8]:
        #             pitch = [60, 62, 64, 65, 67, 69, 71][int(char) - 1]
        #             pitchIndex = tonality.find(char)
        #     if pitch == None:
        #         raise TypeError('Input data error')
        #     for charIndex in range(tonality.__len__()):
        #         char = tonality[charIndex]
        #         if char == '.':
        #             if charIndex < pitchIndex:
        #                 pitch -= 12
        #             else:
        #                 pitch += 12
        #         elif char in _digits:
        #             continue
        #         elif char == '#':
        #             if charIndex != pitchIndex + 1:
        #                 raise TypeError('Input data error')
        #             pitch += 1
        #         elif char == 'b':
        #             if charIndex != pitchIndex + 1:
        #                 raise TypeError('Input data error')
        #             pitch -= 1
        #         else:
        #             raise TypeError('Input data error')
        #     self._arguments['Properties']['音高'] = pitch
        #     return self

        '''
        输入格式：
            tonality: C4, A5 ...
            rising_falling = True 时，为升调，为 False 时降调

        输入范围：
            C0 ~ C8
            注: C0: 24, C1: 36, C2: 48, C3: 60, ..., C8: 120

        '''
        def majorSet_Tonality(self, tonality: str = "C3", rising_falling: Optional[bool] = None) -> "Simple_Instrument":
            if (not isinstance(tonality, str) or
                len(tonality) != 2 or
                tonality.upper()[0] not in "ABCDEFG" or
                tonality[1] not in "012345678" or
                not (isinstance(rising_falling, bool) or rising_falling is None)
            ):
                raise TypeError

            var = 1 if rising_falling is True else 0 if rising_falling is None else -1

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

        # main
        if isinstance(pitch, int):
            if 0 <= pitch < 128:
                self._arguments["Properties"]["音高"] = pitch
            else:
                raise TypeError('Input number out of range')
        elif isinstance(pitch, str):
            majorSet_Tonality(self, pitch, tone)
        else:
            raise TypeError

        return self