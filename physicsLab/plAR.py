# -*- coding: utf-8 -*-
''' 对Physics-Lab-AR(Quantam Physics)进行操作的API '''
import os
import json
import platform

from getpass import getuser
from typing import Optional, Tuple

def get_plAR_version() -> Tuple[int, int, int]:
    ''' 获取物实版本 '''
    if platform.system() != "Windows":
        return None

    try:
        a_dir = tuple(os.walk(f"C:/Users/{getuser()}/AppData/LocalLow/CIVITAS/Quantum Physics/Unity/"))[0][1]
        if len(a_dir) != 1:
            return None

        a_file = f"C:/Users/{getuser()}/AppData/LocalLow/CIVITAS/Quantum Physics/Unity/{a_dir[0]}/Analytics/values"

        with open(a_file) as f:
            ver_str: str = json.load(f)['app_ver']
        return eval(f"({ver_str.replace('.', ',')})")
    except:
        return None

def get_plAR_path() -> Optional[str]:
    ''' 获取物实路径 '''
    if platform.system() == "Windows":
        with open(f"C:/Users/{getuser()}/AppData/LocalLow/CIVITAS/Quantum Physics/Player-prev.log") as f:
            f.readline()
            f.readline()
            res = os.path.dirname(os.path.dirname(f.readline()[25:-2]))

        if res == "":
            return None
        return res
    return None
