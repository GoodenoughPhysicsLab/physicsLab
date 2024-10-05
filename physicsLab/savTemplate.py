# -*- coding: utf-8 -*-

class Generate:
    ''' Dynamically generated at runtime ''' # 运行时动态生成

# 所有模板都是只读的
# 电学实验的sav模板
Circuit = {
    "Type": 0,
    "Experiment": {
        "ID": None,
        "Type": 0, # 实验类型： 0: 电学实验, 1: 电学电路图模式, 2: 天体彩蛋模式, 3：天体物理, 4: 电与磁实验
        "Components": 7,
        "Subject": None,
        "StatusSave": Generate,
        "CameraSave": Generate,
        "Version": 2404,
        "CreationDate": Generate,
        "Paused": False,
        "Summary": None,
        "Plots": None
    },
    "ID": None,
    "Summary": { # 发布实验
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
        "Language": "Chinese",
        "Visits": 0,
        "Stars": 0,
        "Supports": 0,
        "Remixes": 0,
        "Comments": 0,
        "Price": 0,
        "Popularity": 0,
        "CreationDate": Generate,
        "UpdateDate": 0,
        "SortingDate": 0,
        "ID": None, # 实验的ID
        "Category": None,
        "Subject": "",
        "LocalizedSubject": None,
        "Image": 0,
        "ImageRegion": 0,
        "User": {
            "ID": None, # 用户ID
            "Nickname": None, # 用户昵称
            "Signature": None, # 签名
            "Avatar": 0,
            "AvatarRegion": 0,
            "Decoration": 0,
            "Verification": None
        },
        "Visibility": 0,
        "Settings": {},
        "Anonymous": False,
        "Multilingual": False
    },
    "CreationDate": 0,
    "InternalName": Generate, # 存档名
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

# 天体物理的sav模板
Celestial = {
    "Type": 3,
    "Experiment": {
        "ID": None,
        "Type": 3,
        "Components": 0,
        "Subject": None,
        "StatusSave": Generate,
        "CameraSave": Generate,
        "Version": 2407,
        "CreationDate": Generate,
        "Paused": False,
        "Summary": None,
        "Plots": None
    },
    "ID": None,
    "Summary": {
        "Type": 3,
        "ParentID": None,
        "ParentName": None,
        "ParentCategory": None,
        "ContentID": None,
        "Editor": None,
        "Coauthors": [],
        "Description": None,
        "LocalizedDescription": None,
        "Tags": [
            "Type-3"
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
        "CreationDate": Generate,
        "UpdateDate": 0,
        "SortingDate": 0,
        "ID": None,
        "Category": None,
        "Subject": None,
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
    },
    "CreationDate": 0,
    "InternalName": Generate, # 存档名
    "Speed": 1.0,
    "SpeedMinimum": 0.1,
    "SpeedMaximum": 10.0,
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
Electromagnetism = {
    "Type": 4,
    "Experiment": {
        "ID": None,
        "Type": 4,
        "Components": 1,
        "Subject": None,
        "StatusSave": Generate,
        "CameraSave": Generate,
        "Version": 2405,
        "CreationDate": Generate,
        "Paused": False,
        "Summary": None,
        "Plots": None
    },
    "ID": None,
    "Summary": {
        "Type": 4,
        "ParentID": None,
        "ParentName": None,
        "ParentCategory": None,
        "ContentID": None,
        "Editor": None,
        "Coauthors": [],
        "Description": None,
        "LocalizedDescription": None,
        "Tags": [
            "Type-4"
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
        "CreationDate": Generate,
        "UpdateDate": 0,
        "SortingDate": 0,
        "ID": None,
        "Category": None,
        "Subject": None,
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
    },
    "CreationDate": 0,
    "InternalName": Generate, # 存档名
    "Speed": 1.0,
    "SpeedMinimum": 0.1,
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
