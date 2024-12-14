from unittest import TestCase
from physicsLab import *

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

class PLTestBase(TestCase):
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
