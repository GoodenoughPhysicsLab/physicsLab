#coding=utf-8
import os
from typing import Union
import physicsLab.errors as errors

#define
# 电学实验的sav模板
_electricity = {
    "Type": 0,
    "Experiment": {
        "ID": None,
        "Type": 0,  # 实验类型： 0: 电学实验, 1: 电学电路图模式, 2: 天体彩蛋模式, 3：天体物理, 4: 电与磁实验
        "Components": 7,
        "Subject": None,
        "StatusSave": "",  # _StatusSave, 存放以字符串形式存储的json
        "CameraSave": "{\"Mode\":0,\"Distance\":2.7,\"VisionCenter\":\"0.3623461,1.08,-0.4681728\",\"TargetRotation\":\"50,0,0\"}",
        "Version": 2404,
        "CreationDate": 1673100860436,
        "Paused": False,
        "Summary": None,
        "Plots": None
    },
    "ID": None,
    "Summary": {  # 发布实验
        "Type": 0,
        "ParentID": None,
        "ParentName": None,
        "ParentCategory": None,
        "ContentID": None,
        "Editor": None,
        "Coauthors": [],
        "Description": None,  # 实验介绍
        "LocalizedDescription": None,
        "Tags": [
            "Type-0"
        ],
        "ModelID": None,
        "ModelName": None,
        "ModelTags": [],
        "Version": 0,
        "Language": None,
        "Visits": 0,
        "Stars": 0,
        "Supports": 0,
        "Remixes": 0,
        "Comments": 0,
        "Price": 0,
        "Popularity": 0,
        "CreationDate": 1673086932246,
        "UpdateDate": 0,
        "SortingDate": 0,
        "ID": None,
        "Category": None,
        "Subject": "",
        "LocalizedSubject": None,
        "Image": 0,
        "ImageRegion": 0,
        "User": {
            "ID": None,
            "Nickname": None,
            "Signature": None,
            "Avatar": 0,
            "AvatarRegion": 0,
            "Decoration": 0,
            "Verification": None
        },
        "Visibility": 0,
        "Settings": {},
        "Multilingual": False
    }, "CreationDate": 0,
    "InternalName": "",  # file name
    "Speed": 1.0,
    "SpeedMinimum": 0.0002,
    "SpeedMaximum": 2.0,
    "SpeedReal": 0.0,
    "Paused": False,
    "Version": 0,
    "CameraSnapshot": None,
    "Plots": [],
    "Widgets": [],
    "WidgetGroups": [],
    "Bookmarks": {},
    "Interfaces": {
        "Play-Expanded": False,
        "Chart-Expanded": False
    }
}

# 电与磁实验的sav模板
_electromagnetism = {
    'Type': 4,
    'Experiment': {
        'ID': None,
        'Type': 4,
        'Components': 1,
        'Subject': None,
        'StatusSave': '{"SimulationSpeed":1.0,"Elements":[]}',
        'CameraSave': '{"Mode":1,"Distance":3.25,"VisionCenter":"0.1673855,0.88,0.05990592","TargetRotation":"90,0,0"}',
        'Version': 2405,
        'CreationDate': 1683039963710,
        'Paused': False,
        'Summary': None,
        'Plots': None
    },
    'ID': None,
    'Summary': {
        'Type': 4,
        'ParentID': None,
        'ParentName': None,
        'ParentCategory': None,
        'ContentID': None,
        'Editor': None,
        'Coauthors': [],
        'Description': None,
        'LocalizedDescription': None,
        'Tags': [
            'Type-4'
        ],
        'ModelID': None,
        'ModelName': None,
        'ModelTags': [],
        'Version': 0,
        'Language': None,
        'Visits': 0,
        'Stars': 0,
        'Supports': 0,
        'Remixes': 0,
        'Comments': 0,
        'Price': 0,
        'Popularity': 0,
        'CreationDate': 1683039107861,
        'UpdateDate': 0,
        'SortingDate': 0,
        'ID': None,
        'Category': None,
        'Subject': None,
        'LocalizedSubject': None,
        'Image': 0,
        'ImageRegion': 0,
        'User': {
            'ID': None,
            'Nickname': None,
            'Signature': None,
            'Avatar': 0,
            'AvatarRegion': 0,
            'Decoration': 0,
            'Verification': None
        },
        'Visibility': 0,
        'Settings': {},
        'Multilingual': False
    },
    'CreationDate': 0,
    'InternalName': None,
    'Speed': 1.0,
    'SpeedMinimum': 0.1,
    'SpeedMaximum': 2.0,
    'SpeedReal': 0.0,
    'Paused': False,
    'Version': 0,
    'CameraSnapshot': None,
    'Plots': [],
    'Widgets': [],
    'WidgetGroups': [],
    'Bookmarks': {},
    'Interfaces': {
        'Play-Expanded': False,
        'Chart-Expanded': False
    }
}

from sys import platform
FILE_HEAD = None # os.path.abspath(os.sep) # 获取根目录
if platform == "win32":
    from getpass import getuser
    FILE_HEAD = f"C:/Users/{getuser()}/AppData/LocalLow/CIVITAS/Quantum Physics/Circuit"
elif platform == "linux": # Android
    FILE_HEAD = "/storage/emulated/0/physicsLabSav"

SavPath: str = "" # 存档的完整路径，为 f"{FILE_HEAD}/{SavName}"
SavName: str = ""  # sav的文件名
StatusSave: dict = {} # 存放实验元件，导线（如果是电学实验的话）
Elements: list = []  # 装原件的_arguments
Wires: list = []
PlSav: dict = {}

# 通过坐标索引元件
elements_Position: dict = {}  # key: self._position, value: List[self...]
# 通过index（元件生成顺序）索引元件
elements_Index: list = [] # List[self]

# 初始化_fileGlobals的变量
def fileGlobals_init(experimentType: Union[int, str]) -> None:
    if isinstance(experimentType, str):
        experimentType.strip()
    elif not (
        (
            isinstance(experimentType, int) and (
                experimentType == 0 or # 电学实验
                experimentType == 3 or # 天体物理实验
                experimentType == 4    # 电与磁实验
            )
        ) or experimentType is None
    ):
        raise TypeError

    global PlSav, SavName, StatusSave, Elements, Wires, elements_Index, elements_Position
    SavName = ""  # sav的文件名
    Elements = []  # 装原件的_arguments
    Wires = []
    # 电学实验
    if experimentType == 0 or experimentType is None:
        PlSav = _electricity
        StatusSave = {"SimulationSpeed": 1.0, "Elements": [], "Wires": []}
    # 电与磁实验
    elif experimentType == 4 or experimentType == "电与磁实验":
        PlSav = _electromagnetism
        StatusSave = {"SimulationSpeed": 1.0, "Elements": []}

    elements_Position = {}
    elements_Index = []

# 检查实验类型
def check_ExperimentType(targetType: int, error: bool = True):
    if targetType > 4 or targetType < 0:
        raise TypeError

    if error and not targetType == get_experimentType():
        raise errors.experimentTypeError
    else:
        return targetType == get_experimentType()

# 获取sav
def get_Sav() -> dict:
    import copy
    return copy.deepcopy(PlSav)

# 获取实验类型
def get_experimentType() -> int:
    try:
        return PlSav["Type"]
    except KeyError:
        raise errors.openExperimentError