#coding=utf-8
import physicsLab.errors as errors
import physicsLab._fileGlobals as _fileGlobals
import physicsLab.electricity.elementPin as _elementPin

# 检查函数参数是否是导线
def _check_typeWire(func):
    def result(SourcePin: "_elementPin.element_Pin", TargetPin: "_elementPin.element_Pin", color: str = '蓝') -> None:
        if (
                isinstance(SourcePin, _elementPin.element_Pin) and
                isinstance(TargetPin, _elementPin.element_Pin)
        ):
            # 将英文的color转换为中文
            if color in ("black", "blue", "red", "green", "yellow"):
                color = {"black": "黑", "blue": "蓝", "red": "红", "green": "绿", "yellow": "黄"}[color]

            if (color not in ("黑", "蓝", "红", "绿", "黄")):
                raise errors.wireColorError

            _fileGlobals.check_ExperimentType(0)

            func(SourcePin, TargetPin, color)

    return result

# 新版连接导线
@_check_typeWire
def crt_Wire(SourcePin: "_elementPin.element_Pin", TargetPin: "_elementPin.element_Pin", color: str = '蓝') -> None:
    _fileGlobals.Wires.append({"Source": SourcePin.element_self._arguments["Identifier"], "SourcePin": SourcePin.pinLabel,
                   "Target": TargetPin.element_self._arguments["Identifier"], "TargetPin": TargetPin.pinLabel,
                   "ColorName": f"{color}色导线"})

# 删除导线
@_check_typeWire
def del_Wire(SourcePin: "_elementPin.element_Pin", TargetPin: "_elementPin.element_Pin", color: str = '蓝') -> None:
    a_wire = {
        "Source": SourcePin.element_self._arguments["Identifier"], "SourcePin": SourcePin.pinLabel,
        "Target": TargetPin.element_self._arguments["Identifier"], "TargetPin": TargetPin.pinLabel,
        "ColorName": f"{color}色导线"
    }
    if a_wire in _fileGlobals.Wires:
        _fileGlobals.Wires.remove(a_wire)
    else:
        a_wire = {
            "Source": TargetPin.element_self._arguments["Identifier"], "SourcePin": TargetPin.pinLabel,
            "Target": SourcePin.element_self._arguments["Identifier"], "TargetPin": SourcePin.pinLabel,
            "ColorName": f"{color}色导线"
        }
        if a_wire in _fileGlobals.Wires:
            _fileGlobals.Wires.remove(a_wire)
        else:
            raise errors.wireNotFoundError

# 删除所有导线
def clear_Wires() -> None:
    _fileGlobals.check_ExperimentType(0)
    _fileGlobals.Wires.clear()

# 获取当前导线数
def count_Wires() -> int:
    _fileGlobals.check_ExperimentType(0)
    return len(_fileGlobals.Wires)

# 打印导线的json
def print_Wires() -> None:
    print(_fileGlobals.Wires)