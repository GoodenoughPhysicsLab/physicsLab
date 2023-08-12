#coding=utf-8
import physicsLab._tools as _tools
import physicsLab.errors as errors
import physicsLab._fileGlobals as _fileGlobals
import physicsLab.electricity.elementXYZ as _elementXYZ
import physicsLab.electricity.elementsClass as _elementsClass

from typing import *

# 创建原件，本质上仍然是实例化
def crt_Element(
        name: str,
        x: _tools.numType = 0,
        y: _tools.numType = 0,
        z: _tools.numType = 0,
        elementXYZ: Optional[bool] = None
    ):
    if not (isinstance(name, str)
            and isinstance(x, (int, float))
            and isinstance(y, (int, float))
            and isinstance(z, (int, float))
    ):
        raise RuntimeError("Wrong parameter type")

    name = name.strip()
    if name == '':
        raise RuntimeError('Name cannot be an empty string')
        # 元件坐标系
    if elementXYZ == True or (_elementXYZ.is_elementXYZ() == True and elementXYZ is None):
        x, y, z = _elementXYZ.xyzTranslate(x, y, z)
    x, y, z = _tools.roundData(x, y, z)
    if (name == '555 Timer'):
        return _elementsClass.NE555(x, y, z)
    elif (name == '8bit Input'):
        return _elementsClass.eight_bit_Input(x, y, z)
    elif (name == '8bit Display'):
        return _elementsClass.eight_bit_Display(x, y, z)
    else:
        try:
            return eval(f"_elementsClass.{name.replace(' ', '_').replace('-', '_')}({x},{y},{z})")
        except SyntaxError:
            raise RuntimeError(f"{name} original that does not exist")

# 获取对应坐标的self
def get_Element(*args, **kwargs) -> _elementsClass.electricityBase:
    # 通过坐标索引元件
    def position_Element(x: _tools.numType, y: _tools.numType, z: _tools.numType):
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
            raise TypeError('illegal argument')
        position = _tools.roundData(x, y, z)
        if position not in _fileGlobals.elements_Position.keys():
            raise RuntimeError(f"{position} do not exist")
        result: list = _fileGlobals.elements_Position[position]
        return result[0] if len(result) == 1 else result
    # 通过index（元件生成顺序）索引元件
    def index_Element(index: int):
        if 0 < index <= len(_fileGlobals.elements_Index):
            return _fileGlobals.elements_Index[index - 1]
        else:
            raise errors.getElementError

#    _fileGlobals.check_ExperimentType(0)

    # 如果输入参数为 x=, y=, z=
    if list(kwargs.keys()) == ['x', 'y', 'z']:
        return position_Element(kwargs['x'], kwargs['y'], kwargs['z'])
    # 如果输入参数为 index=
    elif list(kwargs.keys()) == ['index']:
        return index_Element(kwargs['index'])
    # 如果输入的参数在args
    elif all(isinstance(value, (int, float)) for value in args):
        # 如果输入参数为坐标
        if args.__len__() == 3:
            return position_Element(args[0], args[1], args[2])
        # 如果输入参数为self._index
        elif args.__len__() == 1:
            return index_Element(args[0])
        else:
            raise TypeError
    else:
        raise TypeError

# 删除原件
def del_Element(self: _elementsClass.electricityBase) -> None:
#    self是物实三大实验支持的所有元件

    if not isinstance(self, _elementsClass.electricityBase):
        raise TypeError

    identifier = self._arguments["Identifier"]

    # 删除Elements中的引用
    for element in _fileGlobals.Elements:
        if element["Identifier"] == identifier:
            _fileGlobals.Elements.remove(element)
            break


    i = 0
    while i < _fileGlobals.Wires.__len__():
        wire = _fileGlobals.Wires[i]
        if wire['Source'] == identifier or wire['Target'] == identifier:
            _fileGlobals.Wires.pop(i)
        else:
            i += 1

    # 删除elements_Position中的引用
    for elements in _fileGlobals.elements_Position.values():
        if self in elements:
            elements.remove(self)
            break

    # 删除elements_Index中的引用
    for element in _fileGlobals.elements_Index:
        if element is self:
            _fileGlobals.elements_Index.remove(self)
            break

# 原件的数量
def count_Elements() -> int:
    return len(_fileGlobals.Elements)

# 清空原件
def clear_Elements() -> None:
    _fileGlobals.Elements.clear()
    _fileGlobals.Wires.clear()
    _fileGlobals.elements_Index.clear()
    _fileGlobals.elements_Position.clear()

# 打印物实存档格式的所有元件
def print_Elements() -> None:
    print(_fileGlobals.Elements)