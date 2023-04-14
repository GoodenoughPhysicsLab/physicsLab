#coding=utf-8
import os as _os
import sys as _sys
import json as _json

import physicsLab._tools as _tool
import physicsLab.errors as errors
import physicsLab._colorUtils as _colorUtils
import physicsLab._fileGlobals as _fileGlobals
from physicsLab.electricity.element import crt_Element

### define ###

# 是否已经有存档被打开或创建
_ifndef_open_Experiment = False

def print_Elements():
    print(_fileGlobals.Elements)

def print_wires():
    print(_fileGlobals.Wires)

def print_elements_Address():
    print(_fileGlobals.elements_Address)

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

    _fileGlobals.savName = f"{_fileGlobals.FILE_HEAD}\\{file}"
    with open(_fileGlobals.savName, encoding="UTF-8") as f:
        InternalName = (_json.loads(f.read().replace('\n', '')))["Summary"]["Subject"]
        _fileGlobals.sav["Summary"]["Subject"] = InternalName
        _fileGlobals.sav["InternalName"] = _fileGlobals.sav["Summary"]["Subject"]

# 将import了physicsLab的文件的第一行添加上 #coding=utf-8
def _utf8_coding(func):
    def result(string: str, *args, **kwargs) -> None:
        try: # 在cmd或者shell上无法执行该功能
            import sys
            s = ''
            with open(sys.argv[0], encoding='utf-8') as f:
                s = f.read()
            if not s.replace('\n', '').startswith('#coding=utf-8'):
                with open(sys.argv[0], 'w', encoding='utf-8') as f:
                    if s.startswith('\n'):
                        f.write(f'#coding=utf-8{s}')
                    else:
                        f.write(f'#coding=utf-8\n{s}')
        except FileNotFoundError:
            # 在cmd或IDLE上运行时会关闭打印彩字功能
            _colorUtils.printColor = False
        func(string, *args, **kwargs)
    return result

# 打开一个指定的sav文件（支持输入本地实验的名字或sav文件名）
@_utf8_coding
def open_Experiment(file : str) -> None:
    _fileGlobals.fileGlobals_init()
    file = file.strip()
    if file.endswith('.sav'):
        old_open_Experiment(file)
    else:
        savs = [i for i in _os.walk(_fileGlobals.FILE_HEAD)][0]
        savs = savs[savs.__len__() - 1]
        savs = [aSav for aSav in savs if aSav.endswith('sav')]
        for aSav in savs:
            with open(f"{_fileGlobals.FILE_HEAD}\\{aSav}", encoding='utf-8') as f:
                try:
                    f = _json.loads(f.read().replace('\n', ''))
                except _json.decoder.JSONDecodeError:
                    pass
                else:
                    if (f.get("InternalName") == file):
                        old_open_Experiment(aSav)
                        return
        raise errors.openExperimentError(f'No such experiment "{file}"')

# 创建存档
@_utf8_coding
def crt_Experiment(name : str) -> None:
    _fileGlobals.fileGlobals_init()
    global _ifndef_open_Experiment
    # 该函数与open_Experiment一起，每次只能运行一次
    if (_ifndef_open_Experiment):
        raise RuntimeError("This function can only be run once")
    _ifndef_open_Experiment = True
    # 检查是否存在重名的存档
    savs = [i for i in _os.walk(_fileGlobals.FILE_HEAD)][0]
    savs = savs[savs.__len__() - 1]
    savs = [aSav for aSav in savs if aSav.endswith('sav')]
    for aSav in savs:
        with open(f"{_fileGlobals.FILE_HEAD}\\{aSav}", encoding='utf-8') as f:
            try:
                f = _json.loads(f.read().replace('\n', ''))
            except:
                pass
            else:
                if f['InternalName'] == name:
                    raise RuntimeError('Duplicate name archives are forbidden')
    # 创建存档
    if not isinstance(name, str):
        name = str(name)
    _fileGlobals.savName = _tool.randString(34)
    _fileGlobals.savName = f'{_fileGlobals.FILE_HEAD}\\{_fileGlobals.savName}.sav'
    with open(_fileGlobals.savName, 'w', encoding='utf-8'):
        pass
    rename_Experiment(name)

# 将编译完成的json写入sav
def write_Experiment() -> None:
    def _format_StatusSave(stringJson: str) -> str:
        stringJson = stringJson.replace('{\\\"ModelID', '\n      {\\\"ModelID') # format element json
        stringJson = stringJson.replace('DiagramRotation\\\": 0}]', 'DiagramRotation\\\": 0}\n    ]') # format end element json
        stringJson = stringJson.replace('{\\\"Source', '\n      {\\\"Source')
        stringJson = stringJson.replace("色导线\\\"}]}", "色导线\\\"}\n    ]}")
        return stringJson

    global _ifndef_open_Experiment
    _ifndef_open_Experiment = False

    _fileGlobals.StatusSave["Elements"] = _fileGlobals.Elements
    _fileGlobals.StatusSave["Wires"] = _fileGlobals.Wires
    _fileGlobals.sav["Experiment"]["StatusSave"] = _json.dumps(_fileGlobals.StatusSave, ensure_ascii=False)
    with open(_fileGlobals.savName, "w", encoding="UTF-8") as f:
        f.write(
                _format_StatusSave(_json.dumps(_fileGlobals.sav, indent=2, ensure_ascii=False))
        )
    # 存档回滚
    f = ''
    try:
        f = open(f'{_fileGlobals.savName[:len(_fileGlobals.savName) - 4:]}_rollBack_sav.txt')
    except FileNotFoundError:
        f = open(f'{_fileGlobals.savName[:len(_fileGlobals.savName) - 4:]}_rollBack_sav.txt', 'w')
    finally:
        f.close()
    experiments = []
    with open(f'{_fileGlobals.savName[:len(_fileGlobals.savName) - 4:]}_rollBack_sav.txt', 'r', encoding='utf-8') as f:
        f = f.read()
        if f == '':
            experiments.append(_fileGlobals.sav)
        else:
            experiments = _json.loads(f)
            experiments.append(_fileGlobals.sav)
        if experiments.__len__() > 10:
            experiments.pop(0)
    with open(f'{_fileGlobals.savName[:len(_fileGlobals.savName) - 4:]}_rollBack_sav.txt', 'w', encoding='utf-8') as f:
        f.write(_json.dumps(experiments, indent=2, ensure_ascii=False))
    # 编译成功，打印信息
    _colorUtils.printf(
        f"Successfully compiled! {_fileGlobals.Elements.__len__()} elements, {_fileGlobals.Wires.__len__()} wires.",
        _colorUtils.GREEN
    )

# 读取sav文件已有的原件与导线
def read_Experiment() -> None:
    with open(_fileGlobals.savName, encoding='UTF-8') as f:
        readmem = _json.loads(f.read().replace('\n', ''))
        # 元件
        _local_Elements = _json.loads(readmem["Experiment"]["StatusSave"])["Elements"]
        # 导线
        _fileGlobals.Wires = _json.loads(readmem['Experiment']['StatusSave'])['Wires']

        for element in _local_Elements:
            # 坐标标准化（消除浮点误差）
            sign1 = element['Position'].find(',')
            sign2 = element['Position'].find(',', sign1 + 1)
            num1 = _tool.roundData(float(element['Position'][:sign1:]))
            num2 = _tool.roundData(float(element['Position'][sign1 + 1: sign2:]))
            num3 = _tool.roundData(float(element['Position'][sign2 + 1::]))
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
    savs = [i for i in _os.walk(_fileGlobals.FILE_HEAD)][0]
    savs = savs[savs.__len__() - 1]
    savs = [aSav for aSav in savs if aSav.endswith('sav')]
    for aSav in savs:
        with open(f"{_fileGlobals.FILE_HEAD}\\{aSav}", encoding='utf-8') as f:
            try:
                f = _json.loads(f.read().replace('\n', ''))
            except:
                pass
            else:
                if f['InternalName'] == name:
                    raise RuntimeError('Duplicate name archives are forbidden')
    # 重命名存档
    name = str(name)
    _fileGlobals.sav["Summary"]["Subject"] = name
    _fileGlobals.sav["InternalName"] = name

# 打开一个存档的窗口
def show_Experiment() -> None:
    _os.popen(f'notepad {_fileGlobals.savName}')
os_Experiment = show_Experiment

# 删除存档
def del_Experiment() -> None:
    _os.remove(_fileGlobals.savName)
    _os.remove(f"{_fileGlobals.savName.replace('.sav', '_rollBack_sav.txt')}")
    try:
        _os.remove(_fileGlobals.savName.replace('.sav', '.jpg'))
    except:
        _sys.exit()

# 存档回滚
def rollBack_Experiment(back: int = 1):
    if not isinstance(back, int) and (back < 1 or back >= 10):
        raise RuntimeError('back must be an integer between 1 and 10')
    f = ''
    try:
        f = open(f'{_fileGlobals.savName[:len(_fileGlobals.savName) - 4:]}_rollBack_sav.txt')
    except FileNotFoundError:
        f = open(f'{_fileGlobals.savName[:len(_fileGlobals.savName) - 4:]}_rollBack_sav.txt', 'w')
    finally:
        f.close()
    with open(f'{_fileGlobals.savName[:len(_fileGlobals.savName) - 4:]}_rollBack_sav.txt', encoding='utf-8') as f:
        reader = f.read().replace('\n', '')
        if reader == '':
            raise RuntimeError('There is no archive to roll back')
        f = _json.loads(reader)
        _fileGlobals.sav = _json.loads(f[len(f) - 1 - back]['Experiment']['StatusSave'])
        _fileGlobals.Elements = _fileGlobals.sav['Elements']
        _fileGlobals.Wires = _fileGlobals.sav['Wires']

# 发布实验时输入实验介绍
def introduce_Experiment(introduction: str) -> None:
    if not isinstance(introduction, str) or introduction is None:
        raise TypeError
    _fileGlobals.sav['Summary']['Description'] = introduction.split('\n')

# 发布实验时输入实验标题
def title_Experiment(title: str) -> None:
    if isinstance(title, str) or title is None:
        raise TypeError
    _fileGlobals.sav['Summary']['Subject'] = title