from typing import Union

def myRound(num : Union[int, float]):
    if isinstance(num, int):
        return float(num)
    return round(num, 4)