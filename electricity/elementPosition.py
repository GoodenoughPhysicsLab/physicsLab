# 元件坐标系
# 一个非门的长为0.15，宽为0.075
# 一个非门的长宽会成为元件坐标系的x, y的单位长度
# z轴的单位长度是原坐标系的0.1
#
# 像二位乘法器这种元件的位置必须经过修正才能使元件整齐排列
# x, z轴不用修正
# y轴的修正为 +0.045

import elementsClass as ecls

# 装饰器
def xyz(elementSelf: ecls.elementObject):
    if elementSelf.isElementPosition == True:
        return 