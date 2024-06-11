# -*- coding: utf-8 -*-
import requests

from typing import Optional, List
from physicsLab.enums import Tag, Category

def get_start_page() -> Optional[dict]:
    ''' 获取主页数据 '''
    response = requests.get("https://physics-api-cn.turtlesim.com/Users")

    if response.status_code == 200:
        return response.json()
    return None

def get_library(token: str, auto_code: str) -> Optional[dict]:
    ''' 获取社区作品列表 '''
    if not isinstance(token, str) or not isinstance(auto_code, str):
        raise TypeError

    response = requests.post(
        "https://physics-api-cn.turtlesim.com/Contents/GetLibrary",
        json={"Identifier": "Discussions", "Language": "Chinese"},
        headers={
            "Content-Type": "application/json",
            "x-API-Token": token,
            "x-API-AuthCode": auto_code,
            "x-API-Version": "2411"
        }
    )

    if response.status_code == 200:
        return response.json()
    return None

def query_experiment(token: str,
                     auto_code: str,
                     tags: List[Tag],
                     category: Category = Category.Experiment,
                     languages: Optional[List[str]]=None,
                     maxnum: int = 18,
                     ) -> Optional[dict]:
    ''' 查询实验
        * tags: 根据列表内的物实实验的标签进行对应的搜索
        * languages: 根据列表内的语言进行对应的搜索
        * maxnum: 最大搜索数量
    '''
    if not isinstance(token, str) or not isinstance(auto_code, str) \
         or not isinstance(category, Category) or (
        not isinstance(tags, list) or not all(isinstance(tag, Tag) for tag in tags)) or languages is not None and (
        not isinstance(languages, list) or not all(isinstance(language, str) for language in languages) or (
        not isinstance(maxnum, int) or maxnum <= 0
        )
        ):
        raise TypeError

    if languages is None:
        languages = []
    tags2 = [tag.value for tag in tags]

    response = requests.post(
        "http://physics-api-cn.turtlesim.com/Contents/QueryExperiments",
        json={
            "Query": {
                "Category": category.value,
                "Languages": languages,
                "ExcludeLanguages": None,
                "Tags": tags2,
                "ModelTags": None,
                "ExcludeTags": None,
                "ModelID": None,
                "ParentID": None,
                "UserID": None,
                "Special": None,
                "From": None,
                "Skip": 0,
                "Take": maxnum,
                "Days": 0,
                "Sort": 0,
                "ShowAnnouncement": False
            }
        },
        headers={
            "Content-Type": "application/json",
            "x-API-Token": token,
            "x-API-AuthCode": auto_code,
        }
    )

    if response.status_code == 200:
        return response.json()
    return None

def anonymous_login(): # TODO
    ''' 匿名登录 '''
    response = requests.post(
        "http://physics-api-cn.turtlesim.com/Users/Authenticate",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Language": "zh-CN"
        },
    )

    if response.status_code == 200:
        return response.json()
    return None