# -*- coding: utf-8 -*-
import unittest
from physicsLab import *
from physicsLab.unit import *
from physicsLab.experiment import stack_Experiment

import format_coding_style as fcs

USE_VIZTRACER: bool = False

if USE_VIZTRACER:
    from viztracer import VizTracer

class TestError(Exception):
    def __init__(self, no_pop: bool=False) -> None:
        self.no_pop = no_pop

    def __str__(self) -> str:
        if not self.no_pop:
            exit_Experiment()
        return "Test Fail"

def my_test_dec(method: Callable):
    def result(*args, **kwarg):
        method(*args, **kwarg)

        if len(stack_Experiment.data) != 0:
            print(f"method \"{method.__code__.co_name}\"({method.__code__.co_firstlineno}) test fail due to len(stack_Experiment) != 0")
            raise TestError
    return result

class MyTestCase(unittest.TestCase):
    # init unittest class
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

    @my_test_dec
    def test_experiment1(self):
        exp: Experiment = Experiment().crt("__test__", force_crt=True)
        a = Yes_Gate()
        self.assertEqual(count_Elements(), 1)
        self.assertEqual(a.get_Position(), (0, 0, 0))
        crt_Wire(a.o, a.i)
        self.assertEqual(count_Wires(), 1)
        clear_Wires()
        self.assertEqual(count_Wires(), 0)
        self.assertEqual(count_Elements(), 1)
        crt_Wire(a.o, a.i)
        crt_Element('Logic Input')
        self.assertEqual(count_Elements(), 2)
        get_Element(0, 0, 0)
        exp.exit()

    @my_test_dec
    def test_read_Experiment(self):
        exp: Experiment = Experiment().crt("__test__", force_crt=True)

        self.assertEqual(count_Elements(), 0)
        self.assertEqual(count_Wires(), 0)
        Logic_Input()
        exp.write()

        exp2: Experiment = Experiment().open("__test__")
        exp2.read()
        self.assertEqual(count_Elements(), 1)
        exp2.delete()

    @my_test_dec
    def test_crt_Experiment(self):
        try:
            exp: Experiment = Experiment().crt("__test__", force_crt=True)
            exp.write()
            Experiment().crt("__test__") # will fail
        except crtExperimentFailError:
            Experiment("__test__").delete()
        else:
            raise TestError

    @my_test_dec
    def test_crt_wire(self):
        with experiment("__test__", is_exit=True, force_crt=True):
            a = Or_Gate()
            crt_Wire(a.o, a.i_up, "red")
            self.assertEqual(count_Wires(), 1)

            del_Wire(a.o, a.i_up)
            self.assertEqual(count_Wires(), 0)
    
    def test_same_crt_wire(self):
        with experiment("__test__", is_exit=True, force_crt=True):
            a = Or_Gate()
            crt_Wire(a.o, a.i_up, "red")
            crt_Wire(a.i_up, a.o, "blue")
            self.assertEqual(count_Wires(), 1)

    @my_test_dec
    def test_union_Sum(self):
        exp: Experiment = Experiment().crt("__test__", force_crt=True)
        unit.Sum(0, -1, 0, 64)
        self.assertEqual(count_Elements(), 64)
        self.assertEqual(count_Wires(), 63)
        clear_Elements()
        self.assertEqual(count_Wires(), 0)
        self.assertEqual(count_Elements(), 0)
        exp.exit()

    @my_test_dec
    def test_get_Element(self):
        exp: Experiment = Experiment().crt("__test__", force_crt=True)
        Or_Gate(0, 0, 0)
        crt_Wire(
            get_Element(0, 0, 0).o,
            get_Element(index=1).i_up
        )
        crt_Wire(get_Element(0,0,0).i_low, get_Element(index=1).o)
        self.assertEqual(count_Wires(), 2)
        exp.exit()

    # 测逝用例未写完
    @my_test_dec
    def test_set_O(self):
        exp: Experiment = Experiment().crt("__test__", force_crt=True)
        set_O(-1, -1, 0)
        for x in range(10):
            for y in range(10):
                Yes_Gate(x, y, 0, True)
        self.assertEqual(count_Elements(), 100)
        exp.exit()

    @my_test_dec
    def test_errors(self):
        try:
            with experiment("__test__", delete=True, force_crt=True):
                pass
            Experiment().open('__test__') # do not exist
        except OpenExperimentError:
            pass
        else:
            raise TestError

    # 测试元件坐标系2
    @my_test_dec
    def test_aTest(self):
        exp: Experiment = Experiment().crt("__test__", force_crt=True)
        set_elementXYZ(True)
        set_O(-1, -1, 0)
        for x in range(10):
            for y in range(10):
                Yes_Gate(x, y, 0)
        for x in range(10):
            for y in [y * 2 + 10 for y in range(5)]:
                Multiplier(x, y, 0)

        crt_Wire(get_Element(index=1).o, get_Element(0, 1, 0).i)
        get_Element(index=2).i - get_Element(index=3).o - get_Element(index=4).i
        self.assertEqual(count_Wires(), 3)
        self.assertEqual(count_Elements(), 150)
        exp.exit()

    @my_test_dec
    def test_open_many_Experiment(self):
        exp: Experiment = Experiment().crt("__test__", force_crt=True)
        with experiment('__test__', is_exit=True, force_crt=True):
            Logic_Input()
            self.assertEqual(1, count_Elements())
        exp.exit()

    @my_test_dec
    def test_with_and_coverPosition(self):
        with experiment("__test__", is_exit=True, force_crt=True):
            Logic_Input()
            Or_Gate()
            self.assertEqual(len(get_Element(0, 0, 0)), 2)

    @my_test_dec
    def test_del_Element(self):
        with experiment("__test__", is_exit=True, force_crt=True):
            Logic_Input().o - Or_Gate().o
            del_Element(get_Element(index=2))
            self.assertEqual(count_Elements(), 1)
            self.assertEqual(count_Wires(), 0)

    # 测逝模块化电路连接导线
    @my_test_dec
    def test_wires(self):
        with experiment("__test__", is_exit=True, elementXYZ=True, force_crt=True):
            a = unit.Inputs(0, 0, 0, 8)
            b = unit.Outputs(0.6, 0, 0, 8, elementXYZ=False)
            Logic_Output(0.6, 0, 0.1, elementXYZ=False)
            c = unit.D_WaterLamp(1, 0, 0, bitLength=8)
            crt_Wires(b.data_Input, c.data_Output)
            self.assertEqual(25, count_Elements())
            self.assertEqual(23, count_Wires())
            del_Wires(c.data_Output, b.data_Input)
            self.assertEqual(15, count_Wires())

    # 测逝模块化加法电路
    @my_test_dec
    def test_union_Sum2(self):
        with experiment("__test__", is_exit=True, elementXYZ=True, force_crt=True):
            a = unit.Inputs(-1, 0, 0, 8)
            b = unit.Inputs(-2, 0, 0, 8)
            c = unit.Sum(0, 0, 0, 8)
            d = unit.Outputs(1, 0, 0, 8)
            a.data_Output - c.data_Input1
            b.data_Output - c.data_Input2
            c.data_Output - d.data_Input

    # 测试打开实验类型与文件不吻合
    @my_test_dec
    def test_experimentType(self):
        with experiment("__test__", experiment_type=experimentType.Electromagnetism, is_exit=True, force_crt=True):
            try:
                Positive_Charge()
                Logic_Input()
            except ExperimentTypeError:
                pass
            else:
                raise TestError

    @my_test_dec
    def test_experimentType3(self):
        with experiment("__test__", experiment_type=experimentType.Circuit, is_exit=True, force_crt=True):
            Logic_Input()
        with experiment("__test__", experiment_type=experimentType.Celestial, is_exit=True, force_crt=True):
            pass
        with experiment("__test__", experiment_type=experimentType.Electromagnetism, is_exit=True, force_crt=True):
            pass

    @my_test_dec
    def test_electromagnetism(self):
        with experiment("__test__", is_exit=True, experiment_type=experimentType.Electromagnetism, force_crt=True):
            Negative_Charge(-0.1, 0, 0)
            Positive_Charge(0.1, 0, 0)
            self.assertEqual(count_Elements(), 2)
            try:
                count_Wires()
            except ExperimentTypeError:
                pass
            else:
                raise TestError

    @my_test_dec
    def test_union_Sub(self):
        with experiment("__test__", is_exit=True, elementXYZ=True, force_crt=True):
            a = unit.Sub(bitLength=8, fold=False)
            crt_Wires(unit.Inputs(-3, 0, 0, 8).data_Output, a.minuend)
            crt_Wires(unit.Inputs(-2, 0, 0, 8).data_Output, a.subtrahend)
            crt_Wires(unit.Outputs(2, 0, 0, 9).data_Input, a.outputs)
            self.assertEqual(count_Elements(), 42)
            self.assertEqual(count_Wires(), 41)

            unit.Sub(-5, 0, 0)

    # 测试简单乐器设置音高的三种方法
    @my_test_dec
    def test_Simple_Instrument(self):
        with experiment("__test__", is_exit=True, elementXYZ=True, force_crt=True):
            a = Simple_Instrument(pitch=48)
            a = Simple_Instrument().set_Tonality(48)
            a = Simple_Instrument(pitch="C3")
            a = Simple_Instrument().set_Tonality("C3")
            Logic_Input(-1, 0, 0).o - a.i
            a.o - Ground_Component(1, 0, 0).i

    @my_test_dec
    def test_getElementError(self):
        with experiment("__test__", is_exit=True, force_crt=True):
            Logic_Input()
            try:
                get_Element(index=2)
            except getElementError:
                pass
            else:
                raise TestError
    
    @my_test_dec
    def test_unionMusic(self):
        music.Note(2)
        try:
            music.Note(0)
        except TypeError:
            pass

    @my_test_dec
    def test_const_is_bigElement(self):
        with experiment("__test__", force_crt=True, is_exit=True):
            a = Multiplier()
            try:
                a.is_bigElement = False
            except AttributeError:
                pass
            else:
                raise TestError

    @my_test_dec
    def test_musicPlayer(self):
        with experiment("__test__", is_exit=True, force_crt=True):
            l = (0, 2, 4, 5, 7, 9, 11)

            t = music.Piece()
            for i in range(7):
                for j in l:
                    n = music.Note(1, pitch=12 * i + j + 21)
                    t.append(n)
                    n.append(music.Note(1, pitch=12 * i + j + 23))
            t.release(-1, -1, 0)
    
    @my_test_dec
    def test_mutiple_notes_in_Simple_Instrument(self):
        with experiment("__test__", force_crt=True, is_exit=True):
            Simple_Instrument().add_note(67) # type: ignore

    @my_test_dec
    def test_merge_Experiment(self):
        with experiment("__test__", force_crt=True, is_exit=True) as exp:
            Logic_Input().o - Logic_Output(1, 0, 0, elementXYZ=True).i

            with experiment("_Test", force_crt=True, is_exit=True) as exp2:
                Logic_Output(0, 0, 0.1)
                exp2.merge(exp, 1, 0, 0, elementXYZ=True)

                self.assertEqual(count_Elements(), 3)

if __name__ == '__main__':
    fcs.main()
    unittest.main()