# -*- coding: utf-8 -*-
import copy
import time

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
                except IndexError:
                    pass

class Bot:
    ''' 初始化 Bot 类的实例

        @param username: 机器人的用户名
        @param password: 机器人的密码
        @param process_fn: 处理函数，用于处理捕获到的消息
        @param catched: 当捕获到新消息时调用的函数
        @param replyed: 当回复消息时调用的函数
        @param finnished: 当所有消息处理完成时调用的函数
    '''
    def __init__(self,
                user: api.User,
                process_fn: Callable,
                catched: Callable,
                replyed: Callable,
                finnished: Callable,
                ) -> None:
        ''' @param user: 机器人要绑定的用户账号
        '''
        if not isinstance(user, api.User):
            raise TypeError

        # 生命周期 捕获－处理－回复－记录[－完成]
        self.user = user
        # self.username = username
        # self.password = password
        self.process_fn = process_fn
        self.catched = catched
        self.replyed = replyed
        self.pending = set()
        self.finnish = set()
        self.finnished = finnished
        self.reply_config = {
            "ignoreReplyToOters": True, # 如果出现回复@{非Bot的用户}，则忽略
            "readHistory": True, # 捕获Bot启动前的消息（最多20条）
            "replyRequired": True, # 只捕获回复@{Bot}的消息
        }

    ''' 初始化

        @param ID: (str) 序列号
        @param type: (str) Discusion 或 Experiment
        @param reply_config: (dict, 可选) 回复配置，包含不同的选项来控制机器人行为。
            - ignoreReplyToOters: (bool) 是否忽略对其他用户的回复。
            - readHistory: (bool) 是否读取历史消息。
            - replyRequired: (bool) 是否需要回复用户的消息。
    '''
    def setConfig(self, ID: str, type: str, reply_config=None) -> None:
        if reply_config is None:
            reply_config = {}

        # super().__login(self, self.username, self.password)
        self.bot_id = self.user.user_id
        self.target_id = ID
        self.target_type = type

        # 合并默认配置和传入配置
        self.reply_config.update(reply_config)

        data = self.user.get_comments(self.target_id, self.target_type, 20)  # 假设 messages 是一个已定义的属性
        if self.reply_config['readHistory']:
            index = ""
            msglist = data['Data']['Comments'][::-1]  # 试图反转列表
            for comment in msglist:
                if comment['UserID'] == self.bot_id:
                    index = comment['ID']
            self.start_index = index
        else:
            self.start_index = data['Data']['Comments'][0]['ID'] if data['Data']['Comments'] else ""

    def run(self):
        re = self.user.get_comments(self.target_id, self.target_type, 20)
        for comment in re['Data']['Comments']:
            if comment['ID'] == self.start_index:
                break
            if comment['UserID'] == self.bot_id:
                continue
            if comment['ID'] in self.pending or comment['ID'] in self.finnish:
                continue
            if ("回复<" in comment['Content'] and
                self.reply_config['ignoreReplyToOters'] and
                self.bot_id not in comment['Content']):
                continue
            if (self.bot_id not in comment['Content'] and
                self.reply_config['replyRequired']):
                continue

            self.catched(comment)
            self.pending.add(comment['ID'])
            reply = self.process_fn(comment, self)
            if reply == "":
                continue

            msg = f"回复@{comment['Nickname']}: {reply}"
            self.user.post_comment(self.target_id, msg, self.target_type)
            self.finnish.add(comment['ID'])
            self.pending.remove(comment['ID'])
            if not self.pending:
                self.finnished(self.finnish)
            self.replyed({**{"msg": msg}, **comment})
