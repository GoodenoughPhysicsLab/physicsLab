# -*- coding: utf-8 -*-
from physicsLab import _tools
from physicsLab import errors
from physicsLab import circuit
from physicsLab.elementBase import ElementBase
from physicsLab.enums import ExperimentType
from physicsLab.experiment import get_Experiment
from physicsLab.typehint import numType, Optional, Union, List

def crt_Element(name: str,
                x: numType = 0,
                y: numType = 0,
                z: numType = 0,
                elementXYZ: Optional[bool] = None,
                *args,
                **kwargs
) -> ElementBase:
    ''' 创建原件，本质上仍然是实例化 '''
    if not (isinstance(name, str)
            and isinstance(x, (int, float))
            and isinstance(y, (int, float))
            and isinstance(z, (int, float))
    ):
        raise TypeError

    name = name.strip().replace(' ', '_').replace('-', '_')
    x, y, z = _tools.roundData(x, y, z) # type: ignore
    _Expe = get_Experiment()
    if _Expe.experiment_type == ExperimentType.Circuit:
        if (name == '555_Timer'):
            return circuit.NE555(x, y, z, elementXYZ)
        elif (name == '8bit_Input'):
            return circuit.eight_bit_Input(x, y, z, elementXYZ)
        elif (name == '8bit_Display'):
            return circuit.eight_bit_Display(x, y, z, elementXYZ)
        else:
            return eval(f"circuit.{name}({x}, {y}, {z}, {elementXYZ}, *{args}, **{kwargs})")
    elif _Expe.experiment_type == ExperimentType.Celestial:
        from physicsLab import celestial
        return eval(f"celestial.{name}({x}, {y}, {z})")
    elif _Expe.experiment_type == ExperimentType.Electromagnetism:
        from physicsLab import electromagnetism
        return eval(f"electromagnetism.{name}({x}, {y}, {z})")
    else:
        raise errors.InternalError

def get_Element(x: Optional[numType] = None,
                y: Optional[numType] = None,
                z: Optional[numType] = None,
                *,
                index: Optional[int] = None,
                **kwargs
) -> Union[ElementBase, List[ElementBase]]:
    ''' 获取对应坐标的元件的reference '''
    # 通过坐标索引元件
    def position_get(x: numType, y: numType, z: numType):
        if not isinstance(x, (int, float)) or \
                not isinstance(y, (int, float)) or \
                not isinstance(z, (int, float)):
            raise TypeError

        position = _tools.roundData(x, y, z)
        if position not in _Expe.elements_Position.keys():
            if "defualt" in kwargs:
                return kwargs["defualt"]
            raise errors.ElementNotFound(f"{position} do not exist")

        result: list = _Expe.elements_Position[position] # type: ignore -> type(position) ==
                                                         # Tuple[numType, numType, numType]
        return result[0] if len(result) == 1 else result

    # 通过index（元件生成顺序）索引元件
    def index_get(index: int):
        if not isinstance(index, int):
            raise TypeError

        if 0 < index <= len(_Expe.Elements):
            return _Expe.Elements[index - 1]
        else:
            if "defualt" in kwargs:
                return kwargs["defualt"]
            raise errors.ElementNotFound

    _Expe = get_Experiment()
    if x is not None and y is not None and z is not None:
        return position_get(x, y, z)
    elif index is not None:
        return index_get(index)
    else:
        raise TypeError

def del_Element(element: ElementBase) -> None:
    ''' 删除原件
        @param element: 三大实验的元件
    '''
    if not isinstance(element, ElementBase):
        raise TypeError

    identifier = element.data["Identifier"] # type: ignore

    _Expe = get_Experiment()

    res_Wires = set()
    for a_wire in _Expe.Wires:
        if a_wire.Source.element_self.data["Identifier"] == identifier or \
           a_wire.Target.element_self.data["Identifier"] == identifier:
           continue

        res_Wires.add(a_wire)
    _Expe.Wires = res_Wires

    # 删除elements_Position中的引用
    for elements in _Expe.elements_Position.values():
        if element in elements:
            elements.remove(element)
            break

    # 删除elements_Index中的引用
    for element in _Expe.Elements:
        if element is element:
            _Expe.Elements.remove(element)
            break

# 原件的数量
def count_Elements() -> int:
    return len(get_Experiment().Elements)

# 清空原件
def clear_Elements() -> None:
    _Expe = get_Experiment()
    _Expe.Wires.clear()
    _Expe.Elements.clear()
    _Expe.elements_Position.clear()
