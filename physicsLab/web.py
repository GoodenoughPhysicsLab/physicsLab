# -*- coding: utf-8 -*-
import os
import time
import requests

from typing import Optional, List, TypedDict

from physicsLab import plAR
from physicsLab import errors
from physicsLab import Experiment
from physicsLab.enums import Tag, Category

def _check_response(response: requests.Response) -> dict:
    response.raise_for_status()

    response_json = response.json()
    status_code = response_json["Status"]

    if status_code == 200:
        return response_json
    raise errors.ResponseFail(f"Physics-Lab-AR returned error code {status_code} : {response_json['Message']}")


def get_start_page() -> dict:
    ''' 获取主页数据 '''
    response = requests.get("https://physics-api-cn.turtlesim.com/Users")

    return _check_response(response)

class _login_res(TypedDict):
    Token: str
    AuthCode: str
    Data: dict

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

        # True: 是匿名登录; False: 不是匿名登录
        self.is_anonymous: bool = True

        if token is not None and auth_code is not None:
            self.token = token
            self.auth_code = auth_code
            self.is_anonymous = False
        else:
            tmp = self.__login(username, passward)

            self.is_anonymous = tmp["Data"]["User"]["Nickname"] is None

            self.token = tmp["Token"]
            self.auth_code = tmp["AuthCode"]

    @staticmethod
    def __login(username: Optional[str], passward: Optional[str]) -> _login_res:
        ''' 登录, 默认为匿名登录

            通过返回字典的Token与AuthCode实现登陆
        '''
        version = plAR.get_plAR_version()
        if version is not None:
            version = int(version.replace(".", ""))
        else:
            version = 2411
        response = requests.post(
            "http://physics-api-cn.turtlesim.com/Users/Authenticate",
            json={
                "Login": username,
                "Password": passward,
                "Version": version,
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

        return _check_response(response) # type: ignore -> response must match _login_res

    def get_library(self) -> dict:
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
            }
        )

        return _check_response(response)

    def query_experiment(self,
                         tags: Optional[List[Tag]] = None,
                         exclude_tags: Optional[List[Tag]] = None,
                         category: Category = Category.Experiment,
                         languages: Optional[List[str]]=None,
                         maxnum: int = 18,
                        ) -> dict:
        ''' 查询实验
            @param tags: 根据列表内的物实实验的标签进行对应的搜索
            @param exclude_tags: 除了列表内的标签的实验都会被搜索到
            @param category: 实验区还是黑洞区
            @param languages: 根据列表内的语言进行对应的搜索
            @param maxnum: 最大搜索数量
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

        return _check_response(response)

    def get_experiment(self, content_id: str):
        ''' 获取实验
            @param content_id: 不是实验的id, 可通过get_summary()["Data"]["ContentID"]获取
        '''

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Contents/GetExperiment",
            json={
                "ContentID": content_id,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode":self.auth_code,
            }
        )

        return _check_response(response)

    # development
    def upload_experiment(self, image_path: str, experiment: Experiment) -> None:
        ''' 上传(发布/更新) 实验
            @param image_path: 图片路径
            @param summary: 实验介绍,
                Experiment.export_summary()与User.get_summary()["Data"]为符合要求的输入
        '''
        if not isinstance(image_path, str) or not isinstance(experiment, Experiment):
            raise TypeError
        if not os.path.exists(image_path) or not os.path.isfile(image_path):
            raise FileNotFoundError
        if self.is_anonymous:
            raise PermissionError("you must register first")

        summary = experiment.PlSav["Summary"]
        summary["CreationDate"] = time.time() * 1000

        # 请求更新实验
        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/SubmitExperiment",
            json={
            "Request": {
                "FileSize": os.path.getsize(image_path),
                'Extension': ".jpg",
            },
            'Summary': summary,
        },
            headers={
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
                'Accept-Encoding': 'gzip',
                'Content-Type': 'gzipped/json',
            }
        )
        _check_response(response)

        # 上传图片
        # with open(image_path, "rb") as f:
        #     data = {
        #         'policy': (None, response.json()['Data']['Token']['Policy'], None),
        #         'authorization': (None, self.auth_code, None),
        #         'file': ('temp.jpg', f, None),
        #     }
        #     requests.post(
        #         "http://v0.api.upyun.com/qphysics",
        #         files=data,
        #     )

    def post_comment(self, target_id: str, content: str) -> dict:
        ''' 发表评论
            @param target_id: 目标用户的ID
            @param content: 评论内容
        '''
        if not isinstance(self.token, str) or not isinstance(self.auth_code, str):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Messages/PostComment",
            json={
                "TargetID": target_id,
                "TargetType": "User",
                "Language": "Chinese",
                "ReplyID": "",
                "Content": content,
                "Special": None
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def get_comments(self, id: str) -> dict:
        ''' 获取留言板信息
            @param id: 物实用户的ID
        '''
        if not isinstance(self.token, str) or not isinstance(self.auth_code, str):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Messages/GetComments",
            json={
                "TargetID": id,
                "TargetType": "User",
                "CommentID": None,
                "Take": 16,
                "Skip": 0
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def get_summary(self, content_id: str, category: Category) -> dict:
        ''' 获取实验介绍
            @param content_id: 实验ID
            @param category: 实验区还是黑洞区
        '''
        if not isinstance(content_id, str) or not isinstance(category, Category):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/GetSummary",
            json={
                "ContentID": content_id,
                "Category": category.value,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def get_derivatives(self, content_id: str, category: Category) -> dict:
        ''' 获取作品的详细信息
            @param content_id: 实验ID
            @param category: 实验区还是黑洞区
        '''
        if not isinstance(content_id, str) or not isinstance(category, Category):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/GetDerivatives",
            json={
                "ContentID": content_id,
                "Category": category.value,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def get_user(self, user_id: str) -> dict:
        ''' 获取用户信息
            @param user_id: 用户ID
        '''
        if not isinstance(user_id, str):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Users/GetUser",
            json={
                "ID": user_id,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)
