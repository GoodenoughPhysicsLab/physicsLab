#coding=utf-8
import json

import mido
import physicsLab.errors as errors
import physicsLab._colorUtils as colorUtils
import physicsLab.electricity.elementXYZ as _elementXYZ
import physicsLab.electricity.elementsClass as _elementsClass

from typing import *
from copy import deepcopy
from math import ceil, sqrt
from os import path as _path
from enum import Enum, unique

from .wires import crt_Wires
from ...element import get_Element
from .unionLogic import D_WaterLamp
from physicsLab._tools import numType

# type
noteType = List[Optional["Note"]] # 音符类型
chordType = Union[Tuple["Note"], List["Note"]] # 和弦类型

# const
NOTE_ON = "note_on"
NOTE_OFF = "note_off"
PROGRAM_CHANGE = "program_change"
SET_TEMPO = "set_tempo"
TEXT = "text"

# midi类，用于提供physicsLab与midi文件之间的桥梁
''' 重要midi事件及作用:
    note_on        -> message: 播放音符
    note_off       -> message: 停止播放音符
    program_change -> message: 改变某个音轨对应的音色
    set_tempo  -> metaMessage: 改变midi播放速度
    text       -> metaMessage: 占位符
'''
class Midi:
    # 仅被Midi.sound方法调用
    # 你也许需要这样写：e.g. player=music.Midi.PLAYER.os
    @unique
    class PLAYER(Enum):
        plmidi = 0
        pygame = 1
        os = 2
    PLAYER = PLAYER

    def __init__(self, midifile: Optional[str] = None) -> None:
        ''' self.messages的参数格式:
            [
                (type: {{note_on or note_off}}, channel, note, velocity, time),
                (type: {{program_change}}, channel, program, time),
                (type: {{set_tempo}}, tempo, time)
            ]
            time: 间隔这么多时间之后执行该type
            note: midi音高 (音调)
            velocity: midi音符的响度
            channel: midi通道
            program: midi音色
            tempo: 播放速度
        '''
        self.midifile: Optional[str] = midifile
        self.messages: Optional[mido.MidiTrack] = None
        if midifile is None:
            return
        self.messages = self.__get_midi_messages()

    # 使用mido打开一个midi文件并获取其tracks
    def __get_midi_messages(self) -> mido.MidiTrack:
        _midifile = mido.MidiFile(self.midifile, clip=True)
        tabsign: bool = False
        res = mido.MidiTrack()
        for msg in mido.merge_tracks(_midifile.tracks):
            if msg.type in (NOTE_ON, NOTE_OFF, PROGRAM_CHANGE, SET_TEMPO):
                res.append(msg)
                tabsign = False

            elif msg.time != 0:
                if not tabsign:
                    res.append(mido.MetaMessage("text", text="", time=msg.time))
                    tabsign = True
                    continue
                res[-1].time += msg.time # type: ignore
        return res

    # 播放midi类存储的信息
    def sound(self, player: Optional[PLAYER] = None) -> Optional["Midi"]:
        # 使用plmidi播放midi
        def sound_by_plmidi() -> bool:
            try:
                from plmidi import sound
            except ImportError:
                return False
            else:
                if self.midifile is None:
                    errors.warning("can not sound because self.midifile is None")
                    return False
                
                sound([(NOTE_ON, 10, 60, 0, 0)])
                return True

        # 使用pygame播放midi
        def sound_by_pygame() -> bool:
            try:
                from pygame import mixer, time
            except ImportError:
                return False
            else:
                if self.midifile is None:
                    errors.warning("can not sound because self.midifile is None")
                    return False
                # 代码参考自musicpy的play函数
                mixer.init()
                mixer.music.load(self.midifile)
                mixer.music.play()
                while mixer.music.get_busy():
                    time.delay(10)
                return True
        
        # 使用系统调用播放midi
        def sound_by_os() -> bool:
            from os import path, system

            if self.midifile is None:
                errors.warning("can not sound because self.midifile is None")
                return False
            
            if path.exists(self.midifile):
                system(self.midifile)
            elif path.exists("pltemp.mid"):
                system("pltemp.mid")
            else:
                return False
            return True

        if not isinstance(player, Midi.PLAYER) and player is not None:
            raise TypeError        

        # main
        if player is not None:
            if not (sound_by_plmidi, sound_by_pygame, sound_by_os)[player.value]():
                errors.warning("can not use this way to sound midi.")
            return
        
        if sound_by_plmidi():
            colorUtils.printf("sound by using plmidi", colorUtils.COLOR.CYAN)
        elif sound_by_pygame():
            colorUtils.printf("sound by using pygame", colorUtils.COLOR.CYAN)
        elif sound_by_os():
            colorUtils.printf("sound by using os", colorUtils.COLOR.CYAN)
        else:
            errors.warning("can not use sound methods")
        
        return self

    # 转换为physicsLab的piece类
    # TODO 转换时忽略note_off，因为物实目前只适合给一个默认值
    # 但超长音符应该考虑下适当调整物实简单乐器播放时长
    def translate_to_piece(self) -> "Piece":
        pass

    ''' *.plm.py文件:
        plm即为 physicsLab music file
        为了修改方便, 默认使用 str(mido.MidiTrack) 的方式导出
        而且是个Py文件, 大家想要自己修改也是很方便的
    '''
    def read_plm(self, plmpath: str = "temp.plm.py") -> "Midi":
        def _read_plm(plmpath):
            context = None
            with open(plmpath, encoding="utf-8") as f:
                context = f.read()
            
            import re
            from mido import MidiFile, MidiTrack, Message, MetaMessage
            # 正则匹配内容: MidiTrack([Message(...), ...])
            re_context = re.search(r"MidiTrack\(\[[^\]]+\]\)", context, re.M)
            if re_context is None:
                raise SyntaxError(f"error context in {plmpath}")
            self.messages = eval(re_context.group())

        if not _path.exists(plmpath):
            raise FileNotFoundError    

        _read_plm(plmpath)
        return self

    # 导出一个 .plm.py 文件
    def write_plm(self, path: str="temp.plm.py") -> "Midi":
        if self.messages is None:
            errors.warning("can not use write_plm because self.messages is None")
            return self
        
        if not path.endswith(".plm.py"):
            path += ".plm.py"

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"from mido import MidiFile, MidiTrack, MetaMessage, Message\n"
                    f"fmidi = MidiFile()\n"
                    f"track = {str(self.messages)}\n"
                    f"fmidi.tracks.append(track)\n"
                    f"fmidi.save(\"temp.mid\")\n"
                    f"from physicsLab.union import Midi\n"
                    f"Midi(\"temp.mid\").sound()")
        
        return self
    
    # 以 .mid 的形式导出, read_midi已经在Midi的__init__中实现
    # update: 是否将Midi.midifile更新
    def write_midi(self, midipath: str = "temp.mid", update: bool = False) -> "Midi":
        if self.messages  is None:
            errors.warning("can not use write_plm because self.messages is None")
            return self
        if not isinstance(midipath, str):
            raise TypeError
        if not midipath.endswith(".mid"):
            midipath += ".mid"

        mid = mido.MidiFile()
        mid.tracks.append(self.messages)
        mid.save(midipath)

        if update:
            self.midifile = midipath
        return self

# 音符类
class Note:
    def __init__(self,
                 time: int, # 在音轨中播放的时间
                 playTime: int = 1,  # 音符发出声音的时长 暂时不支持相关机制
                 instrument: Union[int, str] = 0, # 演奏的乐器，暂时只支持传入数字
                 pitch: Union[int, str] = 60, # 音高/音调
                 volume: numType = 1.0 # 音量/响度
    ) -> None:
        if not (
                isinstance(time, int) or
                isinstance(playTime, int) or
                isinstance(instrument, (int, str)) or
                isinstance(pitch, (int, str)) or
                isinstance(volume, float)
        ):
            raise TypeError
        self.instrument = instrument
        self.pitch = pitch
        self.volume = volume
        self.time = time
        self.playTime = playTime

    def __str__(self) -> str:
        return f"music.Note(time={self.time}, playTime={self.playTime}, instrument={self.instrument}, " \
               f"pitch={self.pitch}, volume={self.volume})"

# 循环类，用于创建一段循环的音乐片段
class Loop:
    def __init__(self, notes: Union[chordType, "Loop"], loopTime: int = 2) -> None:
        if not(
            isinstance(notes, (Loop, tuple, list)) or
            isinstance(loopTime, int)
        ) or any(not isinstance(a_note, Note) for a_note in notes) or loopTime < 2:
            raise TypeError

        if isinstance(notes, Loop):
            raise RuntimeError("Sorry, this is not supported for the moment")

        self.notes = tuple(*notes)
        self.loopTime = loopTime
        self.cases = []

    # loop-case: 每次主循环执行完一遍后会依次播放case中的音符
    def case(self, *notes) -> "Loop":
        self.cases.append(deepcopy(notes))
        return self
    
    def __iter__(self):
        pass

    def __next__(self):
        pass

# 音轨
class Track:
    def __init__(self,
                 notes: Union[List[Union[Note, Loop]], Tuple[Union[Note, Loop]]],
                 # 设置整个音轨的默认参数 Track global variable
                 instrument: int = 0, # 演奏的乐器，暂时只支持传入数字
                 pitch: int = 60, # 音高/音调
                 bpm: int = 100, # 节奏
                 volume: float = 1.0 # 音量/响度
    ) -> None:
        if not (
                isinstance(instrument, int) or
                isinstance(pitch, int) or
                isinstance(bpm, int) or
                0 < volume < 1 or
                isinstance(notes, (list, tuple, Loop)) and all(isinstance(val, Note) for val in notes)
        ):
            raise TypeError

        self.instrument = instrument
        self.pitch = pitch
        self.bpm = bpm
        self.volume = volume
        self.notes: noteType = []
        for a_note in notes:
            tick = 1
            while tick < a_note.time:
                tick += 1
                self.notes.append(None)
            self.notes.append(deepcopy(a_note))

    def __len__(self) -> int:
        return len(self.notes)

    def __str__(self):
        return f"Track: {self.notes}"
    # iterator
    def __iter__(self):
        self.__iter = iter(self.notes)
        return self.__iter

    def __next__(self):
        for a_note in self.__iter:
            yield a_note

# 乐曲类
class Piece:
    def __init__(self, *tracks: Track):
        if not all(isinstance(a_track, Track) for a_track in tracks):
            raise TypeError

        self.tracks: Track = tracks
        self.mergeTrack()

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, item):
        return self.notes[item]

    # iterator
    def __iter__(self):
        self.__iter = iter(self.notes)
        return self.__iter

    def __next__(self):
        for a_note in self.__iter:
            yield a_note
    
    # 将多个音轨合并为一个音轨（方便物实生成）
    def mergeTrack(self) -> "Piece":
        if len(self.tracks) > 1:
            raise RuntimeError("Sorry, multiple tracks are not supported for the moment")
        
        self.notes = self.tracks[0].notes
        
        return self

    # 在物实生成对应的电路
    def play(self, x:numType = 0, y: numType = 0, z: numType = 0, elementXYZ = None) -> None:
        Player(self, x, y, z, elementXYZ)

    # 转换为Midi类
    def translate_to_midi(self) -> Midi:
        pass

# 将piece的数据生成为物实的电路
class Player:
    def __init__(self,
                 musicArray: Union[Piece, List[Piece], Tuple[Piece]],
                 x: numType = 0, y: numType = 0, z: numType = 0,
                 elementXYZ = None
    ):
        if not (
                isinstance(x, (int, float)) or
                isinstance(y, (int, float)) or
                isinstance(z, (int, float))
        ) or not(
                isinstance(musicArray, Piece) or
                all(isinstance(a_piece, Piece) for a_piece in musicArray)
        ):
            raise TypeError

        if not (elementXYZ == True or (_elementXYZ.is_elementXYZ() == True and elementXYZ is None)):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)

        if isinstance(musicArray, (tuple, list)):
            if len(musicArray) > 1:
                raise RuntimeError("Sorry, multiple pieces are not supported for the moment")
            musicArray: Piece = musicArray[0]

        # 计算音乐矩阵的长宽
        side = None
        if len(musicArray) >= 2:
            side = ceil(sqrt(len(musicArray)))
        else:
            side = 2

        tick = _elementsClass.Nimp_Gate(x + 1, y, z, True)
        counter = _elementsClass.Counter(x, y + 1, z, True)
        _elementsClass.Logic_Input(x, y, z, True).o - tick.i_up
        tick.o - tick.i_low
        tick.o - counter.i_up

        xPlayer = D_WaterLamp(x + 1, y + 1, z, unionHeading=True, bitLength=side, elementXYZ=True)
        yPlayer = D_WaterLamp(x, y + 3, z, bitLength=side, elementXYZ=True, is_loop=False).set_HighLeaveValue(1.5)

        yesGate = _elementsClass.Yes_Gate(x + 1, y + 2, z + 1, True)
        xPlayer[0].o_low - yesGate.i
        crt_Wires(counter.o_upmid, xPlayer.data_Input)
        crt_Wires(xPlayer.data_Output[0], yPlayer.data_Input)

        # main
        xcor, ycor, zcor = 0, 0, 0
        for a_note_item, a_note in enumerate(musicArray):
            if a_note is not None:
                # 当time==0时，则为和弦（几个音同时播放）
                # 此时生成的简单乐器与z轴平行
                if zcor != 0:
                    ins = _elementsClass.Simple_Instrument(
                        1 + x + xcor, 4 + y + ycor, z + zcor, pitch=a_note.pitch, elementXYZ=True
                    )
                    ins.i - get_Element(x=1 + x + xcor, y=4 + y + ycor, z=z + zcor - 1).i
                    ins.o - get_Element(x=1 + x + xcor, y=4 + y + ycor, z=z + zcor - 1).o
                else:
                    ins = _elementsClass.Simple_Instrument(
                        1 + x + xcor, 4 + y + ycor, z, pitch=a_note.pitch, elementXYZ=True
                    )
                    # 连接x轴的d触的导线
                    if xcor == 0:
                        yesGate.o - ins.o
                    else:
                        ins.o - xPlayer.data_Output[xcor]
                    # 连接y轴的d触的导线
                    ins.i - yPlayer.neg_data_Output[ycor // 2]

                i = 1
                exit_sign = None
                while True:
                    if a_note_item + i >= len(musicArray):
                        exit_sign = True
                        break
                    if musicArray[a_note_item+i] is None:
                        i += 1
                    else:
                        break
                if exit_sign:
                    break
                next_note = musicArray[a_note_item+i]
                if a_note_item+1 < len(musicArray) and next_note is not None and next_note.time != 0:
                    zcor = 0
                else:
                    zcor += 1
                    continue

            xcor += 1
            if xcor == side:
                xcor = 0
                ycor += 2
