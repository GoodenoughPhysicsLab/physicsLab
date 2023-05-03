#coding=utf-8
import unittest
from physicsLab import *
from viztracer import VizTracer

class myTestCase(unittest.TestCase):
    # init unittest class
    # @classmethod
    # def setUpClass(cls):
    #     tracer = VizTracer()
    #     tracer.start()
    #
    #     cls.tracer = tracer
    #
    # @classmethod
    # def tearDownClass(cls):
    #     tracer = cls.tracer
    #     tracer.stop()
    #     tracer.save() # also takes output_file as an optional argument

    
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
        crt_Element('Logic Input')
        self.assertEqual(count_Elements(), 2)
        get_Element(0, 0, 0)
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

    def test_crt_Experiment(self):
        try:
            crt_Experiment("test")
            crt_Experiment("test")
        except experimentExistError:
            pass

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
        with experiment('test'):
            Logic_Input()
        write_Experiment()
        self.assertEqual(1, count_Elements())
        del_Experiment()

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

    # 测逝模块化电路连接导线
    def test_wires(self):
        with experiment('测逝', elementXYZ=True):
            a = union_Inputs(0, 0, 0, 8)
            b = union_Outputs(0.6, 0, 0, 8, elementXYZ=False)
            Logic_Output(0.6, 0, 0.1, elementXYZ=False)
            c = d_WaterLamp(1, 0, 0, bitLength=8)
            crt_Wires(b.data_Input, c.data_Output)
            self.assertEqual(25, count_Elements())
            self.assertEqual(23, count_Wires())
            del_Wires(c.data_Output, b.data_Input)
            self.assertEqual(15, count_Wires())

    # 测逝模块化加法电路
    def test_union_Sum(self):
        with experiment('测逝', elementXYZ=True):
            a = union_Inputs(-1, 0, 0, 8)
            b = union_Inputs(-2, 0, 0, 8)
            c = union_Sum(0, 0, 0, 8)
            d = union_Outputs(1, 0, 0, 8)
            a.data_Output - c.data_Input1
            b.data_Output - c.data_Input2
            c.data_Output - d.data_Input

    # 测试打开实验类型与文件不吻合
    def test_experimentType(self):
        crt_Experiment("__test__测逝电与磁", type="电与磁实验")
        try:
            Logic_Input()
        except experimentTypeError:
            pass
        write_Experiment()
        del_Experiment()

    def test_experimentType2(self):
        try:
            with experiment(file='电与磁', elementXYZ=True):
                Logic_Input()

            with experiment("电与磁测逝", type="电与磁实验", elementXYZ=True):
                pass
        except experimentTypeError:
            pass

    def test_experimentType3(self):
        with experiment("__tset__", type=0, delete=True):
            Logic_Input()
        with experiment("__test__", type=3, delete=True):
            pass
        with experiment("__test__", type=4, delete=True):
            pass
        with experiment("__test__", type="天体物理实验", delete=True):
            pass
        with experiment("__test__", type="电与磁实验", delete=True):
            pass

if __name__ == '__main__':
    unittest.main()