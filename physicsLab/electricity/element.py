#coding=utf-8
from _fileGlobals import *
from electricity.elementsClass import *

# 创建原件，本质上仍然是实例化
def crt_Element(name: str, x : float = 0, y : float = 0, z : float = 0):
    if not (isinstance(name, str) and isinstance(x, (int, float)) and
            isinstance(y, (int, float)) and isinstance(z, (int, float))
    ):
        raise RuntimeError("Wrong parameter type")
    if name == '':
        raise RuntimeError('Name cannot be an empty string')
    x, y, z = myRound(x), myRound(y), myRound(z)
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

'''# 获取对应坐标的self
def get_Element(x : Union[int, float], y : Union[int, float], z : Union[int, float] = 0):
    global elements_Address
    if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
        raise RuntimeError('illegal argument')
    x, y, z = myRound(x), myRound(y), myRound(z)
    if (x, y, z) not in elements_Address.keys():
        raise RuntimeError("Error coordinates that do not exist")
    return elements_Address[(x, y, z)]'''

# 获取对应坐标的self
def get_Element(*args):
    if all(isinstance(value, (int, float)) for value in args):
        # 如果输入参数为坐标
        if args.__len__() == 3:
            global elements_Address
            x, y, z = args[0], args[1], args[2]
            if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
                raise RuntimeError('illegal argument')
            x, y, z = myRound(x), myRound(y), myRound(z)
            if (x, y, z) not in elements_Address.keys():
                raise RuntimeError("Error coordinates that do not exist")
            return elements_Address[(x, y, z)]
        # 如果输入参数为self._index
        elif args.__len__() == 1:
            global elements_Index
            search = args[0]
            if 0 <= search < len(elements_Index):
                return elements_Index[search]
            else:
                raise RuntimeError
        else:
            raise TypeError
    else:
        raise TypeError

# 删除原件
def del_Element(self) -> None:
    try:
        identifier = self._arguments['Identifier']
        if (self.father_type() == 'element'):
            for element in Elements:
                if (identifier == element['Identifier']):
                    # 删除原件
                    Elements.remove(element)
                    # 删除导线
                    i = 0
                    while (i < wires.__len__()):
                        wire = wires[i]
                        if (wire['Source'] == identifier or wire['Target'] == identifier):
                            wires.pop(i)
                        else:
                            i += 1
                    return
    except:
        raise RuntimeError('Unable to delete a nonexistent element')

# 整理物实原件的角度、位置
def format_Elements() -> None:
    pass

def count_Elements() -> int:
    global Elements
    return len(Elements)

def clear_Elements() -> None:
    Elements.clear()
    wires.clear()
    elements_Index.clear()
    elements_Address.clear()