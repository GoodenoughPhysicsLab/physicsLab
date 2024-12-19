# -*- coding: utf-8 -*-
from datetime import datetime

def id_to_time(id: str) -> datetime:
    ''' 从 用户id/实验id 中获取其对应的时间
    '''
    seconds = int(id[0:8], 16)
    return datetime.fromtimestamp(seconds)
