# -*- coding: utf-8 -*-
from enum import Enum, unique

# 所有实验类型及对应的数据
@unique
class experimentType(Enum):
    # 电学实验
    Circuit = 0
    # 天体物理实验
    Celestial = 3
    # 电与磁实验
    Electromagnetism = 4