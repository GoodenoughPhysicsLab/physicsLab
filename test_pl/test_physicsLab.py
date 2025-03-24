# -*- coding: utf-8 -*-
import os
import sys
import pathlib
import warnings
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
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe1:
            self.assertTrue(_ExperimentStack.inside(expe1))
            with Experiment(OpenMode.crt, "_Test", ExperimentType.Circuit, force_crt=True) as expe2:
                self.assertTrue(_ExperimentStack.inside(expe2))
                expe1.close(delete=True)
                self.assertFalse(_ExperimentStack.inside(expe1))
                expe2.close(delete=True)
                self.assertFalse(_ExperimentStack.inside(expe2))

    @my_test_dec
    def test_load_all_elements(self):
        # 物实导出存档与保存到本地的格式不一样, 因此每种类型的实验都有两种格式的测试数据
        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Circuit-Elements.sav")) as expe:
            self.assertTrue(expe.get_elements_count() == 91)
            expe.save(target_path=os.devnull)
            expe.close()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "Export-All-Circuit-Elements.sav")) as expe:
            self.assertTrue(expe.get_elements_count() == 91)
            expe.save(target_path=os.devnull)
            expe.close()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Celestial-Elements.sav")) as expe:
            self.assertTrue(expe.get_elements_count() == 27)
            expe.save(target_path=os.devnull)
            expe.close()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "Export-All-Celestial-Elements.sav")) as expe:
            self.assertTrue(expe.get_elements_count() == 27)
            expe.save(target_path=os.devnull)
            expe.close()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Electromagnetism-Elements.sav")) as expe:
            self.assertTrue(expe.get_elements_count() == 7)
            expe.save(target_path=os.devnull)
            expe.close()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "Export-All-Electromagnetism-Elements.sav")) as expe:
            self.assertTrue(expe.get_elements_count() == 7)
            expe.save(target_path=os.devnull)
            expe.close()

    @my_test_dec
    def test_load_from_app(self):
        def task1():
            with Experiment(OpenMode.load_by_plar_app, "6774ffb4c45f930f41ccedf8", Category.Discussion, user=user) as expe:
                self.assertTrue(expe.get_elements_count() == 91)
                expe.save(target_path=os.devnull)
                expe.close()

        def task2():
            with Experiment(OpenMode.load_by_plar_app, "677500138c54132a83289f9c", Category.Discussion, user=user) as expe:
                self.assertTrue(expe.get_elements_count() == 27)
                expe.save(target_path=os.devnull)
                expe.close()

        def task3():
            with Experiment(OpenMode.load_by_plar_app, "67750037c45f930f41ccee02", Category.Discussion, user=user) as expe:
                self.assertTrue(expe.get_elements_count() == 7)
                expe.save(target_path=os.devnull)
                expe.close()

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
            expe.close()

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
            expe.close()

    @my_test_dec
    def test_normal_circuit_usage(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
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
            expe.close(delete=True)

    @my_test_dec
    def test_read_experiment(self):
        with Experiment(OpenMode.crt, "__test___read_experiment__", ExperimentType.Circuit, force_crt=True) as expe:
            self.assertEqual(expe.get_elements_count(), 0)
            self.assertEqual(expe.get_wires_count(), 0)
            Logic_Input(0, 0, 0)
            expe.save()
            expe.close(delete=False)

        with Experiment(OpenMode.load_by_sav_name, "__test___read_experiment__") as exp2:
            self.assertEqual(exp2.get_elements_count(), 1)
            exp2.close(delete=True)

    @my_test_dec
    def test_crt_experiment(self):
        expe: Experiment = Experiment(OpenMode.crt, "__test___crt_experiment__", ExperimentType.Circuit, force_crt=True)
        expe.save()
        try:
            Experiment(OpenMode.crt, "__test___crt_experiment__", ExperimentType.Circuit) # will fail
        except ExperimentExistError:
            pass
        else:
            raise TestFail
        finally:
            expe.close(delete=True)

    @my_test_dec
    def test_crt_wire(self):
        with Experiment(OpenMode.crt, "__test___crt_wire__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Or_Gate(0, 0, 0)
            crt_wire(a.o, a.i_up, a.i_low, color=WireColor.red)
            self.assertEqual(expe.get_wires_count(), 2)

            del_wire(a.o, a.i_up)
            self.assertEqual(expe.get_wires_count(), 1)
            expe.close(delete=True)

    def test_same_crt_wire(self):
        with Experiment(OpenMode.crt, "__test___same_crt_wire__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Or_Gate(0, 0, 0)
            crt_wire(a.o, a.i_up, color=WireColor.red)
            crt_wire(a.i_up, a.o)
            self.assertEqual(expe.get_wires_count(), 1)
            expe.close(delete=True)

    @my_test_dec
    def test_edge_trigger(self):
        with Experiment(OpenMode.crt, "__test___edge_trigger__", ExperimentType.Circuit, force_crt=True) as expe:
            lib.RisingEdgeTrigger(0, 0, 0)
            lib.FallingEdgeTrigger(0, 0, 0)
            lib.EdgeTrigger(0, 0, 0)
            self.assertEqual(expe.get_elements_count(), 6)
            expe.close(delete=True)

    @my_test_dec
    def test_Const_NoGate(self):
        with Experiment(OpenMode.crt, "__test___Const_NoGate__", ExperimentType.Circuit, force_crt=True) as expe:
            lib.Const_NoGate(0, 0, 0)
            lib.Const_NoGate(0, 0, 0)
            self.assertEqual(expe.get_elements_count(), 1)

            with Experiment(OpenMode.crt, "__test___Const_NoGate_sub__", ExperimentType.Circuit, force_crt=True) as exp2:
                lib.Const_NoGate(0, 0, 0)
                lib.Const_NoGate(0, 0, 0)
                self.assertEqual(exp2.get_elements_count(), 1)
                exp2.close(delete=True)

            expe.close(delete=True)

    @my_test_dec
    def test_Sum(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            lib.Sum(0, -1, 0, bitnum=64)
            self.assertEqual(expe.get_elements_count(), 64)
            self.assertEqual(expe.get_wires_count(), 63)
            expe.clear_elements()
            self.assertEqual(expe.get_wires_count(), 0)
            self.assertEqual(expe.get_elements_count(), 0)
            expe.close(delete=True)

    @my_test_dec
    def test_get_Element(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            Or_Gate(0, 0, 0)
            crt_wire(
                expe.get_element_from_position(0, 0, 0)[0].o,
                expe.get_element_from_index(1).i_up
            )
            crt_wire(
                expe.get_element_from_position(0, 0, 0)[0].i_low,
                expe.get_element_from_index(1).o
            )
            self.assertEqual(expe.get_wires_count(), 2)
            expe.close(delete=True)

    @my_test_dec
    def test_errors(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            # 确保__test__实验不存在
            expe.close(delete=True)
        try:
            Experiment(OpenMode.load_by_sav_name, '__test__') # do not exist
        except ExperimentNotExistError:
            pass
        else:
            raise TestFail

    @my_test_dec
    def test_elementXYZ_2(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            expe.is_elementXYZ = True
            for x in range(10):
                for y in range(10):
                    Yes_Gate(x, y, 0)
            for x in range(10):
                for y in [y * 2 + 10 for y in range(5)]:
                    Multiplier(x, y, 0)

            crt_wire(expe.get_element_from_index(1).o, expe.get_element_from_position(0, 1, 0)[0].i)
            crt_wire(
                expe.get_element_from_index(2).i,
                expe.get_element_from_index(3).o,
                expe.get_element_from_index(4).i
            )
            self.assertEqual(expe.get_wires_count(), 3)
            self.assertEqual(expe.get_elements_count(), 150)
            expe.close(delete=True)

    @my_test_dec
    def test_open_a_lot_of_experiments(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as exp2:
                Logic_Input(0, 0, 0)
                self.assertEqual(1, exp2.get_elements_count())
                exp2.close(delete=True)
            expe.close(delete=True)

    @my_test_dec
    def test_with_and_coverPosition(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            Logic_Input(0, 0, 0)
            Or_Gate(0, 0, 0)
            self.assertEqual(len(expe.get_element_from_position(0, 0, 0)), 2)
            expe.close(delete=True)

    @my_test_dec
    def test_del_element(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            crt_wire(Logic_Input(0, 0, 0).o, Or_Gate(0, 0, 0).o)
            expe.del_element(expe.get_element_from_index(2))
            self.assertEqual(expe.get_elements_count(), 1)
            self.assertEqual(expe.get_wires_count(), 0)
            expe.close(delete=True)

        with Experiment(OpenMode.load_by_filepath, pathlib.Path(TEST_DATA_DIR) / "All-Circuit-Elements.sav") as expe:
            expe.del_element(expe.get_element_from_index(1))
            self.assertEqual(expe.get_elements_count(), 90)
            expe.close()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Celestial-Elements.sav")) as expe:
            expe.del_element(expe.get_element_from_index(1))
            self.assertEqual(expe.get_elements_count(), 26)
            expe.close()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Electromagnetism-Elements.sav")) as expe:
            expe.del_element(expe.get_element_from_index(1))
            self.assertEqual(expe.get_elements_count(), 6)
            expe.close()

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
            expe.close(delete=True)

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
            expe.close(delete=True)

    # 测试打开实验类型与文件不吻合
    @my_test_dec
    def test_ExperimentType(self):
        with Experiment(OpenMode.crt, "__test___ExperimentType__", ExperimentType.Electromagnetism, force_crt=True) as expe:
            try:
                Positive_Charge(0, 0, 0)
                Logic_Input(0, 0, 0)
            except ExperimentTypeError:
                pass
            else:
                raise TestFail
            finally:
                expe.close(delete=True)

    @my_test_dec
    def test_electromagnetism(self):
        with Experiment(OpenMode.crt, "__test___electromagnetism__", ExperimentType.Electromagnetism, force_crt=True) as expe:
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
                expe.close(delete=True)

    @my_test_dec
    def test_super_and_gate(self):
        with Experiment(OpenMode.crt, "__test___super_and_gate__", ExperimentType.Circuit, force_crt=True) as expe:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                for bitnum in range(2, 100):
                    crt_wires(
                        lib.Inputs(-1, 0, 0, bitnum=bitnum).outputs,
                        lib.Super_AndGate(0, 0, 0, bitnum=bitnum).inputs
                    )
            self.assertEqual(expe.get_elements_count(), 6666)
            self.assertEqual(expe.get_wires_count(), 6636)
            expe.close(delete=True)

    @my_test_dec
    def test_super_or_gate(self):
        with Experiment(OpenMode.crt, "__test___super_or_gate__", ExperimentType.Circuit, force_crt=True) as expe:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                for bitnum in range(2, 100):
                    crt_wires(
                        lib.Inputs(-1, 0, 0, bitnum=bitnum).outputs,
                        lib.Super_OrGate(0, 0, 0, bitnum=bitnum).inputs
                    )
            self.assertEqual(expe.get_elements_count(), 9800)
            self.assertEqual(expe.get_wires_count(), 9702)
            expe.close(delete=True)

    @my_test_dec
    def test_super_nor_gate(self):
        with Experiment(OpenMode.crt, "__test___super_nor_gate__", ExperimentType.Circuit, force_crt=True) as expe:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                for bitnum in range(2, 100):
                    crt_wires(
                        lib.Inputs(-1, 0, 0, bitnum=bitnum).outputs,
                        lib.Super_NorGate(0, 0, 0, bitnum=bitnum).inputs
                    )
            self.assertEqual(expe.get_elements_count(), 9800)
            self.assertEqual(expe.get_wires_count(), 9702)
            expe.close(delete=True)

    @my_test_dec
    def test_lib_sub(self):
        with Experiment(OpenMode.crt, "__test___lib_sub__", ExperimentType.Circuit, force_crt=True) as expe:
            with ElementXYZ():
                a = lib.Sub(0, 0, 0, bitnum=8, fold=False)
                crt_wires(lib.Inputs(-3, 0, 0, bitnum=8).outputs, a.minuend)
                crt_wires(lib.Inputs(-2, 0, 0, bitnum=8).outputs, a.subtrahend)
                crt_wires(lib.Outputs(2, 0, 0, bitnum=9).inputs, a.outputs)
                self.assertEqual(expe.get_elements_count(), 42)
                self.assertEqual(expe.get_wires_count(), 41)

                lib.Sub(-5, 0, 0, bitnum=4)
            expe.close(delete=True)

    @my_test_dec
    def test_Simple_Instrument(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Simple_Instrument(0, 0, 0, pitches=(48,))
            a = Simple_Instrument(0, 0, 0, pitches=(Simple_Instrument.str2num_pitch("C3"),))
            expe.close(delete=True)

    @my_test_dec
    def test_get_element_error(self):
        with Experiment(OpenMode.crt, "__test___get_element_error__", ExperimentType.Circuit, force_crt=True) as expe:
            Logic_Input(0, 0, 0)
            try:
                expe.get_element_from_index(2)
            except ElementNotFound:
                pass
            else:
                raise TestFail
            finally:
                expe.close(delete=True)

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
        with Experiment(OpenMode.crt, "__test___is_bigElement__", ExperimentType.Circuit, force_crt=True) as expe:
            self.assertEqual(Logic_Output.is_bigElement, False)
            self.assertEqual(Multiplier.is_bigElement, True)
            self.assertEqual(Or_Gate.is_bigElement, False)
            self.assertEqual(Logic_Input(0, 0, 0).is_bigElement, False)
            self.assertEqual(Full_Adder(0, 0, 0).is_bigElement, True)
            self.assertEqual(Xor_Gate(0, 0, 0).is_bigElement, False)
            expe.close(delete=True)

    @my_test_dec
    def test_music_player(self):
        with Experiment(OpenMode.crt, "__test___music_player__", ExperimentType.Circuit, force_crt=True) as expe:
            l = (0, 2, 4, 5, 7, 9, 11)

            t = music.Piece()
            for i in range(7):
                for j in l:
                    n = music.Note(1, pitch=12 * i + j + 21)
                    t.append(n)
                    n.append(music.Note(1, pitch=12 * i + j + 23))
            t.release(-1, -1, 0)
            expe.close(delete=True)

    @my_test_dec
    def test_mutiple_notes_in_Simple_Instrument(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            Simple_Instrument(0, 0, 0, pitches=(67,))
            expe.close(delete=True)

    @my_test_dec
    def test_load_midi(self):
        expe = Experiment(OpenMode.crt, "__test___load_midi__", ExperimentType.Circuit, force_crt=True)
        music.Midi(os.path.join(TEST_DATA_DIR, "鼓哥.mid")).to_piece(max_notes=800).release(-1, -1, 0)
        self.assertEqual(expe.get_elements_count(), 510)
        self.assertEqual(expe.get_wires_count(), 1016)
        expe.export("temp.pl.py", "__test___load_midi_sub__")
        expe.close(delete=True)

        os.system(f"{sys.executable} temp.pl.py")
        with Experiment(OpenMode.load_by_sav_name, "__test___load_midi_sub__") as expe:
            self.assertEqual(expe.get_elements_count(), 510)
            self.assertEqual(expe.get_wires_count(), 1016)
            expe.close(delete=True)

    @my_test_dec
    def test_merge_experiment(self):
        with Experiment(OpenMode.crt, "__test___merge_experiment__", ExperimentType.Circuit, force_crt=True) as expe:
            crt_wire(Logic_Input(0, 0, 0).o, Logic_Output(1, 0, 0, elementXYZ=True).i)

            with Experiment(OpenMode.crt, "__test___merge_experiment_sub__", ExperimentType.Circuit, force_crt=True) as exp2:
                Logic_Output(0, 0, 0.1)
                exp2.merge(expe, 1, 0, 0, elementXYZ=True)

                self.assertEqual(exp2.get_elements_count(), 3)
                exp2.close(delete=True)
            expe.close(delete=True)

    @my_test_dec
    def test_link_wire_in_two_experiment(self):
        with Experiment(OpenMode.crt, "__test___link_wire_in_two_experiment__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Logic_Input(0, 0, 0)
            with Experiment(OpenMode.crt, "__test___link_wire_in_two_experiment_sub__", ExperimentType.Circuit, force_crt=True) as exp2:
                b = Logic_Output(0, 0, 0)
                try:
                    crt_wire(a.o, b.i)
                except InvalidWireError:
                    pass
                else:
                    raise TestFail
                finally:
                    exp2.close(delete=True)
            expe.close(delete=True)

    @my_test_dec
    def test_merge_experiment2(self):
        with Experiment(OpenMode.crt, "__test___merge_experiment2__", ExperimentType.Circuit, force_crt=True) as expe:
            e = Yes_Gate(0, 0, 0)
            crt_wire(e.i, e.o)

            with Experiment(OpenMode.crt, "__test___merge_experiment2_sub__", ExperimentType.Circuit, force_crt=True) as exp2:
                Logic_Output(0, 0, 0.1)
                exp2.merge(expe, 1, 0, 0, elementXYZ=True)
                a = exp2.get_element_from_position(1, 0, 0)[0]
                crt_wire(a.i, a.o)

                self.assertEqual(exp2.get_elements_count(), 2)
                self.assertEqual(expe.get_wires_count(), 1)
                exp2.close(delete=True)
            expe.close(delete=True)

    @my_test_dec
    def test_crt_self_wire(self):
        with Experiment(OpenMode.crt, "__test___crt_self_wire__", ExperimentType.Circuit, force_crt=True) as expe:
            e = Logic_Output(0, 0, 0)
            try:
                crt_wire(e.i, e.i)
            except InvalidWireError:
                pass
            else:
                raise TestFail
            finally:
                expe.close(delete=True)

    @my_test_dec
    def test_export(self):
        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "float32_t.sav")) as expe:
            expe.export("temp.pl.py", "__test___export__")
            expe.close()

        os.system(f"{sys.executable} temp.pl.py")
        with Experiment(OpenMode.load_by_sav_name, "__test___export__") as expe:
            self.assertEqual(expe.get_elements_count(), 652)
            self.assertEqual(expe.get_wires_count(), 1385)
            expe.close(delete=True)

    @my_test_dec
    def test_export2(self):
        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "Export-All-Circuit-Elements.sav")) as expe:
            expe.export("temp.pl.py", "__test__")
            expe.close()

        os.system(f"{sys.executable} temp.pl.py")
        with Experiment(OpenMode.load_by_sav_name, "__test__") as expe:
            self.assertTrue(expe.get_elements_count() == 91)
            expe.close(delete=True)

    @my_test_dec
    def test_type_error(self):
        with Experiment(OpenMode.crt, "__test___type_error__", ExperimentType.Circuit, force_crt=True) as expe:
            try:
                Logic_Input(0, 0, 0, True) # type: ignore
            except TypeError:
                pass
            else:
                raise TestFail
            finally:
                expe.close(delete=True)

    @my_test_dec
    def test_wire_is_too_less(self):
        try:
            with Experiment(OpenMode.crt, "__test___wire_is_too_less__", ExperimentType.Circuit, force_crt=True) as expe:
                crt_wire(Logic_Input(0, 0, 0).o)
        except ValueError:
            pass
        else:
            raise TestFail

    @my_test_dec
    def test___exit__(self):
        try:
            with Experiment(OpenMode.crt, "__test___exit__", ExperimentType.Circuit, force_crt=True) as expe:
                Positive_Charge(0, 0, 0)
        except ExperimentTypeError:
            pass
        else:
            raise TestFail

    @my_test_dec
    def test_get_all_pins(self):
        self.assertEqual(len(list(Multiplier.get_all_pins_property())), 8)

    @my_test_dec
    def test_get_pin_name(self):
        with Experiment(OpenMode.crt, "__test___get_pin_name__", ExperimentType.Circuit, force_crt=True) as expe:
            self.assertEqual(Multiplier(0, 0, 0).i_low.get_pin_name(), "i_low")
            expe.close(delete=True)

    @my_test_dec
    def test_type_pin(self):
        self.assertTrue(isinstance(InputPin, type(Pin)))
        self.assertTrue(isinstance(OutputPin, type(Pin)))
        self.assertFalse(isinstance(ElementBase, type(Pin)))

    @my_test_dec
    def test_tick_counter(self):
        with Experiment(OpenMode.crt, "__test___tick_counter__", ExperimentType.Circuit, force_crt=True) as expe:
            logic_input = Logic_Input(0, 0, 0)
            for i in range(2, 16):
                tick_counter = Tick_Counter(0, 0, 0, num=i)
                crt_wire(logic_input.o, tick_counter.i)
                crt_wire(tick_counter.o, Logic_Output(0, 0, 0).i)
            self.assertEqual(expe.get_elements_count(), 65)
            self.assertEqual(expe.get_wires_count(), 121)
            expe.close(delete=True)

    @my_test_dec
    def test_two_four_decoder(self):
        with Experiment(OpenMode.crt, "__test___two_four_decoder__", ExperimentType.Circuit, force_crt=True) as expe:
            i = lib.Inputs(-1, 0, 0, bitnum=2)
            decoder = lib.TwoFour_Decoder(0, 0, 0)
            o = lib.Outputs(1, 0, 0, bitnum=4)
            lib.crt_wires(i.outputs, decoder.inputs)
            lib.crt_wires(decoder.outputs, o.inputs)
            self.assertEqual(expe.get_elements_count(), 10)
            self.assertEqual(expe.get_wires_count(), 12)
            expe.close(delete=True)

    @my_test_dec
    def test_switched_register(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            i1 = lib.Inputs(-1, 0, 0, bitnum=6)
            i2 = lib.Inputs(-0.5, 0, 0, bitnum=6)
            clk = Logic_Input(-1, -1, 0)
            switch = Logic_Input(-0.5, -1, 0)
            decoder = lib.Switched_Register(0, 0, 0, bitnum=6)
            o = lib.Outputs(1, 0, 0, bitnum=6)
            lib.crt_wires(i1.outputs, decoder.inputs1)
            lib.crt_wires(i2.outputs, decoder.inputs2)
            crt_wire(clk.o, decoder.clk)
            crt_wire(switch.o, decoder.switch)
            lib.crt_wires(decoder.outputs, o.inputs)
            self.assertEqual(expe.get_elements_count(), 33)
            self.assertEqual(expe.get_wires_count(), 43)
            expe.close(delete=True)

    @my_test_dec
    def test_super_logic_gate(self):
        with Experiment(OpenMode.crt, "__test___super_logic_gate__", ExperimentType.Circuit, force_crt=True) as expe:
            i1 = lib.Inputs(-1, 0, 0, bitnum=6)
            i2 = lib.Inputs(-0.5, 0, 0, bitnum=6)
            compute = lib.EqualTo(0, 0, 0, bitnum=6)
            o = Logic_Output(0.5, 0, 0)
            lib.crt_wires(i1.outputs, compute.inputs1)
            lib.crt_wires(i2.outputs, compute.inputs2)
            crt_wire(compute.output, o.i)
            self.assertEqual(expe.get_elements_count(), 22)
            self.assertEqual(expe.get_wires_count(), 21)
            expe.close(delete=True)

    @my_test_dec
    def test_analog_lib(self):
        with Experiment(OpenMode.crt, "__test___analog_lib__", ExperimentType.Circuit, force_crt=True) as expe:
            gnd = Ground_Component(5, -6, 0)
            mtr = Multimeter(4, 0, 0)
            crt_wire(mtr.black, gnd.i)
            logic_input1 = Logic_Input(-9, 9, 0)
            logic_input1.output_status = True
            logic_input2 = Logic_Input(-9, -1, 0)
            logic_input2.output_status = True
            nl = lib.log(lib.exp(lib.PinNode(logic_input1.o, gnd)), lib.ln(lib.PinNode(logic_input2.o, gnd)))
            nl.pos = (0, -11, 0)
            lib.lambertW(lib.PinNode(Logic_Input(-9, 11, 0).o, gnd))
            self.assertEqual(expe.get_elements_count(), 107)
            self.assertEqual(expe.get_wires_count(), 159)
            self.assertEqual(len(lib.analog._gn[expe]), 7)
            self.assertEqual(len(lib.analog._gicw[expe]), 25)
            expe.close(delete=True)
