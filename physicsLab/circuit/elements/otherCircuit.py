# -*- coding: utf-8 -*-
import physicsLab.plAR as plar
import physicsLab.errors as errors

from .._circuit_core import _TwoPinMixIn, CircuitBase, Pin
from physicsLab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    Self,
    Generate,
    Union,
    List,
    override,
    Union,
    Tuple,
    LiteralString,
    final,
)

class Buzzer(_TwoPinMixIn):
    ''' 蜂鸣器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Buzzer", "Identifier": Generate, "IsBroken": False,
            "IsLocked": False, "Properties": {"额定电压": 3.0, "额定功率": 0.3, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0,
                            "功率": 0.0, "电压": 0.0, "电流": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "嗡鸣器"

class Spark_Gap(_TwoPinMixIn):
    ''' 火花隙 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Spark Gap", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"击穿电压": 1000.0, "击穿电阻": 1.0, "维持电流": 0.001, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "火花隙"

class Tesla_Coil(_TwoPinMixIn):
    ''' 特斯拉线圈 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Tesla Coil", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"击穿电压": 30000.0, "次级电容": 2.5e-11, "次级电阻": 1.0,
                            "电感1": 0.1, "电感2": 90.0, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "特斯拉线圈"

class Color_Light_Emitting_Diode(CircuitBase):
    ''' 彩色发光二极管 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
    ) -> None:
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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "彩色发光二极管"

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

class Dual_Light_Emitting_Diode(_TwoPinMixIn):
    ''' 演示发光二极管 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
    ) -> None:
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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "演示发光二极管"

class Electric_Bell(_TwoPinMixIn):
    ''' 电铃 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Electric Bell", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"额定电压": 3.0, "额定功率": 0.3, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0,
                            "功率": 0.0, "电压": 0.0, "电流": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "电铃"

class Musical_Box(_TwoPinMixIn):
    ''' 八音盒 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "Musical Box", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"额定电压": 3.0, "额定功率": 0.3, "锁定": 1.0},
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0, "功率": 0.0,
                            "电压": 0.0, "电流": 0.0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "八音盒"

class Resistance_Law(CircuitBase):
    ''' 电阻定律实验 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
    ) -> None:
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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "电阻定律实验"

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
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
    ) -> None:
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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "通电螺线管"

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

class Electric_Fan(_TwoPinMixIn):
    ''' 小电扇 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
    ) -> None:
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

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "小电扇"

class Simple_Instrument(CircuitBase):
    ''' 简单乐器 '''
    def __init__(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
            /, *,
            pitches: Union[List[int], Tuple[int]],
            elementXYZ: Optional[bool] = None,
            identifier: Optional[str] = None,
            rated_oltage: num_type = 3.0,
            volume: num_type = 1,
            bpm: int = 100,
            instrument: int = 0,
            is_ideal: bool = False,
            is_pulse: bool = True,
    ) -> None:
        ''' @param rated_oltage: 额定电压
            @param volume: 音量 (响度)
            @param pitch: 音高
            @param instrument: 演奏的乐器，暂时只支持传入数字
            @param bpm: 节奏
            @param is_ideal: 是否为理想模式
            @param is_pulse: 简单乐器是否只响一次
        '''
        self._data: CircuitElementData = {
            "ModelID": "Simple Instrument", "Identifier": Generate,
            "IsBroken": False, "IsLocked": False,
            "Properties": {"额定电压": Generate, "额定功率": 0.3,
                            "音量": Generate, "音高": Generate, "节拍": Generate,
                            "锁定": 1.0, "和弦": Generate, "乐器": Generate,
                            "理想模式": Generate, "脉冲": Generate, "电平": 0.0},
            "Statistics": {"瞬间功率": 0, "瞬间电流": 0, "瞬间电压": 0,
                            "功率": 0, "电压": 0, "电流": 0},
            "Position": Generate, "Rotation": Generate, "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0}, "DiagramRotation": 0
        }

        self.pitches: List[int] = list(pitches)
        self.set_properties(
            rated_oltage=rated_oltage,
            volume=volume,
            bpm=bpm,
            instrument=instrument,
            is_ideal=is_ideal,
            is_pulse=is_pulse,
        )

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "简单乐器"

    @property
    def data(self) -> CircuitElementData:
        if not all(isinstance(a_pitch, int) for a_pitch in self.pitches):
            raise TypeError
        if not all(0 <= a_pitch < 128 for a_pitch in self.pitches):
            raise ValueError

        plar_version = plar.get_plAR_version()
        if plar_version is not None and plar_version < (2, 4, 7):
            errors.warning("Physics-Lab-AR's version less than 2.4.7")

        # TODO 是否需要先清空所有 "音高"
        for i, a_pitch in enumerate(self.pitches):
            if i == 0:
                self._data["Properties"]["音高"] = a_pitch
            else:
                self._data["Properties"][f"音高{i}"] = a_pitch
        self._data["Properties"]["和弦"] = len(self.pitches)

        return self._data

    @data.setter
    def data(self, data: CircuitElementData) -> None:
        self._data = data

    def set_properties(
            self,
            *,
            rated_oltage: Optional[num_type] = None,
            volume: Optional[num_type] = None,
            bpm: Optional[int] = None,
            instrument: Optional[int] = None,
            is_ideal: Optional[bool] = None,
            is_pulse: Optional[bool] = None,
    ) -> Self:
        if not isinstance(rated_oltage, (int, float, type(None))) \
                or not isinstance(volume, (int, float, type(None))) \
                or not isinstance(bpm, (int, type(None))) \
                or not isinstance(instrument, (int, type(None))) \
                or not isinstance(is_ideal, (bool, type(None))) \
                or not isinstance(is_pulse, (bool, type(None))):
            raise TypeError

        if rated_oltage is not None:
            self.properties["额定电压"] = rated_oltage
        if volume is not None:
            self.properties["音量"] = volume
        if bpm is not None:
            self.properties["节拍"] = bpm
        if instrument is not None:
            self.properties["乐器"] = instrument
        if is_ideal is not None:
            self.properties["理想模式"] = int(is_ideal)
        if is_pulse is not None:
            self.properties["脉冲"] = int(is_pulse)

        assert instrument is not None and bpm is not None and volume is not None
        if not 0 <= instrument <= 128 \
                or not 20 <= bpm <= 240 \
                or not 0 <= volume <= 1:
            raise ValueError

        return self

    @property
    def i(self) -> Pin:
        return Pin(self, 0)

    @property
    def o(self) -> Pin:
        return Pin(self, 1)

    @override
    def __repr__(self) -> str:
        return f"Simple_Instrument({self._position.x}, {self._position.y}, {self._position.z}, " \
            f"elementXYZ={self.is_elementXYZ}, " \
            f"pitches={self.pitches}, " \
            f"instrument={self.properties['乐器']}, " \
            f"bpm={self._data['Properties']['节拍']}, " \
            f"volume={self._data['Properties']['音量']}, " \
            f"rated_oltage={self._data['Properties']['额定电压']}, " \
            f"is_ideal={bool(self._data['Properties']['理想模式'])}, " \
            f"is_pulse={bool(self._data['Properties']['脉冲'])}" \
            f")"

    @staticmethod
    def str2num_pitch(
            pitch: str,
            rising_falling: Optional[bool] = None
    ) -> int:
        """ 输入格式：
                pitch: C4, A5 ...
                rising_falling = True 时，为升调，为 False 时降调

            输入范围：
                C0 ~ C8
                注: C0: 24, C1: 36, C2: 48, C3: 60, ..., C8: 120
        """
        if not isinstance(pitch, str) \
                or not isinstance(rising_falling, (bool, type(None))):
            raise TypeError
        if len(pitch) != 2 \
                or pitch.upper()[0] not in "ABCDEFG" \
                or pitch[1] not in "012345678":
            raise ValueError

        var = 1 if rising_falling is True else 0 if rising_falling is None else -1

        res = {
            'A': 22,
            'B': 23,
            'C': 24,
            'D': 25,
            'E': 26,
            'F': 27,
            'G': 28,
        }[pitch.upper()[0]] + 12 * int(pitch[1]) + var

        return res
