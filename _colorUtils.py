BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
DEFAULT = '\033[39m'

# 打印write_Experiment的信息时是否使用彩色字
printColor = True

# 打印颜色字
def printf(msg: str, color) -> None:
    if not isinstance(msg, str):
        raise TypeError
    if printColor:
        print(f"{color}{msg}{DEFAULT}")
    else:
        print(msg)
