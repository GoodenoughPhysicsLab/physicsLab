from physicsLab import *
from typing import Union

'''
How do you play music in physics Lab AR?
Music extension might make it easier than before!

    How to use it?
>>> music(a_list_or_a_tuple)
>>> write_Experiment()
Then, enjoy your music at physics Lab AR!

    What is the format of the music array?
The format of music array compat netlogo music list(ml) which was used by Li Weijia at Turtle Lab.


'''


# 设置简单乐器的音高（复制粘贴自csdn并作了部分修改）
# 这个代码太烂了，但输入方式更丰富一些，先留着吧
def set_Tonality(tonality: str):
    if not isinstance(tonality, str):
        raise RuntimeError('The entered data type is incorrect')
    tonality = tonality.lower()
    if tonality == "a0":  # 最低音 la
        return 21
    if tonality == "b0":  # 最低的si
        return 23
    if tonality == "c1":  # 低三个八度 do
        return 24
    if tonality == "d1":  # re
        return 26
    if tonality == "e1":  # mi
        return 28
    if tonality == "f1":  # fa
        return 29
    if tonality == "g1":  # so 或者说 sol
        return 31
    if tonality == "a1":  # la
        return 33
    if tonality == "b1":  # si
        return 35
    if tonality == "c2":  # 低两个八度 do
        return 36
    if tonality == "d2":  # re
        return 38
    if tonality == "e2":  # mi
        return 40
    if tonality == "f2":  # fa
        return 41
    if tonality == "g2":  # so 或者说 sol
        return 43
    if tonality == "a2":  # la
        return 45
    if tonality == "b2":  # si
        return 47
    if tonality == "c3" or tonality == ".do" or tonality == ".1":  # 低八度   do
        return 48
    if tonality == "d3" or tonality == ".re" or tonality == ".2":  # re
        return 50
    if tonality == "e3" or tonality == ".mi" or tonality == ".3":  # mi
        return 52
    if tonality == "f3" or tonality == ".fa" or tonality == ".4":  # fa
        return 53
    if tonality == "g3" or tonality == ".so" or tonality == ".sol" or tonality == ".5":  # so 或者说 sol
        return 55
    if tonality == "a3" or tonality == ".la" or tonality == ".6":  # la
        return 57
    if tonality == "b3" or tonality == ".si" or tonality == ".7":  # si
        return 59
    # 中音区
    if tonality == "c4" or tonality == "c" or tonality == "1" or tonality == 1 or tonality == "do":  # 中音do
        return 60
    if tonality == "d4" or tonality == "d" or tonality == "2" or tonality == 2 or tonality == "re":  # 中音re
        return 62
    if tonality == "e4" or tonality == "e" or tonality == "3" or tonality == 3:  # 中音mi
        return 64
    if tonality == "f4" or tonality == "f" or tonality == "4" or tonality == 4:  # 中音fa
        return 65
    if tonality == "g4" or tonality == "g" or tonality == "5" or tonality == 5 or tonality == "so" or tonality == "sol": # 中音so  或者说 sol
        return 67
    if tonality == "a4" or tonality == "a" or tonality == "6" or tonality == 6 or tonality == "la":  # 中音la
        return 69
    if tonality == "b4" or tonality == "b" or tonality == "7" or tonality == 7 or tonality == "si":  # 中音si
        return 71
    # 高音区
    if tonality == "c5" or tonality == "1." or tonality == "do.":  # do
        return 72
    if tonality == "d5" or tonality == "2." or tonality == "re.":  # re
        return 74
    if tonality == "e5" or tonality == "3." or tonality == "mi.":  # mi
        return 76
    if tonality == "f5" or tonality == "4." or tonality == "fa.":  # fa
        return 77
    if tonality == "g5" or tonality == "5." or tonality == "so." or tonality == "sol.":  # so 或者说是 sol
        return 79
    if tonality == "a5" or tonality == "6." or tonality == "la.":  # la
        return 81
    if tonality == "b5" or tonality == "7." or tonality == "si.":  # si
        return 83
    # 从此，退出常用区
    # 高两个八度
    if tonality == "c6":  # do
        return 84
    if tonality == "d6":  # re
        return 86
    if tonality == "e6":  # mi
        return 88
    if tonality == "f6":  # fa
        return 89
    if tonality == "g6":  # so
        return 91
    if tonality == "a6":  # la
        return 93
    if tonality == "b6":  # si
        return 95
    # 高三个八度
    if tonality == "c7":  # do
        return 96
    if tonality == "d7":  # re
        return 98
    if tonality == "e7":  # mi
        return 100
    if tonality == "f7":  # fa
        return 101
    if tonality == "g7":  # so
        return 103
    if tonality == "a7":  # la
        return 105
    if tonality == "b7":  # si
        return 107
    # 高四个八度
    # 最高音do
    if tonality == "c8" or tonality == "highestdo" or tonality == "hdo" or tonality == "h1" or tonality == "highest1":  # do
        return 108
    if tonality == '0':
        return 1
    raise RuntimeError('Input data error')

class union_music:
    def __init__(self, musicArray: Union[list, tuple]):
        pass
