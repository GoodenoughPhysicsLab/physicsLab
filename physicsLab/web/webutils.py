# -*- coding: utf-8 -*-
''' 该文件提供更方便的遍历物实社区一些数据的迭代器
'''
import time
import urllib3
import requests

from ._api import _User, get_avatar
from ._threadpool import ThreadPool, _Task
from physicsLab import errors
from physicsLab.enums import Category, Tag
from physicsLab._typing import Optional, num_type, Callable, List

_DEFAULT_MAX_WORKERS: int = 4

def _run_task(max_retry: Optional[int], func: Callable, *args, **kwargs):
    ''' 运行func, 直到成功或达到max_retry的条件
        @param max_retry: 最大重试次数(大于等于0), 为None时不限制重试次数
    '''
    assert (max_retry is None or max_retry >= 0) and callable(func), "internal error, please bug report"

    if max_retry is None:
        while True:
            try:
                return func(*args, **kwargs)
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
            return func(*args, **kwargs)
        for _ in range(max_retry + 1):
            try:
                return func(*args, **kwargs)
            except (
                TimeoutError,
                urllib3.exceptions.NewConnectionError,
                urllib3.exceptions.MaxRetryError,
                urllib3.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
            ):
                continue
        raise errors.MaxRetryError("max retry reached")

class NotificationsIter:
    ''' 遍历通知页面的消息的迭代器 '''
    TAKE_AMOUNT: int = -101

    def __init__(
            self,
            user: _User,
            /, *,
            category_id: int,
            start_skip: int = 0,
            max_retry: Optional[int] = 0,
            max_workers: int = _DEFAULT_MAX_WORKERS,
    ) -> None:
        ''' @param user: 执行查询操作的用户
            @param category_id: 消息类型:
                0: 全部, 1: 系统邮件, 2: 关注和粉丝, 3: 评论和回复, 4: 作品通知, 5: 管理记录
            @param start_skip: 开始查询的消息的偏移量, 默认为0
            @param max_retry: 单个请求失败后最多重试次数, 默认为0, 即不重试, None为无限次数重试(不推荐)
            @param max_workers: 最大线程数
        '''
        if not isinstance(user, _User) \
                or not isinstance(category_id, int) \
                or not isinstance(start_skip, int) \
                or not isinstance(max_retry, (int, type(None))) \
                or not isinstance(max_workers, int):
            raise TypeError
        if category_id not in range(6) \
                or not isinstance(max_retry, type(None)) and max_retry < 0 \
                or start_skip < 0 \
                or max_workers <= 0:
            raise ValueError

        self.user = user
        self.category_id = category_id
        self.start_skip = start_skip
        self.max_retry = max_retry
        self.max_workers = max_workers

    def __iter__(self):
        tasks: List[_Task] = []
        with ThreadPool(max_workers=self.max_workers) as executor:
            while True:
                # 避免tasks里面的任务过多导致break停止循环的时候迟迟无法退出
                if len(tasks) < 2500:
                    tasks.append(executor.submit(
                        _run_task,
                        self.max_retry,
                        self.user.get_messages,
                        category_id=self.category_id,
                        skip=self.start_skip,
                        take=self.TAKE_AMOUNT,
                        no_templates=True,
                    ))
                    self.start_skip += abs(self.TAKE_AMOUNT)

                if tasks[0].has_result():
                    msgs = tasks.pop(0).result()["Data"]["Messages"]
                    yield from msgs
                    if len(msgs) < abs(self.TAKE_AMOUNT):
                        executor.submit_end()
                        break

class ExperimentsIter:
    '''遍历实验的迭代器 '''
    # 利用物实bug一次性获取更多的实验
    TAKE_AMOUNT: int = -101

    def __init__(
        self,
        user: _User,
        /, *,
        category: Category,
        start_skip: int = 0,
        from_skip: Optional[str] = None,
        tags: Optional[List[Tag]] = None,
        exclude_tags: Optional[List[Tag]] = None,
        languages: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        max_retry: Optional[int] = 0,
        max_workers: int = _DEFAULT_MAX_WORKERS,
    ) -> None:
        ''' @param tags: 包含的标签列表
            @param exclude_tags: 排除的标签列表
            @param category: 实验类别
            @param languages: 语言列表
            @param user_id: 用户ID
            @param take: 每次获取的数量
            @param skip: 起始位置
            @param max_retry: 最大重试次数
            @param max_workers: 最大线程数
        '''
        if not isinstance(category, Category) \
                or not isinstance(user, _User) \
                or not isinstance(tags, (list, type(None))) \
                or tags is not None and not all(isinstance(tag, Tag) for tag in tags) \
                or not isinstance(exclude_tags, (list, type(None))) \
                or exclude_tags is not None and not all(isinstance(tag, Tag) for tag in exclude_tags) \
                or not isinstance(languages, (list, type(None))) \
                or languages is not None and not all(isinstance(language, str) for language in languages) \
                or not isinstance(user_id, (str, type(None))) \
                or not isinstance(max_retry, (int, type(None))) \
                or not isinstance(start_skip, int) \
                or not isinstance(from_skip, (str, type(None))) \
                or not isinstance(max_workers, int):
            raise TypeError
        if start_skip < 0 \
                or max_workers <= 0:
            raise ValueError

        self.user = user
        self.tags = tags
        self.exclude_tags = exclude_tags
        self.category = category
        self.languages = languages
        self.user_id = user_id
        self.max_retry = max_retry
        self.start_skip = start_skip
        self.from_skip = from_skip
        self.max_workers = max_workers

    def __iter__(self):
        while True:
            msgs = _run_task(
                self.max_retry,
                self.user.query_experiments,
                self.category,
                self.tags,
                self.exclude_tags,
                self.languages,
                self.user_id,
                take=self.TAKE_AMOUNT,
                skip=self.start_skip,
                from_skip=self.from_skip,
            )["Data"]["$values"]
            self.start_skip += abs(self.TAKE_AMOUNT)
            self.from_skip = msgs[-1]["ID"]
            yield from msgs
            if len(msgs) < abs(self.TAKE_AMOUNT):
                break

class BannedMsgIter:
    ''' 遍历指定一段时间的封禁信息 (可指定用户) '''
    banned_template = {
        "ID": "5d57f3c139523f0f640c2211",
        "Identifier": "User-Banned-Record",
    }

    def __init__(
            self,
            user: _User,
            /, *,
            start_skip: int = 0,
            start_time: Optional[num_type] = None,
            end_time: Optional[num_type] = None,
            user_id: Optional[str] = None,
            max_retry: Optional[int] = 0,
            get_banned_template: bool = False,
            max_workers: int = _DEFAULT_MAX_WORKERS,
    ) -> None:
        ''' 获取封禁记录
            @param user: 查询者
            @param user_id: 被查询者的id, None表示查询所有用户封禁记录
            @param start_time: 开始时间, None表示遍历完所有封禁记录
            @param end_time: 结束时间, None为当前时间
            @param max_retry: 最大重试次数(大于等于0), 为None时不限制重试次数
            @param get_banned_template: 是否获取封禁信息的模板, False则使用physicsLab提供的模板
                    模板可能会被紫兰斋修改, 但消息模板基本都是稳定的
            @param max_workers: 最大线程数
        '''
        if not isinstance(user, _User) \
                or not isinstance(start_skip, int) \
                or not isinstance(start_time, (int, float, type(None))) \
                or not isinstance(end_time, (int, float, type(None))) \
                or not isinstance(user_id, (str, type(None))) \
                or not isinstance(max_retry, (int, type(None))) \
                or not isinstance(get_banned_template, bool) \
                or not isinstance(max_workers, int):
            raise TypeError
        if max_workers <= 0:
            raise ValueError

        if get_banned_template:
            response = self.user.get_messages(5, take=1, no_templates=False)["Data"]
            for template in response["Templates"]:
                if template["Identifier"] == self.banned_template["Identifier"]:
                    self.banned_template = template
                    break

        if end_time is None:
            self.end_time = time.time()
        else:
            self.end_time = end_time

        if start_time is not None \
                and start_time < self.end_time \
                and start_time < 0 \
                or start_skip < 0:
            raise ValueError

        self.user = user
        self.start_skip = start_skip
        self.start_time = start_time
        self.user_id = user_id
        self.max_retry = max_retry
        self.max_workers = max_workers

    def __iter__(self):
        for msg in NotificationsIter(
            self.user,
            category_id=5,
            start_skip=self.start_skip,
            max_retry=self.max_retry,
            max_workers=self.max_workers,
        ):
            if msg["TemplateID"] == self.banned_template["ID"] \
                    and (self.start_time is None or self.start_time * 1000 <= msg["Timestamp"]) \
                    and msg["Timestamp"] < self.end_time * 1000 \
                    and (self.user_id is None or self.user_id in msg["Users"]):
                yield msg
            if self.start_time is not None and msg["Timestamp"] < self.start_time * 1000:
                return

class CommentsIter:
    ''' 获取评论的迭代器 '''
    def __init__(
            self,
            user: _User,
            /, *,
            content_id: str,
            category: str = "User",
            start_time: int = 0,
            max_retry: Optional[int] = 0,
    ) -> None:
        ''' @param content_id: 用户id或实验id
            @param category: 只能为 "User" 或 "Experiment" 或 "Discussion"
        '''
        if not isinstance(user, _User) \
                or not isinstance(content_id, str) \
                or not isinstance(category, str) \
                or not isinstance(max_retry, (int, type(None))):
            raise TypeError
        if category not in ("User", "Experiment", "Discussion"):
            raise ValueError
        if category == "User" and not user.is_binded:
            raise PermissionError("user must be anonymous")

        self.user = user
        self.content_id = content_id
        self.category = category
        self.start_time = start_time * 1000
        self.max_retry = max_retry

    def __iter__(self):
        TAKE_AMOUNT: int = 20
        while True:
            comments = _run_task(
                self.max_retry,
                self.user.get_comments,
                self.content_id,
                self.category,
                skip=self.start_time,
                take=TAKE_AMOUNT,
            )["Data"]["Comments"]

            if len(comments) == 0:
                return
            self.start_time = comments[-1]["Timestamp"]

            yield from comments

class WarnedMsgIter:
    ''' 获取一段时间的指定用户的警告信息的迭代器 '''
    def __init__(
            self,
            user: _User,
            /, *,
            user_id: str,
            start_time: num_type,
            end_time: Optional[num_type] = None,
            maybe_warned_message_callback: Optional[Callable] = None,
    ) -> None:
        ''' 查询警告记录
            @param user: 查询者
            @param user_id: 被查询者的id, 但无法查询所有用户的警告记录
            @param start_time: 开始时间
            @param end_time: 结束时间, None为当前时间
            @param banned_message_callback: 封禁记录回调函数
        '''
        if not isinstance(user, _User) \
                or not isinstance(user_id, str) \
                or not isinstance(start_time, (int, float)) \
                or not isinstance(end_time, (int, float, type(None))) \
                or maybe_warned_message_callback is not None \
                and not callable(maybe_warned_message_callback):
            raise TypeError
        if not user.is_binded:
            raise PermissionError("Unbinded user cannot use this iter")

        if end_time is None:
            end_time = time.time()

        self.user = user
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time
        self.maybe_warned_message_callback = maybe_warned_message_callback

    def __iter__(self):
        for comment in CommentsIter(self.user, content_id=self.user_id, category="User"):
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

class RelationsIter:
    ''' 获取用户的关注/粉丝的迭代器 '''
    # 利用物实bug在每次请求中获取更多的数据
    TAKE_AMOUNT = -101

    def __init__(
            self,
            user: _User,
            /, *,
            user_id: str,
            display_type: str = "Follower",
            max_retry: Optional[int] = 0,
            amount: Optional[int] = None,
            query: str = "",
            max_workers: int = _DEFAULT_MAX_WORKERS,
    ) -> None:
        ''' 查询用户关系
            @param user: 查询者
            @param user_id: 被查询者的id
            @param display_type: 关系类型, "Follower"为粉丝, "Following"为关注
            @param max_retry: 最大重试次数(大于等于0), 为None时不限制重试次数
            @param amount: Follower/Following的数量, 为None时api将自动查询
            @param max_workers: 最大线程数
        '''
        if not isinstance(user, _User) \
                or not isinstance(user_id, str) \
                or not isinstance(display_type, str) \
                or not isinstance(max_retry, (int, type(None))) \
                or not isinstance(amount, (int, type(None))) \
                or display_type not in ("Follower", "Following") \
                or not isinstance(max_workers, int):
            raise TypeError
        if max_retry is not None and max_retry < 0 \
                or max_workers <= 0:
            raise ValueError

        self.user = user
        self.user_id = user_id
        self.display_type = display_type
        self.max_retry = max_retry
        self.query = query
        if amount is None:
            if self.display_type == "Follower":
                self.amount = self.user.get_user(user_id=self.user_id)['Data']['Statistic']['FollowerCount']
            elif self.display_type == "Following":
                self.amount = self.user.get_user(user_id=self.user_id)['Data']['Statistic']['FollowingCount']
            else:
                errors.unreachable()
        else:
            self.amount = amount
        self.max_workers = max_workers

    def __iter__(self):
        with ThreadPool(max_workers=self.max_workers) as executor:
            tasks: List[_Task] = [
                executor.submit(
                    _run_task,
                    self.max_retry,
                    self.user.get_relations,
                    user_id=self.user_id,
                    display_type=self.display_type,
                    skip=_skip,
                    take=self.TAKE_AMOUNT,
                    query=self.query,
                )
                for _skip in range(0, self.amount + 1, abs(self.TAKE_AMOUNT))
            ]
            executor.submit_end()

            for task in tasks:
                yield from task.result()["Data"]["$values"]

class AvatarsIter:
    ''' 遍历头像的迭代器 '''
    def __init__(
            self,
            user: _User,
            /, *,
            target_id: str,
            category: str,
            size_category: str = "full",
            max_retry: Optional[int] = 0,
            max_img_index: Optional[int] = None,
            max_workers: int = _DEFAULT_MAX_WORKERS,
    ) -> None:
        ''' @param user_id: 用户id
            @param category: 只能为 "Experiment" 或 "Discussion" 或 "User"
            @param size_category: 只能为 "small.round" 或 "thumbnail" 或 "full"
            @param user: 查询者, None为匿名用户
            @param max_retry: 最大重试次数(大于等于0), 为None时不限制重试次数
            @param max_workers: 最大线程数
        '''
        if not isinstance(target_id, str) \
                or not isinstance(category, str) \
                or not isinstance(size_category, str) \
                or not isinstance(user, _User) \
                or not isinstance(max_retry, (int, type(None))) \
                or not isinstance(max_img_index, (int, type(None))) \
                or not isinstance(max_workers, int):
            raise TypeError
        if category not in ("User", "Experiment", "Discussion") \
                or size_category not in ("small.round", "thumbnail", "full") \
                or max_img_index is not None and max_img_index < 0 \
                or max_workers <= 0:
            raise ValueError

        if max_img_index is None:
            if category == "User":
                self.max_img_index = user.get_user(user_id=target_id)["Data"]["User"]["Avatar"]
                category = "users"
            elif category == "Experiment":
                self.max_img_index = user.get_summary(target_id, Category.Experiment)["Data"]["Image"]
                category = "experiments"
            elif category == "Discussion":
                self.max_img_index = user.get_summary(target_id, Category.Discussion)["Data"]["Image"]
                category = "experiments"
            else:
                errors.unreachable()
        else:
            self.max_img_index = max_img_index

        self.target_id = target_id
        self.category = category
        self.size_category = size_category
        self.user = user
        self.max_retry = max_retry
        self.max_workers = max_workers

    def __iter__(self):
        with ThreadPool(max_workers=self.max_workers) as executor:
            tasks: List[_Task] = [
                executor.submit(
                    _run_task,
                    self.max_retry,
                    get_avatar,
                    self.target_id,
                    index,
                    self.category,
                    self.size_category,
                )
                for index in range(self.max_img_index + 1)
            ]
            executor.submit_end()
            for task in tasks:
                try:
                    img = task.result()
                except IndexError:
                    continue
                else:
                    yield img
