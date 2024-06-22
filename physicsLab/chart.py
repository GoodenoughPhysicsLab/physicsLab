from physicsLab.typehint import TypedDict, Self, List

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

    def add_dependent_var(self, element, color=None) -> Self:
        ''' 添加一个因变量 '''
        self.data["Series"].append({
            "Type": 0,
            "Name": element.data["Identifier"],
            "Index": 0,
            "Subject": element.__doc__,
            "Color": "5JRE/w==",
            "Interval": 0.0,
            "SourceX": None,
            "SourceY": "电压BE",
            "SourceType": 0
        })
        return self