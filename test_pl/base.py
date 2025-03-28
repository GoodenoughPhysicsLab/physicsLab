import os
from unittest import TestCase, IsolatedAsyncioTestCase
from physicsLab import *

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(TEST_DIR, "data")

USE_VIZTRACER: bool = False

if USE_VIZTRACER:
    from viztracer import VizTracer

class TestFail(Exception):
    def __init__(self, err_msg: str = "Test fail", no_pop: bool=False) -> None:
        self.err_msg: str = err_msg
        self.no_pop = no_pop

    def __str__(self) -> str:
        if not self.no_pop:
            get_current_experiment().close()
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

# this is a temp user without any binding
user = web.token_login(
    token="tGTf8gbQBR9P0ZnWhSILjJ5oF6UOkVdm",
    auth_code="xJwcHC7oOnlSdzUTh9NDZ0t1Q32MjPyB",
)
