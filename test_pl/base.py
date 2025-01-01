import os
from unittest import TestCase
from physicsLab import *

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(TEST_DIR, "data")

USE_VIZTRACER: bool = False

if USE_VIZTRACER:
    from viztracer import VizTracer

class TestError(Exception):
    def __init__(self, err_msg: str = "Test fail", no_pop: bool=False) -> None:
        self.err_msg: str = err_msg
        self.no_pop = no_pop

    def __str__(self) -> str:
        if not self.no_pop:
            get_current_experiment().exit()
        return self.err_msg

class ViztracerTool:
    if USE_VIZTRACER:
        @classmethod
        def setUpClass(cls):
            tracer = VizTracer()
            tracer.start()

            cls.tracer = tracer

        @classmethod
        def tearDownClass(cls):
            tracer = cls.tracer
            tracer.stop()
            tracer.save() # also takes output_file as an optional argument

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
