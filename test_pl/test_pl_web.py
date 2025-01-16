# -*- coding: utf-8 -*-
import inspect
import asyncio
import time
from datetime import datetime
from .base import *

class WebTest(IsolatedAsyncioTestCase, ViztracerTool):
    @staticmethod
    async def test_get_start_page():
        await web.async_get_start_page()

    async def test_get_avatar(self):
        await web.async_get_avatar(
            target_id="5ce629e157035932b52f9315",  # 用户ID
            index=1,  # 头像索引
            category="users",  # 用户头像
            size_category="small.round"  # 头像尺寸
        )

    async def test_get_library(self):
        await user.async_get_library()

    async def test_query_experiments(self):
        await user.async_query_experiments(
            tags=[Tag.Featured],  # 精选标签
            category=Category.Experiment  # 实验区
        )

    async def test_get_experiment(self):
        await user.async_get_experiment(
            content_id="6317fabebfd18200013c710c",  # 作品序列号
            category=Category.Experiment
        )

    async def test_get_comments(self):
        await user.async_get_comments(
            target_id="6317fabebfd18200013c710c",
            target_type="Experiment"  # 目标类型为实验
        )

    async def test_get_summary(self):
        await user.async_get_summary(
            content_id="6317fabebfd18200013c710c",
            category=Category.Experiment
        )

    async def test_get_derivatives(self):
        await user.async_get_derivatives(
            content_id="6317fabebfd18200013c710c",
            category=Category.Experiment
        )

    async def test_get_user(self):
        await user.async_get_user(user_id="5ce629e157035932b52f9315")

    async def test_get_profile(self):
        await user.async_get_profile()

    async def test_notifications_msg_iter(self):
        counter = 0
        for _ in web.NotificationsMsgIter(
                datetime(2025, 1, 1).timestamp(), datetime(2025, 1, 2).timestamp(),
                user=user, max_retry=4, category_id=5
        ):
            counter += 1
        self.assertEqual(counter, 96)

    async def test_banned_msg_iter(self):
        counter = 0
        for _ in web.BannedMsgIter(
            datetime(2025, 1, 1).timestamp(), datetime(2025, 1, 16).timestamp(),
            user=user, max_retry=4
        ):
            counter += 1
        self.assertEqual(counter, 1)
