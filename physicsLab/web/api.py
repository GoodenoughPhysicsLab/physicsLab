# -*- coding: utf-8 -*-
''' 该文件提供协程风格的api的封装
    所有以`async_`开头的函数/方法均为协程风格的api
'''
import sys
import asyncio
import functools
import contextvars
import requests
from ._api import _User, get_avatar, get_start_page, _check_response, _api_result
from physicsLab import plAR
from physicsLab import enums
from physicsLab import errors
from physicsLab.enums import Tag, Category
from physicsLab._typing import Callable, Optional, List, Awaitable

async def _async_wrapper(func: Callable, *args, **kwargs):
    if sys.version_info < (3, 9):
        # copied from asyncio.to_thread
        loop = asyncio.get_running_loop()
        ctx = contextvars.copy_context()
        func_call = functools.partial(ctx.run, func, *args, **kwargs)
        return await loop.run_in_executor(None, func_call)
    else:
        return await asyncio.to_thread(func, *args, **kwargs)

async def async_get_start_page() -> Awaitable[_api_result]:
    return await _async_wrapper(get_start_page)

async def async_get_avatar(target_id: str, index: int, category: str, size_category: str) -> Awaitable[_api_result]:
    return await _async_wrapper(get_avatar, target_id, index, category, size_category)

class User(_User):
    ''' 该class提供协程风格的api '''
    def __init__(
            self,
            info: _api_result,
    ) -> None:
        ''' 仅提供数据的初始化
        '''
        # TODO 用assert_true检查类型
        self.token: str = info["Token"]
        assert info["AuthCode"] is not None, errors.BUG_REPORT
        self.auth_code: str = info["AuthCode"]
        # True: 绑定了账号; False: 未绑定账号，是匿名登录
        self.is_binded: bool = info["Data"]["User"]["IsBinded"]
        # 硬件指纹
        self.device_token: str = info["Data"]["DeviceToken"]
        # 账号id
        self.user_id: str = info["Data"]["User"]["ID"]
        # 昵称
        self.nickname: Optional[str] = info["Data"]["User"]["Nickname"]
        # 签名
        self.signature: Optional[str] = info["Data"]["User"]["Signature"]
        # 金币数量
        self.gold: int = info["Data"]["User"]["Gold"]
        # 用户等级
        self.level: int = info["Data"]["User"]["Level"]
        # 头像的索引
        self.avatar: int = info["Data"]["User"]["Avatar"]
        self.avatar_region: int = info["Data"]["User"]["AvatarRegion"]
        self.decoration: int = info["Data"]["User"]["Decoration"]
        self.verification = info["Data"]["User"]["Verification"]
        # 存储了所有与每日活动有关的奖励信息 (比如ActivityID)
        self.statistic: dict = info["Data"]["Statistic"]

    async def async_get_library(self) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_library)

    async def async_query_experiments(
            self,
            category: Category,
            tags: Optional[List[Tag]] = None,
            exclude_tags: Optional[List[Tag]] = None,
            languages: Optional[List[str]] = None,
            exclude_languages: Optional[List[str]] = None,
            user_id: Optional[str] = None,
            take: int = 20,
            skip: int = 0,
            from_skip: Optional[str] = None,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(
            self.query_experiments,
            category,
            tags,
            exclude_tags,
            languages,
            exclude_languages,
            user_id,
            take,
            skip,
            from_skip,
        )

    async def async_get_experiment(
            self,
            content_id: str,
            category: Optional[Category] = None,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_experiment, content_id, category)

    async def async_confirm_experiment(self, summary_id: str, category: Category, image_counter: int) -> Awaitable[_api_result]:
        return await _async_wrapper(self.confirm_experiment, summary_id, category, image_counter)

    async def async_remove_experiment(
            self,
            summary_id: str,
            category: Category,
            reason: Optional[str] = None,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.remove_experiment, summary_id, category, reason)

    async def async_post_comment(
            self,
            target_id: str,
            target_type: str,
            content: str,
            reply_id: Optional[str] = None,
            special: Optional[str] = None,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.post_comment, target_id, target_type, content, reply_id, special)

    async def async_remove_comment(self, comment_id: str, target_type:str) -> Awaitable[_api_result]:
        return await _async_wrapper(self.remove_comment, comment_id, target_type)

    async def async_get_comments(
            self,
            target_id: str,
            target_type: str,
            take: int = 16,
            skip: int = 0,
            comment_id: Optional[str] = None,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_comments, target_id, target_type, take, skip, comment_id)

    async def async_get_summary(self, content_id: str, category: Category) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_summary, content_id, category)

    async def async_get_derivatives(self, content_id: str, category: Category) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_derivatives, content_id, category)

    async def async_get_user(
            self,
            msg: str,
            get_user_mode: enums.GetUserMode,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_user, msg, get_user_mode)

    async def async_get_profile(self) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_profile)

    async def async_star_content(
            self,
            content_id: str,
            category: Category,
            star_type: int,
            status: bool = True,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.star_content, content_id, category, star_type, status)

    async def async_upload_image(self, policy: str, authorization: str, image_path: str) -> Awaitable[_api_result]:
        return await _async_wrapper(self.upload_image, policy, authorization, image_path)

    async def async_get_message(self, message_id: str) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_message, message_id)

    async def async_get_messages(
            self,
            category_id: int,
            skip: int = 0,
            take: int = 16,
            no_templates: bool = True,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_messages, category_id, skip, take, no_templates)

    async def async_get_supporters(
            self,
            content_id: str,
            category: Category,
            skip: int = 0,
            take: int = 16,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_supporters, content_id, category, skip, take)

    async def async_get_relations(
            self,
            user_id: str,
            display_type: str = "Follower",
            skip: int = 0,
            take: int = 20,
            query: str = "",
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_relations, user_id, display_type, skip, take, query)

    async def async_follow(self, target_id: str, action: bool = True) -> Awaitable[_api_result]:
        return await _async_wrapper(self.follow, target_id, action)

    async def async_rename(self, nickname: str) -> Awaitable[_api_result]:
        return await _async_wrapper(self.rename, nickname)

    async def async_modify_information(self, target: str) -> Awaitable[_api_result]:
        return await _async_wrapper(self.modify_information, target)

    async def async_receive_bonus(self, activity_id: str, index: int) -> Awaitable[_api_result]:
        return await _async_wrapper(self.receive_bonus, activity_id, index)

    async def async_ban(self, target_id: str, reason: str, length: int) -> Awaitable[_api_result]:
        return await _async_wrapper(self.ban, target_id, reason, length)

    async def async_unban(self, target_id: str, reason: str) -> Awaitable[_api_result]:
        return await _async_wrapper(self.unban, target_id, reason)

def anonymous_login() -> User:
    ''' 匿名登录物实
    '''
    plar_version = plAR.get_plAR_version()
    if plar_version is not None:
        plar_version = int(f"{plar_version[0]}{plar_version[1]}{plar_version[2]}")
    else:
        plar_version = 2411

    response = requests.post(
        "http://physics-api-cn.turtlesim.com/Users/Authenticate",
        json={
            "Login": None,
            "Password": None,
            "Version": plar_version,
            "Device": {
                "Identifier": "7db01528cf13e2199e141c402d79190e",
                "Language": "Chinese"
            },
        },
        headers={
            "Content-Type": "application/json",
        },
    )

    return User(_check_response(response))

def email_login(email: str, password: str) -> User:
    ''' 通过邮箱登录物实
    '''
    if not isinstance(email, str):
        errors.type_error(f"Parameter email must be of type `str`, but got value {email} of type `{type(email).__name__}`")
    if not isinstance(password, str):
        errors.type_error(f"Parameter password must be of type `str`, but got value {password} of type `{type(password).__name__}`")

    plar_version = plAR.get_plAR_version()
    if plar_version is not None:
        plar_version = int(f"{plar_version[0]}{plar_version[1]}{plar_version[2]}")
    else:
        plar_version = 2411

    response = requests.post(
        "http://physics-api-cn.turtlesim.com/Users/Authenticate",
        json={
            "Login": email,
            "Password": password,
            "Version": plar_version,
            "Device": {
                "Identifier": "7db01528cf13e2199e141c402d79190e",
                "Language": "Chinese"
            },
        },
        headers={
            "Content-Type": "application/json",
        },
    )

    return User(_check_response(response))

def token_login(token: str, auth_code: str) -> User:
    ''' 通过token登录物实
    '''
    if not isinstance(token, str):
        errors.type_error(f"Parameter email must be of type `str`, but got value {token} of type `{type(token).__name__}`")
    if not isinstance(auth_code, str):
        errors.type_error(f"Parameter password must be of type `str`, but got value {auth_code} of type `{type(auth_code).__name__}`")

    plar_version = plAR.get_plAR_version()
    if plar_version is not None:
        plar_version = int(f"{plar_version[0]}{plar_version[1]}{plar_version[2]}")
    else:
        plar_version = 2411

    response = requests.post(
        "http://physics-api-cn.turtlesim.com/Users/Authenticate",
        json={
            "Login": None,
            "Password": None,
            "Version": plar_version,
            "Device": {
                "Identifier": "7db01528cf13e2199e141c402d79190e",
                "Language": "Chinese"
            },
        },
        headers={
            "Content-Type": "application/json",
            "x-API-Token": token,
            "x-API-AuthCode": auth_code,
        },
    )

    return User(_check_response(response))

async def async_anonymous_login() -> Awaitable[User]:
    return await _async_wrapper(anonymous_login)

async def async_email_login(email: str, password: str) -> Awaitable[User]:
    return await _async_wrapper(email_login, email, password)

async def async_token_login(token: str) -> Awaitable[User]:
    return await _async_wrapper(token_login, token)
