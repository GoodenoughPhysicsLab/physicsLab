# 用于存放自定义错误类
# 由于有时在package外需要异常处理，故不为文件私有变量
import physicsLab._colorUtils as _colorUtils

def warning(msg: str) -> None:
    _colorUtils.printf(msg, _colorUtils.YELLOW)

# 打开实验异常
class openExperimentError(Exception):
    pass

class wireColorError(Exception):
    pass

class wireNotFoundError(Exception):
    def __str__(self):
        return "Unable to delete a nonexistent wire"