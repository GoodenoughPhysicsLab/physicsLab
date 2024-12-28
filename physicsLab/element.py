# -*- coding: utf-8 -*-
import json
from . import _tools
from . import errors
from .enums import Category, ExperimentType
from .Experiment import Experiment, _ExperimentStack
from .web.api import User
from .circuit.wire import _read_wires
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

def get_element_from_index(experiment: Experiment, index: int, **kwargs: dict):
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

def _read_elements(experiment: Experiment, _elements: list) -> None:
    assert isinstance(_elements, list)

    for element in _elements:
        position = eval(f"({element['Position']})")
        x, y, z = position[0], position[2], position[1]

        # 实例化对象
        if experiment.experiment_type == ExperimentType.Circuit:
            if element["ModelID"] == "Simple Instrument":
                from .circuit.elements.otherCircuit import Simple_Instrument
                obj = Simple_Instrument(
                    x, y, z, elementXYZ=False,
                    instrument=int(element["Properties"]["乐器"]),
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

def read_plsav(experiment: Experiment) -> Experiment:
    ''' 读取实验已有状态 '''
    if not experiment.is_open_or_crt:
        raise errors.ExperimentNotOpenError
    if experiment.is_readed:
        errors.warning("experiment has been read")
        return experiment
    experiment.is_readed = True
    if experiment.is_crted:
        errors.warning("can not read because you create this experiment")
        return experiment

    status_sav = json.loads(experiment.PlSav["Experiment"]["StatusSave"])

    # TODO 需要 read_CameraSave 吗?
    if experiment.experiment_type == ExperimentType.Circuit:
        _read_elements(experiment, status_sav["Elements"])
        _read_wires(experiment, status_sav["Wires"])
    elif experiment.experiment_type == ExperimentType.Celestial:
        _read_elements(experiment, list(status_sav["Elements"].values()))
    elif experiment.experiment_type == ExperimentType.Electromagnetism:
        _read_elements(experiment, status_sav["Elements"])
    else:
        raise errors.InternalError

    return experiment

def read_plsav_from_web(
        experiment: Experiment,
        id: str,
        category: Category,
        user: Optional[User] = None,
        no_read_experiment_status: bool = False,
) -> Experiment:
    ''' 获取已经发布到物实的实验的实验状态(包括元件, 导线, 发布后的标题, 实验介绍)

        由于存档名与发布后的标题可以不同, 因此该方法只会修改发布后的标题, 不会修改存档名
        @sav_name: 获取到的实验保存到本地存档的名字
        @id: 物实实验的id
        @category: 实验区还是黑洞区
    '''
    if not experiment.is_open_or_crt:
        raise errors.ExperimentHasOpenError
    if not isinstance(id, str) or \
        not isinstance(category, Category) or \
        not isinstance(no_read_experiment_status, bool):
        raise TypeError

    if user is None:
        user = User()

    _summary = user.get_summary(id, category)["Data"]
    if not no_read_experiment_status:
        _experiment = user.get_experiment(_summary["ContentID"])["Data"]
        status_sav = json.loads(_experiment["StatusSave"])
        experiment._read_CameraSave(_experiment["CameraSave"])

        if experiment.experiment_type == ExperimentType.Circuit:
            _read_elements(experiment, status_sav["Elements"])
            _read_wires(experiment, status_sav["Wires"])
        elif experiment.experiment_type == ExperimentType.Celestial:
            _read_elements(experiment, list(status_sav["Elements"].values()))
        elif experiment.experiment_type == ExperimentType.Electromagnetism:
            _read_elements(experiment, status_sav["Elements"])
        else:
            raise errors.InternalError

    del _summary["$type"]
    _summary["Category"] = category.value
    experiment.PlSav["Summary"] = _summary
    return experiment

class experiment:
    ''' 仅提供通过with操作存档的高层次api '''
    def __init__(self,
                 sav_name: str, # 实验名(非存档文件名)
                 read: bool = False, # 是否读取存档原有状态
                 delete: bool = False, # 是否删除实验
                 write: bool = True, # 是否写入实验
                 elementXYZ: bool = False, # 元件坐标系
                 experiment_type: ExperimentType = ExperimentType.Circuit, # 若创建实验，支持传入指定实验类型
                 extra_filepath: Optional[str] = None, # 将存档写入额外的路径
                 force_crt: bool = False, # 强制创建一个实验, 若已存在则覆盖已有实验
                 is_exit: bool = False, # 退出试验
                 ):
        if not isinstance(sav_name, str) or \
                not isinstance(read, bool) or \
                not isinstance(delete, bool) or \
                not isinstance(elementXYZ, bool) or \
                not isinstance(write, bool) or \
                not isinstance(experiment_type, ExperimentType) or \
                not isinstance(force_crt, bool) or \
                not isinstance(is_exit, bool) or \
                not isinstance(extra_filepath, (str, type(None))):
            raise TypeError

        self.savName: str = sav_name
        self.read: bool = read
        self.delete: bool = delete
        self.write: bool = write
        self.elementXYZ: bool = elementXYZ
        self.ExperimentType: ExperimentType = experiment_type
        self.extra_filepath: Optional[str] = extra_filepath
        self.force_crt: bool = force_crt
        self.is_exit: bool = is_exit

    def __enter__(self) -> Experiment:
        if self.force_crt:
            self._Experiment: Experiment = Experiment().crt(self.savName, self.ExperimentType, force_crt=True)
        else:
            self._Experiment: Experiment = Experiment().open_or_crt(self.savName, self.ExperimentType)

        if self.read:
            read_plsav(self._Experiment)
        if self.elementXYZ:
            if self._Experiment.experiment_type != ExperimentType.Circuit:
                _ExperimentStack.pop()
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
            self._Experiment.write(extra_filepath=self.extra_filepath)
        if self.delete:
            self._Experiment.delete()
            return
