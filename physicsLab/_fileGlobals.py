#coding=utf-8
from getpass import getuser as _getuser
from typing import Union

FILE_HEAD = f'C:\\Users\\{_getuser()}\\AppData\\LocalLow\\CIVITAS\\Quantum Physics\\Circuit'
# _xxx 不是文件向外暴露出的接口，文件外无法访问
savName = ""  # sav的文件名
StatusSave = {"SimulationSpeed": 1.0, "Elements": [], "Wires": []}
Elements = []  # 装原件的_arguments
Wires = []
sav = {}

elements_Address = {}  # key: self._position，value: dict([self], ...)
elements_Index = {}  # key: self.index, value: dict([self], ...)


def fileGlobals_init() -> None:
    global sav, savName, StatusSave, Elements, Wires, elements_Index, elements_Address
    savName = ""  # sav的文件名
    StatusSave = {"SimulationSpeed": 1.0, "Elements": [], "Wires": []}
    Elements = []  # 装原件的_arguments
    Wires = []
    sav = {
        "Type": 0,
        "Experiment": {
            "ID": None,
            "Type": 0,
            "Components": 7,
            "Subject": None,
            "StatusSave": "",  # _StatusSave
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
            "Description": None,
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

    elements_Address = {}  # key: self._position，value: self
    elements_Index = {}  # key: self.index, value: self