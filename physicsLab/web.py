# -*- coding: utf-8 -*-
import requests
import platform

from typing import Optional, List, TypedDict

from physicsLab import errors
from physicsLab.enums import Tag, Category

def get_start_page() -> Optional[dict]:
    ''' 获取主页数据 '''
    response = requests.get("https://physics-api-cn.turtlesim.com/Users")

    if response.status_code == 200:
        return response.json()
    return None


class _login_res(TypedDict):
    Token: str
    AuthCode: str

class User:
    def __init__(self,
                 username: Optional[str] = None,
                 passward: Optional[str] = None,
                 *,
                 token: Optional[str] = None,
                 auth_code: Optional[str] = None
                 ) -> None:
        if username is not None and not isinstance(username, str) or \
                passward is not None and not isinstance(passward, str) or \
                token is not None and not isinstance(token, str) or \
                auth_code is not None and not isinstance(auth_code, str):
            raise TypeError

        if token is not None and auth_code is not None:
            self.token = token
            self.auth_code = auth_code
        else:
            tmp = self._login(username, passward)

            if tmp is None:
                raise Exception("log in failed")

            self.token = tmp["Token"]
            self.auth_code = tmp["AuthCode"]

    @staticmethod
    def _login(username: Optional[str], passward: Optional[str]) -> Optional[_login_res]:
        ''' 登录, 默认为匿名登录
            通过返回字典的Token与AuthCode实现登陆
        '''
        response = requests.post(
            "http://physics-api-cn.turtlesim.com/Users/Authenticate",
            json={
                "Login": username,
                "Password": passward,
                "Version": 2411,
                "Device": {
                    "ID": None,
                    "Identifier": "7db01528cf13e2199e141c402d79190e",
                    "Platform": "Android",
                    "Model": "HONOR ROD-W09",
                    "System": "Android OS 12 / API-31 (HONORROD-W09/7.0.0.186C00)",
                    "CPU": "ARM64 FP ASIMD AES",
                    "GPU": "Mali-G610 MC6",
                    "SystemMemory": 7691,
                    "GraphicMemory": 2048,
                    "ScreenWidth": 2560,
                    "ScreenHeight": 1600,
                    "ScreenDPI": 360,
                    "ScreenSize": 8.4,
                    "Timezone": "Local",
                    "Language": "Chinese"
                 },
                "Statistic": None
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Accept-Language": "zh-CN"
            },
        )

        if response.status_code == 200:
            return response.json()
        return None

    def get_library(self) -> Optional[dict]:
        ''' 获取社区作品列表 '''
        if not isinstance(self.token, str) or not isinstance(self.auth_code, str):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/GetLibrary",
            json={"Identifier": "Discussions", "Language": "Chinese"},
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
                "x-API-Version": "2411"
            }
        )

        if response.status_code == 200:
            return response.json()
        return None

    def query_experiment(self,
                         tags: Optional[List[Tag]] = None,
                         exclude_tags: Optional[List[Tag]] = None,
                         category: Category = Category.Experiment,
                         languages: Optional[List[str]]=None,
                         maxnum: int = 18,
                        ) -> Optional[dict]:
        ''' 查询实验
            * tags: 根据列表内的物实实验的标签进行对应的搜索
            * languages: 根据列表内的语言进行对应的搜索
            * maxnum: 最大搜索数量
        '''
        if not isinstance(self.token, str) or not isinstance(self.auth_code, str) \
            or not isinstance(category, Category) or tags is not None and (
            not isinstance(tags, list) or not all(isinstance(tag, Tag) for tag in tags)) or languages is not None and (
            not isinstance(languages, list) or not all(isinstance(language, str) for language in languages) or (
            not isinstance(maxnum, int) or maxnum <= 0)
            ):
            raise TypeError

        if languages is None:
            languages = []
        if tags is not None:
            tags2 = [tag.value for tag in tags]
        else:
            tags2 = None

        if exclude_tags is not None:
            exclude_tags = [tag.value for tag in exclude_tags] # type: ignore

        response = requests.post(
            "http://physics-api-cn.turtlesim.com/Contents/QueryExperiments",
            json={
                "Query": {
                    "Category": category.value,
                    "Languages": languages,
                    "ExcludeLanguages": None,
                    "Tags": tags2,
                    "ModelTags": None,
                    "ExcludeTags": exclude_tags,
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
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        if response.status_code == 200:
            return response.json()
        return None

    def get_comments(self):
        ''' 获取留言板信息 '''
        pass