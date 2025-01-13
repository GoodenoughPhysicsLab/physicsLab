# -*- coding: utf-8 -*-
''' 对Physics-Lab-AR(Quantam Physics)进行操作的API '''
import os
import json
import platform

from getpass import getuser
from typing import Optional, Tuple

if platform.system() == "Windows":
    WIN_PLAR_HOME_DIR = f"C:\\Users\\{getuser()}\\AppData\\LocalLow\\CIVITAS\\Quantum Physics"

_plar_version_mem: Optional[Tuple[int, int, int]] = None

def get_plAR_version() -> Optional[Tuple[int, int, int]]:
    ''' 获取物实版本 '''
    global _plar_version_mem
    if _plar_version_mem is not None:
        return _plar_version_mem

    if platform.system() != "Windows":
        return None

    try:
        a_dir = os.listdir(os.path.join(WIN_PLAR_HOME_DIR, "Unity"))
        if len(a_dir) != 1:
            return None

        a_file = os.path.join(WIN_PLAR_HOME_DIR, "Unity", a_dir[0], "Analytics", "values")

        with open(a_file) as f:
            ver_str: str = json.load(f)['app_ver']
        _plar_version_mem = eval(f"({ver_str.replace('.', ',')})")
        return _plar_version_mem
    except (json.decoder.JSONDecodeError, UnicodeDecodeError, FileNotFoundError):
        return None

def get_plAR_path() -> Optional[str]:
    ''' 获取物实路径 '''
    if platform.system() != "Windows":
        return None

    with open(os.path.join(WIN_PLAR_HOME_DIR, "Player-prev.log")) as f:
        f.readline()
        f.readline()
        res = os.path.dirname(os.path.dirname(f.readline()[25:-2]))

    if res == "":
        return None
    return res
