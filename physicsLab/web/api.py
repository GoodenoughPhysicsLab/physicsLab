# -*- coding: utf-8 -*-
''' 该文件提供协程风格的api的封装
    所有以`async_`开头的函数/方法均为协程风格的api
'''
import sys
import asyncio
import functools
import contextvars
from ._api import get_avatar, get_start_page, _User
from physicsLab.enums import Tag, Category
from physicsLab._typing import Callable, Optional, List, Awaitable

# 从 threading._threading_atexits 中注销掉 furure._python_exit
# import types
# import threading
# from concurrent.futures import thread

# python3.14之前, threading.Thread.join 在 Windows 上会阻塞异常的传播
# 也就是说, 在join结束之前, Python无法及时抛出 KeyboardInterrupt
# 而 python 并未提供公开的方法操作 threading._threading_atexit
# 如果你确实被阻塞的问题困扰的话, 可以参考下面的代码讲 _python_exit 注销掉
# NOTE: 依赖于 asyncio 与 concurrent.futures.thread 的实现细节
# if sys.version_info < (3, 14) and hasattr(threading, "_threading_atexits"):
#     _threading_atexits = []
#     for fn in threading._threading_atexits:
#         if isinstance(fn, types.FunctionType) and fn is not thread._python_exit:
#             _threading_atexits.append(fn)
#         elif isinstance(fn, functools.partial) and fn.func is not thread._python_exit:
#             _threading_atexits.append(fn)
#     threading._threading_atexits = _threading_atexits

async def _async_wrapper(func: Callable, *args, **kwargs):
    if sys.version_info < (3, 9):
        # copied from asyncio.to_thread
        loop = asyncio.get_running_loop()
        ctx = contextvars.copy_context()
        func_call = functools.partial(ctx.run, func, *args, **kwargs)
        return await loop.run_in_executor(None, func_call)
    else:
        return await asyncio.to_thread(func, *args, **kwargs)

async def async_get_start_page() -> Awaitable[dict]:
    return await _async_wrapper(get_start_page)

async def async_get_avatar(target_id: str, index: int, category: str, size_category: str) -> Awaitable[dict]:
    return await _async_wrapper(get_avatar, target_id, index, category, size_category)

class User(_User):
    ''' 该class提供协程风格的api '''
    async def async_get_library(self) -> Awaitable[dict]:
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
    ) -> Awaitable[dict]:
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
    ) -> Awaitable[dict]:
        return await _async_wrapper(self.get_experiment, content_id, category)

    async def async_confirm_experiment(self, summary_id: str, category: Category, image_counter: int) -> Awaitable[dict]:
        return await _async_wrapper(self.confirm_experiment, summary_id, category, image_counter)

    async def async_remove_experiment(
            self,
            summary_id: str,
            category: Category,
            reason: Optional[str] = None,
    ) -> Awaitable[dict]:
        return await _async_wrapper(self.remove_experiment, summary_id, category, reason)

    async def async_post_comment(
            self,
            target_id: str,
            target_type: str,
            content: str,
            reply_id: Optional[str] = None,
    ) -> Awaitable[dict]:
        return await _async_wrapper(self.post_comment, target_id, target_type, content, reply_id)

    async def async_remove_comment(self, comment_id: str, target_type:str) -> Awaitable[dict]:
        return await _async_wrapper(self.remove_comment, comment_id, target_type)

    async def async_get_comments(
            self,
            target_id: str,
            target_type: str,
            take: int = 16,
            skip: int = 0,
            comment_id: Optional[str] = None,
    ) -> Awaitable[dict]:
        return await _async_wrapper(self.get_comments, target_id, target_type, take, skip, comment_id)

    async def async_get_summary(self, content_id: str, category: Category) -> Awaitable[dict]:
        return await _async_wrapper(self.get_summary, content_id, category)

    async def async_get_derivatives(self, content_id: str, category: Category) -> Awaitable[dict]:
        return await _async_wrapper(self.get_derivatives, content_id, category)

    async def async_get_user(
            self,
            user_id: Optional[str] = None,
            name: Optional[str] = None,
    ) -> Awaitable[dict]:
        return await _async_wrapper(self.get_user, user_id, name)

    async def async_get_profile(self) -> Awaitable[dict]:
        return await _async_wrapper(self.get_profile)

    async def async_star_content(
            self,
            content_id: str,
            category: Category,
            star_type: int,
            status: bool = True,
    ) -> Awaitable[dict]:
        return await _async_wrapper(self.star_content, content_id, category, star_type, status)

    async def async_upload_image(self, policy: str, authorization: str, image_path: str) -> Awaitable[dict]:
        return await _async_wrapper(self.upload_image, policy, authorization, image_path)

    async def async_get_message(self, message_id: str) -> Awaitable[dict]:
        return await _async_wrapper(self.get_message, message_id)

    async def async_get_messages(
            self,
            category_id: int,
            skip: int = 0,
            take: int = 16,
            no_templates: bool = True,
    ) -> Awaitable[dict]:
        return await _async_wrapper(self.get_messages, category_id, skip, take, no_templates)

    async def async_get_supporters(
            self,
            content_id: str,
            category: Category,
            skip: int = 0,
            take: int = 16,
    ) -> Awaitable[dict]:
        return await _async_wrapper(self.get_supporters, content_id, category, skip, take)

    async def async_get_relations(
            self,
            user_id: str,
            display_type: str = "Follower",
            skip: int = 0,
            take: int = 20,
            query: str = "",
    ) -> Awaitable[dict]:
        return await _async_wrapper(self.get_relations, user_id, display_type, skip, take, query)

    async def async_follow(self, target_id: str, action: bool = True) -> Awaitable[dict]:
        return await _async_wrapper(self.follow, target_id, action)

    async def async_rename(self, nickname: str) -> Awaitable[dict]:
        return await _async_wrapper(self.rename, nickname)

    async def async_modify_information(self, target: str) -> Awaitable[dict]:
        return await _async_wrapper(self.modify_information, target)

    async def async_receive_bonus(self, activity_id: str, index: int) -> Awaitable[dict]:
        return await _async_wrapper(self.receive_bonus, activity_id, index)
