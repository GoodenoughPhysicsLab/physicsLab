# -*- coding: utf-8 -*-
import base64

from physicsLab import errors
from physicsLab.Experiment import Experiment
from physicsLab.circuit.elements import CircuitBase
from physicsLab.typehint import TypedDict, Self, List, Optional

class _PlotDataDict(TypedDict):
    Name: str
    LabelX: str
    LabelY: str
    Series: List[dict]

class Plot:
    def __init__(self, data: _PlotDataDict):
        if not isinstance(data, dict):
            raise TypeError

        self.data = data

    def add_dependent_var(self, element: CircuitBase, color: int = 0x5778a4) -> Self:
        ''' 添加一个因变量
            * element: 与因变量有关的元件
            * color: 使用16进制表示颜色
        '''
        if not isinstance(element, CircuitBase) or \
                color is not None and not isinstance(color, int):
            raise TypeError
        if color < 0:
            raise ValueError

        self.data["Series"].append({
            "Type": 0,
            "Name": element.data["Identifier"],
            "Index": 0,
            "Subject": element.__doc__,
            "Color": f"{base64.b64encode(bytes.fromhex(hex(color).replace('0x', '') + 'ff'))}",
            "Interval": 0.0,
            "SourceX": None,
            "SourceY": "电压BE",
            "SourceType": 0
        })
        return self

def add_graph_to(experiment: Experiment) -> Optional[List[Plot]]:
    ''' 获取物实示波器图表的封装类 '''
    if not isinstance(experiment, Experiment):
        raise TypeError

    if not experiment.is_open_or_crt:
        raise errors.ExperimentNotOpenError

    if experiment.PlSav["Plots"] is None:
        return None

    res = [Plot(a_graph) for a_graph in experiment.PlSav["Plots"]]
    return res
