﻿# -*- coding: utf-8 -*-
import mido
import physicsLab._colorUtils as colorUtils
import physicsLab.circuit.elementXYZ as _elementXYZ

from math import ceil, sqrt
from enum import Enum, unique

from physicsLab import errors
from physicsLab.circuit import elements
from physicsLab._tools import roundData
from physicsLab.lib import crt_Wires, D_WaterLamp
from physicsLab.typehint import Optional, Union, List, Iterator, Dict, Self, numType

def _format_velocity(velocity: float) -> float:
    velocity = min(1, velocity)

    return velocity

# midi类，用于提供physicsLab与midi文件之间的桥梁
''' 重要midi事件及作用:
    note_on        -> message: 播放音符
    note_off       -> message: 停止播放音符
    program_change -> message: 改变某个音轨对应的音色
    set_tempo  -> metaMessage: 改变midi播放速度
'''
class Midi:
    # 仅被Midi.sound方法调用
    # 你也许需要这样写：e.g. player=music.Midi.PLAYER.os
    @unique
    class PLAYER(Enum):
        plmidi = 0
        pygame = 1
        os = 2

    def __init__(self, midifile: str) -> None:
        ''' self.messages的参数格式:
            mido.MidiTrack([
                Message -> (type: {{note_on or note_off}}, channel, note, velocity, time),
                Message ->(type: {{program_change}}, channel, program, time),
                MetaMessage -> (type: {{set_tempo}}, tempo, time)
            ])
            time: 间隔这么多时间之后执行该type
            note: midi音高 (音调)
            velocity: midi音符的响度
            channel: midi通道
            program: midi音色
            tempo: 播放速度
        '''
        def read_midopy(plpath: str = "temp.mido.py") -> Self:
            self.midifile = "temp.mid"

            context = None
            with open(plpath, encoding="utf-8") as f:
                context = f.read()

            import re
            from mido import MidiFile, MidiTrack, Message, MetaMessage
            # 正则匹配内容: MidiTrack([Message(...), ...])
            re_context = re.search(r"MidiTrack\(\[[^\]]+\]\)", context, re.M)
            if re_context is None:
                raise SyntaxError(f"error context in {plpath}")
            self.messages = eval(re_context.group()) # 用到mido import出的内容

            return self

        if not isinstance(midifile, str):
            raise TypeError

        from os import path
        if not path.exists(midifile):
            raise FileNotFoundError

        if midifile.endswith(".mido.py"):
            read_midopy(midifile)
        else:
            self.midifile: str = midifile

        self.messages: mido.MidiTrack = self.__get_midi_messages()

    def __get_midi_messages(self) -> mido.MidiTrack:
        ''' 使用mido打开一个midi文件并获取其messages '''
        self._midifile = mido.MidiFile(self.midifile, clip=True)
        wait_time: numType = 0
        res = mido.MidiTrack()
        for msg in self._midifile.merged_track:
            if msg.type in ("note_on", "note_off", "program_change", "set_tempo"):
                res.append(msg)
                msg.time += wait_time
                wait_time = 0
            elif msg.time != 0:
                wait_time += msg.time

        return res

    # 播放midi类存储的信息
    def sound(self, player: Optional[PLAYER] = None, is_sourcefile: bool = False) -> Self:
        # 使用plmidi播放midi
        def sound_by_plmidi() -> bool:
            try:
                import plmidi
            except ImportError:
                return False
            else:
                colorUtils.color_print("sound by using plmidi", colorUtils.COLOR.CYAN)

                try:
                    plmidi.sound(midifile)
                except (plmidi.OpenMidiFileError, plmidi.plmidiInitError):
                    return False

                return True

        # 使用pygame播放midi
        def sound_by_pygame() -> bool:
            import os
            os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
            try:
                from pygame import mixer, time
            except ImportError:
                return False
            else:
                colorUtils.color_print("sound by using pygame", colorUtils.COLOR.CYAN)

                # 代码参考自musicpy的play函数
                mixer.init()
                mixer.music.load(midifile)
                try:
                    mixer.music.play()
                    while mixer.music.get_busy():
                        time.delay(10)
                except KeyboardInterrupt:
                    pass
                return True

        # 使用系统调用播放midi
        def sound_by_os() -> bool:
            from os import path, system
            colorUtils.color_print("sound by using os", colorUtils.COLOR.CYAN)

            if path.exists(midifile):
                system(midifile)
                return True

            return False

        if not isinstance(player, Midi.PLAYER) and player is not None:
            raise TypeError

        if is_sourcefile:
            midifile = self.midifile
        else:
            midifile = "temp.mid"
            self.write_midi()

        if player is not None:
            f = (sound_by_plmidi, sound_by_pygame, sound_by_os)[player.value]
            if not f():
                errors.warning(f"can not use {f.__name__} to sound midi.")
            return self

        if sound_by_plmidi():
            pass # needless to do anything
        elif sound_by_pygame():
            pass
        elif sound_by_os():
            pass
        else:
            errors.warning("can not use sound methods")

        return self

    def set_tempo(self, num: numType = 1) -> Self:
        ''' 将time重设为原来的num倍 '''
        if not isinstance(num, (int, float)):
            raise TypeError

        for msg in self.messages:
            msg.time *= num

        return self

    # 返回 [Note(...), Chord(...), ...]
    def _get_notes_list(self,
                        div_time: Optional[numType],
                        max_notes: Optional[int],
                        fix_strange_note: bool = False,
                        ) -> List[Union["Note", "Chord"]]:

        res: List[Union[Note, Chord]] = []
        wait_time: int = 0
        len_res: int = 0
        channels: List[int] = [0] * 16
        tempo: int = 500_000
        _div_time = div_time

        for msg in self.messages:
            if msg.type == "program_change":
                channels[msg.channel] = msg.program
            if msg.type == "set_tempo":
                tempo = msg.tempo
                if div_time is None:
                    _div_time = mido.second2tick(0.11, self._midifile.ticks_per_beat, tempo)

            if msg.type == "note_on":
                velocity: float = _format_velocity(msg.velocity / 127) # 音符的响度
                ins: int = channels[msg.channel]

                if velocity == 0 or (fix_strange_note and ins == 0 and velocity >= 0.85):
                    if msg.time != 0:
                        wait_time += msg.time
                    continue

                len_res += 1
                if _div_time is None:
                    raise RuntimeError("find some error in midifile, please manually pass in the div_time parameter")
                note_time = round((msg.time + wait_time) / _div_time)

                if note_time != 0 or len(res) == 0:
                    if note_time == 0:
                        note_time = 1
                    res.append(Note(time=note_time, instrument=ins, pitch=msg.note, velocity=velocity))
                else:
                    # res[-1]是`Note`或`Chord`且在赋值之后一定是Chord, 此时Note的time的值不重要(因为和弦的音符是同时播放的)
                    res[-1] = res[-1].append(Note(time=1, instrument=ins, pitch=msg.note, velocity=velocity))
                wait_time = 0
            elif msg.time != 0:
                wait_time += msg.time

            if max_notes is not None and len_res >= max_notes:
                break

        return res

    def to_piece(self,
                 div_time: Optional[numType] = None,
                 max_notes: Optional[int] = 800,
                 is_optimize: bool = True, # 是否将多个音符优化为和弦
                 fix_strange_note: bool = False, # 是否修正一些奇怪的音符
                 ) -> "Piece":
        ''' 转换为Piece类 '''

        return Piece(self._get_notes_list(div_time, max_notes, fix_strange_note),
                     is_optimize=is_optimize)

    ''' *.pl.py文件:
        pl即为 physicsLab file
        为了更方便于手动调控物实音乐电路的生成而诞生的文件格式
        该文件运行之后即可生成对应的物实播放音乐电路
    '''
    '''
        *.mido.py
        为了更方便的研究Midi而诞生的文件格式
        为了修改方便, 默认使用 str(mido.MidiTrack) 的方式导出
        而且是个Py文件, 大家想要自己修改也是很方便的
    '''

    def write_midopy(self, path: str="temp.mido.py") -> Self:
        ''' 导出一个 .mido.py 文件 '''
        if not path.endswith(".mido.py"):
            path += ".mido.py"

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"import os\n"
                    f"os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'\n"
                    f"from mido import MidiFile, MidiTrack, MetaMessage, Message\n"
                    f"mid = MidiFile(type={self._midifile.type}, "
                    f"ticks_per_beat={self._midifile.ticks_per_beat}, "
                    f"charset='{self._midifile.charset}', "
                    f"clip={self._midifile.clip})\n"
                    f"track = {self.messages}\n"
                    f"mid.tracks.append(track)\n"
                    f"mid.save(\"temp.mid\")\n"
                    f"from physicsLab.music import Midi\n"
                    f"Midi(\"temp.mid\").sound()")

        return self

    def write_midi(self, midipath: str = "temp.mid") -> Self:
        """ 导出一个 .mid 文件 """
        if not isinstance(midipath, str):
            raise TypeError
        if not midipath.endswith(".mid"):
            midipath += ".mid"

        mid = mido.MidiFile(ticks_per_beat=self._midifile.ticks_per_beat,
                            type=self._midifile.type,
                            charset=self._midifile.charset)
        mid.tracks.append(self.messages)
        mid.save(midipath)

        return self

    def write_plpy(self,
                  filepath: str = "temp.pl.py",
                  div_time: numType = 100, # midi的time的单位长度与Note的time的单位长度不同，支持用户手动调整
                  max_notes: Optional[int] = 800, # 最大的音符数，因为物实没法承受过多的元件
                  sav_name: str = "temp" # 产生的存档的名字, 也可直接在生成.pl.py中修改
    ) -> Self:
        ''' 以.pl.py的格式导出 '''
        if not (isinstance(div_time, (int, float)) or
                isinstance(max_notes, int)) and max_notes is not None:
           raise TypeError

        if not filepath.endswith(".pl.py"):
            filepath += ".pl.py"

        l_notes: List[Union[Note, Chord]] = self._get_notes_list(div_time, max_notes)
        notes_str = ""
        for a_note in l_notes:
            notes_str += "        " + repr(a_note) + ",\n"

        with open(filepath, "w") as f:
            f.write(f"from physicsLab import experiment\n"
                    f"from physicsLab.music import Note, Piece, Chord\n"
                    f"with experiment(\"{sav_name}\"):\n"
                    f"    Piece([\n{notes_str}    ]).release(-1, -1, 0)")

        return self

# TODO 增加更多的设置pitch的方法 -> 参考Simple_Instrument
class Note:
    ''' 音符类 '''
    def __init__(self,
                 time: int, # 间隔多少时间才播放此Note
                 playTime: int = 1,  # 音符发出声音的时长 暂时不支持相关机制
                 instrument: int = 0, # 演奏的乐器，暂时只支持传入数字
                 pitch: int = 60, # 音高/音调
                 velocity: Union[int, float] = 0.64 # 音量/响度
    ) -> None:
        if not (
                isinstance(time, int) and
                isinstance(playTime, int) and
                isinstance(instrument, int) and
                isinstance(pitch, int) and
                0 <= pitch < 128 and
                isinstance(velocity, (int, float)) and 0 < velocity <= 1
        ) or time <= 0:
            raise TypeError

        self.instrument = instrument
        self.pitch: int = pitch
        self.velocity = velocity
        self.time = time
        self.playTime = playTime

    def __repr__(self) -> str:
        return f"Note(time={self.time}, playTime={self.playTime}, instrument={self.instrument}, " \
               f"pitch={self.pitch}, velocity={self.velocity})"

    def append(self, other: "Note") -> "Chord":
        return Chord(self, other, time=self.time)

class Chord:
    ''' 和弦类 '''
    def __init__(self, *notes: Note, time: int) -> None:
        if len(notes) < 1 or time < 1:
            raise TypeError

        self.time = time
        self._notes = []
        # {instrument: List[Note], ...}
        self.ins_notes: Dict[int, List[Note]] = {}

        for a_note in notes:
            self.append(a_note)

    def __repr__(self) -> str:
        s: str = ""
        for a_note in self._notes:
            s += repr(a_note) + ", "
        return f"Chord({s}time={self.time})"

    def __len__(self) -> int:
        return len(self.ins_notes.keys())

    @staticmethod
    def _get_velocity(notes: List[Note], is_average: bool = False) -> float:
        if is_average:
            sum = 0
            for a_note in notes:
                sum += a_note.velocity
            return _format_velocity(sum / len(notes))
        else:
            return _format_velocity(max([a_note.velocity for a_note in notes]))

    # 将新的音符加入到和弦中
    def append(self, a_note: Note) -> Self:
        if not isinstance(a_note, Note):
            raise TypeError

        if a_note not in self._notes:
            self._notes.append(a_note)

        if a_note.instrument in self.ins_notes.keys():
            if a_note not in self.ins_notes[a_note.instrument]:
                self.ins_notes[a_note.instrument].append(a_note)
        else:
            self.ins_notes[a_note.instrument] = [a_note]

        return self

    # 将Chord存储的数据转变为对应的物实的电路
    def release(self,
                x: numType = 0,
                y: numType = 0,
                z: numType = 0,
                elementXYZ: Optional[bool] = None,
                is_optimize: bool = True,
                ) -> elements.Simple_Instrument:
        # 元件坐标系，如果输入坐标不是元件坐标系就强转为元件坐标系
        if not (elementXYZ is True or (_elementXYZ.is_elementXYZ() is True and elementXYZ is None)):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)
        x, y, z = roundData(x, y, z) # type: ignore -> result type: tuple

        first_ins: Optional[elements.Simple_Instrument] = None # 第一个音符
        if is_optimize:
            for delta_z, ins in enumerate(self.ins_notes):
                notes: List[Note] = self.ins_notes[ins]
                temp: elements.Simple_Instrument = elements.Simple_Instrument(
                    x, y, z + delta_z, elementXYZ=True,instrument=ins,
                    pitch=notes[0].pitch, is_ideal_model=True, velocity=self._get_velocity(notes, is_average=True)
                ).set_Rotation(0, 0, 0)

                if first_ins is None:
                    first_ins = temp
                else:
                    temp.i - first_ins.i
                    temp.o - first_ins.o

                for a_note in notes:
                    temp.add_note(a_note.pitch)
        else:
            delta_z = 0
            for ins, notes in self.ins_notes.items():
                for a_note in notes:
                    temp = elements.Simple_Instrument(
                        x, y, z + delta_z, elementXYZ=True,instrument=ins,
                        pitch=a_note.pitch, is_ideal_model=True, velocity=a_note.velocity
                    ).set_Rotation(0, 0, 0)

                    if first_ins is None:
                        first_ins = temp
                    else:
                        temp.i - first_ins.i
                        temp.o - first_ins.o

                    delta_z += 1

        assert first_ins is not None
        return first_ins

# 循环类，用于创建一段循环的音乐片段
# TODO: 完善Loop存储的数据结构
class Loop:
    def __init__(self, loop_time: int = 2, *notes: Union[Note, "Loop"]) -> None:
        if not(
            isinstance(notes, (Loop, tuple, list)) or
            isinstance(loop_time, int)
        ) or any(not isinstance(a_note, Note) for a_note in notes) or loop_time < 2:
            raise TypeError

        if isinstance(notes, Loop):
            raise RuntimeError("Sorry, this is not supported for the moment")

        self.notes = list(notes)
        self.loop_time = loop_time
        self.cases = []

    # loop-case: 每次主循环执行完一遍后会依次播放case中的音符
    def case(self, *notes) -> Self:
        self.cases.append(notes)
        return self

    def __iter__(self):
        pass

    def __next__(self):
        pass

class Rest_symbol:
    ''' 休止符 '''
    __singleton: Optional[Self] = None
    def __new__(cls) -> Self:
        if cls.__singleton is None:
            cls.__singleton = super().__new__(cls)
        return cls.__singleton

class Piece:
    ''' 乐曲类 '''
    def __init__(self,
                 notes: Optional[List[Union[Note, Chord]]] = None, # TODO: support Loop
                 is_optimize: bool = True, # 是否将多个音符优化为和弦
                 ) -> None:
        if (
            ( not isinstance(notes, list)
            or not all(isinstance(val, (Note, Chord)) for val in notes) )
            and notes is not None
        ):
            raise TypeError

        self.is_optimize = is_optimize

        # self.notes会将Note与Chord中用time表示的休止符展开为Rest_symbol
        if notes is None:
            self.notes = []
        else:
            self.notes: List[Union[Note, Chord, Rest_symbol]] = []
            for a_note in notes:
                self.append(a_note)

    # 向Piece类添加数据成员
    def append(self, other: Union[Note, Chord]) -> Self:
        if not isinstance(other, (Note, Chord)):
            raise TypeError

        while other.time > 1:
            self.notes.append(Rest_symbol())
            other.time -= 1
        self.notes.append(other)
        return self

    # 将Piece转化为midi文件(暂不支持Chord)
    def write_midi(self,
                   filepath: str = "temp.mid",
                   basic_time: int = 100 # 将Note的time变为Midi的time扩大的倍数
    ) -> Self:
        def write_a_midi_note(a_note: Note):
            channel: int = 0
            try:
                channel = channels.index(a_note.instrument)
            except ValueError:
                try:
                    channel = channels.index(0)
                except ValueError:
                    raise RuntimeError("amount of midi track out of 16")
                else:
                    channels[channel] = a_note.instrument

            track.append(
                mido.Message("note_off",
                             channel=channel,
                             note=a_note.pitch,
                             velocity=int(a_note.velocity * 100),
                             time=basic_time * none_counter)
                ) # time通过音符后的None的数量确定
            track.append(
                mido.Message("note_on",
                             channel=channel,
                             note=a_note.pitch,
                             velocity=int(a_note.velocity * 100),
                             time=0)
            )

        track = mido.MidiTrack()
        mid = mido.MidiFile(tracks=[track])
        channels: List[int] = [0] * 16

        none_counter: int = 0
         # 500_000 / 100, 500_000是Midi.tempo的默认数字，100是self.bpm的默认数字
        track.append(mido.MetaMessage("set_tempo", tempo=self.bpm * 5000, time=0))
        for a_note in self.notes:
            if isinstance(a_note, Rest_symbol):
                none_counter += 1
            elif isinstance(a_note, Chord):
                for note_list in a_note.ins_notes.values():
                    for _a_note in note_list:
                        write_a_midi_note(_a_note)
                        none_counter = 0
            elif isinstance(a_note, Note):
                write_a_midi_note(a_note)
                none_counter = 0

        for channel, program in enumerate(channels):
            track.insert(1, mido.Message("program_change", channel=channel, program=program, time=0))

        with open("temp.test.py", "w") as f:
            f.write(repr(track))
        mid.save(filepath)
        return self

    # 将Piece类转换为Midi
    def to_midi(self, filepath="temp.mid") -> Midi:
        self.write_midi(filepath)
        return Midi(filepath)

    # 将Piece转换为物实对应的电路
    def release(self, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ = None) -> "Player":
        return Player(self, x, y, z, elementXYZ, self.is_optimize)

    # Piece中所有Notes与Chord的数量
    def count_notes(self) -> int:
        res = 0
        for note in self.notes:
            if isinstance(note, (Note, Chord)):
                res += 1
        return res

    def __len__(self) -> int:
        return len(self.notes)

    def __getitem__(self, item: int) -> Union[Note, Chord, Rest_symbol]:
        if not isinstance(item, int):
            raise TypeError
        return self.notes[item]

    def __setitem__(self, item: int, value) -> None:
        if not isinstance(item, int):
            raise TypeError
        self.notes[item] = value

    def __repr__(self) -> str:
        return f"Piece({self.notes})".replace("No", "\n  No")

    def __iter__(self) -> Iterator:
        self.__iter = iter(self.notes)
        return self.__iter

    def __next__(self):
        yield next(self.__iter)

# 将piece的数据生成为物实的电路
class Player:
    def __init__(self,
                 musicArray: Piece,
                 x: numType = 0,
                 y: numType = 0,
                 z: numType = 0,
                 elementXYZ = None,
                 is_optimize: bool = True,
                 ) -> None:
        from physicsLab.element import count_Elements
        count_elements_start: int = count_Elements()

        if not (
                isinstance(x, (int, float)) and
                isinstance(y, (int, float)) and
                isinstance(z, (int, float)) and
                isinstance(musicArray, Piece)
        ):
            raise TypeError

        if not (elementXYZ is True or (_elementXYZ.is_elementXYZ() is True and elementXYZ is None)):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)

        # 给乐器增加休止符
        while isinstance(musicArray.notes[-1], Rest_symbol):
            musicArray.notes.pop()
        while isinstance(musicArray.notes[0], Rest_symbol):
            musicArray.notes.pop(0)

        len_musicArray: int = len(musicArray)

        # 计算音乐矩阵的长宽
        side = None
        if len_musicArray >= 2:
            side = ceil(sqrt(len_musicArray))
        else:
            side = 2

        tick = elements.Nimp_Gate(x + 1, y, z, True)
        counter = elements.Counter(x, y + 1, z, True)
        l_input = elements.Logic_Input(x, y, z, True)
        l_input.o - tick.i_up
        tick.o - tick.i_low
        tick.o - counter.i_up

        try:
            xPlayer = D_WaterLamp(x + 1, y + 1, z, unionHeading=True, bitLength=side, elementXYZ=True)
            yPlayer = D_WaterLamp(x, y + 3, z, bitLength=ceil(len_musicArray / side), elementXYZ=True)
        except errors.bitLengthError as e:
            from physicsLab._colorUtils import color_print, COLOR
            color_print(
                "bigLength of D_WaterLamp is too short, "
                "try to use argument \"div_time\" in class Midi to solve this problem",
                COLOR.RED
            )
            raise e


        yesGate = elements.Full_Adder(x + 1, y + 1, z + 1, True)
        yesGate.i_low - yesGate.i_mid
        xPlayer[0].o_low - yesGate.i_up # type: ignore
        crt_Wires(xPlayer.data_Output[0], yPlayer.data_Input)

        check1 = elements.No_Gate(x + 2, y, z, True)
        check2 = elements.Multiplier(x + 3, y, z, True)
        # 上升沿触发器
        no_gate = elements.No_Gate(x + 1, y, z + 1, True)
        and_gate = elements.And_Gate(x + 2, y, z + 1, True)
        no_gate.o - and_gate.i_low
        no_gate.i - and_gate.i_up

        l_input.o - no_gate.i
        check1.o - check2.i_low
        yesGate.o_low - check2.i_upmid
        check2.i_lowmid - and_gate.o
        counter.o_upmid - check2.i_up
        crt_Wires(check2.o_lowmid, xPlayer.data_Input)

        # main
        xcor, ycor = -1, 0
        for a_note in musicArray:
            if isinstance(a_note, Rest_symbol):
                xcor += 1
                if xcor == side:
                    xcor = 0
                    ycor += 2
                continue

            # 当time==0时，则为和弦（几个音同时播放）
            # 此时生成的简单乐器与z轴平行
            xcor += 1
            if xcor == side:
                xcor = 0
                ycor += 2
            if isinstance(a_note, Chord):
                ins = a_note.release(1 + x + xcor,  4 + y + ycor, z, elementXYZ=True, is_optimize=is_optimize)
            elif isinstance(a_note, Note):
                ins = elements.Simple_Instrument(
                    1 + x + xcor, 4 + y + ycor, z, pitch=a_note.pitch,
                    instrument=a_note.instrument,
                    elementXYZ=True,
                    is_ideal_model=True,
                    velocity=a_note.velocity
                ).set_Rotation(0, 0, 0) # type: ignore
            # 连接x轴的d触的导线
            if xcor == 0:
                yesGate.o_up - ins.i
            else:
                ins.i - xPlayer.data_Output[xcor]
            # 连接y轴的d触的导线
            ins.o - yPlayer.neg_data_Output[ycor // 2] # type: ignore -> yPlayer must has attr neg_data_Output

        stop = elements.And_Gate(x + 1, y + ycor + 3, z, True)
        stop.o - yesGate.i_low - check1.i
        stop.i_up - yPlayer[ycor // 2].o_up # type: ignore -> D_Flipflop must has attr o_up
        stop.i_low - xPlayer[side - 1].o_up # type: ignore -> D_Flipflop must has attr neg_data_Output

        count_elements_end: int = count_Elements()
        self._count_elements = count_elements_end - count_elements_start

    # 返回Player创建的元件数量
    def count_elements(self) -> int:
        return self._count_elements