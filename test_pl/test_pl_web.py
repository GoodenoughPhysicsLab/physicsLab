# -*- coding: utf-8 -*-
import inspect
import asyncio
import time
from .base import *

class _WebTest:
    # NOTE: 暴露token与auth_code是危险的行为
    # 但 @AMDYES 主动暴露了自己的token与auth_code
    # 详见 <discussion=674ab7f4ce449cb493ced3a7>转让此号</discussion>
    user = web.User(
        token="yYReEg0oCtGlVmJqQwFr1zZXhL9NAvBH",
        auth_code="nENz1xlrueQUmkqjYZKtCG9SI53vF8Xc"
    )

    if user.user_id != "5ce629e157035932b52f9315":
        raise TestError

    @staticmethod
    async def test_get_start_page():
        await web.async_get_start_page()

    @classmethod
    async def test_get_library(cls):
        await cls.user.async_get_library()

    @classmethod
    async def test_query_experiments(cls):
        await cls.user.async_query_experiments()

    @classmethod
    async def test_get_experiment(cls):
        await cls.user.async_get_experiment("642cf37a494746375aae306a", Category.Discussion)

async def test_web_main():
    test_tasks = []
    for _, a_test_task in inspect.getmembers(_WebTest, inspect.iscoroutinefunction):
        test_tasks.append(a_test_task)
    await asyncio.gather(*[a_test() for a_test in test_tasks])

class WebTest(TestCase, ViztracerTool):
    @staticmethod
    def test_web_impl():
        start = time.time()
        asyncio.run(test_web_main())
        end = time.time()
        print(f"{WebTest.test_web_impl.__name__} takes {end - start}", end='')
