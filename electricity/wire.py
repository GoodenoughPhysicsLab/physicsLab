#coding=utf-8
import physicsLab._fileGlobals as _fileGlobals
import electricity.elementPin as _elementPin

# 老版本连接导线函数，不推荐使用
def old_crt_wire(SourceLabel, SourcePin : int, TargetLabel, TargetPin : int, color = "蓝") -> None: # SourceLabel : Union[_element, tuple]
    SourcePin, TargetPin = int(SourcePin), int(TargetPin)
    if (isinstance(SourceLabel, tuple) and len(SourceLabel) == 3):
        SourceLabel = _fileGlobals.elements_Address[SourceLabel]
    elif (SourceLabel not in _fileGlobals.elements_Address.values()):
        raise RuntimeError("SourceLabel must be a Positon or self")
    if (isinstance(TargetLabel, tuple) and len(TargetLabel) == 3):
        TargetLabel = _fileGlobals.elements_Address[TargetLabel]
    elif (TargetLabel not in _fileGlobals.elements_Address.values()):
        raise RuntimeError("TargetLabel must be a Positon or self")

    if (color not in ["黑", "蓝", "红", "绿", "黄"]):
        raise RuntimeError("illegal color")
    _fileGlobals.Wires.append({"Source": SourceLabel._arguments["Identifier"], "SourcePin": SourcePin,
                   "Target": TargetLabel._arguments["Identifier"], "TargetPin": TargetPin,
                   "ColorName": f"{color}色导线"})

# 检查函数参数是否是导线
def _check_typeWire(func):
    def result(SourcePin, TargetPin, color : str = '蓝') -> None:
        try:
            if isinstance(SourcePin, _elementPin.element_Pin) and isinstance(TargetPin, _elementPin.element_Pin):
                if (color not in ["黑", "蓝", "红", "绿", "黄"]):
                    raise RuntimeError("illegal color")

                func(SourcePin, TargetPin, color)
        except:
            raise RuntimeError('Error type of input function argument')
    return result

# 新版连接导线
@_check_typeWire
def crt_Wire(SourcePin, TargetPin, color: str = '蓝') -> None:
    _fileGlobals.Wires.append({"Source": SourcePin.element_self._arguments["Identifier"], "SourcePin": SourcePin.pinLabel,
                   "Target": TargetPin.element_self._arguments["Identifier"], "TargetPin": TargetPin.pinLabel,
                   "ColorName": f"{color}色导线"})

# 删除导线
@_check_typeWire
def del_Wire(SourcePin, TargetPin, color : str = '蓝') -> None:
    a_wire = {"Source": SourcePin.element_self._arguments["Identifier"], "SourcePin": SourcePin.pinLabel,
                   "Target": TargetPin.element_self._arguments["Identifier"], "TargetPin": TargetPin.pinLabel,
                   "ColorName": f"{color}色导线"}
    if (a_wire in _fileGlobals.Wires):
        _fileGlobals.Wires.remove(a_wire)
    else:
        raise RuntimeError("Unable to delete a nonexistent wire")

# 删除所有导线
def clear_Wires() -> None:
    _fileGlobals.Wires.clear()

# 获取当前导线数
def count_Wires() -> int:
    return len(_fileGlobals.Wires)