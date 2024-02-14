# -*- coding: utf-8 -*-
import physicsLab.circuit.elementXYZ as _elementXYZ

from physicsLab import _tools
from physicsLab import errors
from physicsLab.circuit import elements

from physicsLab.experiment import stack_Experiment
from physicsLab.typehint import numType, Optional, Union, List
from physicsLab.circuit.elements._elementBase import CircuitBase

NnumType = Optional[numType]

# 创建原件，本质上仍然是实例化
def crt_Element(name: str, x: numType = 0, y: numType = 0, z: numType = 0, elementXYZ: Optional[bool] = None) -> CircuitBase:
    if not (isinstance(name, str)
            and isinstance(x, (int, float))
            and isinstance(y, (int, float))
            and isinstance(z, (int, float))
    ):
        raise RuntimeError("Wrong parameter type")

    name = name.strip()
    # 元件坐标系
    if elementXYZ is True or (_elementXYZ.is_elementXYZ() is True and elementXYZ is None):
        x, y, z = _elementXYZ.xyzTranslate(x, y, z)
    x, y, z = _tools.roundData(x, y, z) # type: ignore
    if (name == '555 Timer'):
        return elements.NE555(x, y, z)
    elif (name == '8bit Input'):
        return elements.eight_bit_Input(x, y, z)
    elif (name == '8bit Display'):
        return elements.eight_bit_Display(x, y, z)
    else:
        return eval(f"elements.{name.replace(' ', '_').replace('-', '_')}({x},{y},{z})")

# 获取对应坐标的self
def get_Element(x: NnumType=None, y: NnumType=None, z: NnumType=None, *, index: NnumType=None) -> Union[CircuitBase, List[CircuitBase]]:
    # 通过坐标索引元件
    def position_Element(x: numType, y: numType, z: numType):
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
            raise TypeError('illegal argument')

        position = _tools.roundData(x, y, z)
        if position not in _Expe.elements_Position.keys():
            raise errors.ElementNotExistError(f"{position} do not exist")

        result: list = _Expe.elements_Position[position]
        return result[0] if len(result) == 1 else result

    # 通过index（元件生成顺序）索引元件
    def index_Element(index: int):
        if not isinstance(index, int):
            raise TypeError

        if 0 < index <= len(_Expe.Elements):
            return _Expe.Elements[index - 1]
        else:
            raise errors.getElementError

    _Expe = stack_Experiment.top()
    if None not in [x, y, z]:
        return position_Element(x, y, z)
    elif index is not None:
        return index_Element(index)
    else:
        raise TypeError

# 删除原件
def del_Element(
        self: CircuitBase # self是物实三大实验支持的所有元件
) -> None:

    if not isinstance(self, CircuitBase):
        raise TypeError

    identifier = self._arguments["Identifier"] # type: ignore

    _Expe = stack_Experiment.top()

    i = 0
    while i < _Expe.Wires.__len__():
        wire = _Expe.Wires[i]
        if wire.Source.element_self._arguments["Identifier"] == identifier or wire.Target.element_self._arguments["Identifier"] == identifier:
            _Expe.Wires.pop(i)
        else:
            i += 1

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