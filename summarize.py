# -*- coding: utf-8 -*-
import os
from typing import List

ignores: List[str] = [
    #
]

if __name__ == "__main__":
    len_py_file: int = 0
    count_line: int = 0

    for root, dirs, files in os.walk("physicsLab"):
        dirs.remove("__pycache__")
        for file in files:
            if file in ignores:
                continue

            len_py_file += 1
            with open(f"{root}/{file}", encoding="utf-8") as f:
                count_line += len(f.read().splitlines())

    print("lines of physicsLab: ", count_line)
    print("amount of python files: ", len_py_file)
