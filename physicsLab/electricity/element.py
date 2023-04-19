#coding=utf-8
import physicsLab._tools as _tools
import physicsLab._fileGlobals as _fileGlobals
from physicsLab.electricity.elementsClass import *
import physicsLab.electricity.elementXYZ as _elementXYZ

# 创建原件，本质上仍然是实例化
def crt_Element(name: str,
                x: _tools.number = 0,
                y: _tools.number = 0,
                z: _tools.number = 0,
                elementXYZ: bool = None):
    if not (isinstance(name, str)
            and isinstance(x, (int, float))
            and isinstance(y, (int, float))
            and isinstance(z, (int, float))
    ):
        raise RuntimeError("Wrong parameter type")
    if name == '':
        raise RuntimeError('Name cannot be an empty string')
        # 元件坐标系
    if elementXYZ == True or (_elementXYZ.elementXYZ == True and elementXYZ is None):
        x, y, z = _elementXYZ.xyzTranslate(x, y, z)
    x, y, z = _tools.roundData(x), _tools.roundData(y), _tools.roundData(z)
    if (name == '555 Timer'):
        return NE555(x, y, z)
    elif (name == '8bit Input'):
        return eight_bit_Input(x, y, z)
    elif (name == '8bit Display'):
        return eight_bit_Display(x, y, z)
    else:
        try:
            return eval(name.replace(' ', '_').replace('-', '_') + f'({x},{y},{z})')
        except SyntaxError:
            raise RuntimeError(f"{name} original that does not exist")

# 获取对应坐标的self
def get_Element(*args, **kwargs):
    # 通过坐标索引元件
    def position_Element(x: _tools.number, y: _tools.number, z: _tools.number):
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
            raise RuntimeError('illegal argument')
        x, y, z = _tools.roundData(x), _tools.roundData(y), _tools.roundData(z)
        if (x, y, z) not in _fileGlobals.elements_Address.keys():
            raise RuntimeError("Error coordinates that do not exist")
        return _fileGlobals.elements_Address[(x, y, z)]['self']
    # 通过index（元件生成顺序）索引元件
    def index_Element(index: int):
        if 0 < index <= len(_fileGlobals.elements_Index):
            return _fileGlobals.elements_Index[index]['self']
        else:
            raise RuntimeError

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
def del_Element(self) -> None:
    try:
        identifier = self._arguments['Identifier']
        if (self.father_type() == 'element'):
            for element in _fileGlobals.Elements:
                if (identifier == element['Identifier']):
                    # 删除原件
                    _fileGlobals.Elements.remove(element)
                    # 删除导线
                    i = 0
                    while (i < _fileGlobals.Wires.__len__()):
                        wire = _fileGlobals.Wires[i]
                        if (wire['Source'] == identifier or wire['Target'] == identifier):
                            _fileGlobals.Wires.pop(i)
                        else:
                            i += 1
                    return
    except:
        raise RuntimeError('Unable to delete a nonexistent element')

# 整理物实原件的角度、位置
def format_Elements() -> None:
    pass

# 原件的数量
def count_Elements() -> int:
    return len(_fileGlobals.Elements)

# 清空原件
def clear_Elements() -> None:
    _fileGlobals.Elements.clear()
    _fileGlobals.Wires.clear()
    _fileGlobals.elements_Index.clear()
    _fileGlobals.elements_Address.clear()