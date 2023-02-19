#coding=utf-8
import json
import re
import sys
from random import sample
from string import ascii_letters, digits
from os import walk, popen, remove

from _utf_8 import utf8_coding
import _fileGlobals as fileGlobals
from electricity.element import crt_Element

### define ###

_ifndef_open_Experiment = False

def print_Elements():
    print(fileGlobals.Elements)

def print_wires():
    print(fileGlobals.Wires)

def print_elements_Address():
    print(fileGlobals.elements_Address)

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

    fileGlobals.savName = f"{fileGlobals.FILE_HEAD}\\{file}"
    with open(fileGlobals.savName, encoding="UTF-8") as f:
        try:
            InternalName = (json.loads(f.read().replace('\n', '')))["Summary"]["Subject"]
            fileGlobals.sav["Summary"]["Subject"] = InternalName
            fileGlobals.sav["InternalName"] = fileGlobals.sav["Summary"]["Subject"]
        except:
            raise RuntimeError('Data errors in the file')

# 打开一个指定的sav文件（支持输入本地实验的名字或sav文件名）
@utf8_coding
def open_Experiment(file : str) -> None:
    fileGlobals.fileGlobals_init()
    file = file.strip()
    if file.endswith('.sav'):
        old_open_Experiment(file)
    else:
        savs = [i for i in walk(fileGlobals.FILE_HEAD)][0]
        savs = savs[savs.__len__() - 1]
        savs = [aSav for aSav in savs if aSav.endswith('sav')]
        for aSav in savs:
            with open(f"{fileGlobals.FILE_HEAD}\\{aSav}", encoding='utf-8') as f:
                try:
                    f = json.loads(f.read().replace('\n', ''))
                except:
                    pass
                else:
                    if (f.get("InternalName") == file):
                        old_open_Experiment(aSav)
                        return
        raise FileNotFoundError(f'No such experiment: {file}')

# 创建存档
@utf8_coding
def crt_Experiment(name : str) -> None:
    fileGlobals.fileGlobals_init()
    global _ifndef_open_Experiment
    # 该函数与open_Experiment一起，每次只能运行一次
    if (_ifndef_open_Experiment):
        raise RuntimeError("This function can only be run once")
    _ifndef_open_Experiment = True
    # 检查是否存在重名的存档
    savs = [i for i in walk(fileGlobals.FILE_HEAD)][0]
    savs = savs[savs.__len__() - 1]
    savs = [aSav for aSav in savs if aSav.endswith('sav')]
    for aSav in savs:
        with open(f"{fileGlobals.FILE_HEAD}\\{aSav}", encoding='utf-8') as f:
            try:
                f = json.loads(f.read().replace('\n', ''))
            except:
                pass
            else:
                if f['InternalName'] == name:
                    raise RuntimeError('Duplicate name archives are forbidden')
    # 创建存档
    if not isinstance(name, str):
        name = str(name)
    fileGlobals.savName = ''.join(sample(ascii_letters + digits, 34))
    fileGlobals.savName = f'{fileGlobals.FILE_HEAD}\\{fileGlobals.savName}.sav'
    with open(fileGlobals.savName, 'w', encoding='utf-8'):
        pass
    rename_Experiment(name)

# 将编译完成的json写入sav
def write_Experiment() -> None:
    def _format_StatusSave(stringJson: str) -> str:
        stringJson = stringJson.replace('{\\\"ModelID', '\n      {\\\"ModelID') # format element json
        stringJson = stringJson.replace('DiagramRotation\\\": 0}]', 'DiagramRotation\\\": 0}\n    ]') # format end element json
        stringJson = stringJson.replace('{\\\"Source', '\n      {\\\"Source')
        stringJson = stringJson.replace('}]}\", \"CameraSave', '}\n    ]}\", \"CameraSave')
        return stringJson
    def _format_Experiment(stringJson: str) -> str:
        charIndex = 0
        listStringJson = list(stringJson)
        tab = 0
        tabString = '  '
        isString = False
        while charIndex < listStringJson.__len__():
            char = listStringJson[charIndex]
            if char == ',':
                if not isString:
                    listStringJson[charIndex] = ',\n' + (tabString * tab)[1:]
            elif char == '\"':
                isString = not isString
            elif char == '{':
                if not isString:
                    listStringJson[charIndex] = '{\n' + tabString * (tab + 1)
                    tab += 1
            elif char == '}':
                if not isString:
                    tab -= 1
                    listStringJson[charIndex] = '\n' + tabString * tab + '}'
            elif char == '\\':
                charIndex += 1
            charIndex += 1
        return ''.join(listStringJson)

    global _ifndef_open_Experiment
    _ifndef_open_Experiment = False

    fileGlobals.StatusSave["Elements"] = fileGlobals.Elements
    fileGlobals.StatusSave["Wires"] = fileGlobals.Wires
    fileGlobals.sav["Experiment"]["StatusSave"] = json.dumps(fileGlobals.StatusSave)
    with open(fileGlobals.savName, "w", encoding="UTF-8") as f:
        f.write(
            _format_Experiment(
                _format_StatusSave(json.dumps(fileGlobals.sav))
            )
        )
    # 存档回滚
    f = ''
    try:
        f = open(f'{fileGlobals.savName[:len(fileGlobals.savName) - 4:]}_rollBack_sav.txt')
    except FileNotFoundError:
        f = open(f'{fileGlobals.savName[:len(fileGlobals.savName) - 4:]}_rollBack_sav.txt', 'w')
    finally:
        f.close()
    experiments = []
    with open(f'{fileGlobals.savName[:len(fileGlobals.savName) - 4:]}_rollBack_sav.txt', 'r', encoding='utf-8') as f:
        f = f.read()
        if f == '':
            experiments.append(fileGlobals.sav)
        else:
            experiments = json.loads(f)
            experiments.append(fileGlobals.sav)
        if experiments.__len__() > 10:
            experiments.pop(0)
    with open(f'{fileGlobals.savName[:len(fileGlobals.savName) - 4:]}_rollBack_sav.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(experiments))
    print(f'\nCompile successfully! {fileGlobals.Elements.__len__()} elements, {fileGlobals.Wires.__len__()} wires.')
    # clear_Experiment
    # 为write之后可以再次crt或open_Experiment而开发
    pass

# 读取sav文件已有的原件与导线
def read_Experiment() -> None:
    with open(fileGlobals.savName, encoding='UTF-8') as f:
        readmem = json.loads(f.read().replace('\n', ''))
        # 元件
        _local_Elements = json.loads(readmem["Experiment"]["StatusSave"])["Elements"]
        # 导线
        for aWire in json.loads(readmem['Experiment']['StatusSave'])['Wires']:
            fileGlobals.Wires.append(aWire)

        for element in _local_Elements:
            # 坐标标准化（消除浮点误差）
            sign1 = element['Position'].find(',')
            sign2 = element['Position'].find(',', sign1 + 1)
            num1 = fileGlobals.myRound(float(element['Position'][:sign1:]))
            num2 = fileGlobals.myRound(float(element['Position'][sign1 + 1: sign2:]))
            num3 = fileGlobals.myRound(float(element['Position'][sign2 + 1::]))
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
            elif obj.type() == '8bit Input':
                obj._arguments['Statistics'] = element['Statistics']
                obj._arguments['Properties']['十进制'] = element['Properties']['十进制']

# 重命名sav
def rename_Experiment(name: str) -> None:
    # 检查是否重名
    savs = [i for i in walk(fileGlobals.FILE_HEAD)][0]
    savs = savs[savs.__len__() - 1]
    savs = [aSav for aSav in savs if aSav.endswith('sav')]
    for aSav in savs:
        with open(f"{fileGlobals.FILE_HEAD}\\{aSav}", encoding='utf-8') as f:
            try:
                f = json.loads(f.read().replace('\n', ''))
            except:
                pass
            else:
                if f['InternalName'] == name:
                    raise RuntimeError('Duplicate name archives are forbidden')
    # 重命名存档
    name = str(name)
    fileGlobals.sav["Summary"]["Subject"] = name
    fileGlobals.sav["InternalName"] = name

# 打开一个存档的窗口
def show_Experiment() -> None:
    popen(f'notepad {fileGlobals.savName}')
os_Experiment = show_Experiment

# 删除存档
def del_Experiment() -> None:
    remove(fileGlobals.savName)
    remove(f"{fileGlobals.savName.replace('.sav', '_rollBack_sav.txt')}")
    try:
        remove(fileGlobals.savName.replace('.sav', '.jpg'))
    except:
        sys.exit()

# 存档回滚
def rollBack_Experiment(back : int = 1):
    if not isinstance(back, int) and (back < 1 or back >= 10):
        raise RuntimeError('back must be an integer between 1 and 10')
    f = ''
    try:
        f = open(f'{fileGlobals.savName[:len(fileGlobals.savName) - 4:]}_rollBack_sav.txt')
    except FileNotFoundError:
        f = open(f'{fileGlobals.savName[:len(fileGlobals.savName) - 4:]}_rollBack_sav.txt', 'w')
    finally:
        f.close()
    with open(f'{fileGlobals.savName[:len(fileGlobals.savName) - 4:]}_rollBack_sav.txt', encoding='utf-8') as f:
        reader = f.read().replace('\n', '')
        if reader == '':
            raise RuntimeError('There is no archive to roll back')
        f = json.loads(reader)
        fileGlobals.sav = json.loads(f[len(f) - 1 - back]['Experiment']['StatusSave'])
        fileGlobals.Elements = fileGlobals.sav['Elements']
        fileGlobals.Wires = fileGlobals.sav['Wires']

# 发布实验时输入实验介绍
def introduce_Experiment(introduction: str) -> None:
    if not isinstance(introduction, str) or introduction is None:
        raise TypeError
    introduction = introduction.replace('\n', ' \n')
    fileGlobals.sav['Summary']['Description'] = [s[:len(s) - 1] for s in re.compile('[^\n]+').findall(introduction)]

# 发布实验时输入实验标题
def title_Experiment(title: str) -> None:
    if isinstance(title, str) or title is None:
        raise TypeError
    fileGlobals.sav['Summary']['Subject'] = title