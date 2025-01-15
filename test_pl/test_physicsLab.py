# -*- coding: utf-8 -*-
import os
import sys
import threading
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
            raise TestFail
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
            self.assertTrue(expe.get_elements_count() == 91)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "Export-All-Circuit-Elements.sav")) as expe:
            self.assertTrue(expe.get_elements_count() == 91)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Celestial-Elements.sav")) as expe:
            self.assertTrue(expe.get_elements_count() == 27)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "Export-All-Celestial-Elements.sav")) as expe:
            self.assertTrue(expe.get_elements_count() == 27)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Electromagnetism-Elements.sav")) as expe:
            self.assertTrue(expe.get_elements_count() == 7)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "Export-All-Electromagnetism-Elements.sav")) as expe:
            self.assertTrue(expe.get_elements_count() == 7)
            expe.exit()

    @my_test_dec
    def test_load_from_app(self):
        def task1():
            expe = Experiment(OpenMode.load_by_plar_app, "6774ffb4c45f930f41ccedf8", Category.Discussion, user=user)
            self.assertTrue(expe.get_elements_count() == 91)
            expe.exit()

        def task2():
            expe = Experiment(OpenMode.load_by_plar_app, "677500138c54132a83289f9c", Category.Discussion, user=user)
            self.assertTrue(expe.get_elements_count() == 27)
            expe.exit()

        def task3():
            expe = Experiment(OpenMode.load_by_plar_app, "67750037c45f930f41ccee02", Category.Discussion, user=user)
            self.assertTrue(expe.get_elements_count() == 7)
            expe.exit()

        thread1 = threading.Thread(target=task1)
        thraed2 = threading.Thread(target=task2)
        thread3 = threading.Thread(target=task3)
        thread1.start()
        thraed2.start()
        thread3.start()
        thread1.join()
        thraed2.join()
        thread3.join()

    @my_test_dec
    def test_double_load_error(self):
        expe = Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Circuit-Elements.sav"))
        try:
            Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Circuit-Elements.sav"))
        except ExperimentOpenedError:
            pass
        else:
            raise TestFail
        finally:
            expe.exit()

    @my_test_dec
    def test_load_invalid_sav(self):
        try:
            Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "invalid.sav"))
        except InvalidSavError:
            pass
        else:
            raise TestFail

    @my_test_dec
    def test_float32_t_sav(self):
        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "float32_t.sav")) as expe:
            self.assertEqual(expe.get_elements_count(), 652)
            self.assertEqual(expe.get_wires_count(), 1385)
            expe.exit()

    @my_test_dec
    def test_normal_circuit_usage(self):
        expe: Experiment = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        a = Yes_Gate(0, 0, 0)
        self.assertEqual(expe.get_elements_count(), 1)
        self.assertEqual(a.get_position(), (0, 0, 0))
        crt_wire(a.o, a.i)
        self.assertEqual(expe.get_wires_count(), 1)
        expe.clear_wires()
        self.assertEqual(expe.get_wires_count(), 0)
        self.assertEqual(expe.get_elements_count(), 1)
        crt_wire(a.o, a.i)
        expe.crt_element("Logic Input", 0, 0, 0)
        self.assertEqual(expe.get_elements_count(), 2)
        expe.get_element_from_position(0, 0, 0)
        expe.exit(delete=True)

    @my_test_dec
    def test_read_experiment(self):
        expe: Experiment = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)

        self.assertEqual(expe.get_elements_count(), 0)
        self.assertEqual(expe.get_wires_count(), 0)
        Logic_Input(0, 0, 0)
        expe.save()
        expe.exit()

        exp2: Experiment = Experiment(OpenMode.load_by_sav_name, "__test__")
        self.assertEqual(exp2.get_elements_count(), 1)
        exp2.exit(delete=True)

    @my_test_dec
    def test_crt_experiment(self):
        exp: Experiment = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        exp.save()
        try:
            Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit) # will fail
        except ExperimentExistError:
            pass
        else:
            raise TestFail
        finally:
            exp.exit(delete=True)

    @my_test_dec
    def test_crt_wire(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Or_Gate(0, 0, 0)
            crt_wire(a.o, a.i_up, a.i_low, color=WireColor.red)
            self.assertEqual(expe.get_wires_count(), 2)

            del_wire(a.o, a.i_up)
            self.assertEqual(expe.get_wires_count(), 1)
            expe.exit(delete=True)

    def test_same_crt_wire(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Or_Gate(0, 0, 0)
            crt_wire(a.o, a.i_up, color=WireColor.red)
            crt_wire(a.i_up, a.o)
            self.assertEqual(expe.get_wires_count(), 1)
            expe.exit(delete=True)

    @my_test_dec
    def test_edge_trigger(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            lib.Rising_edge_trigger(0, 0, 0)
            lib.Falling_edge_trigger(0, 0, 0)
            lib.Edge_trigger(0, 0, 0)
            self.assertEqual(expe.get_elements_count(), 6)
            expe.exit(delete=True)

    @my_test_dec
    def test_Const_NoGate(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            lib.Const_NoGate(0, 0, 0)
            lib.Const_NoGate(0, 0, 0)
            self.assertEqual(expe.get_elements_count(), 1)

            with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as exp2:
                lib.Const_NoGate(0, 0, 0)
                lib.Const_NoGate(0, 0, 0)
                self.assertEqual(exp2.get_elements_count(), 1)
                exp2.exit(delete=True)

            expe.exit(delete=True)

    @my_test_dec
    def test_Sum(self):
        expe: Experiment = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        lib.Sum(0, -1, 0, bitnum=64)
        self.assertEqual(expe.get_elements_count(), 64)
        self.assertEqual(expe.get_wires_count(), 63)
        expe.clear_elements()
        self.assertEqual(expe.get_wires_count(), 0)
        self.assertEqual(expe.get_elements_count(), 0)
        expe.exit(delete=True)

    @my_test_dec
    def test_get_Element(self):
        expe: Experiment = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        Or_Gate(0, 0, 0)
        crt_wire(
            expe.get_element_from_position(0, 0, 0).o,
            expe.get_element_from_index(1).i_up
        )
        crt_wire(
            expe.get_element_from_position(0, 0, 0).i_low,
            expe.get_element_from_index(1).o
        )
        self.assertEqual(expe.get_wires_count(), 2)
        expe.exit(delete=True)

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
            raise TestFail

    @my_test_dec
    def test_elementXYZ_2(self):
        expe: Experiment = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        set_elementXYZ(True)
        for x in range(10):
            for y in range(10):
                Yes_Gate(x, y, 0)
        for x in range(10):
            for y in [y * 2 + 10 for y in range(5)]:
                Multiplier(x, y, 0)

        crt_wire(expe.get_element_from_index(1).o, expe.get_element_from_position(0, 1, 0).i)
        crt_wire(
            expe.get_element_from_index(2).i,
            expe.get_element_from_index(3).o,
            expe.get_element_from_index(4).i
        )
        self.assertEqual(expe.get_wires_count(), 3)
        self.assertEqual(expe.get_elements_count(), 150)
        expe.exit(delete=True)

    @my_test_dec
    def test_open_manyExperiment(self):
        expe: Experiment = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as exp2:
            Logic_Input(0, 0, 0)
            self.assertEqual(1, exp2.get_elements_count())
            exp2.exit(delete=True)
        expe.exit(delete=True)

    @my_test_dec
    def test_with_and_coverPosition(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            Logic_Input(0, 0, 0)
            Or_Gate(0, 0, 0)
            self.assertEqual(len(expe.get_element_from_position(0, 0, 0)), 2)
            expe.exit(delete=True)

    @my_test_dec
    def test_del_element(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            crt_wire(Logic_Input(0, 0, 0).o, Or_Gate(0, 0, 0).o)
            expe.del_element(expe.get_element_from_index(2))
            self.assertEqual(expe.get_elements_count(), 1)
            self.assertEqual(expe.get_wires_count(), 0)
            expe.exit(delete=True)

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Circuit-Elements.sav")) as expe:
            expe.del_element(expe.get_element_from_index(1))
            self.assertEqual(expe.get_elements_count(), 90)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Celestial-Elements.sav")) as expe:
            expe.del_element(expe.get_element_from_index(1))
            self.assertEqual(expe.get_elements_count(), 26)
            expe.exit()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Electromagnetism-Elements.sav")) as expe:
            expe.del_element(expe.get_element_from_index(1))
            self.assertEqual(expe.get_elements_count(), 6)
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
            self.assertEqual(25, expe.get_elements_count())
            self.assertEqual(23, expe.get_wires_count())
            del_wires(c.outputs, b.inputs)
            self.assertEqual(15, expe.get_wires_count())
            expe.exit(delete=True)

    # 测试模块化加法电路
    @my_test_dec
    def test_union_Sum2(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            a = lib.Inputs(-1, 0, 0, bitnum=8)
            b = lib.Inputs(-2, 0, 0, bitnum=8)
            c = lib.Sum(0, 0, 0, bitnum=8)
            d = lib.Outputs(1, 0, 0, bitnum=8)
            crt_wires(a.outputs, c.inputs1)
            crt_wires(b.outputs, c.inputs2)
            crt_wires(c.outputs, d.inputs)
            expe.exit(delete=True)

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
                raise TestFail
            finally:
                expe.exit(delete=True)

    @my_test_dec
    def test_electromagnetism(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Electromagnetism, force_crt=True) as expe:
            Negative_Charge(-0.1, 0, 0)
            Positive_Charge(0.1, 0, 0)
            self.assertEqual(expe.get_elements_count(), 2)
            try:
                expe.get_wires_count()
            except ExperimentTypeError:
                pass
            else:
                raise TestFail
            finally:
                expe.exit(delete=True)

    @my_test_dec
    def test_super_and_gate(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                for bitnum in range(2, 100):
                    crt_wires(
                        lib.Inputs(-1, 0, 0, bitnum=bitnum).outputs,
                        lib.Super_AndGate(0, 0, 0, bitnum=bitnum).inputs
                    )
            self.assertEqual(expe.get_elements_count(), 6666)
            self.assertEqual(expe.get_wires_count(), 6636)
            expe.exit(delete=True)

    @my_test_dec
    def test_super_or_gate(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                for bitnum in range(2, 100):
                    crt_wires(
                        lib.Inputs(-1, 0, 0, bitnum=bitnum).outputs,
                        lib.Super_OrGate(0, 0, 0, bitnum=bitnum).inputs
                    )
            self.assertEqual(expe.get_elements_count(), 9800)
            self.assertEqual(expe.get_wires_count(), 9702)
            expe.exit(delete=True)

    @my_test_dec
    def test_super_nor_gate(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                for bitnum in range(2, 100):
                    crt_wires(
                        lib.Inputs(-1, 0, 0, bitnum=bitnum).outputs,
                        lib.Super_NorGate(0, 0, 0, bitnum=bitnum).inputs
                    )
            self.assertEqual(expe.get_elements_count(), 9800)
            self.assertEqual(expe.get_wires_count(), 9702)
            expe.exit(delete=True)

    @my_test_dec
    def test_union_Sub(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            set_elementXYZ(True)
            a = lib.Sub(0, 0, 0, bitnum=8, fold=False)
            crt_wires(lib.Inputs(-3, 0, 0, bitnum=8).outputs, a.minuend)
            crt_wires(lib.Inputs(-2, 0, 0, bitnum=8).outputs, a.subtrahend)
            crt_wires(lib.Outputs(2, 0, 0, bitnum=9).inputs, a.outputs)
            self.assertEqual(expe.get_elements_count(), 42)
            self.assertEqual(expe.get_wires_count(), 41)

            lib.Sub(-5, 0, 0, bitnum=4)
            expe.exit(delete=True)

    @my_test_dec
    def test_Simple_Instrument(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Simple_Instrument(0, 0, 0, pitches=(48,))
            a = Simple_Instrument(0, 0, 0, pitches=(Simple_Instrument.str2num_pitch("C3"),))
            expe.exit(delete=True)

    @my_test_dec
    def test_getElementError(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            Logic_Input(0, 0, 0)
            try:
                expe.get_element_from_index(2)
            except ElementNotFound:
                pass
            else:
                raise TestFail
            finally:
                expe.exit(delete=True)

    @my_test_dec
    def test_unionMusic(self):
        music.Note(2)
        try:
            music.Note(0)
        except TypeError: # TODO 应该改为ValueError
            pass
        else:
            raise TestFail

    @my_test_dec
    def test_is_bigElement(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            self.assertEqual(Logic_Output.is_bigElement, False)
            self.assertEqual(Multiplier.is_bigElement, True)
            self.assertEqual(Or_Gate.is_bigElement, False)
            self.assertEqual(Logic_Input(0, 0, 0).is_bigElement, False)
            self.assertEqual(Full_Adder(0, 0, 0).is_bigElement, True)
            self.assertEqual(Xor_Gate(0, 0, 0).is_bigElement, False)
            expe.exit(delete=True)

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
            expe.exit(delete=True)

    @my_test_dec
    def test_mutiple_notes_in_Simple_Instrument(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            Simple_Instrument(0, 0, 0, pitches=(67,))
            expe.exit(delete=True)

    @my_test_dec
    def test_load_midi(self):
        expe = Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True)
        music.Midi(os.path.join(TEST_DATA_DIR, "鼓哥.mid")).to_piece(max_notes=800).release(-1, -1, 0)
        self.assertEqual(expe.get_elements_count(), 510)
        self.assertEqual(expe.get_wires_count(), 1016)
        expe.export("temp.pl.py", "_Test")
        expe.exit(delete=True)

        os.system(f"{sys.executable} temp.pl.py")
        with Experiment(OpenMode.load_by_sav_name, "_Test") as expe:
            self.assertEqual(expe.get_elements_count(), 510)
            self.assertEqual(expe.get_wires_count(), 1016)
            expe.exit(delete=True)

    @my_test_dec
    def test_mergeExperiment(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            crt_wire(Logic_Input(0, 0, 0).o, Logic_Output(1, 0, 0, elementXYZ=True).i)

            with Experiment(OpenMode.crt, "_Test", ExperimentType.Circuit, force_crt=True) as exp2:
                Logic_Output(0, 0, 0.1)
                exp2.merge(expe, 1, 0, 0, elementXYZ=True)

                self.assertEqual(exp2.get_elements_count(), 3)
                exp2.exit(delete=True)
            expe.exit(delete=True)

    @my_test_dec
    def test_link_wire_in_twoExperiment(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Logic_Input(0, 0, 0)
            with Experiment(OpenMode.crt, "_Test", ExperimentType.Circuit, force_crt=True) as exp2:
                b = Logic_Output(0, 0, 0)
                try:
                    crt_wire(a.o, b.i)
                except InvalidWireError:
                    pass
                else:
                    raise TestFail
                finally:
                    exp2.exit(delete=True)
            expe.exit(delete=True)

    @my_test_dec
    def test_merge_Experiment2(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            e = Yes_Gate(0, 0, 0)
            crt_wire(e.i, e.o)

            with Experiment(OpenMode.crt, "_Test", ExperimentType.Circuit, force_crt=True) as exp2:
                Logic_Output(0, 0, 0.1)
                exp2.merge(expe, 1, 0, 0, elementXYZ=True)
                a = exp2.get_element_from_position(1, 0, 0)
                crt_wire(a.i, a.o)

                self.assertEqual(exp2.get_elements_count(), 2)
                self.assertEqual(expe.get_wires_count(), 1)
                exp2.exit(delete=True)
            expe.exit(delete=True)

    @my_test_dec
    def test_crt_self_wire(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            e = Logic_Output(0, 0, 0)
            try:
                crt_wire(e.i, e.i)
            except InvalidWireError:
                pass
            else:
                raise TestFail
            finally:
                expe.exit(delete=True)

    @my_test_dec
    def test_export(self):
        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "float32_t.sav")) as expe:
            expe.export("temp.pl.py", "__test__")
            expe.exit()

        os.system(f"{sys.executable} temp.pl.py")
        with Experiment(OpenMode.load_by_sav_name, "__test__") as expe:
            self.assertEqual(expe.get_elements_count(), 652)
            self.assertEqual(expe.get_wires_count(), 1385)
            expe.exit(delete=True)

    @my_test_dec
    def test_typeerror(self):
        try:
            expe = Experiment(OpenMode.crt, "test", ExperimentType.Circuit, force_crt=True)
            Logic_Input(0, 0, 0, True)
        except TypeError:
            pass
        else:
            raise TestFail
        finally:
            expe.exit(delete=True)
