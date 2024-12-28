# -*- coding: utf-8 -*-
import os

if __name__ == "__main__":
    ROOT = os.path.dirname(os.path.abspath(__file__))
    len_py_file: int = 0
    count_line: int = 0

    for root, dirs, files in os.walk(os.path.join(ROOT, "physicsLab")):
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")
        if "mido" in dirs:
            dirs.remove("mido")
        for file in files:
            len_py_file += 1
            with open(os.path.join(root, file), encoding="utf-8") as f:
                count_line += len(f.read().splitlines())

    print("lines of physicsLab: ", count_line)
    print("amount of python files: ", len_py_file)
