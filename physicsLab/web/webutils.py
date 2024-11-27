# -*- coding: utf-8 -*-
import copy
import time
import asyncio
import requests

from . import api
from . import _async_tool
from physicsLab import errors
from physicsLab.enums import Category
from physicsLab.typehint import Optional, Callable, numType

async def _run_task(max_retry: Optional[int], func: Callable, *args, **kwargs):
    ''' 运行func, 直到成功或达到max_retry的条件
        @param max_retry: 最大重试次数(大于等于0), 为None时不限制重试次数
    '''
    assert (max_retry is None or max_retry >= 0) and callable(func), "internal error, please bug report"

    import urllib3
    if max_retry is None:
        while True:
            try:
                return await func(*args, **kwargs)
            except (
                TimeoutError,
                urllib3.exceptions.NewConnectionError,
                urllib3.exceptions.MaxRetryError,
                urllib3.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
            ):
                continue
    else:
        if max_retry == 0:
            return await func(*args, **kwargs)
        for _ in range(max_retry + 1):
            try:
                return await func(*args, **kwargs)
            except (
                TimeoutError,
                urllib3.exceptions.NewConnectionError,
                urllib3.exceptions.MaxRetryError,
                urllib3.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
            ):
                continue
        raise urllib3.exceptions.MaxRetryError

class ManageMsgIter(_async_tool.AsyncTool):
    ''' 获取一段时间的管理记录 (可指定用户) '''
    def __init__(
            self,
            start_time: numType,
            end_time: Optional[numType] = None,
            user: Optional[api.User] = None,
            user_id: Optional[str] = None,
            max_retry: Optional[int] = 0,
    ) -> None:
        ''' 获取封禁记录
            @param user: 查询者
            @param user_id: 被查询者的id, None表示查询所有封禁记录
            @param start_time: 开始时间
            @param end_time: 结束时间, None为当前时间
            @param max_retry: 最大重试次数(大于等于0), 为None时不限制重试次数
        '''

        if not isinstance(user, (api.User, type(None))) or \
                not isinstance(start_time, (int, float)) or \
                not isinstance(end_time, (int, float, type(None))) or \
                not isinstance(user_id, (str, type(None))) or \
                not isinstance(max_retry, (int, type(None))):
            raise TypeError

        if end_time is None:
            end_time = time.time()
        if user is None:
            user = api.User()
        if start_time >= end_time:
            raise ValueError

        super().__init__()
        self.start_time = start_time
        self.end_time = end_time
        self.user = user
        self.user_id = user_id
        self.max_retry = max_retry

    async def _async_main(self) -> None:
        def _make_task(i):
            return asyncio.create_task(
                _run_task(
                    self.max_retry,
                    self._fetch_manage_msgs,
                    i + counter * FETCH_AMOUNT
                )
            )

        assert self.start_time < self.end_time

        self.is_fetching_end: bool = False
        FETCH_AMOUNT = 100
        counter: int = 0

        while not self.is_fetching_end:
            tasks = [_make_task(i) for i in range(FETCH_AMOUNT)]

            for task in tasks:
                for message in await task:
                    self._put_res(message)
            counter += 1
        self._put_end()

    async def _fetch_manage_msgs(self, skip: int):
        assert skip >= 0, "InternalError: please bug-report"
        assert self.end_time is not None, "InternalError: please bug-report"

        TAKE_MESSAGES_AMOUNT = 20
        messages = await self.user.async_get_messages(
            5, skip=skip * TAKE_MESSAGES_AMOUNT, take=TAKE_MESSAGES_AMOUNT,
        )
        messages = messages["Data"]["Messages"]

        res = []
        for message in messages:
            # a month ~ 2629743 seconds
            if message["TimestampInitial"] < (self.start_time - 2629743) * 1000:
                self.is_fetching_end = True
                break
            if self.start_time * 1000 <= message["TimestampInitial"] <= self.end_time * 1000:
                if self.user_id is None or self.user_id == message["Users"][0]:
                    res.append(message)
        return res

class BannedMsgIter:
    ''' 获取一段时间的封禁信息 (可指定用户) '''
    banned_template = None

    def __init__(
            self,
            start_time: numType,
            end_time: Optional[numType] = None,
            user: Optional[api.User] = None,
            user_id: Optional[str] = None,
            max_retry: Optional[int] = 0,
    ) -> None:
        ''' 获取封禁记录
            @param user: 查询者
            @param user_id: 被查询者的id, None表示查询所有封禁记录
            @param start_time: 开始时间
            @param end_time: 结束时间, None为当前时间
            @param max_retry: 最大重试次数(大于等于0), 为None时不限制重试次数
        '''

        if not isinstance(user, (api.User, type(None))) or \
                not isinstance(start_time, (int, float)) or \
                not isinstance(end_time, (int, float, type(None))) or \
                not isinstance(user_id, (str, type(None))) or \
                not isinstance(max_retry, (int, type(None))):
            raise TypeError

        if end_time is None:
            end_time = time.time()
        if user is None:
            user = api.User()

        self.start_time = start_time
        self.end_time = end_time
        self.user = user
        self.user_id = user_id
        self.max_retry = max_retry

    def __iter__(self):
        self.is_fetching_end: bool = False

        if self.start_time >= self.end_time:
            raise ValueError("start_time >= end_time")

        # fetch banned_template
        if self.banned_template is None:
            response = self.user.get_messages(5, take=1, no_templates=False)["Data"]

            for template in response["Templates"]:
                if template["Identifier"] == "User-Banned-Record":
                    self.banned_template = copy.deepcopy(template)
                    break

        # main
        for manage_msg in ManageMsgIter(
                self.start_time,
                self.end_time,
                self.user,
                self.user_id,
                self.max_retry,
                ):
            if manage_msg["TemplateID"] == self.banned_template["ID"]:
                yield manage_msg

class WarnedMsgIter:
    ''' 获取一段时间的指定用户的警告信息的迭代器 '''
    def __init__(
            self,
            user: api.User,
            user_id: str,
            start_time: numType,
            end_time: Optional[numType] = None,
            maybe_warned_message_callback: Optional[Callable] = None,
    ) -> None:
        ''' 查询警告记录
            @param user: 查询者
            @param user_id: 被查询者的id, 但无法查询所有用户的警告记录
            @param start_time: 开始时间
            @param end_time: 结束时间, None为当前时间
            @param banned_message_callback: 封禁记录回调函数
            @return: 封禁记录列表
        '''
        if not isinstance(user, api.User) or \
                not isinstance(user_id, str) or \
                not isinstance(start_time, (int, float)) or \
                not isinstance(end_time, (int, float, type(None))) or \
                maybe_warned_message_callback is not None \
                and not callable(maybe_warned_message_callback):
            raise TypeError
        if user.is_anonymous:
            raise PermissionError("user must be anonymous")

        if end_time is None:
            end_time = time.time()

        self.user = user
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time
        self.maybe_warned_message_callback = maybe_warned_message_callback

    def __iter__(self):
        for comment in CommentsIter(self.user, self.user_id, "User"):
            if comment["Timestamp"] < self.start_time * 1000:
                return

            if self.start_time * 1000 <= comment["Timestamp"] <= self.end_time * 1000:
                if comment["Flags"] is not None \
                        and "Locked" in comment["Flags"] \
                        and "Reminder" in comment["Flags"]:
                    yield comment
                elif "警告" in comment["Content"] \
                        and comment["Verification"] in \
                        ("Volunteer", "Editor", "Emeritus", "Administrator") \
                        and self.maybe_warned_message_callback is not None:
                    self.maybe_warned_message_callback(comment)

class CommentsIter:
    ''' 获取评论的迭代器 '''
    def __init__(self, user: api.User, id: str, category: str = "User") -> None:
        if not isinstance(user, api.User) or \
                not isinstance(id, str) or \
                not isinstance(category, str) and \
                category not in ("User", "Experiment", "Discussion"):
            raise TypeError
        if category == "User" and user.is_anonymous:
            raise PermissionError("user must be anonymous")

        self.user = user
        self.id = id
        self.category = category

    def __iter__(self):
        TAKE: int = 20
        skip_time: int = 0
        while True:
            comments = self.user.get_comments(
                self.id, self.category, skip=skip_time, take=TAKE
            )["Data"]["Comments"]

            if len(comments) == 0:
                return
            skip_time = comments[-1]["Timestamp"]

            for comment in comments:
                yield comment

class RelationsIter(_async_tool.AsyncTool):
    ''' 获取用户的关注/粉丝的迭代器 '''
    def __init__(
            self,
            user: api.User,
            user_id: str,
            display_type: str = "Follower",
            max_retry: Optional[int] = 0,
            amount: Optional[int] = None,
    ) -> None:
        ''' 查询用户关系
            @param user: 查询者
            @param user_id: 被查询者的id
            @param display_type: 关系类型, "Follower"为粉丝, "Following"为关注
            @param max_retry: 最大重试次数(大于等于0), 为None时不限制重试次数
            @param amount: Follower/Following的数量, 为None时api将自动查询
        '''
        if not isinstance(user, api.User) or \
                not isinstance(user_id, str) or \
                not isinstance(display_type, str) or \
                not isinstance(max_retry, (int, type(None))) or \
                not isinstance(amount, (int, type(None))) or \
                display_type not in ("Follower", "Following"):
            raise TypeError
        if max_retry is not None and max_retry < 0:
            raise ValueError

        super().__init__()
        self.user = user
        self.user_id = user_id
        self.display_type = display_type
        self.max_retry = max_retry
        if amount is None:
            if self.display_type == "Follower":
                self.amount = self.user.get_user(self.user_id)['Data']['Statistic']['FollowerCount']
            elif self.display_type == "Following":
                self.amount = self.user.get_user(self.user_id)['Data']['Statistic']['FollowingCount']
            else:
                raise errors.InternalError
        else:
            self.amount = amount

    async def _async_main(self) -> None:
        def _make_task(i: int):
            return asyncio.create_task(
                _run_task(
                    self.max_retry,
                    self.user.async_get_relations,
                    self.user_id, self.display_type, skip=i, take=24,
                )
            )
        tasks = [_make_task(i) for i in range(0, self.amount, 24)]
        for task in tasks:
            for res in (await task)["Data"]["$values"]:
                self._put_res(res)
        self._put_end()

class AvatarsIter(_async_tool.AsyncTool):
    ''' 获取头像的迭代器 '''
    def __init__(
            self,
            search_id: str,
            category: str,
            user: Optional[api.User] = None,
            size_category: str = "full",
            max_retry: Optional[int] = 0,
    ) -> None:
        ''' @param search_id: 用户id
            @param category: 只能为 "Experiment" 或 "Discussion" 或 "User"
            @param size_category: 只能为 "small.round" 或 "thumbnail" 或 "full"
            @param user: 查询者, None为匿名用户
            @param max_retry: 最大重试次数(大于等于0), 为None时不限制重试次数
        '''
        if not isinstance(search_id, str) or \
                not isinstance(category, str) or \
                not isinstance(size_category, str) or \
                not isinstance(user, (api.User, type(None))) or \
                not isinstance(max_retry, (int, type(None))):
            raise TypeError
        if category not in ("User", "Experiment", "Discussion") or \
                size_category not in ("small.round", "thumbnail", "full"):
            raise ValueError

        if user is None:
            user = api.User()

        if category == "User":
            self.max_img_counter = user.get_user(search_id)["Data"]["User"]["Avatar"]
            category = "users"
        elif category == "Experiment":
            self.max_img_counter = user.get_summary(search_id, Category.Experiment)["Data"]["Image"]
            category = "experiments"
        elif category == "Discussion":
            self.max_img_counter = user.get_summary(search_id, Category.Discussion)["Data"]["Image"]
            category = "experiments"
        else:
            raise errors.InternalError

        super().__init__()
        self.search_id = search_id
        self.category = category
        self.size_category = size_category
        self.user = user
        self.max_retry = max_retry

    async def _async_main(self) -> None:
        def _make_task(i):
            return asyncio.create_task(
                _run_task(
                    self.max_retry,
                    api.async_get_avatar,
                    self.search_id, i, self.category, self.size_category,
                )
            )
        tasks = [_make_task(i) for i in range(self.max_img_counter + 1)]
        for task in tasks:
            try:
                res = await task
            except IndexError:
                pass
            else:
                self._put_res(res)
        self._put_end()

class Bot:
    ''' 由@故事里的人 贡献, 我也没用过() '''
    def __init__(
            self,
            bind_user: api.User,
            target_id: str,
            target_type: str,
            is_ignore_reply_to_others: bool = True,
            is_read_history: bool = True,
            is_reply_required: bool = True
    ) -> None:
        ''' @param bind_user: 机器人要绑定的用户账号
            @param target_id: 目标id
            @param target_type: 目标类型, 只能为 "User" 或 "Experiment" 或 "Discussion"
            @param is_ignore_reply_to_others: 如果出现回复@{非Bot的用户}，则忽略
            @param is_read_history: 捕获Bot启动前的消息 (最多20条)
            @param is_reply_required: 只捕获回复@{Bot}的消息
        '''
        if not isinstance(bind_user, api.User) or \
                not isinstance(target_id, str) or \
                not isinstance(target_type, str) or \
                not isinstance(is_ignore_reply_to_others, bool) or \
                not isinstance(is_read_history, bool) or \
                not isinstance(is_reply_required, bool):
            raise TypeError
        if target_type not in ("User", "Experiment", "Discussion"):
            raise ValueError
        if bind_user.is_anonymous:
            raise PermissionError("user must be anonymous")

        # 生命周期 捕获－处理－回复－记录[－完成]
        self.bind_user = bind_user
        self.target_id = target_id
        self.target_type = target_type
        self.is_ignore_reply_to_others = is_ignore_reply_to_others
        self.is_reply_required = is_reply_required

        self.bot_id = self.bind_user.user_id

        comments = self.bind_user.get_comments(target_id, target_type, 20)["Data"]["Comments"]
        if is_read_history:
            index = ""
            for comment in comments[::-1]:
                if comment['UserID'] == self.bot_id:
                    index = comment['ID']
            self.start_index = index
        else:
            self.start_index = comments[0]['ID'] if len(comments) != 0 else ""

    def run(self,
            process_callback: Callable,
            catch_callback: Optional[Callable] = None,
            reply_callback: Optional[Callable] = None,
            finish_callback: Optional[Callable] = None,
            ) -> None:
        ''' @param process_callback: 处理函数，用于处理捕获到的消息
            @param catch_callbakc: 当捕获到新消息时调用的函数
            @param reply_callback: 当回复消息时调用的函数
            @param finnish_callback: 当所有消息处理完成时调用的函数
        '''
        if not callable(process_callback) or \
                catch_callback is not None and not callable(catch_callback) or \
                reply_callback is not None and not callable(reply_callback) or \
                finish_callback is not None and not callable(finish_callback):
            raise TypeError

        pending = set()
        finish = set()

        for comment in self.bind_user.get_comments(self.target_id, self.target_type, 20)['Data']['Comments']:
            if comment['ID'] == self.start_index:
                break
            if comment['UserID'] == self.bot_id:
                continue
            if comment['ID'] in pending or comment['ID'] in finish:
                continue
            if not comment['Content'].startswith(f"回复<user={self.bot_id}") \
                    and self.is_ignore_reply_to_others:
                continue
            if self.bot_id not in comment['Content'] and self.is_reply_required:
                continue

            if catch_callback is not None:
                catch_callback(comment)
            pending.add(comment['ID'])
            reply = process_callback(self, comment)
            if reply == "":
                continue

            msg = f"回复@{comment['Nickname']}: {reply}"
            self.bind_user.post_comment(self.target_id, msg, self.target_type)
            finish.add(comment['ID'])
            pending.remove(comment['ID'])
            if len(pending) == 0:
                if finish_callback is not None:
                    finish_callback(finish)
            if reply_callback is not None:
                reply_callback({**{"msg": msg}, **comment})
