# -*- coding: utf-8 -*-
import os
import requests

from typing import Optional, List, TypedDict

from physicsLab import plAR
from physicsLab import errors
from physicsLab.enums import Tag, Category

def _check_response(response: requests.Response, callback = None) -> dict:
    ''' 检查返回的response
        @callback: 自定义物实返回的status对应的报错信息,
                    要求传入status_code(捕获物实返回体中的status_code), 无返回值
    '''
    response.raise_for_status()

    response_json = response.json()
    status_code = response_json["Status"]

    if status_code == 200:
        return response_json
    if callback is not None:
        callback(status_code)
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
                 auth_code: Optional[str] = None,
                 ) -> None:
        if username is not None and not isinstance(username, str) or \
                passward is not None and not isinstance(passward, str) or \
                token is not None and not isinstance(token, str) or \
                auth_code is not None and not isinstance(auth_code, str):
            raise TypeError

        if token is not None and auth_code is not None:
            self.token = token
            self.auth_code = auth_code

            tmp = self.__login()
            self.is_anonymous = False

            self.user_id = tmp["Data"]["User"]["ID"]
            self.nickname = tmp["Data"]["User"]["Nickname"]
            self.signature = tmp["Data"]["User"]["Signature"]
            self.avatar = tmp["Data"]["User"]["Avatar"]
            self.avatar_region = tmp["Data"]["User"]["AvatarRegion"]
            self.decoration = tmp["Data"]["User"]["Decoration"]
            self.verification = tmp["Data"]["User"]["Verification"]

        else:
            tmp = self.__login(username, passward)

            self.token = tmp["Token"]
            self.auth_code = tmp["AuthCode"]
            self.user_id = tmp["Data"]["User"]["ID"]

            # True: 是匿名登录; False: 不是匿名登录
            self.is_anonymous: bool = tmp["Data"]["User"]["Nickname"] is None

            if self.is_anonymous:
                self.nickname = None
                self.signature = None
                self.avatar = None
                self.avatar_region = None
                self.decoration = None
                self.verification = None
            else:
                self.nickname = tmp["Data"]["User"]["Nickname"]
                self.signature = tmp["Data"]["User"]["Signature"]
                self.avatar = tmp["Data"]["User"]["Avatar"]
                self.avatar_region = tmp["Data"]["User"]["AvatarRegion"]
                self.decoration = tmp["Data"]["User"]["Decoration"]
                self.verification = tmp["Data"]["User"]["Verification"]

    def __login(self,
                username: Optional[str] = None,
                passward: Optional[str] = None) -> _login_res:
        ''' 登录, 默认为匿名登录

            通过返回字典的Token与AuthCode实现登陆
        '''
        version = plAR.get_plAR_version()
        if version is not None:
            version = int(version.replace(".", ""))
        else:
            version = 2411

        headers = {
            "x-API-Version": str(version),
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Accept-Language": "zh-CN",
        }
        if hasattr(self, "token") and hasattr(self, "auth_code"):
            headers["x-API-Token"] = self.token
            headers["x-API-AuthCode"] = self.auth_code

        response = requests.post(
            "http://physics-api-cn.turtlesim.com/Users/Authenticate",
            json={
                "Login": username,
                "Password": passward,
                "Version": version,
                "Device": {
                    "Identifier": "7db01528cf13e2199e141c402d79190e",
                    "Language": "Chinese"
                    },
            },
            headers=headers,
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
                         languages: Optional[List[str]] = None,
                         take: int = 18,
                         skip: int = 0,
                        ) -> dict:
        ''' 查询实验
            @param tags: 根据列表内的物实实验的标签进行对应的搜索
            @param exclude_tags: 除了列表内的标签的实验都会被搜索到
            @param category: 实验区还是黑洞区
            @param languages: 根据列表内的语言进行对应的搜索
            @param take: 搜索数量
        '''
        if not isinstance(category, Category) or \
            not isinstance(tags, (list, type(None))) or \
            tags is not None and not all(isinstance(tag, Tag) for tag in tags) or \
            not isinstance(exclude_tags, (list, type(None))) or \
            exclude_tags is not None and not all(isinstance(tag, Tag) for tag in exclude_tags) or \
            not isinstance(languages, (list, type(None))) or \
            languages is not None and not all(isinstance(language, str) for language in languages) or \
            not isinstance(take, int) or \
            not isinstance(skip, int):
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
                    "Skip": skip,
                    "Take": take,
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

    def confirm_experiment(self, summary_id: str, category: Category, image_counter: int) -> dict:
        ''' 确认发布实验
        '''
        if not isinstance(summary_id, str) or \
            not isinstance(category, Category) or \
            not isinstance(image_counter, int):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/ConfirmExperiment",
            json={
                "SummaryID": summary_id,
                "Category": category.value,
                "Image": image_counter,
                "Extension": ".jpg",
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode":self.auth_code,
            }
        )

        return _check_response(response)

    def post_comment(self, target_id: str, content: str, target_type: str) -> dict:
        ''' 发表评论
            @param target_id: 目标用户/实验的ID
            @param content: 评论内容
            @param target_type: User, Discussion, Experiment
        '''
        if not isinstance(self.token, str) or \
            not isinstance(self.auth_code, str) or \
            not isinstance(target_id, str):
            raise TypeError
        if target_type not in ("User", "Discussion", "Experiment"):
            raise ValueError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Messages/PostComment",
            json={
                "TargetID": target_id,
                "TargetType": target_type,
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

    def get_comments(self,
                     id: str,
                     target_type: str,
                     take: int = 16,
                     skip: int = 0,
                     ) -> dict:
        ''' 获取留言板信息
            @param id: 物实用户的ID/实验的id
            @param target_type: User, Discussion, Experiment
            @param take: 获取留言的数量
            @param skip: 跳过的留言数量, 为(unix时间戳 * 1000)
        '''
        if not isinstance(self.token, str) or \
            not isinstance(self.auth_code, str) or \
            not isinstance(target_type, str) or \
            not isinstance(take, int) or \
            not isinstance(skip, int):
            raise TypeError
        if target_type not in ("User", "Discussion", "Experiment") or \
            take <= 0 or skip < 0:
            raise ValueError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Messages/GetComments",
            json={
                "TargetID": id,
                "TargetType": target_type,
                "CommentID": None,
                "Take": take,
                "Skip": skip,
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

        def callback(status_code):
            if status_code == 403:
                raise PermissionError("login failed")
            if status_code == 404:
                raise errors.ResponseFail("experiment not found(may be you select category wrong)")

        return _check_response(response, callback)

    def get_derivatives(self, content_id: str, category: Category) -> dict:
        ''' 获取作品的详细信息, 物实第一次读取作品是会使用此接口
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

    def get_profile(self) -> dict:
        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Contents/GetProfile",
            json={
                "ID": self.user_id,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def star(self, content_id: str, category: Category, status: bool = True):
        ''' 添加收藏
            @param content_id: 实验的ID
            @param category: 实验区, 黑洞区
            @param status: True: 收藏, False: 取消收藏
        '''
        if not isinstance(content_id, str) or \
            not isinstance(category, Category) or \
            not isinstance(status, bool):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/StarContent",
            json={
                "ContentID": content_id,
                "Status": status,
                "Category": category.value,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def upload_image(self, policy: str, authorization: str, image_path: str) -> dict:
        ''' 上传实验图片
            @policy @authorization 可通过/Contents/SubmitExperiment获取
            @param image_path: 待上传的图片在本地的路径
        '''
        if policy is None or authorization is None:
            raise RuntimeError("Sorry, Physics-Lab-AR can't upload this iamge")
        if not isinstance(policy, str) or \
            not isinstance(authorization, str) or \
            not isinstance(image_path, str):
            raise TypeError
        if not os.path.exists(image_path) or not os.path.isfile(image_path):
            raise FileNotFoundError

        with open(image_path, "rb") as f:
            data = {
                "policy": (None, policy, None),
                "authorization": (None, authorization, None),
                "file": ("temp.jpg", f, None),
            }
            response = requests.post(
                "http://v0.api.upyun.com/qphysics",
                files=data,
            )
            response.raise_for_status()
            if response.json()["code"] != 200:
                raise errors.ResponseFail(f"error code {response.json()['code']}: "
                                          f"{response.json()['message']}")
            return response.json()

    def get_messages(self,
                     category_id: int = 0,
                     skip: int = 0,
                     take: int = 16,
                     no_templates: bool = True,
                     ) -> dict:
        ''' 获取用户收到的消息
            @param category_id: 消息类型:
                0: 全部, 1: 系统邮件, 2: 评论和回复, 3: 关注和粉丝, 4: 作品通知, 5: 管理记录
            @param skip: 传入一个时间戳, 跳过skip条消息
            @param take: 取take条消息
        '''
        if category_id not in (0, 1, 2, 3, 4, 5) or \
            not isinstance(skip, int) or \
            not isinstance(take, int) or \
            not isinstance(no_templates, bool):
            raise TypeError

        if take <= 0 or skip < 0:
            raise ValueError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Messages/GetMessages",
            json={
                "CategoryID": category_id,
                "Skip": skip,
                "Take": take,
                "NoTemplates": no_templates,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    def get_supporters(self,
                       content_id: str,
                       category: Category,
                       skip: int = 0,
                       take: int = 16,
                       ) -> dict:
        ''' 获取支持列表
            @param category: .Experiment 或 .Discussion
            @param skip: 传入一个时间戳, 跳过skip条消息
            @param take: 取take条消息
        '''
        if not isinstance(content_id, str) or \
                not isinstance(category, Category) or \
                not isinstance(skip, int) or \
                not isinstance(take, int):
            raise TypeError

        if take <= 0 or skip < 0:
            raise ValueError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/GetSupporters",
            json={
                "ContentID": content_id,
                "Category": category.value,
                "Skip": skip,
                "Take": take,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)
