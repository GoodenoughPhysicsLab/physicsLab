# -*- coding: utf-8 -*-
import physicsLab.plAR as plar
import physicsLab.errors as errors

from ..wire import Pin
from ._circuitbase import TwoPinMixIn, CircuitBase
from physicsLab.typehint import Optional, numType, CircuitElementData, Self, Generate, Union, List, override

class Buzzer(TwoPinMixIn):
    ''' 蜂鸣器 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Buzzer", "Identifier": Generate, "IsBroken": False,
            "IsLocked": False, "Properties": {"额定电压": 3.0, "额定功率": 0.3},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0,
                            "功率": 0.0, "电压": 0.0, "电流": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

class Spark_Gap(TwoPinMixIn):
    ''' 火花隙 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Spark Gap", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"击穿电压": 1000.0, "击穿电阻": 1.0, "维持电流": 0.001, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

class Tesla_Coil(TwoPinMixIn):
    ''' 特斯拉线圈 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Tesla Coil", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"击穿电压": 30000.0, "次级电容": 2.5e-11, "次级电阻": 1.0,
                            "电感1": 0.1, "电感2": 90.0, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

class Color_Light_Emitting_Diode(CircuitBase):
    ''' 彩色发光二极管 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Color Light-Emitting Diode", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"反向耐压": 6.0, "击穿电压": 0.0, "前向压降": 2.1024259,
                            "工作电流": 0.01, "工作电压": 3.0, "锁定": 1.0},
            "Statistics": {"电流1": 0.0, "电压1": 0.0, "功率1": 0.0, "亮度1": 0.0,
                            "电流2": 0.0, "电压2": 0.0, "功率2": 0.0, "亮度2": 0.0,
                            "电流3": 0.0, "电压3": 0.0, "功率3": 0.0, "亮度3": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @property
    def l_up(self) -> Pin:
        return Pin(self, 0)

    @property
    def l_mid(self) -> Pin:
        return Pin(self, 1)

    @property
    def l_low(self) -> Pin:
        return Pin(self, 2)

    @property
    def r(self) -> Pin:
        return Pin(self, 3)

class Dual_Light_Emitting_Diode(TwoPinMixIn):
    ''' 演示发光二极管 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Dual Light-Emitting Diode", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"反向耐压": 6.0, "击穿电压": 0.0, "前向压降": 2.1024259,
                            "工作电流": 0.01, "工作电压": 3.0, "锁定": 1.0},
            "Statistics": {"电流1": 0.0, "电压1": 0.0, "功率1": 0.0, "亮度1": 0.0, "电流2": 0.0,
                            "电压2": 0.0, "功率2": 0.0, "亮度2": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

class Electric_Bell(TwoPinMixIn):
    ''' 电铃 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Electric Bell", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"额定电压": 3.0, "额定功率": 0.3, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0,
                            "功率": 0.0, "电压": 0.0, "电流": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

class Musical_Box(TwoPinMixIn):
    ''' 八音盒 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Musical Box", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"额定电压": 3.0, "额定功率": 0.3, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0, "功率": 0.0,
                            "电压": 0.0, "电流": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

class Resistance_Law(CircuitBase):
    ''' 电阻定律实验 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Resistance Law", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"电阻率": 1.0, "电阻率2": 4.0, "电阻率3": 1.0, "最大长度": 2.0,
                            "最小长度": 0.1, "长度": 1.0, "最大半径": 0.01, "最小半径": 0.0001,
                            "半径": 0.0005, "电阻": 1.4, "电阻2": 0.56, "电阻3": 0.02, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0, "功率": 0.0,
                            "电压": 0.0, "电流": 0.0, "瞬间功率1": 0.0, "瞬间电流1": 0.0,
                            "瞬间电压1": 0.0, "功率1": 0.0, "电压1": 0.0, "电流1": 0.0,
                            "瞬间功率2": 0.0, "瞬间电流2": 0.0, "瞬间电压2": 0.0, "功率2": 0.0,
                            "电压2": 0.0, "电流2": 0.0, "瞬间功率3": 0.0, "瞬间电流3": 0.0,
                            "瞬间电压3": 0.0, "功率3": 0.0, "电压3": 0.0, "电流3": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @property
    def l_low(self) -> Pin:
        return Pin(self, 0)

    @property
    def l_lowmid(self) -> Pin:
        return Pin(self, 1)

    @property
    def l_upmid(self) -> Pin:
        return Pin(self, 2)

    @property
    def l_up(self) -> Pin:
        return Pin(self, 3)

    @property
    def r_low(self) -> Pin:
        return Pin(self, 4)

    @property
    def r_lowmid(self) -> Pin:
        return Pin(self, 5)

    @property
    def r_upmid(self) -> Pin:
        return Pin(self, 6)

    @property
    def r_up(self) -> Pin:
        return Pin(self, 7)

class Solenoid(CircuitBase):
    ''' 通电螺线管 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Solenoid", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"插入铁芯": 1.0, "内圈状态": 0.0, "切割速度": 1.0, "锁定": 1.0,
                            "线圈匝数": 100.0, "线圈位置": 0.0, "内线圈半径": 0.1, "磁通量": 0.0},
            "Statistics": {"电流-内线圈": 0.0, "功率-内线圈": 0.0, "电压-内线圈": 0.0,
                            "磁感应强度": 0.0, "磁通量": 0.0, "电压-外线圈": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @property
    def subred(self) -> Pin:
        return Pin(self, 0)

    @property
    def subblack(self) -> Pin:
        return Pin(self, 1)

    @property
    def red(self) -> Pin:
        return Pin(self, 2)

    @property
    def black(self) -> Pin:
        return Pin(self, 3)

class Electric_Fan(TwoPinMixIn):
    ''' 小电扇 '''
    def __init__(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Electric Fan", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"额定电阻": 1.0, "马达常数": 0.1, "转动惯量": 0.01,
                            "电感": 5e-05, "负荷扭矩": 0.01, "反电动势系数": 0.001,
                            "粘性摩擦系数": 0.01, "角速度": 0, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0, "瞬间电流": 0, "瞬间电压": 0, "功率": 0,
                            "电压": 0, "电流": 0, "摩擦扭矩": 0, "角速度": 0,
                            "反电动势": 0, "转速": 0, "输入功率": 0, "输出功率": 0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

class Simple_Instrument(TwoPinMixIn):
    ''' 简单乐器 '''
    def __init__(
            self,
            x: numType,
            y: numType,
            z: numType,
            elementXYZ: Optional[bool] = None,
            instrument: Union[int, str] = 0, # 演奏的乐器，暂时只支持传入数字
            pitch: Union[int, str] = 60, # 音高/音调: 20 ~ 128
            bpm: int = 100, # 节奏
            velocity: numType = 1.0, # 音量/响度
            rated_oltage: numType = 3.0, # 额定电压
            is_ideal_model: bool = False, # 是否为理想模式
            is_single: bool = True, # 简单乐器是否只响一次
    ) -> None:
        if not (
            (isinstance(instrument, int) and 0 <= instrument <= 128) and
            (isinstance(bpm, int) and 20 <= bpm <= 240) and
            (isinstance(velocity, (int, float)) and 0 <= velocity <= 1) and
            isinstance(rated_oltage, (int, float)) and
            isinstance(is_ideal_model, bool) and
            isinstance(is_single, bool)
        ):
            raise TypeError

        self.data: CircuitElementData = {
            "ModelID": "Simple Instrument", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"额定电压": rated_oltage, "额定功率": 0.3,
                            "音量": velocity, "音高": None, "节拍": bpm,
                            "锁定": 1.0, "和弦": 1.0, "乐器": instrument,
                            "理想模式": int(is_ideal_model),
                            "脉冲": int(is_single), "电平": 0.0},
            "Statistics": {"瞬间功率": 0, "瞬间电流": 0, "瞬间电压": 0,
                            "功率": 0, "电压": 0, "电流": 0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

        self.set_tonality(pitch)
        self.notes: List[int] = [self.data["Properties"]["音高"]] # 仅用于记录self已有的音符

    @property
    def i(self) -> Pin:
        return Pin(self, 0)

    @property
    def o(self) -> Pin:
        return Pin(self, 1)

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._position.x}, {self._position.y}, {self._position.z}, " \
               f"elementXYZ={self.is_elementXYZ}, instrument={self.data['Properties']['乐器']}, " \
               f"pitch={self.data['Properties']['音高']}, bpm={self.data['Properties']['节拍']}, " \
               f"velocity={self.data['Properties']['音量']}, " \
               f"rated_oltage={self.data['Properties']['额定电压']}, " \
               f"is_ideal_model={self.data['Properties']['理想模式']}, " \
               f"is_single={bool(self.data['Properties']['脉冲'])}" \
               f").add_note({str(self.notes)[1:-2]})"

    def add_note(self, *pitchs: int) -> Self:
        ''' 物实v2.4.7功能: 简单乐器同时播放多个音符 '''
        if not all(isinstance(a_pitch, int) and 0 <= a_pitch < 128 for a_pitch in pitchs):
            raise TypeError

        plar_version = plar.get_plAR_version()
        if plar_version is not None and plar_version < (2, 4, 7):
            errors.warning("Physics-Lab-AR's version less than 2.4.7")

        for a_pitch in pitchs:
            if a_pitch not in self.notes:
                amount: int = int(self.data["Properties"]["和弦"])
                self.data["Properties"][f"音高{amount}"] = a_pitch
                self.data["Properties"]["和弦"] += 1
                self.notes.append(a_pitch)

        return self

    def get_chord(self) -> tuple:
        ''' 获取简单乐器已有的和弦 '''
        return tuple(self.notes)

    def get_instrument(self) -> int:
        return self.data["Properties"]["乐器"]

    def set_tonality(self, pitch: Union[int, str], rising_falling: Optional[bool] = None) -> "Simple_Instrument":
        ''' 输入格式：
            tonality: C4, A5 ...
            rising_falling = True 时, 为升调, 为 False 时降调
        '''

        if isinstance(pitch, int):
            if 0 <= pitch < 128:
                self.data["Properties"]["音高"] = pitch
            else:
                raise TypeError("Input number out of range")
        elif isinstance(pitch, str):
            self.data["Properties"]["音高"] = majorSet_Tonality(pitch, rising_falling)
        else:
            raise TypeError

        return self

def majorSet_Tonality(pitch: str,
                      rising_falling: Optional[bool] = None
                      ) -> int:
    """ 输入格式：
            tonality: C4, A5 ...
            rising_falling = True 时，为升调，为 False 时降调

        输入范围：
            C0 ~ C8
            注: C0: 24, C1: 36, C2: 48, C3: 60, ..., C8: 120
    """
    if (not isinstance(pitch, str) or
        len(pitch) != 2 or
        pitch.upper()[0] not in "ABCDEFG" or
        pitch[1] not in "012345678" or
        not (isinstance(rising_falling, bool) or rising_falling is None)
    ):
        raise TypeError

    var = 1 if rising_falling is True else 0 if rising_falling is None else -1

    res = {
        'A': 22,
        'B': 23,
        'C': 24,
        'D': 25,
        'E': 26,
        'F': 27,
        'G': 28
    }[pitch.upper()[0]] + 12 * int(pitch[1]) + var

    return res
