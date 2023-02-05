# Òý½ÅÀà
class element_Pin:
    def __init__(self, input_self,  pinLabel : int):
        self.element_self = input_self
        self.pinLabel = pinLabel

    def type(self) -> str:
        return 'element Pin'