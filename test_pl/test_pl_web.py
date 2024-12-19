# -*- coding: utf-8 -*-
from .base import *

class WebTest(PLTestBase):
    def setUp(self) -> None: # test_login
        # NOTE: 暴露token与auth_code是危险的行为
        # 但 @AMDYES 主动暴露了自己的token与auth_code
        # 详见 <discussion=674ab7f4ce449cb493ced3a7>转让此号</discussion>
        self.user = web.User(
            token="yYReEg0oCtGlVmJqQwFr1zZXhL9NAvBH",
            auth_code="nENz1xlrueQUmkqjYZKtCG9SI53vF8Xc"
        )

    # TODO: 异步跑这些测试
    def test_get_start_page(self):
        web.get_start_page()

    def test_get_library(self):
        self.user.get_library()

    def test_query_experiments(self):
        self.user.query_experiments()

    def test_get_experiment(self):
        self.user.get_experiment("642cf37a494746375aae306a", Category.Discussion)
