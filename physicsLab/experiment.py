#coding=utf-8
import json
import re
import sys
from random import sample
from string import ascii_letters, digits
from os import walk, popen, remove

from _utf_8 import utf8_coding
from _fileGlobals import *
from electricity.element import crt_Element

### define ###

_ifndef_open_Experiment = False
_elements_Address = {} # key为position，value为self

def print_Elements():
    print(Elements)

def print_wires():
    print(wires)

def print_elements_Address():
    print(_elements_Address)

### end define ###

# 输入sav文件名并读取（旧函数，不建议使用）
def old_open_Experiment(file: str) -> None:
    file = file.strip()
    if (not file.endswith('.sav')):
        raise RuntimeError("The input parameters are incorrect")

    global _ifndef_open_Experiment
    if (_ifndef_open_Experiment):
        raise RuntimeError("This function can only be run once")
    _ifndef_open_Experiment = True

    global savName
    savName = f"{FILE_HEAD}\\{file}"
    with open(savName, encoding="UTF-8") as f:
        try:
            InternalName = (json.loads(f.read().__str__()))["Summary"]["Subject"]
            sav["Summary"]["Subject"] = InternalName
            sav["InternalName"] = sav["Summary"]["Subject"]
        except:
            raise RuntimeError('Data errors in the file')

# 打开一个指定的sav文件（支持输入本地实验的名字或sav文件名）
@utf8_coding
def open_Experiment(file : str) -> None:
    file = file.strip()
    if file.endswith('.sav'):
        old_open_Experiment(file)
    else:
        savs = [i for i in walk(FILE_HEAD)][0]
        savs = savs[savs.__len__() - 1]
        savs = [aSav for aSav in savs if aSav.endswith('sav')]
        is_error = True
        for aSav in savs:
            try:
                with open(f"{FILE_HEAD}\\{aSav}", encoding='utf-8') as f:
                    try:
                        f = json.loads(f.read())
                    except:
                        pass
                    else:
                        if (f.get("InternalName") == file):
                            if f.get('InternalName') == '自动保存-电学':
                                rename_Experiment('自动保存-电学')
                            old_open_Experiment(aSav)
                            return
                is_error = False
            except:
                if is_error:
                    raise RuntimeError('The input parameters are incorrect')

# 创建存档
@utf8_coding
def crt_Experiment(name : str) -> None:
    global savName, _ifndef_open_Experiment
    # 该函数与open_Experiment一起，每次只能运行一次
    if (_ifndef_open_Experiment):
        raise RuntimeError("This function can only be run once")
    _ifndef_open_Experiment = True
    # 检查是否存在重名的存档
    savs = [i for i in walk(FILE_HEAD)][0]
    savs = savs[savs.__len__() - 1]
    savs = [aSav for aSav in savs if aSav.endswith('sav')]
    for sav in savs:
        with open(f"{FILE_HEAD}\\{sav}", encoding='utf-8') as f:
            try:
                f = json.loads(f.read())
            except:
                pass
            else:
                if f['InternalName'] == name:
                    raise RuntimeError('Duplicate name archives are forbidden')
    # 创建存档
    if not isinstance(name, str):
        name = str(name)
    savName = ''.join(sample(ascii_letters + digits, 34))
    savName = f'{FILE_HEAD}\\{savName}.sav'
    with open(savName, 'w', encoding='utf-8'):
        pass
    rename_Experiment(name)

# 将编译完成的json写入sav
def write_Experiment() -> None:
    global savName, sav, StatusSave
    StatusSave["Elements"] = Elements
    StatusSave["Wires"] = wires
    sav["Experiment"]["StatusSave"] = json.dumps(StatusSave)
    with open(savName, "w", encoding="UTF-8") as f:
        f.write(json.dumps(sav))
    # 存档回滚
    f = ''
    try:
        f = open(f'{savName[:len(savName) - 4:]}_rollBack_sav.txt')
    except FileNotFoundError:
        f = open(f'{savName[:len(savName) - 4:]}_rollBack_sav.txt', 'w')
    finally:
        f.close()
    experiments = []
    with open(f'{savName[:len(savName) - 4:]}_rollBack_sav.txt', 'r', encoding='utf-8') as f:
        f = f.read()
        if f == '':
            experiments.append(sav)
        else:
            experiments = json.loads(f)
            experiments.append(sav)
        if experiments.__len__() > 10:
            experiments.pop(0)
    with open(f'{savName[:len(savName) - 4:]}_rollBack_sav.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(experiments))
    print(f'\nCompile successfully! {len(Elements)} elements, {len(wires)} wires.')
load_Experiment = write_Experiment

# # 将编译完成的json写入sav
# def write_Experiment() -> None:
#     global savName, sav, StatusSave
#     StatusSave["Elements"] = Elements
#     StatusSave["Wires"] = wires
#     sav["Experiment"]["StatusSave"] = json.dumps(StatusSave)
#     with open(savName, "w", encoding="UTF-8") as f:
#         # format_Experiment (bug)
#         writen = list(json.dumps(sav).replace(' ', ''))
#         # isString = False
#         # isValue = False
#         # stack = []
#         # tab = '  '
#         # charIndex = 0
#         # stackLenMem = None
#         # while charIndex < len(writen):
#         #     char = writen[charIndex]
#         #     if char == ':':
#         #         isValue = True
#         #     elif char == ',':
#         #         isValue = False
#         #         if not isString:
#         #             writen.insert(charIndex + 1, '\n' + tab * len(stack))
#         #     elif char == '\"' and isValue:
#         #         isString = not isString
#         #         if isString:
#         #             stack.append('\"')
#         #         else:
#         #             stack.pop()
#         #     elif char == '{':
#         #         if not isString:
#         #             writen.insert(charIndex, '\n' + tab * len(stack))
#         #             charIndex += 1
#         #             stack.append(char)
#         #             writen.insert(charIndex + 1, '\n' + tab * len(stack))
#         #         else:
#         #             if stackLenMem is None:
#         #                 stackLenMem = len(stack)
#         #                 writen.insert(charIndex, '\n' + tab * len(stack))
#         #             charIndex += 1
#         #     elif char == '}':
#         #         if not isString:
#         #             stack.pop()
#         #             writen.insert(charIndex, '\n' + tab * len(stack))
#         #             charIndex += 1
#         #         else:
#         #             if len(stack) == stackLenMem:
#         #                 stackLenMem = None
#         #                 writen.insert(charIndex, '\n' + tab * len(stack))
#         #                 charIndex += 1
#         #     charIndex += 1
#         f.write(''.join(writen))#[1:])
#     # 存档回滚
#     f = None
#     try:
#         f = open(f'{savName[:len(savName) - 4:]}_rollBack_sav.txt')
#     except FileNotFoundError:
#         f = open(f'{savName[:len(savName) - 4:]}_rollBack_sav.txt', 'w')
#     finally:
#         f.close()
#     experiments = []
#     with open(f'{savName[:len(savName) - 4:]}_rollBack_sav.txt', 'r', encoding='utf-8') as f:
#         f = f.read()
#         if f == '':
#             experiments.append(sav)
#         else:
#             experiments = json.loads(f)
#             experiments.append(sav)
#         if experiments.__len__() > 10:
#             experiments.pop(0)
#     with open(f'{savName[:len(savName) - 4:]}_rollBack_sav.txt', 'w', encoding='utf-8') as f:
#         f.write(json.dumps(experiments))
#     print(f'\nCompile successfully! {len(Elements)} elements, {len(wires)} wires.')
# load_Experiment = write_Experiment

# 读取sav文件已有的原件与导线
def read_Experiment() -> None:
    global wires
    with open(savName, encoding='UTF-8') as f:
        readmem = json.loads(f.read())
        _local_Elements = json.loads(readmem["Experiment"]["StatusSave"])["Elements"]

        for element in _local_Elements:
            # 坐标标准化（消除浮点误差）
            sign1 = element['Position'].find(',')
            sign2 = element['Position'].find(',', sign1 + 1)
            num1 = myRound(float(element['Position'][:sign1:]))
            num2 = myRound(float(element['Position'][sign1 + 1: sign2:]))
            num3 = myRound(float(element['Position'][sign2 + 1::]))
            element['Position'] = f"{num1},{num2},{num3}"  # x, z, y
            # 实例化对象
            obj = crt_Element(element["ModelID"], num1, num3, num2)
            sign1 = element['Rotation'].find(',')
            sign2 = element['Rotation'].find(',', sign1 + 1)
            x = float(element['Rotation'][:sign1:])
            z = float(element['Rotation'][sign1 + 1: sign2:])
            y = float(element['Rotation'][sign2 + 1::])
            obj.set_Rotation(x, y, z)
            obj._arguments['Identifier'] = element['Identifier']
            # 如果obj是逻辑输入
            if obj.type() == 'Logic Input' and element['Properties'].get('开关') == 1:
                obj.set_highLevel()
            # 如果obj是8位输入器
            if obj.type() == '8bit Input':
                obj._arguments['Statistics'] = element['Statistics']
                obj._arguments['Properties']['十进制'] = element['Properties']['十进制']
            # 导线
        wires = json.loads(readmem['Experiment']['StatusSave'])['Wires']

# 重命名sav
def rename_Experiment(name: str) -> None:
    global sav
    # 检查是否重名
    savs = [i for i in walk(FILE_HEAD)][0]
    savs = savs[savs.__len__() - 1]
    savs = [aSav for aSav in savs if aSav.endswith('sav')]
    for aSav in savs:
        with open(f"{FILE_HEAD}\\{aSav}", encoding='utf-8') as f:
            try:
                f = json.loads(f.read())
            except:
                pass
            else:
                if f['InternalName'] == name:
                    raise RuntimeError('Duplicate name archives are forbidden')
    # 重命名存档
    name = str(name)
    sav["Summary"]["Subject"] = name
    sav["InternalName"] = name

# 打开一个存档的窗口
def show_Experiment() -> None:
    popen(f'notepad {savName}')
os_Experiment = show_Experiment

# 删除存档
def del_Experiment() -> None:
    remove(savName)
    remove(f"{savName.replace('.sav', '_rollBack_sav.txt')}")
    try:
        remove(savName.replace('.sav', '.jpg'))
    except:
        sys.exit()

# 存档回滚
def rollBack_Experiment(back : int = 1):
    if not isinstance(back, int) and (back < 1 or back >= 10):
        raise RuntimeError('back must be an integer between 1 and 10')
    f = ''
    try:
        f = open(f'{savName[:len(savName) - 4:]}_rollBack_sav.txt')
    except FileNotFoundError:
        f = open(f'{savName[:len(savName) - 4:]}_rollBack_sav.txt', 'w')
    finally:
        f.close()
    with open(f'{savName[:len(savName) - 4:]}_rollBack_sav.txt', encoding='utf-8') as f:
        reader = f.read()
        if reader == '':
            raise RuntimeError('There is no archive to roll back')
        f = json.loads(reader)
        global Elements, wires
        sav = json.loads(f[len(f) - 1 - back]['Experiment']['StatusSave'])
        Elements = sav['Elements']
        wires = sav['Wires']

# 输入实验介绍
def introduce_Experiment(introduction : str) -> None:
    if not isinstance(introduction, str):
        raise RuntimeError
    introduction = introduction.replace('\n', ' \n')
    regex = re.compile('[^\n]+')
    sav['Summary']['Description'] = regex.findall(introduction)
