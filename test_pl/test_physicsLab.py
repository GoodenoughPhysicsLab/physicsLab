# -*- coding: utf-8 -*-
import os
from .base import *
from physicsLab.lib import *
from physicsLab._core import _ExperimentStack

def my_test_dec(method: Callable):
    def result(*args, **kwarg):
        method(*args, **kwarg)

        if len(_ExperimentStack.data) != 0:
            print(f"File {os.path.abspath(__file__)}, line {method.__code__.co_firstlineno} : "
                  f"test fail due to len(stack_Experiment) != 0")
            _ExperimentStack.clear()
            raise TestError
    return result

class BasicTest(TestCase, ViztracerTool):
    @my_test_dec
    def test_experiment_stack(self):
        expe1 = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        self.assertTrue(_ExperimentStack.inside(expe1))
        expe2 = Experiment(OpenMode.crt, "_Test", ExperimentType.Circuit, force_crt=True)
        self.assertTrue(_ExperimentStack.inside(expe2))
        expe1.exit()
        self.assertFalse(_ExperimentStack.inside(expe1))
        expe2.exit()
        self.assertFalse(_ExperimentStack.inside(expe2))

    @my_test_dec
    def test_load_all_elements(self):
        # 物实导出存档与保存到本地的格式不一样, 因此每种类型的实验都有两种格式的测试数据
        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Circuit-Elements.sav")) as expe:
            self.assertTrue(count_elements(expe) == 91)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "Export-All-Circuit-Elements.sav")) as expe:
            self.assertTrue(count_elements(expe) == 91)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Celestial-Elements.sav")) as expe:
            self.assertTrue(count_elements(expe) == 27)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "Export-All-Celestial-Elements.sav")) as expe:
            self.assertTrue(count_elements(expe) == 27)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Electromagnetism-Elements.sav")) as expe:
            self.assertTrue(count_elements(expe) == 7)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "Export-All-Electromagnetism-Elements.sav")) as expe:
            self.assertTrue(count_elements(expe) == 7)
            expe.exit()

    @my_test_dec
    def test_load_from_app(self):
        expe = Experiment(OpenMode.load_by_plar_app, "6774ffb4c45f930f41ccedf8", Category.Discussion, user=user)
        self.assertTrue(count_elements(expe) == 91)
        expe.exit()

        expe = Experiment(OpenMode.load_by_plar_app, "677500138c54132a83289f9c", Category.Discussion, user=user)
        self.assertTrue(count_elements(expe) == 27)
        expe.exit()

        expe = Experiment(OpenMode.load_by_plar_app, "67750037c45f930f41ccee02", Category.Discussion, user=user)
        self.assertTrue(count_elements(expe) == 7)
        expe.exit()

    @my_test_dec
    def test_double_load_error(self):
        expe = Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Circuit-Elements.sav"))
        try:
            Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Circuit-Elements.sav"))
        except ExperimentOpenedError:
            pass
        else:
            raise TestError
        finally:
            expe.exit()

    @my_test_dec
    def test_load_invalid_sav(self):
        try:
            Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "invalid.sav"))
        except InvalidSavError:
            pass
        else:
            raise TestError

    @my_test_dec
    def test_normal_circuit_usage(self):
        expe: Experiment = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        a = Yes_Gate(0, 0, 0)
        self.assertEqual(count_elements(expe), 1)
        self.assertEqual(a.get_position(), (0, 0, 0))
        crt_wire(a.o, a.i)
        self.assertEqual(count_wires(), 1)
        clear_wires()
        self.assertEqual(count_wires(), 0)
        self.assertEqual(count_elements(expe), 1)
        crt_wire(a.o, a.i)
        crt_element(expe, "Logic Input")
        self.assertEqual(count_elements(expe), 2)
        get_element_from_position(expe, 0, 0, 0)
        expe.exit()

    @my_test_dec
    def test_readExperiment(self):
        expe: Experiment = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)

        self.assertEqual(count_elements(expe), 0)
        self.assertEqual(count_wires(), 0)
        Logic_Input(0, 0, 0)
        expe.save()
        expe.exit()

        exp2: Experiment = Experiment(OpenMode.load_by_sav_name, "__test__")
        self.assertEqual(count_elements(exp2), 1)
        exp2.exit(delete=True)

    @my_test_dec
    def test_crtExperiment(self):
        exp: Experiment = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        exp.save()
        try:
            Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit) # will fail
        except ExperimentExistError:
            pass
        else:
            raise TestError
        finally:
            exp.exit(delete=True)

    @my_test_dec
    def test_crt_wire(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Or_Gate(0, 0, 0)
            crt_wire(a.o, a.i_up, "red")
            self.assertEqual(count_wires(), 1)

            del_wire(a.o, a.i_up)
            self.assertEqual(count_wires(), 0)
            expe.exit()

    def test_same_crt_wire(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Or_Gate(0, 0, 0)
            crt_wire(a.o, a.i_up, "red")
            crt_wire(a.i_up, a.o, "blue")
            self.assertEqual(count_wires(), 1)
            expe.exit()

    @my_test_dec
    def test_union_Sum(self):
        expe: Experiment = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        lib.Sum(0, -1, 0, bitnum=64)
        self.assertEqual(count_elements(expe), 64)
        self.assertEqual(count_wires(), 63)
        clear_elements(expe)
        self.assertEqual(count_wires(), 0)
        self.assertEqual(count_elements(expe), 0)
        expe.exit()

    @my_test_dec
    def test_get_Element(self):
        expe: Experiment = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        Or_Gate(0, 0, 0)
        crt_wire(
            get_element_from_position(expe, 0, 0, 0).o,
            get_element_from_index(expe, index=1).i_up
        )
        crt_wire(
            get_element_from_position(expe, 0, 0, 0).i_low,
            get_element_from_index(expe, index=1).o
        )
        self.assertEqual(count_wires(), 2)
        expe.exit()

    @my_test_dec
    def test_errors(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            ''' 确保__test__实验不存在 '''
            expe.exit(delete=True)
        try:
            Experiment(OpenMode.load_by_sav_name, '__test__') # do not exist
        except ExperimentNotExistError:
            pass
        else:
            raise TestError

    @my_test_dec
    def test_elementXYZ_2(self):
        expe: Experiment = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        set_elementXYZ(True)
        set_O(-1, -1, 0)
        for x in range(10):
            for y in range(10):
                Yes_Gate(x, y, 0)
        for x in range(10):
            for y in [y * 2 + 10 for y in range(5)]:
                Multiplier(x, y, 0)

        crt_wire(get_element_from_index(expe, 1).o, get_element_from_position(expe, 0, 1, 0).i)
        get_element_from_index(expe, 2).i - get_element_from_index(expe, 3).o - get_element_from_index(expe, 4).i
        self.assertEqual(count_wires(), 3)
        self.assertEqual(count_elements(expe), 150)
        expe.exit()

    @my_test_dec
    def test_open_manyExperiment(self):
        expe: Experiment = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as exp2:
            Logic_Input(0, 0, 0)
            self.assertEqual(1, count_elements(exp2))
            exp2.exit()
        expe.exit()

    @my_test_dec
    def test_with_and_coverPosition(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            Logic_Input(0, 0, 0)
            Or_Gate(0, 0, 0)
            self.assertEqual(len(get_element_from_position(expe, 0, 0, 0)), 2)
            expe.exit()

    @my_test_dec
    def test_del_element(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            Logic_Input(0, 0, 0).o - Or_Gate(0, 0, 0).o
            del_element(expe, get_element_from_index(expe, 2))
            self.assertEqual(count_elements(expe), 1)
            self.assertEqual(count_wires(), 0)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Circuit-Elements.sav")) as expe:
            del_element(expe, get_element_from_index(expe, 1))
            self.assertEqual(count_elements(expe), 90)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Celestial-Elements.sav")) as expe:
            del_element(expe, get_element_from_index(expe, 1))
            self.assertEqual(count_elements(expe), 26)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Electromagnetism-Elements.sav")) as expe:
            del_element(expe, get_element_from_index(expe, 1))
            self.assertEqual(count_elements(expe), 6)
            expe.exit()

    # 测试模块化电路连接导线
    @my_test_dec
    def test_wires(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            a = lib.Inputs(0, 0, 0, bitnum=8)
            b = lib.Outputs(0.6, 0, 0, bitnum=8, elementXYZ=False)
            Logic_Output(0.6, 0, 0.1, elementXYZ=False)
            c = lib.D_WaterLamp(1, 0, 0, bitnum=8)
            crt_wires(b.inputs, c.outputs)
            self.assertEqual(25, count_elements(expe))
            self.assertEqual(23, count_wires())
            del_wires(c.outputs, b.inputs)
            self.assertEqual(15, count_wires())
            expe.exit()

    # 测试模块化加法电路
    @my_test_dec
    def test_union_Sum2(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            a = lib.Inputs(-1, 0, 0, bitnum=8)
            b = lib.Inputs(-2, 0, 0, bitnum=8)
            c = lib.Sum(0, 0, 0, bitnum=8)
            d = lib.Outputs(1, 0, 0, bitnum=8)
            a.outputs - c.inputs1
            b.outputs - c.inputs2
            c.outputs - d.inputs
            expe.exit()

    # 测试打开实验类型与文件不吻合
    @my_test_dec
    def test_ExperimentType(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Electromagnetism, force_crt=True) as expe:
            try:
                Positive_Charge(0, 0, 0)
                Logic_Input(0, 0, 0)
            except ExperimentTypeError:
                pass
            else:
                raise TestError
            finally:
                expe.exit()

    @my_test_dec
    def test_electromagnetism(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Electromagnetism, force_crt=True) as expe:
            Negative_Charge(-0.1, 0, 0)
            Positive_Charge(0.1, 0, 0)
            self.assertEqual(count_elements(expe), 2)
            try:
                count_wires()
            except ExperimentTypeError:
                pass
            else:
                raise TestError
            finally:
                expe.exit()

    @my_test_dec
    def test_union_Sub(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            set_elementXYZ(True)
            a = lib.Sub(0, 0, 0, bitnum=8, fold=False)
            crt_wires(lib.Inputs(-3, 0, 0, bitnum=8).outputs, a.minuend)
            crt_wires(lib.Inputs(-2, 0, 0, bitnum=8).outputs, a.subtrahend)
            crt_wires(lib.Outputs(2, 0, 0, bitnum=9).inputs, a.outputs)
            self.assertEqual(count_elements(expe), 42)
            self.assertEqual(count_wires(), 41)

            lib.Sub(-5, 0, 0, bitnum=4)
            expe.exit()

    # 测试简单乐器设置音高的三种方法
    @my_test_dec
    def test_Simple_Instrument(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Simple_Instrument(0, 0, 0, pitch=48)
            a = Simple_Instrument(0, 0, 0).set_tonality(48)
            a = Simple_Instrument(0, 0, 0, pitch="C3")
            a = Simple_Instrument(0, 0, 0).set_tonality("C3")
            Logic_Input(-1, 0, 0).o - a.i
            a.o - Ground_Component(1, 0, 0).i
            expe.exit()

    @my_test_dec
    def test_getElementError(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            Logic_Input(0, 0, 0)
            try:
                get_element_from_index(expe, 2)
            except ElementNotFound:
                pass
            else:
                raise TestError
            finally:
                expe.exit()

    @my_test_dec
    def test_unionMusic(self):
        music.Note(2)
        try:
            music.Note(0)
        except TypeError: # TODO 应该改为ValueError
            pass
        else:
            raise TestError

    @my_test_dec
    def test_is_bigElement(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            self.assertEqual(Logic_Output.is_bigElement, False)
            self.assertEqual(Multiplier.is_bigElement, True)
            self.assertEqual(Or_Gate.is_bigElement, False)
            self.assertEqual(Logic_Input(0, 0, 0).is_bigElement, False)
            self.assertEqual(Full_Adder(0, 0, 0).is_bigElement, True)
            self.assertEqual(Xor_Gate(0, 0, 0).is_bigElement, False)
            expe.exit()

    @my_test_dec
    def test_musicPlayer(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            l = (0, 2, 4, 5, 7, 9, 11)

            t = music.Piece()
            for i in range(7):
                for j in l:
                    n = music.Note(1, pitch=12 * i + j + 21)
                    t.append(n)
                    n.append(music.Note(1, pitch=12 * i + j + 23))
            t.release(-1, -1, 0)
            expe.exit()

    @my_test_dec
    def test_mutiple_notes_in_Simple_Instrument(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            Simple_Instrument(0, 0, 0).add_note(67) # type: ignore
            expe.exit()

    @my_test_dec
    def test_load_midi(self):
        expe = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        music.Midi(os.path.join(TEST_DATA_DIR, "鼓哥.mid")).to_piece(max_notes=None).release(-1, -1, 0)
        self.assertTrue(count_elements(expe) == 4268)
        expe.exit()

    @my_test_dec
    def test_mergeExperiment(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            Logic_Input(0, 0, 0).o - Logic_Output(1, 0, 0, elementXYZ=True).i

            with Experiment(OpenMode.crt, "_Test", ExperimentType.Circuit, force_crt=True) as exp2:
                Logic_Output(0, 0, 0.1)
                exp2.merge(expe, 1, 0, 0, elementXYZ=True)

                self.assertEqual(count_elements(exp2), 3)
                exp2.exit()
            expe.exit()

    @my_test_dec
    def test_link_wire_in_twoExperiment(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Logic_Input(0, 0, 0)
            with Experiment(OpenMode.crt, "_Test", ExperimentType.Circuit, force_crt=True) as exp2:
                b = Logic_Output(0, 0, 0)
                try:
                    a.o - b.i
                except ExperimentError: # 也许改为InvalidLinkError更好?
                    pass
                else:
                    raise TestError
                finally:
                    exp2.exit()
            expe.exit()

    @my_test_dec
    def test_merge_Experiment2(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            e = Yes_Gate(0, 0, 0)
            e.i - e.o

            with Experiment(OpenMode.crt, "_Test", ExperimentType.Circuit, force_crt=True) as exp2:
                Logic_Output(0, 0, 0.1)
                exp2.merge(expe, 1, 0, 0, elementXYZ=True)
                a = get_element_from_position(exp2, 1, 0, 0)
                a.i - a.o

                self.assertEqual(count_elements(exp2), 2)
                self.assertEqual(count_wires(), 1)
                exp2.exit()
            expe.exit()

    @my_test_dec
    def test_crt_self_wire(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            e = Logic_Output(0, 0, 0)
            try:
                e.i - e.i
            except ExperimentError: # TODO 改进此报错的类型
                pass
            else:
                raise TestError
            finally:
                expe.exit()
