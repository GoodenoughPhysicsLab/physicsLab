# -*- coding: utf-8 -*-
import json
from . import _tools
from . import errors
from .enums import ExperimentType
from .Experiment import Experiment, _ExperimentStack, OpenMode, _check_method
from .circuit.wire import _load_wires
from ._element_base import ElementBase
from .typehint import numType, Optional

def crt_element(
        experiment: Experiment,
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
        experiment: Experiment,
        x: numType,
        y: numType,
        z: numType,
        **kwargs: dict,
):
    ''' 通过坐标索引元件 '''
    if not isinstance(x, (int, float)) or \
            not isinstance(y, (int, float)) or \
            not isinstance(z, (int, float)):
        raise TypeError

    position = _tools.roundData(x, y, z)
    if position not in experiment._elements_position.keys():
        if "defualt" in kwargs:
            return kwargs["defualt"]
        raise errors.ElementNotFound(f"{position} do not exist")

    result: list = experiment._elements_position[position]
    return result[0] if len(result) == 1 else result

def get_element_from_index(experiment: Experiment, index: int, **kwargs: dict) -> ElementBase:
    ''' 通过index (元件生成顺序) 索引元件 '''
    if not isinstance(index, int):
        raise TypeError

    if 0 < index <= len(experiment.Elements):
        return experiment.Elements[index - 1]
    else:
        if "defualt" in kwargs:
            return kwargs["defualt"]
        raise errors.ElementNotFound

def del_element(experiment: Experiment, element: ElementBase) -> None:
    ''' 删除元件
        @param element: 三大实验的元件
    '''
    if not isinstance(element, ElementBase):
        raise TypeError

    identifier = element.data["Identifier"] # type: ignore

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

def count_elements(experiment: Experiment) -> int:
    ''' 元件的数量 '''
    return len(experiment.Elements)

def clear_elements(experiment: Experiment) -> None:
    ''' 清空元件 '''
    experiment.Wires.clear()
    experiment.Elements.clear()
    experiment._elements_position.clear()

def _load_elements(experiment: Experiment, _elements: list) -> None:
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

@_check_method
def load_elements(experiment: Experiment) -> Experiment:
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

class experiment:
    ''' 仅提供通过with操作存档的高层次api '''
    def __init__(
            self,
            sav_name: str, # 实验名(非存档文件名)
            load_elements: bool = False, # 是否导入存档的元件信息 # TODO 改为默认为True
            delete: bool = False, # 是否删除实验
            write: bool = True, # 是否写入实验
            elementXYZ: bool = False, # 元件坐标系
            experiment_type: ExperimentType = ExperimentType.Circuit, # 若创建实验，支持传入指定实验类型
            extra_filepath: Optional[str] = None, # 将存档写入额外的路径
            force_crt: bool = False, # 强制创建一个实验, 若已存在则覆盖已有实验
            is_exit: bool = False, # 退出试验而不保存修改
    ) -> None:
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
        self.ExperimentType: ExperimentType = experiment_type
        self.extra_filepath: Optional[str] = extra_filepath
        self.force_crt: bool = force_crt
        self.is_exit: bool = is_exit

    def __enter__(self) -> Experiment:
        if self.force_crt:
            self._Experiment: Experiment = Experiment(OpenMode.crt, self.sav_name, self.ExperimentType, True)
        else:
            try:
                self._Experiment: Experiment = Experiment(OpenMode.load_by_sav_name, self.sav_name)
            except errors.ExperimentNotExistError:
                self._Experiment: Experiment = Experiment(OpenMode.crt, self.sav_name, self.ExperimentType, False)

        if self.load_elements:
            load_elements(self._Experiment)

        # 也许改为先判断是否为电学实验更好?
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
