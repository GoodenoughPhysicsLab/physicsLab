# -*- coding: utf-8 -*-
import json
from . import _tools
from . import errors
from .enums import ExperimentType
from ._experiment import _Experiment, _ExperimentStack, OpenMode, _check_method
from .circuit.wire import Wire, Pin
from ._element_base import ElementBase
from .typehint import numType, Optional, Union, List

def crt_element(
        experiment: _Experiment,
        name: str,
        x: numType = 0,
        y: numType = 0,
        z: numType = 0,
        elementXYZ: Optional[bool] = None,
        *args,
        **kwargs
) -> ElementBase:
    ''' 通过元件的ModelID或其类名创建元件 '''
    if not isinstance(name, str) or \
            not isinstance(x, (int, float)) or \
            not isinstance(y, (int, float)) or \
            not isinstance(z, (int, float)):
        raise TypeError

    from physicsLab import circuit

    name = name.strip().replace(' ', '_').replace('-', '_')
    x, y, z = _tools.roundData(x, y, z) # type: ignore

    if experiment.experiment_type == ExperimentType.Circuit:
        if (name == '555_Timer'):
            return circuit.NE555(x, y, z, elementXYZ)
        elif (name == '8bit_Input'):
            return circuit.eight_bit_Input(x, y, z, elementXYZ)
        elif (name == '8bit_Display'):
            return circuit.eight_bit_Display(x, y, z, elementXYZ)
        else:
            return eval(f"circuit.{name}({x}, {y}, {z}, {elementXYZ}, *{args}, **{kwargs})")
    elif experiment.experiment_type == ExperimentType.Celestial:
        from physicsLab import celestial
        return eval(f"celestial.{name}({x}, {y}, {z})")
    elif experiment.experiment_type == ExperimentType.Electromagnetism:
        from physicsLab import electromagnetism
        return eval(f"electromagnetism.{name}({x}, {y}, {z})")
    else:
        raise errors.InternalError

def get_element_from_position(
        experiment: _Experiment,
        x: numType,
        y: numType,
        z: numType,
) -> Union[ElementBase, List[ElementBase]]:
    ''' 通过坐标索引元件 '''
    if not isinstance(x, (int, float)) or \
            not isinstance(y, (int, float)) or \
            not isinstance(z, (int, float)):
        raise TypeError

    position = _tools.roundData(x, y, z)
    if position not in experiment._elements_position.keys():
        raise errors.ElementNotFound(f"{position} do not exist")

    result: list = experiment._elements_position[position]
    return result[0] if len(result) == 1 else result

def get_element_from_index(experiment: _Experiment, index: int) -> ElementBase:
    ''' 通过index (元件生成顺序) 索引元件 '''
    if not isinstance(index, int):
        raise TypeError

    if 0 < index <= len(experiment.Elements):
        return experiment.Elements[index - 1]
    else:
        raise errors.ElementNotFound

def get_element_from_identifier(experiment: _Experiment, identifier: str) -> ElementBase:
    ''' 通过原件的id获取元件的引用 '''
    for element in experiment.Elements:
        assert hasattr(element, "data")
        if element.data["Identifier"] == identifier:
            return element
    raise errors.ElementNotFound

def del_element(experiment: _Experiment, element: ElementBase) -> None:
    ''' 删除元件
        @param element: 三大实验的元件
    '''
    if not isinstance(element, ElementBase):
        raise TypeError

    identifier = element.data["Identifier"]

    res_Wires = set()
    for a_wire in experiment.Wires:
        if a_wire.Source.element_self.data["Identifier"] == identifier or \
        a_wire.Target.element_self.data["Identifier"] == identifier:
            continue

        res_Wires.add(a_wire)
    experiment.Wires = res_Wires

    # 删除_elements_position中的引用
    for elements in experiment._elements_position.values():
        if element in elements:
            elements.remove(element)
            break

    # 删除elements_Index中的引用
    for element in experiment.Elements:
        if element is element:
            experiment.Elements.remove(element)
            break

def count_elements(experiment: _Experiment) -> int:
    ''' 元件的数量 '''
    return len(experiment.Elements)

def clear_elements(experiment: _Experiment) -> None:
    ''' 清空元件 '''
    experiment.Wires.clear()
    experiment.Elements.clear()
    experiment._elements_position.clear()

def _load_elements(experiment: _Experiment, _elements: list) -> None:
    assert isinstance(_elements, list)

    for element in _elements:
        # Unity 采用左手坐标系
        x, z, y = eval(f"({element['Position']})")

        # 实例化对象
        if experiment.experiment_type == ExperimentType.Circuit:
            if element["ModelID"] == "Simple Instrument":
                from .circuit.elements.otherCircuit import Simple_Instrument
                obj = Simple_Instrument(
                    x, y, z, elementXYZ=False,
                    instrument=int(element["Properties"].get("乐器", 0)),
                    pitch=int(element["Properties"]["音高"]),
                    velocity=element["Properties"]["音量"],
                    rated_oltage=element["Properties"]["额定电压"],
                    is_ideal_model=bool(element["Properties"]["理想模式"]),
                    is_single=bool(element["Properties"]["脉冲"])
                )
                for attr, val in element["Properties"].items():
                    if attr.startswith("音高"):
                        obj.add_note(int(val))
            else:
                obj = crt_element(experiment, element["ModelID"], x, y, z, elementXYZ=False)
                obj.data["Properties"] = element["Properties"]
                obj.data["Properties"]["锁定"] = 1.0
            # 设置角度信息
            rotation = eval(f'({element["Rotation"]})')
            r_x, r_y, r_z = rotation[0], rotation[2], rotation[1]
            obj.set_rotation(r_x, r_y, r_z)
            obj.data['Identifier'] = element['Identifier']

        elif experiment.experiment_type == ExperimentType.Celestial:
            obj = crt_element(experiment, element["Model"], x, y, z)
            obj.data = element
        elif experiment.experiment_type == ExperimentType.Electromagnetism:
            obj = crt_element(experiment, element["ModelID"], x, y, z)
            obj.data = element
        else:
            raise errors.InternalError

def _load_wires(experiment: _Experiment, _wires: list) -> None:
    assert experiment.experiment_type == ExperimentType.Circuit

    for wire_dict in _wires:
        experiment.Wires.add(
            Wire(
                Pin(get_element_from_identifier(experiment, wire_dict["Source"]), wire_dict["SourcePin"]),
                Pin(get_element_from_identifier(wire_dict["Target"]), wire_dict["TargetPin"]),
                wire_dict["ColorName"][0] # e.g. "蓝"
            )
        )

@_check_method
def load_elements(experiment: _Experiment) -> _Experiment:
    ''' 读取实验已有状态 '''
    if experiment.is_load_elements:
        errors.warning("experiment has been read")
        return experiment
    experiment.is_load_elements = True
    if experiment.open_mode == OpenMode.crt:
        errors.warning("can not read because you create this experiment")
        return experiment

    status_sav = json.loads(experiment.PlSav["Experiment"]["StatusSave"])

    if experiment.experiment_type == ExperimentType.Circuit:
        _load_elements(experiment, status_sav["Elements"])
        _load_wires(experiment, status_sav["Wires"])
    elif experiment.experiment_type == ExperimentType.Celestial:
        _load_elements(experiment, list(status_sav["Elements"].values()))
    elif experiment.experiment_type == ExperimentType.Electromagnetism:
        _load_elements(experiment, status_sav["Elements"])
    else:
        raise errors.InternalError

    return experiment

class Experiment(_Experiment):
    def __enter__(self) -> _Experiment:
        if self.open_mode != OpenMode.crt:
            load_elements(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # 如果无异常抛出且用户未在with语句里调用过.exit(), 则保存存档并退出实验
        if exc_type is None and _ExperimentStack.inside(self):
            self.save()
            self.exit(delete=False)

class experiment:
    def __init__(
            self,
            sav_name: str,
            load_elements: bool = False,
            delete: bool = False,
            write: bool = True,
            elementXYZ: bool = False,
            experiment_type: ExperimentType = ExperimentType.Circuit,
            extra_filepath: Optional[str] = None,
            force_crt: bool = False,
            is_exit: bool = False,
    ) -> None:
        errors.warning("`with experiment` is deprecated, use `with Experiment` instead")
        if not isinstance(sav_name, str) or \
                not isinstance(load_elements, bool) or \
                not isinstance(delete, bool) or \
                not isinstance(elementXYZ, bool) or \
                not isinstance(write, bool) or \
                not isinstance(experiment_type, ExperimentType) or \
                not isinstance(force_crt, bool) or \
                not isinstance(is_exit, bool) or \
                not isinstance(extra_filepath, (str, type(None))):
            raise TypeError

        self.sav_name: str = sav_name
        self.load_elements: bool = load_elements
        self.delete: bool = delete
        self.write: bool = write
        self.elementXYZ: bool = elementXYZ
        self.experiment_type: ExperimentType = experiment_type
        self.extra_filepath: Optional[str] = extra_filepath
        self.force_crt: bool = force_crt
        self.is_exit: bool = is_exit

    def __enter__(self) -> _Experiment:
        if self.force_crt:
            self._Experiment: _Experiment = _Experiment(OpenMode.crt, self.sav_name, self.experiment_type, True)
        else:
            try:
                self._Experiment: _Experiment = _Experiment(OpenMode.load_by_sav_name, self.sav_name)
            except errors.ExperimentNotExistError:
                self._Experiment: _Experiment = _Experiment(OpenMode.crt, self.sav_name, self.experiment_type, False)

        if self.load_elements:
            load_elements(self._Experiment)

        if self.elementXYZ:
            if self._Experiment.experiment_type != ExperimentType.Circuit:
                _ExperimentStack.remove(self._Experiment)
                raise errors.ExperimentTypeError
            import physicsLab.circuit.elementXYZ as _elementXYZ
            _elementXYZ.set_elementXYZ(True)

        return self._Experiment

    def __exit__(self, exc_type, exc_val, traceback) -> None:
        if exc_type is not None:
            self._Experiment.exit()
            return

        if self.is_exit:
            self._Experiment.exit()
            return
        if self.write and not self.delete:
            self._Experiment.save(extra_filepath=self.extra_filepath)
        self._Experiment.exit(delete=self.delete)
