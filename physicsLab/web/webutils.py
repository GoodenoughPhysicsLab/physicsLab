# -*- coding: utf-8 -*-
import os
import copy
import time
import threading

from physicsLab import web
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from physicsLab.typehint import Optional, Callable, numType
from . import api

def get_banned_messages(user: api.User,
               start_time: numType,
               user_id: Optional[str] = None,
               end_time: Optional[numType] = None,
               banned_message_callback: Optional[Callable] = None,
               ) -> list:
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

    if not isinstance(user, api.User) or \
            not isinstance(start_time, (int, float)) or \
            not isinstance(end_time, (int, float, type(None))) or \
            not isinstance(user_id, (str, type(None))):
        raise TypeError

    banned_messages = []
    is_fetching_end: bool = False

    if end_time is None:
        end_time = time.time()

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
                    user, start_time, end_time, user_id, i + counter * FETCH_AMOUNT,
                    banned_template
                )
        counter += 1
    return banned_messages

def get_warned_messages(user: api.User,
                       start_time: numType,
                       user_id: str,
                       end_time: Optional[numType] = None,
                       warned_message_callback: Optional[Callable] = None,
                       maybe_warned_message_callback: Optional[Callable] = None,
                       ) -> list:
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
                elif "警告" in comment["Content"]: # TODO 判断执行者是否是管理人员
                    if maybe_warned_message_callback is not None:
                        maybe_warned_message_callback(comment)
        return comments[-1]["Timestamp"]

    if not isinstance(user, api.User) or \
            not isinstance(start_time, (int, float)) or \
            not isinstance(end_time, (int, float, type(None))) or \
            not isinstance(user_id, str):
        raise TypeError

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