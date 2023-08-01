#coding=utf-8
import os
import json
from typing import Union

import physicsLab._tools as _tools
import physicsLab.errors as errors
import physicsLab.electricity as electricity
import physicsLab._colorUtils as _colorUtils
import physicsLab._fileGlobals as _fileGlobals

# 实验（存档）类，主要与'with'关键字搭配使用
class experiment:
    def __init__(
            self,
            file: str,
            read: bool = False, # 是否读取存档原有状态
            delete: bool = False, #是否删除实验
            write: bool = True,
            elementXYZ: bool = False,
            type: Union[int, str] = None
    ):
        if not (
            isinstance(file, str) or
            isinstance(read, bool) or
            isinstance(delete, bool) or
            isinstance(elementXYZ, bool) or
            isinstance(write, bool) or
            (
                isinstance(type, (int ,str)) or
                type is None
            )
        ):
            raise TypeError

        self.file = file
        self.read = read
        self.delete = delete
        self.write = write
        self.elementXYZ = elementXYZ
        self.type = type

    # 上下文管理器，搭配with使用
    def __enter__(self):
        try:
            open_Experiment(self.file)
        except errors.openExperimentError: # 如果存档不存在
            crt_Experiment(self.file, self.type)
        except TypeError:
            raise TypeError

        if self.read:
            read_Experiment()
        if self.elementXYZ:
            _fileGlobals.check_ExperimentType(0)
            import physicsLab.electricity.elementXYZ as _elementXYZ
            _elementXYZ.set_elementXYZ(True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.write:
            write_Experiment()
        if self.delete:
            del_Experiment()

# 检测实验是否存在，输入为存档名，若存在则返回存档对应的文件名，若不存在则返回None
def exist_Experiment(savName: str) -> Union[str, None]:
    savs = _tools.getAllSav()
    for aSav in savs:
        with open(f"{_fileGlobals.FILE_HEAD}/{aSav}", encoding='utf-8') as f:
            try:
                f = json.loads(f.read().replace('\n', ''))
            except json.decoder.JSONDecodeError: # 文件不是物实存档
                continue
            else:
                if f["InternalName"]== savName:
                    return aSav
    return None

# 打开一个指定的sav文件（支持输入本地实验的名字或sav文件名）
def open_Experiment(fileName : str) -> None:
    # 输入sav（存档）的文件名并读取部分实验内容
    def _open_Experiment(file: str) -> None:        
        _fileGlobals.SavPath = f"{_fileGlobals.FILE_HEAD}/{file}"
        with open(_fileGlobals.SavPath, encoding="UTF-8") as f:
            f = json.loads(f.read().replace('\n', ''))
            # 初始化package全局变量
            _fileGlobals.fileGlobals_init(f["Type"])

            _fileGlobals.PlSav["InternalName"] = f["InternalName"]
            try: # 当Summary为None时触发TypeError
                _fileGlobals.PlSav["Summary"]["Subject"] = f["InternalName"]
            except TypeError:
                pass

    fileName = fileName.strip()
    if fileName.endswith('.sav'):
        _open_Experiment(fileName)
        return

    _fileGlobals.SavName = exist_Experiment(fileName)
    if _fileGlobals.SavName is None:
        raise errors.openExperimentError(f'No such experiment "{fileName}"')

    _open_Experiment(_fileGlobals.SavName)

# 创建存档，输入为存档名
def crt_Experiment(savName : str, experimentType: str = None) -> None:
    _fileGlobals.fileGlobals_init(experimentType)
    if exist_Experiment(savName) is not None:
        raise errors.crtExperimentFailError
    
    # 创建存档
    if not isinstance(savName, str):
        savName = str(savName)
    _fileGlobals.SavName = _tools.randString(34)
    _fileGlobals.SavPath = f'{_fileGlobals.FILE_HEAD}/{_fileGlobals.SavName}.sav'
    rename_Experiment(savName)

# 将编译完成的json写入sav
def write_Experiment() -> None:
    def _format_StatusSave(stringJson: str) -> str:
        stringJson = stringJson.replace('{\\\"ModelID', '\n      {\\\"ModelID') # format element json
        stringJson = stringJson.replace('DiagramRotation\\\": 0}]', 'DiagramRotation\\\": 0}\n    ]') # format end element json
        stringJson = stringJson.replace('{\\\"Source', '\n      {\\\"Source')
        stringJson = stringJson.replace("色导线\\\"}]}", "色导线\\\"}\n    ]}")
        return stringJson

    _fileGlobals.StatusSave["Elements"] = _fileGlobals.Elements
    _fileGlobals.StatusSave["Wires"] = _fileGlobals.Wires
    _fileGlobals.PlSav["Experiment"]["StatusSave"] = \
        json.dumps(_fileGlobals.StatusSave, ensure_ascii=False, separators=(',', ': '))
    with open(_fileGlobals.SavPath, "w", encoding="UTF-8") as f:
        f.write(
                _format_StatusSave(json.dumps(_fileGlobals.PlSav, indent=2, ensure_ascii=False, separators=(',', ': ')))
        )
    # 编译成功，打印信息
    if _fileGlobals.get_experimentType() == 0:
        _colorUtils.printf(
            f"Successfully compiled! {_fileGlobals.Elements.__len__()} elements, {_fileGlobals.Wires.__len__()} wires.",
            _colorUtils.COLOR.GREEN
        )
    else:
        _colorUtils.printf(
            f"Successfully compiled! {_fileGlobals.Elements.__len__()} elements.",
            _colorUtils.COLOR.GREEN
        )

# 读取sav文件已有的原件与导线
def read_Experiment() -> None:
    with open(_fileGlobals.SavPath, encoding='UTF-8') as f:
        readmem = json.loads(f.read().replace('\n', ''))
        # 元件
        _local_Elements = json.loads(readmem["Experiment"]["StatusSave"])["Elements"]
        # 导线
        _fileGlobals.Wires = json.loads(readmem['Experiment']['StatusSave'])['Wires']
        # 实验介绍
        _fileGlobals.PlSav['Summary']["Description"] = readmem["Summary"]["Description"]

        for element in _local_Elements:
            # 坐标标准化（消除浮点误差）
            sign1 = element['Position'].find(',')
            sign2 = element['Position'].find(',', sign1 + 1)
            num1 = _tools.roundData(float(element['Position'][:sign1:]))
            num2 = _tools.roundData(float(element['Position'][sign1 + 1: sign2:]))
            num3 = _tools.roundData(float(element['Position'][sign2 + 1::]))
            element['Position'] = f"{num1},{num2},{num3}"  # x, z, y
            # 实例化对象
            obj = None
            from physicsLab.element import crt_Element

            if _fileGlobals.get_experimentType() == 0:
                obj = crt_Element(element["ModelID"], num1, num3, num2, elementXYZ=False)
            elif _fileGlobals.get_experimentType() == 3 or _fileGlobals.get_experimentType() == 4:
                obj = crt_Element(element["ModelID"], num1, num3, num2)
            else:
                raise errors.openExperimentError

            sign1 = element['Rotation'].find(',')
            sign2 = element['Rotation'].find(',', sign1 + 1)
            x = float(element['Rotation'][:sign1:])
            z = float(element['Rotation'][sign1 + 1: sign2:])
            y = float(element['Rotation'][sign2 + 1::])
            obj.set_Rotation(x, y, z)
            obj._arguments['Identifier'] = element['Identifier']
            # 如果obj是逻辑输入
            if isinstance(obj, electricity.Logic_Input) and element['Properties'].get('开关') == 1:
                obj.set_highLevel()
            # 如果obj是8位输入器
            elif isinstance(obj, electricity.eight_bit_Input):
                obj._arguments['Statistics'] = element['Statistics']
                obj._arguments['Properties']['十进制'] = element['Properties']['十进制']

# 重命名sav
def rename_Experiment(name: str) -> None:
    # 检查是否重名
    savs = [i for i in os.walk(_fileGlobals.FILE_HEAD)][0]
    savs = savs[savs.__len__() - 1]
    savs = [aSav for aSav in savs if aSav.endswith('sav')]
    for aSav in savs:
        with open(f"{_fileGlobals.FILE_HEAD}/{aSav}", encoding='utf-8') as f:
            try:
                f = json.loads(f.read().replace('\n', ''))
            except:
                pass
            else:
                if f['InternalName'] == name:
                    raise RuntimeError('Duplicate name archives are forbidden')
    # 重命名存档
    name = str(name)
    _fileGlobals.PlSav["Summary"]["Subject"] = name
    _fileGlobals.PlSav["InternalName"] = name

# 打开一个存档的窗口
def show_Experiment() -> None:
    # os.system() 在文件夹有空格的时候会出现错误
    os.popen(f'notepad {_fileGlobals.SavPath}')

# 删除存档
def del_Experiment() -> None:
    os.remove(_fileGlobals.SavPath)
    try: # 用存档生成的实验无图片，因此可能删除失败
        os.remove(_fileGlobals.SavPath.replace('.sav', '.jpg'))
    except FileNotFoundError:
        pass
    _colorUtils.printf("Successfully delete experiment!", _colorUtils.COLOR.BLUE)

# 发布实验
def yield_Experiment(title: str = None, introduction: str = None) -> None:
    # 发布实验时输入实验介绍
    def introduce_Experiment(introduction: str) -> None:
        if introduction is not None:
            _fileGlobals.PlSav['Summary']['Description'] = introduction.split('\n')

    # 发布实验时输入实验标题
    def title_Experiment(title: str) -> None:
        if title is not None:
            _fileGlobals.PlSav['Summary']['Subject'] = title

    if (not isinstance(title, str) and title is not None) or \
            (not isinstance(introduction, str) and introduction is not None):
        raise TypeError

    introduce_Experiment(introduction)
    title_Experiment(title)