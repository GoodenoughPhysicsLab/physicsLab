#coding=utf-8
import unittest
from physicsLab import *
from viztracer import VizTracer

class MyTestCase(unittest.TestCase):
    # init unittest class
    @classmethod
    def setUpClass(cls):
        tracer = VizTracer()
        cls.tracer = tracer
        tracer.start()

    @classmethod
    def tearDownClass(cls):
        tracer = cls.tracer
        tracer.stop()
        tracer.save() # also takes output_file as an optional argument

    
    #-#-#-#-#

    def test_experiment1(self):
        open_Experiment('测逝')
        a = Yes_Gate()
        self.assertEqual(count_Elements(), 1)
        self.assertEqual(a.get_Position(), (0, 0, 0))
        crt_Wire(a.o, a.i)
        self.assertEqual(count_Wires(), 1)
        clear_Wires()
        self.assertEqual(count_Wires(), 0)
        self.assertEqual(count_Elements(), 1)
        write_Experiment()
        crt_Wire(a.o, a.i)
        write_Experiment()

    def test_read_Experiment(self):
        open_Experiment('测逝')
        write_Experiment()

        open_Experiment('测逝')
        self.assertEqual(count_Elements(), 0)
        self.assertEqual(count_Wires(), 0)
        Logic_Input()
        write_Experiment()

        open_Experiment('测逝')
        read_Experiment()
        self.assertEqual(count_Elements(), 1)

    def test_union_Sum(self):
        open_Experiment('测逝')
        union_Sum(0, -1, 0, 64)
        self.assertEqual(count_Elements(), 64)
        self.assertEqual(count_Wires(), 63)
        write_Experiment()
        clear_Elements()
        self.assertEqual(count_Wires(), 0)
        self.assertEqual(count_Elements(), 0)

    def test_get_Element(self):
        open_Experiment('测逝')
        Or_Gate(0, 0, 0)
        crt_Wire(
            get_Element(x=0, y=0, z=0).o,
            get_Element(1).i_up
        )
        crt_Wire(get_Element(0,0,0).i_low, get_Element(index=1).o)
        self.assertEqual(count_Wires(), 2)
        write_Experiment()

    # 测逝用例未写完
    def test_set_O(self):
        open_Experiment('测逝')
        set_O(-1, -1, 0)
        for x in range(10):
            for y in range(10):
                Yes_Gate(x, y, 0, True)
        self.assertEqual(count_Elements(), 100)
        write_Experiment()

    def test_errors(self):
        try:
            open_Experiment('blabla')
        except errors.openExperimentError:
            pass
        else:
            raise RuntimeError

    # 测试元件坐标系2
    def test_aTest(self):
        open_Experiment('测逝')
        set_elementXYZ(True)
        set_O(-1, -1, 0)
        for x in range(10):
            for y in range(10):
                Yes_Gate(x, y, 0)
        for x in range(10):
            for y in [y * 2 + 10 for y in range(5)]:
                Multiplier(x, y, 0)

        crt_Wire(get_Element(1).o, get_Element(0, 1, 0).i)
        get_Element(2).i - get_Element(3).o - get_Element(4).i
        self.assertEqual(count_Wires(), 3)
        self.assertEqual(count_Elements(), 150)
        write_Experiment()

    def test_open_many_Experiment(self):
        open_Experiment('测逝')
        open_Experiment('test')
        Logic_Input()
        write_Experiment()

    def test_with_and_coverPosition(self):
        with experiment('测逝'):
            Logic_Input()
            Or_Gate()
            self.assertEqual(len(get_Element(0, 0, 0)), 2)

    def test_del_Element(self):
        with experiment('测逝'):
            Logic_Input()
            Or_Gate()
            del_Element(get_Element(2))
            self.assertEqual(count_Elements(), 1)

if __name__ == '__main__':
    unittest.main()