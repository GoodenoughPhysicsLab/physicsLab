# -*- coding: utf-8 -*-
import physicsLab.circuit.elementXYZ as _elementXYZ

from physicsLab import _tools
from physicsLab import errors
from physicsLab.circuit import elements

from physicsLab.experiment import stack_Experiment
from physicsLab.typehint import numType, Optional, Union, List
from physicsLab.circuit.elements._elementBase import CircuitBase

def crt_Element(name: str,
                x: numType = 0,
                y: numType = 0,
                z: numType = 0,
                elementXYZ: Optional[bool] = None,
                *args,
                **kwargs
) -> CircuitBase:
    ''' 创建原件，本质上仍然是实例化 '''
    if not (isinstance(name, str)
            and isinstance(x, (int, float))
            and isinstance(y, (int, float))
            and isinstance(z, (int, float))
    ):
        raise TypeError

    name = name.strip()
    x, y, z = _tools.roundData(x, y, z) # type: ignore
    if (name == '555 Timer'):
        return elements.NE555(x, y, z, elementXYZ)
    elif (name == '8bit Input'):
        return elements.eight_bit_Input(x, y, z, elementXYZ)
    elif (name == '8bit Display'):
        return elements.eight_bit_Display(x, y, z, elementXYZ)
    else:
        return eval(f"elements.{name.replace(' ', '_').replace('-', '_')}"
                    f"({x}, {y}, {z}, {elementXYZ}, *{args}, **{kwargs})")

def get_Element(x: Optional[numType] = None,
                y: Optional[numType] = None,
                z: Optional[numType] = None,
                *,
                index: Optional[numType] = None,
                **kwargs
) -> Union[CircuitBase, List[CircuitBase]]:
    ''' 获取对应坐标的元件的reference '''
    # 通过坐标索引元件
    def position_get(x: numType, y: numType, z: numType):
        if not (
            isinstance(x, (int, float))
            and isinstance(y, (int, float))
            and isinstance(z, (int, float))
        ):
            raise TypeError

        position = _tools.roundData(x, y, z)
        if position not in _Expe.elements_Position.keys():
            if "defualt" in kwargs:
                return kwargs["defualt"]
            raise errors.ElementNotFound(f"{position} do not exist")

        result: list = _Expe.elements_Position[position]
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

    _Expe = stack_Experiment.top()
    if None not in [x, y, z]:
        return position_get(x, y, z)
    elif index is not None:
        return index_get(index)
    else:
        raise TypeError

def del_Element(
        self: CircuitBase # self是物实三大实验支持的所有元件
) -> None:
    ''' 删除原件 '''
    if not isinstance(self, CircuitBase):
        raise TypeError

    identifier = self.data["Identifier"] # type: ignore

    _Expe = stack_Experiment.top()

    res_Wires = set()
    for a_wire in _Expe.Wires:
        if a_wire.Source.element_self.data["Identifier"] == identifier or \
           a_wire.Target.element_self.data["Identifier"] == identifier:
           continue

        res_Wires.add(a_wire)
    _Expe.Wires = res_Wires

    # 删除elements_Position中的引用
    for elements in _Expe.elements_Position.values():
        if self in elements:
            elements.remove(self)
            break

    # 删除elements_Index中的引用
    for element in _Expe.Elements:
        if element is self:
            _Expe.Elements.remove(self)
            break

# 原件的数量
def count_Elements() -> int:
    return len(stack_Experiment.top().Elements)

# 清空原件
def clear_Elements() -> None:
    _Expe = stack_Experiment.top()
    _Expe.Wires.clear()
    _Expe.Elements.clear()
    _Expe.elements_Position.clear()