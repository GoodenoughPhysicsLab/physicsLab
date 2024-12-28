# -*- coding: utf-8 -*-
''' 对物实网络api的封装
    除了上传实验的api的封装在class Experiment的__upload
    同时提供对多线程, 协程风格的api的调用方式的支持
    所有以`async_`开头的函数/方法均为协程风格的api
'''

import os
import asyncio
import requests

from typing import Optional, List, TypedDict, Callable

from physicsLab import plAR
from physicsLab import errors
from physicsLab.enums import Tag, Category

# 从 threading._threading_atexits 中注销掉 furure._python_exit
import sys
import types
import functools
import threading
from concurrent.futures import thread

# python3.14之前, threading.Thread.join 在 Windows 上会阻塞异常的传播
# 也就是说, 在join结束之前, Python无法及时抛出 KeyboardInterrupt
# 而 python 并未提供公开的方法操作 threading._threading_atexit
# NOTE: 依赖于 asyncio 与 concurrent.futures.thread 的实现细节
if sys.version_info < (3, 14) and hasattr(threading, "_threading_atexits"):
    _threading_atexits = []
    for fn in threading._threading_atexits:
        if isinstance(fn, types.FunctionType) and fn is not thread._python_exit:
            _threading_atexits.append(fn)
        elif isinstance(fn, functools.partial) and fn.func is not thread._python_exit:
            _threading_atexits.append(fn)
    threading._threading_atexits = _threading_atexits

def _check_response(response: requests.Response, err_callback: Optional[Callable] = None) -> dict:
    ''' 检查返回的response
        @callback: 自定义物实返回的status对应的报错信息,
                    要求传入status_code(捕获物实返回体中的status_code), 无返回值
    '''
    assert err_callback is None or callable(err_callback)

    response.raise_for_status()

    response_json = response.json()
    status_code = response_json["Status"]

    if status_code == 200:
        return response_json
    if err_callback is not None:
        err_callback(status_code)
    raise errors.ResponseFail(
        f"Physics-Lab-AR returned error code {status_code} : {response_json['Message']}"
    )

async def _async_wrapper(func: Callable, *args, **kwargs):
    return await asyncio.get_running_loop().run_in_executor(None, func, *args, **kwargs)

def get_start_page() -> dict:
    ''' 获取主页数据 '''
    response = requests.get("https://physics-api-cn.turtlesim.com/Users")

    return _check_response(response)

async def async_get_start_page():
    return await _async_wrapper(get_start_page)

class _login_res(TypedDict):
    Token: str
    AuthCode: str
    Data: dict

def get_avatar(id: str, index: int, category: str, size_category: str) -> bytes:
    ''' 获取头像/实验封面
        @param id: 用户id或实验id
        @param index: 历史图片的索引
        @param category: 只能为 "experiments" 或 "users"
        @param size_category: 只能为 "small.round" 或 "thumbnail" 或 "full"
    '''
    if not isinstance(id, str) or \
            not isinstance(index, int) or \
            not isinstance(category, str) or \
            not isinstance(size_category, str):
        raise TypeError
    if category not in ("experiments", "users"):
        raise ValueError
    if size_category not in ("small.round", "thumbnail", "full"):
        raise ValueError

    if category == "users":
        category += "/avatars"
    elif category == "experiments":
        category += "/images"

    response = requests.get(
        f"http://physics-static-cn.turtlesim.com:80/{category}"
        f"/{id[0:4]}/{id[4:6]}/{id[6:8]}/{id[8:]}/{index}.jpg!{size_category}",
    )

    if b'<Error>' in response.content:
        raise IndexError("avatar not found")
    return response.content

async def async_get_avatar(id: str, index: int, category: str, size_category: str):
    return await _async_wrapper(get_avatar, id, index, category, size_category)

class User:
    def __init__(
            self,
            username: Optional[str] = None,
            password: Optional[str] = None,
            *,
            token: Optional[str] = None,
            auth_code: Optional[str] = None,
    ) -> None:
        if not isinstance(username, (str, type(None))) or \
                not isinstance(password, (str, type(None))) or \
                not isinstance(token, (str, type(None))) or \
                not isinstance(auth_code, (str, type(None))):
            raise TypeError

        if token is not None and auth_code is not None:
            # 只有登录一定会返回auth_code, 其他api返回的AuthCode可能是无效的None
            self.token = token
            self.auth_code = auth_code

            tmp = self.__login()
            self.is_anonymous = False

            self.user_id: str = tmp["Data"]["User"]["ID"]
            self.nickname: Optional[str] = tmp["Data"]["User"]["Nickname"]
            self.signature = tmp["Data"]["User"]["Signature"]
            self.avatar: Optional[int] = tmp["Data"]["User"]["Avatar"]
            self.avatar_region = tmp["Data"]["User"]["AvatarRegion"]
            self.decoration = tmp["Data"]["User"]["Decoration"]
            self.verification = tmp["Data"]["User"]["Verification"]

        else:
            tmp = self.__login(username, password)

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

        assert isinstance(self.token, str) and isinstance(self.auth_code, str)

    def __login(
            self,
            username: Optional[str] = None,
            password: Optional[str] = None
    ) -> _login_res:
        ''' 登录, 默认为匿名登录

            通过返回字典的Token与AuthCode实现登陆
        '''
        assert isinstance(username, (str, type(None))) and isinstance(password, (str, type(None)))

        plar_version = plAR.get_plAR_version()
        if plar_version is not None:
            plar_version = int(f"{plar_version[0]}{plar_version[1]}{plar_version[2]}")
        else:
            plar_version = 2411

        headers = {
            "x-API-Version": str(plar_version),
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
                "Password": password,
                "Version": plar_version,
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
        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/GetLibrary",
            json={
                "Identifier": "Discussions",
                "Language": "Chinese",
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    async def async_get_library(self):
        return await _async_wrapper(self.get_library)

    def query_experiments(
            self,
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
            _tags = [tag.value for tag in tags]
        else:
            _tags = None

        if exclude_tags is not None:
            exclude_tags = [tag.value for tag in exclude_tags] # type: ignore

        response = requests.post(
            "http://physics-api-cn.turtlesim.com/Contents/QueryExperiments",
            json={
                "Query": {
                    "Category": category.value,
                    "Languages": languages,
                    "ExcludeLanguages": None,
                    "Tags": _tags,
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
                    "ShowAnnouncement": False,
                }
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
        )

        return _check_response(response)

    async def async_query_experiments(
            self,
            tags: Optional[List[Tag]] = None,
            exclude_tags: Optional[List[Tag]] = None,
            category: Category = Category.Experiment,
            languages: Optional[List[str]] = None,
            take: int = 18,
            skip: int = 0,
    ):
        return await _async_wrapper(self.query_experiments, tags, exclude_tags, category, languages, take, skip)

    def get_experiment(
            self,
            content_id: str,
            category: Optional[Category] = None,
    ) -> dict:
        ''' 获取实验
            @param content_id: 当category不为None时, content_id为实验ID,
                               否则会被识别为get_summary()["Data"]["ContentID"]的结果
            @param category: 实验区还是黑洞区
        '''
        if not isinstance(content_id, str) or \
                not isinstance(category, (Category, type(None))):
            raise TypeError

        if category is not None:
            # 如果传入的是实验ID, 先获取summary来得到ContentID
            summary = self.get_summary(content_id, category)
            content_id = summary["Data"]["ContentID"]

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

    async def async_get_experiment(
            self,
            content_id: str,
            category: Optional[Category] = None,
    ) -> dict:
        return await _async_wrapper(self.get_experiment, content_id, category)

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

    async def async_confirm_experiment(self, summary_id: str, category: Category, image_counter: int):
        return await _async_wrapper(self.confirm_experiment, summary_id, category, image_counter)

    def post_comment(
            self,
            target_id: str,
            target_type: str,
            content: str,
            reply_id: Optional[str] = None,
    ) -> dict:
        ''' 发表评论
            @param target_id: 目标用户/实验的ID
            @param target_type: User, Discussion, Experiment
            @param content: 评论内容
            @param reply_id: 被回复的user的ID (可被自动推导)
        '''
        if not isinstance(target_id, str) or \
                not isinstance(content, str) or \
                not isinstance(target_type, str) or \
                not isinstance(reply_id, (str, type(None))):
            raise TypeError
        if target_type not in ("User", "Discussion", "Experiment"):
            raise ValueError

        if reply_id is None:
            reply_id = ""

            # 物实支持多语: 中文、英文、法文、德文、西班牙文、日文、乌克兰文、波兰文
            if content.startswith("回复@") \
                    or content.startswith("Reply@") \
                    or content.startswith("Répondre@") \
                    or content.startswith("Antworten@") \
                    or content.startswith("Respuesta@") \
                    or content.startswith("応答@") \
                    or content.startswith("Відповісти@") \
                    or content.startswith("Odpowiadać@"):
                _nickname = ""
                is_match: bool = False
                for chr in content:
                    if chr in (':', ' '):
                        break
                    elif is_match:
                        _nickname += chr
                    elif chr == '@':
                        is_match = True
                        continue

                if _nickname != "":
                    try:
                        reply_id = self.get_user(name=_nickname)["Data"]["User"]["ID"]
                    except errors.ResponseFail:
                        pass

        assert isinstance(reply_id, str)

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Messages/PostComment",
            json={
                "TargetID": target_id,
                "TargetType": target_type,
                "Language": "Chinese",
                "ReplyID": reply_id,
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

    async def async_post_comment(
            self,
            target_id: str,
            target_type: str,
            content: str,
            reply_id: Optional[str] = None,
    ) -> dict:
        return await _async_wrapper(self.post_comment, target_id, target_type, content, reply_id)

    def remove_comment(self, CommentID: str, target_type: str) -> dict:
        ''' 删除评论
            @param CommentID: 评论ID, 可以通过`get_comments`获取
            @param target_type: User, Discussion, Experiment
        '''
        if not isinstance(CommentID, str) or \
                not isinstance(target_type, str):
            raise TypeError
        if target_type not in ("User", "Discussion", "Experiment"):
            raise ValueError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Messages/RemoveComment",
            json={
                "TargetType": target_type,
                "CommentID": CommentID,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    async def async_remove_comment(self, CommentID: str, target_type:str):
        return await _async_wrapper(self.remove_comment, CommentID, target_type)

    def get_comments(
            self,
            target_id: str,
            target_type: str,
            take: int = 16,
            skip: int = 0,
            comment_id: Optional[str] = None,
    ) -> dict:
        ''' 获取留言板信息
            @param id: 物实用户的ID/实验的id
            @param target_type: User, Discussion, Experiment
            @param take: 获取留言的数量
            @param skip: 跳过的留言数量, 为(unix时间戳 * 1000)
            @param comment_id: 从comment_id开始获取take条消息 (另一种skip的规则)
        '''
        if not isinstance(self.token, str) or \
                not isinstance(self.auth_code, str) or \
                not isinstance(target_type, str) or \
                not isinstance(take, int) or \
                not isinstance(skip, int) or \
                not isinstance(comment_id, (str, type(None))):
            raise TypeError
        if target_type not in ("User", "Discussion", "Experiment") or \
            take <= 0 or skip < 0:
            raise ValueError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Messages/GetComments",
            json={
                "TargetID": target_id,
                "TargetType": target_type,
                "CommentID": comment_id,
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

    async def async_get_comments(
            self,
            id: str,
            target_type: str,
            take: int = 16,
            skip: int = 0,
    ):
        return await _async_wrapper(self.get_comments, id, target_type, take, skip)

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

    async def async_get_summary(self, content_id: str, category: Category):
        return await _async_wrapper(self.get_summary, content_id, category)

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

    async def async_get_derivatives(self, content_id: str, category: Category):
        return await _async_wrapper(self.get_derivatives, content_id, category)

    def get_user(
            self,
            user_id: Optional[str] = None,
            name: Optional[str] = None,
    ) -> dict:
        ''' 获取用户信息
            @param user_id: 用户ID
            @param name: 用户名
        '''
        if not isinstance(user_id, (str, type(None))) or \
                    not isinstance(name, (str, type(None))) or \
                    user_id is None and name is None:
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/GetUser",
            json={
                "ID": user_id,
                "Name": name,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    async def async_get_user(
            self,
            user_id: Optional[str] = None,
            name: Optional[str] = None,
    ):
        return await _async_wrapper(self.get_user, user_id, name)

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

    async def async_get_profile(self):
        return await _async_wrapper(self.get_profile)

    def star(self, content_id: str, category: Category, status: bool = True) -> dict:
        ''' 添加收藏
            @param content_id: 实验ID
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

    async def async_star(self, content_id: str, category: Category, status: bool = True):
        return await _async_wrapper(self.star, content_id, category, status)

    def star_content(self, content_id: str, category: Category, status: bool = True) -> dict:
        if not isinstance(content_id, str) or \
                not isinstance(category, Category) or \
                not isinstance(status, bool):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Contents/StarContent",
            json={
                "ContentID": content_id,
                "Status": status,
                "Category": category.value,
                "Status": status,
                "Type": 1,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    async def async_star_content(self, content_id: str, category: Category, status: bool = True):
        return await _async_wrapper(self.star_content, content_id, category, status)

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
                raise errors.ResponseFail(
                    f"Physics-Lab-AR returned error code {response.json()['code']} : "
                    f"{response.json()['message']}"
                )
            return response.json()

    async def async_upload_image(self, policy: str, authorization: str, image_path: str):
        return await _async_wrapper(self.upload_image, policy, authorization, image_path)

    def get_message(self, message_id: str) -> dict:
        if not isinstance(message_id, str):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Messages/GetMessage",
            json={
                "MessageID": message_id,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
        )

        return _check_response(response)

    async def async_get_message(self, message_id: str):
        return await _async_wrapper(self.get_message, message_id)

    def get_messages(
            self,
            category_id: int = 0,
            skip: int = 0,
            take: int = 16,
            no_templates: bool = True,
    ) -> dict:
        ''' 获取用户收到的消息
            @param category_id: 消息类型:
                0: 全部, 1: 系统邮件, 2: 关注和粉丝, 3: 评论和回复, 4: 作品通知, 5: 管理记录
            @param skip: 跳过skip条消息
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

    async def async_get_messages(
            self,
            category_id: int = 0,
            skip: int = 0,
            take: int = 16,
            no_templates: bool = True,
    ):
        return await _async_wrapper(self.get_messages, category_id, skip, take, no_templates)

    def get_supporters(
            self,
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

    async def async_get_supporters(
            self,
            content_id: str,
            category: Category,
            skip: int = 0,
            take: int = 16,
    ):
        return await _async_wrapper(self.get_supporters, content_id, category, skip, take)

    def get_relations(
            self,
            user_id: str,
            display_type: str = "Follower",
            skip: int = 0,
            take: int = 20,
            query: str = "",
    ) -> dict:
        ''' 获取用户的关注/粉丝列表
            @param display_type: 只能为 Follower: 粉丝, Following: 关注
            @param skip: 跳过skip个用户
            @param take: 取take个用户
            @param query: 为用户id或昵称
        '''
        if display_type not in ("Follower, Following") or \
                not isinstance(user_id, str) or \
                not isinstance(skip, int) or \
                not isinstance(take, int):
            raise TypeError

        if display_type == "Follower":
            display_type_ = 0
        elif display_type == "Following":
            display_type_ = 1
        else:
            raise errors.InternalError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/GetRelations",
            json={
                "UserID": user_id,
                "DisplayType": display_type_,
                "Skip": skip,
                "Take": take,
                "Query": query,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            }
        )

        return _check_response(response)

    async def async_get_relations(
            self,
            user_id: str,
            display_type: str = "Follower",
            skip: int = 0,
            take: int = 20,
            query: str = "",
    ):
        return await _async_wrapper(self.get_relations, user_id, display_type, skip, take, query)

    def follow(self, target_id: str, action: bool = True) -> dict:
        ''' 关注用户
            @param target_id: 被关注的用户的id
            @param action: true为关注, false为取消关注
        '''
        if not isinstance(target_id, str) or \
                not isinstance(action, bool):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/Follow",
            json={
                "TargetID": target_id,
                "Action": int(action),
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
        )

        return _check_response(response)

    async def async_follow(self, target_id: str, action: bool = True):
        return await _async_wrapper(self.follow, target_id, action)

    def rename(self, nickname: str) -> dict:
        ''' 修改用户昵称
            @param nickname: 新昵称
        '''
        if not isinstance(nickname, str):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/Rename",
            json={
                "Target": nickname,
                "UserID": self.user_id,
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
       )

        return _check_response(response)

    async def async_rename(self, nickname: str):
        return await _async_wrapper(self.rename, nickname)

    def modify_info(self, target: str) -> dict:
        ''' 修改用户签名
            @param target: 新签名
        '''
        if not isinstance(target, str):
            raise TypeError

        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/ModifyInformation",
            json={
                "Target": target,
                "Field":"Signature",
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
       )

        return _check_response(response)

    async def async_modify_info(self, target: str):
        return await _async_wrapper(self.modify_info, target)

    def receive_bonus(self) -> dict:
        ''' 领取每日签到奖励
        '''
        response = requests.post(
            "https://physics-api-cn.turtlesim.com:443/Users/ReceiveBonus",
            json={
                "ActivityID": "66d2103b8c1a9a5dbc238435",
                "Index": 0,
                "Statistic": {
                    "ID": self.user_id,
                    "PushToken": None,
                    "PushRecord": 0,
                    "UnreadMessages": 0,
                    "UnreadLetters": 0,
                    "LoginContinuity": 0,
                    "LoginCounter": 4,
                    "ResearchSurvey": None,
                    "PushTags": [],
                    "PushFrequency": 0,
                    "Cover": None,
                    "CommentCount": 1,
                    "Activities": [
                        {
                            "ActivityID": "5efd54a9a533c76504c81ba9",
                            "Counters": [0, 0, 0, 0, 0, 0, 0],
                            "Gains": [0],
                            "Avails": [],
                            "Expiration": "2024-12-31T14:00:00+08:00",
                            "LastModified": "2024-10-27T08:00:00+08:00",
                            "Finished": False,
                        },{
                            "ActivityID": "66d2103b8c1a9a5dbc238435",
                            "Counters": [0, 0, 0],
                            "Gains": [],
                            "Avails": [0],
                            "Expiration": "2025-01-01T14:00:00+08:00",
                            "LastModified": "2024-10-27T08:00:00+08:00",
                            "Finished": False,
                        },{
                            "ActivityID": "5b63edc3795d574798950a82",
                            "Counters": [0],
                            "Gains": [],
                            "Avails": [],
                            "Expiration": "2030-12-31T14:00:00+08:00",
                            "LastModified": "0001-01-01T08:00:00+08:00",
                            "Finished": False,
                        },{
                            "ActivityID": "65c289c78a2841c2ff426eeb",
                            "Counters": [0],
                            "Gains": [],
                            "Avails": [],
                            "Expiration": "2024-12-31T14:00:00+08:00",
                            "LastModified": "0001-01-01T08:00:00+08:00",
                            "Finished": False,
                        },{
                            "ActivityID": "65ca49f3b061f3711a7237a8",
                            "Counters": [0],
                            "Gains": [],
                            "Avails": [],
                            "Expiration": "2024-12-31T14:00:00+08:00",
                            "LastModified": "0001-01-01T08:00:00+08:00",
                            "Finished": False,
                        },
                    ],
                    "Counters": {},
                    "Surveys": {},
                    "LastVersion": 2500,
                    "LastLanguage": "Chinese",
                },
            },
            headers={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
        )

        return _check_response(response)

    async def async_receive_bonus(self):
        return await _async_wrapper(self.receive_bonus)
