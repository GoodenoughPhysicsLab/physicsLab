# -*- coding: utf-8 -*-
import copy
import time
import urllib3

from . import api
from physicsLab import errors
from physicsLab.enums import Category
from concurrent.futures import ThreadPoolExecutor, as_completed
from physicsLab.typehint import Optional, Callable, numType

def get_banned_messages(start_time: numType,
                        user: Optional[api.User] = None,
                        user_id: Optional[str] = None,
                        end_time: Optional[numType] = None,
                        banned_message_callback: Optional[Callable] = None,
                        ) -> list:
    ''' 获取封禁记录
        @param user: 查询者
        @param user_id: 被查询者的id, None表示查询所有封禁记录
        @param start_time: 开始时间
        @param end_time: 结束时间, None为当前时间
        @param banned_message_callback: 封禁记录回调函数
        @return: 封禁记录列表
    '''
    def _fetch_banned_messages(user: api.User,
                           start_time: numType,
                           end_time: numType,
                           user_id: Optional[str],
                           skip: int,
                           banned_template: dict,
                           ) -> None:
        assert skip >= 0, "internal error, please bug report"
        assert end_time is not None, "internal error, please bug report"

        TAKE_MESSAGES_AMOUNT = 20
        messages = user.get_messages(
            5, skip=skip * TAKE_MESSAGES_AMOUNT, take=TAKE_MESSAGES_AMOUNT,
        )["Data"]["Messages"]

        assert banned_template is not None, "internal error, please bug report"

        nonlocal is_fetching_end, banned_messages, banned_message_callback
        for message in messages:
            if message["TimestampInitial"] < start_time * 1000:
                is_fetching_end = True
                break
            if start_time * 1000 <= message["TimestampInitial"] <= end_time * 1000:
                if (user_id is None or user_id == message["Users"][0]) \
                        and message["TemplateID"] == banned_template["ID"]:
                    message = copy.deepcopy(message)
                    banned_messages.append(message)
                    if banned_message_callback is not None:
                        banned_message_callback(message)

    if not isinstance(user, (api.User, type(None))) or \
            not isinstance(start_time, (int, float)) or \
            not isinstance(end_time, (int, float, type(None))) or \
            not isinstance(user_id, (str, type(None))) or \
            banned_message_callback is not None and not callable(banned_message_callback):
        raise TypeError

    banned_messages = []
    is_fetching_end: bool = False

    if end_time is None:
        end_time = time.time()
    if user is None:
        user = api.User()

    if start_time >= end_time:
        raise ValueError("start_time >= end_time")

    # fetch_banned_template
    banned_template = None
    response = user.get_messages(5, take=1, no_templates=False)["Data"]

    for template in response["Templates"]:
        if template["Identifier"] == "User-Banned-Record":
            banned_template = copy.deepcopy(template)
            break
    assert banned_template is not None, "internal error, please bug report"

    # main
    FETCH_AMOUNT = 100
    counter: int = 0
    while not is_fetching_end:
        with ThreadPoolExecutor(max_workers=FETCH_AMOUNT + 50) as executor:
             for i in range(FETCH_AMOUNT):
                executor.submit(
                    _fetch_banned_messages,
                    user, start_time, end_time, user_id, i + counter * FETCH_AMOUNT, banned_template
                )
        counter += 1
    return banned_messages

def get_warned_messages(start_time: numType,
                        user: api.User,
                        user_id: str,
                        end_time: Optional[numType] = None,
                        warned_message_callback: Optional[Callable] = None,
                        maybe_warned_message_callback: Optional[Callable] = None,
                        ) -> list:
    ''' 查询警告记录
        @param user: 查询者
        @param user_id: 被查询者的id, 但无法查询所有用户的警告记录
        @param start_time: 开始时间
        @param end_time: 结束时间, None为当前时间
        @param banned_message_callback: 封禁记录回调函数
        @return: 封禁记录列表
    '''
    def _fetch_warned_messages(user_id: str, skip: int) -> int:
        assert end_time is not None, "internal error, please bug report"

        nonlocal TAKE_MESSAGE_AMOUNT, is_fetching_end, warned_messages, \
            warned_message_callback, maybe_warned_message_callback

        comments = user.get_comments(
            user_id, "User", skip=skip, take=TAKE_MESSAGE_AMOUNT
        )["Data"]["Comments"]

        if len(comments) == 0:
            is_fetching_end = True
            return -1

        for comment in comments:
            if comment["Timestamp"] < start_time * 1000:
                is_fetching_end = True
                break

            if start_time * 1000 <= comment["Timestamp"] <= end_time * 1000:
                if comment["Flags"] is not None \
                        and "Locked" in comment["Flags"] \
                        and "Reminder" in comment["Flags"] \
                        and comment not in warned_messages:
                    comment = copy.deepcopy(comment)
                    warned_messages.append(comment)
                    if warned_message_callback is not None:
                        warned_message_callback(comment)
                elif "警告" in comment["Content"] \
                        and comment["Verification"] in ("Volunteer", "Editor", "Emeritus", "Administrator"):
                    if maybe_warned_message_callback is not None:
                        maybe_warned_message_callback(comment)
        return comments[-1]["Timestamp"]

    if not isinstance(user, api.User) or \
            not isinstance(start_time, (int, float)) or \
            not isinstance(end_time, (int, float, type(None))) or \
            not isinstance(user_id, str) or \
            warned_message_callback is not None and not callable(warned_message_callback) or \
            maybe_warned_message_callback is not None and not callable(maybe_warned_message_callback):
        raise TypeError
    if user.is_anonymous:
        raise PermissionError("user must be anonymous")

    TAKE_MESSAGE_AMOUNT = 20
    warned_messages = []
    is_fetching_end = False

    if end_time is None:
        end_time = time.time()

    counter2 = 0
    fetch_end_time = int(end_time * 1000)
    while not is_fetching_end:
        fetch_end_time = _fetch_warned_messages(user_id, fetch_end_time)
        counter2 += 1

    return warned_messages

class CommentsIter:
    ''' 获取评论的迭代器 '''
    def __init__(self, user: api.User, id: str, category: str = "User") -> None:
        if not isinstance(user, api.User) or \
                not isinstance(id, str) or \
                not isinstance(category, str) and \
                category not in ("User", "Experiment", "Discussion"):
            raise TypeError
        if user.is_anonymous:
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

class RelationsIter:
    class _relate_user:
        def __init__(self, data: dict) -> None:
            self.data = data

        def __eq__(self, other):
            assert isinstance(other, RelationsIter._relate_user)

            return self.data["User"]["ID"] == other.data["User"]["ID"]

        def __hash__(self) -> int:
            return hash(self.data["User"]["ID"])

    def __init__(self, user: api.User, user_id: str, display_type: str = "Follower") -> None:
        self.user = user
        self.user_id = user_id
        self.display_type = display_type

    def wrapper(self,
                user_id: str,
                display_type: str = "Follower",
                skip: int = 0,
                take: int = 20,
                ):
        return skip, \
            self.user.get_relations(user_id, display_type, skip=skip, take=take)["Data"]["$values"]

    def __iter__(self):
        if self.display_type == "Follower":
            amount = self.user.get_user(self.user_id)['Data']['Statistic']['FollowerCount']
        elif self.display_type == "Following":
            amount = self.user.get_user(self.user_id)['Data']['Statistic']['FollowingCount']
        else:
            raise errors.InternalError

        cache = set()
        try_again = None
        with ThreadPoolExecutor(max_workers=150) as pool:
            tasks = [
                pool.submit(
                    self.wrapper, self.user_id, self.display_type, skip=i, take=20
                ) for i in range(0, amount + 1, 20)
            ]

            for task in as_completed(tasks):
                skip, results = task.result()

                if len(results) == 0:
                    if try_again is None or skip < try_again:
                        try_again = skip
                    continue

                for relation in results:
                    cache.add(self._relate_user(relation))
                    yield relation

            if try_again is not None:
                tasks2 = [
                    pool.submit(
                        self.user.get_relations, self.user_id, self.display_type, skip=i, take=20
                    ) for i in range(try_again - 20, try_again)
                ]
                for task2 in as_completed(tasks2):
                    results2 = task2.result()["Data"]["$values"]

                    for relation2 in results2:
                        if self._relate_user(relation2) in cache:
                            continue
                        cache.add(self._relate_user(relation2))
                        yield relation2

def get_avatars(search_id: str,
                category: str,
                size_category: str = "full",
                user: Optional[api.User] = None,
                ):
        ''' 获取一位用户的头像
            @param search_id: 用户id
            @param category: 只能为 "Experiment" 或 "Discussion" 或 "User"
            @param size_category: 只能为 "small.round" 或 "thumbnail" 或 "full"
            @param user: 查询者, None为匿名用户
        '''
        if not isinstance(search_id, str) or \
                not isinstance(category, str) or \
                not isinstance(size_category, str) or \
                not isinstance(user, (api.User, type(None))):
            raise TypeError
        if category not in ("User", "Experiment", "Discussion") or \
                size_category not in ("small.round", "thumbnail", "full"):
            raise ValueError

        if user is None:
            user = api.User()

        if category == "User":
            max_img_counter = user.get_user(search_id)["Data"]["User"]["Avatar"]
            category = "users"
        elif category == "Experiment":
            max_img_counter = user.get_summary(search_id, Category.Experiment)["Data"]["Image"]
            category = "experiments"
        elif category == "Discussion":
            max_img_counter = user.get_summary(search_id, Category.Discussion)["Data"]["Image"]
            category = "experiments"
        else:
            raise errors.InternalError

        with ThreadPoolExecutor(max_workers=150) as executor:
            tasks = [
                executor.submit(api.get_avatar, search_id, i, category, size_category)
                for i in range(max_img_counter + 1)
            ]

            for task in as_completed(tasks):
                try:
                    yield task.result()
                except (IndexError, TimeoutError,
                        urllib3.exceptions.NewConnectionError,
                        urllib3.exceptions.MaxRetryError,
                        urllib3.exceptions.ConnectionError,
                        ):
                    pass

class Bot:
    def __init__(self,
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
            process_callback: Optional[Callable],
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
