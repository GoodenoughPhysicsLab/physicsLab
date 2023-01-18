'''
    这个是xuzhengx曾经的一个精选
    用来当做他的 物实程序化3.py 的示例代码
'''
import sys
sys.path.append("C:/Users/Administrator/AppData/LocalLow/CIVITAS/Quantum Physics/Circuit/python/include")
from xuzhengxPhysicsLab import *

default_path = r"C:\Users\Administrator\AppData\LocalLow\CIVITAS\Quantum Physics\Circuit"
source_file = '08fa0eb3-68d9-450c-8e6d-0670abb54aa9.sav'
element_manager = ElementManager(default_path, source_file)
element_manager.load_file('6e6a0b14-ab91-4e55-a3e2-a149e5a9b92f.sav')
element_manager.clear_experiment()

x, y = 4, 4

resistance_law_elements_a = [[], [], [], []]  # 中间细胞
resistance_law_elements_b = [[], [], [], []]  # 周围细胞


def get_erl(n):
    pos = (x * 4 + 1, y + 1)
    erl = []
    maxn = max([len(resistance_law_elements_a[p]) for p in range(3)])
    if maxn:
        for pin in range(4):
            if len(resistance_law_elements_a[pin]) == maxn:
                erl.append(resistance_law_elements_a[pin].pop())
                break
    else:
        e = element_manager.create_element('R', 'Resistance Law', pos)
        e.set_attr(2.0, 'Properties', '长度')
        erl.append(e)
        for p in range(1, 4):
            resistance_law_elements_a[p].append(e)
        pin = 0

    if len(resistance_law_elements_b[pin]) >= n - 1:
        for i in range(n - 1):
            erl.append(resistance_law_elements_b[pin].pop())
    else:
        d = n - 1 - len(resistance_law_elements_b[pin])
        erl.extend(resistance_law_elements_b[pin])
        resistance_law_elements_b[pin] = []
        for i in range(d):
            e = element_manager.create_element('R', 'Resistance Law', pos)
            erl.append(e)
            for p in range(4):
                if p != pin:
                    resistance_law_elements_b[p].append(e)
    return pin, erl


e_start = element_manager.create_element('重置', 'Push Switch', (0, -1))
e_nstart = element_manager.create_element('未重置', 'No Gate', (2, -1))
e_source = element_manager.create_element('电源', 'No Gate', (0, -2))
element_manager.create_wire(e_source, 1, e_start, 0)
element_manager.create_wire(e_start, 1, e_nstart, 0)

e_next = element_manager.create_element('下一个', 'Push Switch', (4, -1))
element_manager.create_wire(e_source, 1, e_next, 0)

e_clka = element_manager.create_element('时钟a', 'Or Gate', (-2, y))
e_clkb = element_manager.create_element('时钟b', 'Yes Gate', (-2, y + 1))
e_clkc = element_manager.create_element('时钟', 'Yes Gate', (-2, y + 2))
element_manager.create_wire(e_clka, 2, e_clkb, 0)
element_manager.create_wire(e_clkb, 1, e_clkc, 0)
element_manager.create_wire(e_start, 1, e_clka, 0)  # 重置
element_manager.create_wire(e_next, 1, e_clka, 1)  # 下一个

for i in range(x):
    for j in range(y):
        ea = element_manager.create_element('输入%d%d' % (i, j), 'Logic Input', (i * 2, j))
        eb = element_manager.create_element('存储%d%d' % (i, j), 'D Flipflop', (i * 2, j * 2 + y + 0.5))
        ec = element_manager.create_element('输出%d%d' % (i, j), 'Logic Output', ((x + i) * 2, j))
        ed = element_manager.create_element('选择%d%d' % (i, j), 'Multiplier', (i * 2, j * 2 + 3 * y + 0.5))

        element_manager.create_wire(eb, 0, ec, 0)  # 输出
        element_manager.create_wire(ed, 2, eb, 2)  # 输入
        element_manager.create_wire(ea, 0, ed, 7)  # 10时重置
        element_manager.create_wire(e_start, 1, ed, 4)  # 重置位
        element_manager.create_wire(e_nstart, 1, ed, 5)  # 计算
        element_manager.create_wire(eb, 3, e_clkc, 1)  # 更新

for i in range(x):
    for j in range(y):
        edl = []
        ed = element_manager.find_element('存储%d%d' % (i, j))[0]
        edl.append(ed)
        n = 1
        for ii in range(i - 1, i + 2):
            for jj in range(j - 1, j + 2):
                if 0 <= ii < x and 0 <= jj < y and (ii, jj) != (i, j):
                    e = element_manager.find_element('存储%d%d' % (ii, jj))[0]
                    edl.append(e)
                    n += 1
        pin, erl = get_erl(n)
        for k in range(n):
            element_manager.create_wire(edl[k], 0, erl[k], pin)

        em = element_manager.find_element('选择%d%d' % (i, j))[0]
        if n <= 4:
            minv = 2.5 / (n - 0.5) * 3 * 2
            ey = element_manager.create_element('', 'Yes Gate', (2 * (x + i), y + j * 2))
            ey.set_attr(minv - 0.01, 'Properties', '高电平')
            for k in range(n):
                element_manager.create_wire(erl[k], pin + 4, ey, 0)
            element_manager.create_wire(ey, 1, em, 6)
        else:
            minv = 2.5 / (n - 0.5) * 3 * 2
            maxv = 3.5 / (n - 0.5) * 3 * 2
            en = element_manager.create_element('', 'No Gate', (2 * (x + i), y + j * 2))
            en.set_attr(maxv + 0.01, 'Properties', '高电平')
            ea = element_manager.create_element('', 'And Gate', (2 * (x + i), y + j * 2 + 1))
            ea.set_attr(minv - 0.01, 'Properties', '高电平')
            for k in range(n):
                element_manager.create_wire(erl[k], pin + 4, en, 0)
            # element_manager.create_wire(erl[k], pin+4, ea, 1)
            element_manager.create_wire(en, 0, ea, 1)
            element_manager.create_wire(en, 1, ea, 0)
            element_manager.create_wire(ea, 2, em, 6)

element_manager.rename('生命游戏-数模结合（申精）')
element_manager.save('7d6a4b60-eaae-4966-8fdd-c7cfd9a8d9c2.sav')