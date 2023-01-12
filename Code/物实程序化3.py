''' 
    这个文件是xuzhengx写的 
    仅供学习与参考（当然你也没法拿这个卖钱）
    （应该是卖不出去的）
    没有通知xuzhengx，未来可能会删除
'''

import json, os, random, re, copy

DEFAULT_PATH = r"C:\Users\Administrator\AppData\LocalLow\CIVITAS\Quantum Physics\Circuit"
SOURCE_FILE = 'source.sav'
EMPTY_FILE = 'empty.sav'


class Element(object):
    '''元件类，存储元件名称、元件代码、其它内容'''

    def __init__(self, name: str, element: dict):
        '''元件名称，元件代码'''
        self.name = name
        self.element = element
        self.data = None

    def get_attr(self, *attributes):
        '''获得元件属性'''
        e = self.element
        for attr in attributes:
            e = e[attr]
        return e

    def set_attr(self, value, *attributes):
        '''改变元件属性的值'''
        e = self.element
        for attr in attributes[:-1]:
            if attr in e:
                e = e[attr]
            else:
                e[attr] = dict()
                e = e[attr]
        e[attributes[-1]] = value
        return

    def get_position(self):
        '''获得元件位置'''
        return [float(s) for s in self.get_attr('Position').split(',')]

    def set_position(self, x, y, z):
        '''设置元件位置（物实坐标系）'''
        self.set_attr('%f,%f,%f' % (x, y, z), 'Position')
        return

    def move(self, x, y, z=0.0):
        '''设置元件位置（桌面坐标系）'''
        x = x * 0.081 - 1.0
        y = -(y * 0.081 - 1.04)
        z = z * 0.081
        self.set_attr('%f,%f,%f' % (x, z, y), 'Position')
        return '%f,%f,%f' % (x, z, y)

    def rotate(self, x, y, z):
        '''设置旋转角度, ZXY欧拉'''
        self.set_attr('%f,%f,%f' % (-x, -y, z), 'Rotation')
        return '%f,%f,%f' % (-x, -y, z)


class ElementManager(object):
    def __init__(self, default_path=DEFAULT_PATH, source_file=SOURCE_FILE):
        '''实验管理类，读取与存储文件，创建元件、导线
        参数：默认存储路径，元件资源文件'''
        self.path = default_path  # 默认文件存储路径
        self.load_file(source_file)
        self.source_element_dict = dict()  # 设置元件模板
        for x in self.elements:
            self.source_element_dict[x.get_attr('ModelID')] = x
            x.move(0.0, 0.0, 0.0)
            x.set_attr('%f,%f,%f' % (0.0, 180.0, 0.0), 'Rotation')
            x.set_attr(1.0, 'Properties', '锁定')

        # 属性清零
        self.experiment = dict()
        self.elements = []
        self.wires = []

    def get_identifier(self):
        '''新生成随机Identifier值'''
        return ''.join([random.choice('0123456789abcdef') for i in range(32)])

    def load_file(self, filename=EMPTY_FILE):
        '''读取sav文件，返回实验'''
        if not os.path.isfile(filename):
            filename = os.path.join(self.path, filename)
        self.experiment = json.loads(open(filename, encoding='utf-8-sig').read())
        self.experiment['Experiment']['StatusSave'] = json.loads(self.experiment['Experiment']['StatusSave'])
        self.elements = self.experiment['Experiment']['StatusSave']['Elements']
        self.wires = self.experiment['Experiment']['StatusSave']['Wires']
        for i in range(len(self.elements)):
            self.elements[i] = Element(self.elements[i]['ModelID'], self.elements[i])
        return self.experiment

    def save(self, filename: str):
        '''将实验文本写入sav文件'''
        filename = os.path.join(self.path, filename)
        experiment = copy.deepcopy(self.experiment)
        elements = experiment['Experiment']['StatusSave']['Elements']
        for i in range(len(elements)):
            elements[i] = elements[i].element
        experiment['Experiment']['StatusSave'] = json.dumps(experiment['Experiment']['StatusSave'], ensure_ascii=False)
        experiment = json.dumps(experiment, ensure_ascii=False)
        with open(filename, 'w', encoding='utf-8-sig') as f:
            f.write(experiment)
        return

    def load_experiment(self, filename: str):
        '''从文件中获取所有元件和导线，加入原实验'''
        if not os.path.isfile(filename):
            filename = os.path.join(self.path, filename)
        experiment = json.loads(json.loads(open(filename, encoding='utf-8-sig').read())['Experiment']['StatusSave'])
        self.elements.extend([Element(x['ModelID'], x) for x in experiment['Elements']])
        self.wires.extend(experiment['Wires'])
        return

    def clear_experiment(self):
        self.elements.clear()
        self.wires.clear()

    def element_filter(self, value, *attributes):
        '''找出属性对应的元件'''
        return list(filter(lambda x: x.get_attr(*attributes) == value, self.elements))

    def find_elements(self, pattern: str):
        '''找出所有名称匹配的元件'''
        return list(filter(lambda x: re.fullmatch(pattern, x.name), self.elements))

    def find_wires(self, element_a=None, pin_a=None, element_b=None, pin_b=None):
        '''找出所有信息符合的导线'''

        def is_wire(e, p, wire):
            if isinstance(e, Element):
                if e.get_attr('Identifier') == wire["Source"]:
                    return p == None or p == wire["SourcePin"]
                elif e.get_attr('Identifier') == wire["Target"]:
                    return p == None or p == wire["TargetPin"]
            else:
                if p in (None, wire["SourcePin"], wire["TargetPin"]):
                    return True
            return False

        wires = []
        for wire in self.wires:
            if all([is_wire(*x, wire) for x in [(element_a, pin_a), (element_b, pin_b)]]):
                wires.append(wire)
        return wires

    def create_element(self, name: str, model_id: str, pos=None):
        '''创造新的元件。元件名称，元件'''
        new_element = copy.deepcopy(self.source_element_dict[model_id])
        new_element.set_attr(self.get_identifier(), 'Identifier')
        new_element.name = name
        if not pos is None:
            new_element.move(*pos)
        self.add_element(new_element)
        return new_element

    def add_element(self, element: Element):
        '''将元件加入元件列表'''
        self.elements.append(element)
        return

    def create_wire(self, element_a: Element, pin_a: int, element_b: Element, pin_b: int, color='蓝'):
        '''返回导线，连接元件a的接线柱pin_a和元件b的接线柱pin_b'''
        new_wire = {"Source": element_a.get_attr('Identifier'), "SourcePin": pin_a,
                    "Target": element_b.get_attr('Identifier'), "TargetPin": pin_b, "ColorName": "%s色导线" % color}
        self.add_wire(new_wire)
        return new_wire

    def add_wire(self, wire: str):
        '''将导线加入导线列表'''
        self.wires.append(wire)
        return

    def rename(self, experiment_name: str):
        '''改实验名称'''
        self.experiment['InternalName'] = experiment_name
        return
