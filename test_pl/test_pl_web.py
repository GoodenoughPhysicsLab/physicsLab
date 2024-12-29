# -*- coding: utf-8 -*-
import inspect
import asyncio
import time
from .base import *
from physicsLab.web.api import User, get_start_page, Category, Tag, TestError

class _WebTest:
    # NOTE: 暴露token与auth_code是危险的行为，可能导致被盗号
    # 但 @AMDYES 主动暴露了自己的token与auth_code
    # 详见 <discussion=674ab7f4ce449cb493ced3a7>转让此号</discussion>
    user = User(
        token="yYReEg0oCtGlVmJqQwFr1zZXhL9NAvBH",
        auth_code="nENz1xlrueQUmkqjYZKtCG9SI53vF8Xc"
    )

    # 验证用户ID是否为测试用户
    if user.user_id != "5ce629e157035932b52f9315":
        raise TestError("User ID does not match")
    
    @staticmethod
    def check_test_res(res, api_name="API"):
        ''' 检查返回结果是否为字典，并验证状态码 '''
        if not isinstance(res, dict):
            raise TestError(f"{api_name} response is not a dict: {type(res)}")
        if "Status" not in res:
            raise TestError(f"{api_name} response has no 'Status' field")
        if res["Status"] != 200:
            raise TestError(f"{api_name} status is not 200: {res['Status']}")
    
    @staticmethod
    async def test_get_start_page():
        ''' 测试获取主页数据 '''
        res = await web.async_get_start_page()
        _WebTest.check_test_res(res, "get_start_page")
        
    @classmethod
    async def test_get_avatar(cls):
        ''' 测试获取头像 '''
        res = await cls.user.async_get_avatar(
            id="5ce629e157035932b52f9315",  # 用户ID
            index=0,  # 头像索引
            category="users",  # 用户头像
            size_category="small.round"  # 头像尺寸
        )
        assert isinstance(res, bytes), "返回值不是字节类型"

    @classmethod
    async def test_get_library(cls):
        ''' 测试获取社区作品列表 '''
        res = await cls.user.async_get_library()
        cls.check_test_res(res, "get_library")

    @classmethod
    async def test_query_experiments(cls):
        ''' 测试查询实验 '''
        res = await cls.user.async_query_experiments(
            tags=[Tag.Featured],  # 使用 Featured 标签
            category=Category.Experiment  # 实验区
        )
        cls.check_test_res(res, "query_experiments")

    @classmethod
    async def test_get_experiment(cls):
        ''' 测试获取实验数据 '''
        res = await cls.user.async_get_experiment(
            content_id="6317fabebfd18200013c710c",  # 实验区作品序列号
            category=Category.Experiment  # 实验区
        )
        cls.check_test_res(res, "get_experiment")

    @classmethod
    async def test_post_comment(cls):
        ''' 测试发表评论 '''
        res = await cls.user.async_post_comment(
            target_id="6317fabebfd18200013c710c",  # 实验区作品序列号
            target_type="Experiment",  # 目标类型为实验
            content="测试"  # 评论内容
        )
        cls.check_test_res(res, "post_comment")

    @classmethod
    async def test_remove_comment(cls):
        ''' 测试删除评论 '''
        # 先发表一条评论
        comment = await cls.user.async_post_comment(
            target_id="6317fabebfd18200013c710c",
            target_type="Experiment",
            content="测试"
        )
        # 删除评论
        res = await cls.user.async_remove_comment(
            CommentID=comment["Data"]["CommentID"],  # 评论ID
            target_type="Experiment"  # 目标类型为实验
        )
        cls.check_test_res(res, "remove_comment")

    @classmethod
    async def test_get_comments(cls):
        ''' 测试获取评论 '''
        res = await cls.user.async_get_comments(
            target_id="6317fabebfd18200013c710c",  # 实验区作品序列号
            target_type="Experiment"  # 目标类型为实验
        )
        cls.check_test_res(res, "get_comments")

    @classmethod
    async def test_get_summary(cls):
        ''' 测试获取实验介绍 '''
        res = await cls.user.async_get_summary(
            content_id="6317fabebfd18200013c710c",  # 实验区作品序列号
            category=Category.Experiment  # 实验区
        )
        cls.check_test_res(res, "get_summary")

    @classmethod
    async def test_get_derivatives(cls):
        ''' 测试获取作品详细信息 '''
        res = await cls.user.async_get_derivatives(
            content_id="6317fabebfd18200013c710c",  # 实验区作品序列号
            category=Category.Experiment  # 实验区
        )
        cls.check_test_res(res, "get_derivatives")

    @classmethod
    async def test_get_user(cls):
        ''' 测试获取用户信息 '''
        res = await cls.user.async_get_user(user_id="5ce629e157035932b52f9315")
        cls.check_test_res(res, "get_user")

    @classmethod
    async def test_get_profile(cls):
        ''' 测试获取用户个人资料 '''
        res = await cls.user.async_get_profile()
        cls.check_test_res(res, "get_profile")

    @classmethod
    async def test_star(cls):
        ''' 测试收藏实验 '''
        res = await cls.user.async_star(
            content_id="6317fabebfd18200013c710c",  # 实验区作品序列号
            category=Category.Experiment  # 实验区
        )
        cls.check_test_res(res, "star")

    @classmethod
    async def test_follow(cls):
        ''' 测试关注用户 '''
        res = await cls.user.async_follow(
            target_id="62d3fd092f3a2a60cc8ccc9e"  # 用户ID
        )
        cls.check_test_res(res, "follow")

    @classmethod
    async def test_rename(cls):
        ''' 测试修改用户昵称 '''
        res = await cls.user.async_rename(nickname="新昵称")
        cls.check_test_res(res, "rename")

    @classmethod
    async def test_modify_info(cls):
        ''' 测试修改用户签名 '''
        res = await cls.user.async_modify_info(target="新签名")
        cls.check_test_res(res, "modify_info")

    @classmethod
    async def test_receive_bonus(cls):
        ''' 测试领取每日签到奖励 '''
        res = await cls.user.async_receive_bonus()
        cls.check_test_res(res, "receive_bonus")

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

if __name__ == '__main__':
    unittest.main()
