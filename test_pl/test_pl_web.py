# -*- coding: utf-8 -*-
import inspect
import asyncio
import time
from .base import *

class _WebTest:
    # NOTE: 暴露token与auth_code是危险的行为，可能导致被盗号
    # 但 @AMDYES 主动暴露了自己的token与auth_code
    # 详见 <discussion=674ab7f4ce449cb493ced3a7>转让此号</discussion>
    user = web.User(
        token="yYReEg0oCtGlVmJqQwFr1zZXhL9NAvBH",
        auth_code="nENz1xlrueQUmkqjYZKtCG9SI53vF8Xc"
    )

    # 验证用户ID是否为测试用户
    if user.user_id != "5ce629e157035932b52f9315":
        raise TestError("User ID does not match")
    
    @staticmethod
    async def test_get_start_page():
        ''' 测试获取主页数据 '''
        await web.async_get_start_page()
        
    @staticmethod
    async def test_get_avatar():
        ''' 测试获取头像 '''
        await web.async_get_avatar(
            target_id="5ce629e157035932b52f9315",  # 用户ID
            index=1,  # 头像索引
            category="users",  # 用户头像
            size_category="small.round"  # 头像尺寸
        )

    @classmethod
    async def test_get_library(cls):
        ''' 测试获取社区作品列表 '''
        await cls.user.async_get_library()

    @classmethod
    async def test_query_experiments(cls):
        ''' 测试查询实验 '''
        await cls.user.async_query_experiments(
            tags=[Tag.Featured],  # 精选标签
            category=Category.Experiment  # 实验区
        )

    @classmethod
    async def test_get_experiment(cls):
        ''' 测试获取实验数据 '''
        await cls.user.async_get_experiment(
            content_id="6317fabebfd18200013c710c",  # 作品序列号
            category=Category.Experiment
        )

    @classmethod
    async def test_get_comments(cls):
        ''' 测试获取评论 '''
        await cls.user.async_get_comments(
            target_id="6317fabebfd18200013c710c",
            target_type="Experiment"  # 目标类型为实验
        )

    @classmethod
    async def test_get_summary(cls):
        ''' 测试获取实验介绍 '''
        await cls.user.async_get_summary(
            content_id="6317fabebfd18200013c710c",
            category=Category.Experiment
        )

    @classmethod
    async def test_get_derivatives(cls):
        ''' 测试获取作品详细信息 '''
        await cls.user.async_get_derivatives(
            content_id="6317fabebfd18200013c710c",
            category=Category.Experiment
        )

    @classmethod
    async def test_get_user(cls):
        ''' 测试获取用户信息 '''
        await cls.user.async_get_user(user_id="5ce629e157035932b52f9315")

    @classmethod
    async def test_get_profile(cls):
        ''' 测试获取用户个人资料 '''
        await cls.user.async_get_profile()

async def test_web_main():
    ''' 收集并运行所有测试任务 '''
    test_tasks = []
    for _, a_test_task in inspect.getmembers(_WebTest, inspect.iscoroutinefunction):
        test_tasks.append(a_test_task)
    await asyncio.gather(*[a_test() for a_test in test_tasks])

class WebTest(TestCase, ViztracerTool):
    @staticmethod
    def test_web_impl():
        ''' 运行所有测试并记录耗时 '''
        start = time.time()
        asyncio.run(test_web_main())
        end = time.time()
        print(f"{WebTest.test_web_impl.__name__} takes {end - start}", end='')

