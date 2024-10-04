# -*- coding: utf-8 -*-
import copy
import time

from . import api
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
            not isinstance(user_id, (str, type(None))):
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
            not isinstance(user_id, str):
        raise TypeError
    if user.is_anonymous:
        raise ValueError("user must be anonymous")

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
            raise ValueError("user must be anonymous")

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

def get_avatars(id: str,
                category: str,
                size_category: str,
                user: Optional[api.User] = None,
                ) -> list:
        if not isinstance(id, str) or \
                not isinstance(category, str) or \
                not isinstance(size_category, str) or \
                not isinstance(user, (api.User, type(None))):
            raise TypeError

        if user is None:
            user = api.User()

        res: list = []

        with ThreadPoolExecutor(max_workers=150) as executor:
            tasks = [
                executor.submit(api.get_avatars, id, i + 1, category, size_category)
                for i in range(user.get_user(id)["Data"]["User"]["Avatar"])
            ]

            for task in as_completed(tasks):
                try:
                    res.append(task.result())
                except IndexError:
                    pass
        return res

class Bot(api.User):
    '''
    初始化 Bot 类的实例。

    @param username: 机器人的用户名
    @param password: 机器人的密码
    @param process_fn: 处理函数，用于处理捕获到的消息
    @param catched: 当捕获到新消息时调用的函数
    @param replyed: 当回复消息时调用的函数
    @param finnished: 当所有消息处理完成时调用的函数
    @return: None
    '''
    def __init__(self, 
                username: str, 
                password: str, 
                process_fn: callable, 
                catched: callable, 
                replyed: callable, 
                finnished: callable
                ):
        super().__init__(self, username, password)
        # 生命周期 捕获－处理－回复－记录[－完成]
        self.username = username
        self.password = password
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

    '''
    初始化

    @param ID: (str) 序列号
    @param type: (str) Discusion 或 Experiment
    @param reply_config: (dict, 可选) 回复配置，包含不同的选项来控制机器人行为。
        - ignoreReplyToOters: (bool) 是否忽略对其他用户的回复。
        - readHistory: (bool) 是否读取历史消息。
        - replyRequired: (bool) 是否需要回复用户的消息。

    @return: None - 此方法不返回任何内容，主要用于初始化状态和配置。
    '''
    async def setConfig(self, ID: str, type: str, reply_config=None):
        if reply_config is None:
            reply_config = {}
        
        await super().__login(self, self.username, self.password) 
        self.bot_id = self.user_id
        self.target_id = ID
        self.target_type = type
        
        # 合并默认配置和传入配置
        self.reply_config.update(reply_config)
        
        data = await self.get_comments(self, self.target_id, self.target_type, 20)  # 假设 messages 是一个已定义的属性
        if self.reply_config['readHistory']:
            index = ""
            msglist = data['Data']['Comments'][::-1]  # 试图反转列表
            for comment in msglist:
                if comment['UserID'] == self.bot_id:
                    index = comment['ID']
            self.start_index = index
        else:
            self.start_index = data['Data']['Comments'][0]['ID'] if data['Data']['Comments'] else ""

    async def run(self):
        re = await self.get_comments(self, self.target_id, self.target_type, 20)
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
            
            await self.catched(comment)
            self.pending.add(comment['ID'])
            reply = await self.process_fn(comment, self)
            if reply == "":
                continue
            
            msg = f"回复@{comment['Nickname']}: {reply}"
            await self.post_comment(self, self.target_id, msg, self.target_type) 
            self.finnish.add(comment['ID'])
            self.pending.remove(comment['ID'])
            if not self.pending:
                await self.finnished(self.finnish)
            await self.replyed({**{"msg": msg}, **comment})