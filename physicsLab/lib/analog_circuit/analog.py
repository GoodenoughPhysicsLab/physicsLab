# -*- coding: utf-8 -*-
from types import FunctionType

from physicsLab._core import (
    get_current_experiment, _Experiment, native_to_elementXYZ, elementXYZ_to_native
)
from physicsLab import _tools
from physicsLab.circuit.elements import *
from physicsLab.circuit._circuit_core import Pin, crt_wire, Wire
from physicsLab.typehint import Optional, num_type, List, Set, Dict, FrozenSet

# 全部节点列表
_gn: Dict[_Experiment, List["Node"]] = {}

# 全部节点间导线
_gicw: Dict[_Experiment, Set[FrozenSet["Vertex"]]] = {}

multiply_mode = "mos"


class Vertex(Pin):
    ''' 节点的接线柱 '''
    def __init__(self, pin: Pin, node: "Node"):
        if not isinstance(pin, Pin):
            raise TypeError
        super().__init__(pin.element_self, pin._pin_label)
        self.node = node

class VoidVertex(Vertex):
    ''' 空接线柱 '''
    def __init__(self, node):
        self.node = node

    def __eq__(self, other):
        return isinstance(other, VoidVertex)

    def __hash__(self):
        return hash(self.__class__.__name__)

class Node:
    ''' 模电节点 '''
    def __init__(self,
                 x: num_type,
                 y: num_type,
                 z: num_type,
                 name: str,
                 gnd: Ground_Component,
                 /, *,
                 elementXYZ: Optional[bool] = None) -> None:
        self.elements: List[CircuitBase] = []
        self._input: List[Vertex] = []
        self._output: Vertex = VoidVertex(self)
        self.name = name
        if not isinstance(gnd, Ground_Component):
            raise GroundNotFoundError
        self.gnd = gnd
        self.wires: Set[Wire] = set()
        expe = get_current_experiment()
        if _gn.get(expe) is None:
            _gn[expe] = [self]
        else:
            _gn[expe].append(self)

        # 元件坐标系，如果输入坐标不是元件坐标系就强转为元件坐标系
        if not (elementXYZ is True or (get_current_experiment().is_elementXYZ is True and elementXYZ is None)):
            x, y, z = native_to_elementXYZ(x, y, z)
        x, y, z = _tools.round_data(x), _tools.round_data(y), _tools.round_data(z)
        self._pos = _tools.position(x, y, z)

    def extend(self, elements: List[CircuitBase], wires: Set[Wire]) -> Self:
        ''' 扩大元件列表和导线集 '''
        self.elements.extend(elements)
        self.wires |= wires
        return self

    @property
    def antecedent(self) -> Set["Node"]:
        ''' 返回与该节点输入端相连的所有节点 '''
        res = set()
        for i in _gicw[get_current_experiment()]:
            candidate = i - set(self.input)
            if len(candidate) == 1: # 长度为0说明该导线两边连的都是该节点，长度为2说明导线没连上该节点
                res.add(list(candidate)[0].node)
        return res

    @property
    def consequent(self) -> Set["Node"]:
        ''' 返回与该节点输出端相连的所有节点 '''
        return {list(i - {self.output})[0].node for i in _gicw[get_current_experiment()] if self.output in i}

    @property
    def width(self) -> num_type:
        ''' 节点宽度，用于自动排布，已计入元件宽度 '''
        if self.elements == []:
            return 1
        x = [i.get_position().x for i in self.elements]
        return max(x) - min(x) + 1

    @property
    def height(self) -> num_type:
        ''' 节点高度，用于自动排布，已计入元件高度 '''
        if self.elements == []:
            return 1
        y = [i.get_position().y for i in self.elements]
        return max(y) - min(y) + 1

    @property
    def depth(self) -> num_type:
        ''' 节点深度，用于自动排布，未计入元件厚度 '''
        if self.elements == []:
            return 0
        z = [i.get_position().z for i in self.elements]
        return max(z) - min(z)

    @property
    def pos(self) -> _tools.position:
        ''' 节点位置 '''
        x, y, z = self._pos
        if not get_current_experiment().is_elementXYZ:
            x, y, z = elementXYZ_to_native(x, y, z)
        return _tools.position(x, y, z)

    def shift(self, x: num_type, y: num_type, z: num_type, /, *, elementXYZ: bool = True) -> Self:
        ''' 平移节点 '''
        if not elementXYZ:
            xe, ye, ze = native_to_elementXYZ(x, y, z)
        else:
            xe, ye, ze = x, y, z
        xe, ye, ze = _tools.round_data(xe), _tools.round_data(ye), _tools.round_data(ze)
        self._pos = _tools.position(self._pos.x + xe, self._pos.y + ye, self._pos.z + ze)
        for i in self.elements:
            pos = i.get_position()
            if i.is_elementXYZ:
                i.set_position(pos.x + xe, pos.y + ye, pos.z + ze, True)
            elif elementXYZ:
                xp, yp, zp = elementXYZ_to_native(x, y, z)
                xp, yp, zp = _tools.round_data(xp), _tools.round_data(yp), _tools.round_data(zp)
                i.set_position(pos.x + xp, pos.y + yp, pos.z + zp)
            else:
                i.set_position(pos.x + x, pos.y + y, pos.z + z)
        return self

    def locate(self, x: num_type, y: num_type, z: num_type, /, *, elementXYZ: bool = True) -> Self:
        self.shift(x - self._pos.x, y - self._pos.y, z - self._pos.z, elementXYZ=elementXYZ)

    @pos.setter
    def pos(self, value: tuple) -> None:
        if len(value) != 3:
            raise ValueError
        x, y, z = value
        if not isinstance(x, num_type) or \
            not isinstance(y, num_type) or \
            not isinstance(z, num_type):
            raise TypeError
        if not get_current_experiment().is_elementXYZ:
            x, y, z = native_to_elementXYZ(x, y, z)
        x, y, z = _tools.round_data(x), _tools.round_data(y), _tools.round_data(z)
        self.locate(x, y, z)

    def _adjust_flat(self, *nodes: "Node", z: Optional[num_type] = None) -> None:
        space = .25
        expe = get_current_experiment()
        if z is None:
            z = max(_gn[expe])
        same_level_y = [i.pos.y - i.height/2 for i in _gn[expe] if i.pos.z == z]
        if len(nodes) == 0:
            self.locate(self.width/2 - 6,
                        (12 if same_level_y == [] else min(same_level_y) - self.height/2 - space) - self.height/2, z)
        elif len(nodes) == 1:
            self.locate(nodes[0].pos.x + nodes[0].width/2 + self.width/2 + space, nodes[0].pos.y, z)
        elif len(nodes) == 2:
            if abs(nodes[0].pos.x - nodes[1].pos.x) + nodes[0].width/2 + nodes[1].width/2 \
                < nodes[0].width + nodes[1].width:
                # 横向有重合
                self.locate(max(nodes[0].pos.x + nodes[0].width/2, nodes[1].pos.x + nodes[1].width/2) + self.width/2 + space,
                            nodes[0].pos.y/2 + nodes[1].pos.y/2, z)
            elif abs(nodes[0].pos.y - nodes[1].pos.y) + nodes[0].height/2 + nodes[1].height/2 \
                < nodes[0].height + nodes[1].height:
                # 纵向有重合
                right = nodes[0] if nodes[0].pos.x > nodes[1].pos.x else nodes[1]
                self.locate(right.pos.x + right.width/2 + self.width/2 + space, right.pos.y, z)
            else:
                down = nodes[0] if nodes[0].pos.y < nodes[1].pos.y else nodes[1]
                self.locate(down.pos.x + down.width/2 + self.width/2 + space, down.pos.y, z)
            for i in _gn[expe]:
                if i.pos == self.pos:
                    i.shift(0, .5 + i.height/2, 0)
                    self.shift(0, -.5 - i.height/2, 0)
        else:
            raise NotImplementedError

    def adjust(self, *nodes: "Node") -> Self:
        ''' 根据所给节点自动调整位置 '''
        upper_depths = []
        depths = []
        for i in nodes:
            if not isinstance(i, Node):
                raise TypeError
            depths.append(i.pos.z)
            upper_depths.append(i.pos.z + i.depth/2)
        if nodes == []:
            self._adjust_flat()
        top = max(depths)
        upper_top = max(upper_depths)
        if upper_top != top:
            self._adjust_flat(z=upper_top + 1)
        else:
            self._adjust_flat(*(i for i in nodes if i.pos.z == top), z=top)
        return self

    def auto_adjust(self) -> Self:
        ''' 根据自己的前接节点自动调整位置 '''
        self.adjust(*self.antecedent)
        return self

    def recursive_auto_adjust(self) -> Self:
        ''' 自动调整自己和所有后接节点的位置 '''
        self.auto_adjust()
        for i in self.consequent:
            i.recursive_auto_adjust()
        return self

    def recursive_adjust(self, *nodes: "Node") -> Self:
        ''' 根据所给节点自动调整位置，并自动调整所有后接节点的位置 '''
        self.adjust(*nodes)
        for i in self.consequent:
            i.recursive_auto_adjust()
        return self

    @property
    def input(self) -> List[Vertex]:
        return self._input

    @property
    def output(self) -> Vertex:
        return self._output

    @input.setter
    def input(self, value: List[Pin]) -> None:
        if not isinstance(value, list):
            raise TypeError
        self._input = [Vertex(i, self) for i in value]

    @output.setter
    def output(self, value: Pin) -> None:
        self._output = Vertex(value, self)

    def __repr__(self) -> str:
        return "Node(name={}, input={}, output={}).extend({}, {})".format(self.name, self.input, self.output, self.elements, self.wires)

    def __sub__(self, other: Union["Node", num_type]) -> Union["SubNode", "LinearNode"]:
        if isinstance(other, (int, float)):
            sub = LinearNode(*self._pos, self.gnd, 1, -other).adjust(self)
            connect(self.output, sub.input[0])
        elif isinstance(other, Node):
            sub = SubNode(*self._pos, self.gnd).adjust(self, other)
            connect(self.output, sub.input[0])
            connect(other.output, sub.input[1])
        else:
            raise TypeError
        return sub

    def __rsub__(self, other: num_type) -> "SubNode":
        if not isinstance(other, (int, float)):
            raise TypeError
        sub = LinearNode(*self._pos, self.gnd, -1, other).adjust(self)
        connect(self.output, sub.input[0])
        return sub

    def __neg__(self) -> "LinearNode":
        neg = LinearNode(*self._pos, self.gnd, -1).adjust(self)
        connect(self.output, neg.input[0])
        return neg

    def __add__(self, other: Union["Node", num_type]) -> Union["SubNode", "LinearNode"]:
        return add(self, other)

    def __radd__(self, other: num_type) -> "LinearNode":
        return add(other, self)

    def __mul__(self, other: Union["Node", num_type]) -> Union["ComplexNode", "LinearNode"]:
        if isinstance(other, (int, float)):
            mul = LinearNode(*self._pos, self.gnd, other).adjust(self)
            connect(self.output, mul.input[0])
            return mul
        elif isinstance(other, Node):
            return multiply(self, other)
        else:
            raise TypeError

    def __rmul__(self, other: num_type) -> "LinearNode":
        return self * other

    def __truediv__(self, other: Union["Node", num_type]) -> Union["ComplexNode", "LinearNode"]:
        if isinstance(other, (int, float)):
            return self * (1/other)
        elif isinstance(other, Node):
            return divide(self, other)
        else:
            raise TypeError

class GroundNotFoundError(Exception):
    ''' 未找到接地元件 '''
    def __str__(self):
        return "Unable to find a ground component for the node to be generated"

class NodeNotFoundError(Exception):
    ''' 未找到节点 '''
    def __str__(self):
        return "Unable to find a node as required"

def connect(*verteses: Vertex) -> List[Wire]:
    ''' 连接节点的接线柱 '''
    if not all(isinstance(i, Vertex) for i in verteses):
        raise TypeError
    pins = [i for i in verteses if not isinstance(i, VoidVertex)]
    res = crt_wire(*pins)
    expe = get_current_experiment()
    if _gicw.get(expe) is None:
        _gicw[expe] = set()
    for i in range(len(verteses) - 1):
        source_vertex, target_vertex = verteses[i], verteses[i + 1]
        if source_vertex == target_vertex: # 这里假定了VoidVertex间不能相连，可能出bug
            raise errors.InvalidWireError("can't link wire to itself")
        _gicw[expe].add(frozenset({source_vertex, target_vertex}))
    return res

def node_wrapper(name: str) -> Node:
    '''用于将函数的作用效果整体包装为一个节点\n
    将所有在函数作用过程中与函数参数中Node对象的输出端相连的Pin作为新Node的输入端，
    并将函数的返回的Node的输出端作为新Node的输出端\n
    新Node的元件集为作用过程中所有以正常方法新增的元件，
    导线集为作用过程中所有以正常方法新增的导线除去，
    位置为作用过程中产生的所有元件的正中央，
    接地为函数参数中的Node对象的或者作用过程中新增的接地元件\n
    该装饰器只能用于返回Node对象的函数
    '''
    def decorator_node_wrapper(func: FunctionType) -> Node:
        def wrapper(*args, **kwargs):
            expe = get_current_experiment()
            ele_count = len(expe.Elements)
            if _gicw.get(expe) is None:
                _gicw[expe] = set()
            if _gn.get(expe) is None:
                _gn[expe] = []
            # prev_wires = expe.Wires.copy()  # a deep copy doesn't seem to be necessary
            prev_vertex_wires = _gicw[expe].copy()
            prev_nodes = _gn[expe].copy()
            res: Node = func(*args, **kwargs)
            if not isinstance(res, Node):
                raise TypeError("The return value of the function must be a Node object")
            elements: List[CircuitBase] = expe.Elements[ele_count:]
            # all_wires = expe.Wires - prev_wires
            all_vertex_wires = _gicw[expe] - prev_vertex_wires
            nodes = set(_gn[expe]) - set(prev_nodes)
            # wires = all_wires.copy()

            gnd = None
            inputs: Set[Vertex] = set()
            input_nodes = []
            for i in list(args) + list(kwargs.values()):
                if isinstance(i, Node):
                    input_nodes.append(i)
                    gnd = i.gnd
                    for k in all_vertex_wires: # 这里必须用vertex_wires，因为可能有试探用的空接线柱
                        if i.output in k:
                            inputs |= k - {i.output}
                            # wires.remove(k)
            if input_nodes == []:
                raise NodeNotFoundError
            if gnd is None:
                for i in elements:
                    if isinstance(i, Ground_Component):
                        gnd = i
                        break
            if gnd is None:
                raise GroundNotFoundError

            for i in inputs:
                i.node.recursive_adjust(*input_nodes)
            positions = [i.get_position() if i.is_elementXYZ else native_to_elementXYZ(*i.get_position()) for i in elements]
            x, y, z = zip(*positions)
            width = (max(x) + min(x))/2
            height = (max(y) + min(y))/2
            depth = (max(z) + min(z))/2

            node = ComplexNode(nodes, width, height, depth, name, gnd, elementXYZ=True)
            node.extend(elements, set())
            # node.extend(elements, {crt_wire(*i)[0] for i in wires}) # 这一步冗余接线，但正好用来检查有没有空导线
            node.output = res.output
            node.input = list(inputs)
            return node
        return wrapper
    return decorator_node_wrapper

class PinNode(Node):
    ''' 接线柱节点 '''
    def __init__(self, pin: Pin, gnd) -> None:
        pos = pin.element_self.get_position()
        super().__init__(pos.x, pos.y, pos.z, "pin", gnd, elementXYZ=pin.element_self.is_elementXYZ)
        self.input = [pin]
        self.output = pin

class VoidNode(Node):
    def __init__(self, x, y, z, gnd, /, *, elementXYZ = None):
        super().__init__(x, y, z, "void", gnd, elementXYZ=elementXYZ)

class ComplexNode(Node):
    def __init__(self, subnodes: Set[Node], x, y, z, name, gnd, /, *, elementXYZ = None):
        super().__init__(x, y, z, name, gnd, elementXYZ=elementXYZ)
        self.subnodes = subnodes
        expe = get_current_experiment()
        for i in subnodes:
            if i in _gn[expe]:
                _gn[expe].remove(i)
            else:
                raise NodeNotFoundError

class SubNode(Node):
    ''' 减法节点 (y=x1-x2)  '''
    ''' 来源：@xuzhengx '''
    def __init__(self, x, y, z, gnd: Ground_Component) -> None:
        super().__init__(x, y, z, "sub", gnd)
        x, y, z = self._pos

        r11 = Resistor(x - 1, y + .5, z, elementXYZ=True).set_resistance(99)
        r12 = Resistor(x, y + .5, z, elementXYZ=True).set_resistance(1)
        r21 = Resistor(x - 1, y - .5, z, elementXYZ=True).set_resistance(99)
        r22 = Resistor(x, y - .5, z, elementXYZ=True).set_resistance(1)
        opamp = Operational_Amplifier(x + 1, y, z, elementXYZ=True).set_properties(100)
        crt_wire(r12.red, r11.black)
        crt_wire(r11.black, opamp.i_pos)
        crt_wire(r22.red, r21.black)
        crt_wire(r21.black, opamp.i_neg)
        crt_wire(r12.black, gnd.i)
        crt_wire(r22.black, gnd.i)

        self.elements = [r11, r12, r21, r22, opamp]
        self.input = [r11.red, r21.red]
        self.output = opamp.o

class LinearNode(Node):
    ''' 线性节点 (y=kx+b)  '''
    ''' 来源：@xuzhengx '''

    def __init__(self, x, y, z, gnd: Ground_Component, k: num_type, b: num_type = 0) -> None:
        super().__init__(x, y, z, "scale", gnd)
        x, y, z = self._pos
        scale = b == 0

        if k == 0:
            st1 = Schmitt_Trigger(x, y, z, elementXYZ=True, inverted=True, high_level=b)

            self.elements = [st1]
            self.output = st1.o
        elif k == 1 and scale:
            oa1 = Operational_Amplifier(x, y, z, elementXYZ=True, gain=10_000_000)
            crt_wire(oa1.i_neg, oa1.o)

            self.elements = [oa1]
            self.input = [oa1.i_pos]
            self.output = oa1.o
        elif 0 < k < 100:
            oa1 = Operational_Amplifier(x + .5 if scale else x + 1, y, z, elementXYZ=True, gain=100)
            r1 = Resistor(x - .5 if scale else x, y - .5 if scale else y + .5, z, elementXYZ=True, resistance=1)
            r2 = Resistor(x - .5 if scale else x - 1, y + .5, z, elementXYZ=True, resistance=100/k - 1)
            crt_wire(r2.black, oa1.i_pos)
            crt_wire(r1.red, r2.black)
            crt_wire(gnd.i, r1.black)

            self.elements = [r1, r2, oa1]
            self.input = [r2.red]
            self.output = oa1.o
            positive = False
        elif k >= 100:
            oa1 = Operational_Amplifier(x + .5, y, z, elementXYZ=True, gain=k)

            self.elements = [oa1]
            self.input = [oa1.i_pos]
            self.output = oa1.o
            positive = False
        elif -100 < k < 0:
            oa1 = Operational_Amplifier(x + .5, y, z, elementXYZ=True, gain=100)
            r1 = Resistor(x - .5 if scale else x, y - .5 if scale else y + .5, z, elementXYZ=True, resistance=1)
            r2 = Resistor(x - .5 if scale else x - 1, y + .5, z, elementXYZ=True, resistance=-100/k - 1)
            crt_wire(r2.black, oa1.i_neg)
            crt_wire(r1.red, r2.black)
            crt_wire(gnd.i, r1.black)

            self.elements = [r1, r2, oa1]
            self.input = [r2.red]
            self.output = oa1.o
            positive = True
        elif k <= -100:
            oa1 = Operational_Amplifier(x + .5, y, z, elementXYZ=True, gain=-k)

            self.elements = [oa1]
            self.input = [oa1.i_neg]
            self.output = oa1.o
            positive = True

        if not scale and k != 0:
            st1 = Schmitt_Trigger(x, y - .5, z, elementXYZ=True, inverted=True, high_level=(b if positive else -b)/oa1.properties['增益系数'])
            crt_wire(st1.o, oa1.i_pos if positive else oa1.i_neg)
            self.elements.append(st1)

@node_wrapper("add")
def add(n1: Node, other: Union[Node, num_type]) -> SubNode:
    ''' 加法 '''
    return n1 - -other

class PrimitiveLogTransistorNode(Node):
    ''' 三极管原始对数节点 (y=-0.025ln(x)-0.69077552617129989)  '''
    ''' 来源：@xuzhengx '''
    def __init__(self, x, y, z, gnd: Ground_Component) -> None:
        super().__init__(x, y, z, "primitive_log_transistor", gnd)
        x, y, z = self._pos

        oa1 = Operational_Amplifier(x + .5, y - .5, z, elementXYZ=True, max_voltage=15, min_voltage=-15)
        r1 = Resistor(x - .5, y - .5, z, elementXYZ=True)
        t1 = Transistor(x + .5, y + 1, z, elementXYZ=True, is_PNP=False)
        crt_wire(r1.black, t1.C)
        crt_wire(gnd.i, t1.B)
        crt_wire(t1.E, oa1.o)
        crt_wire(r1.black, oa1.i_neg)

        self.elements = [oa1, r1, t1]
        self.input = [r1.red]
        self.output = oa1.o

def pri_log(n: Node) -> PrimitiveLogTransistorNode:
    ''' 原始对数 (y=-0.025ln(x)-0.69077552617129989)  '''
    log = PrimitiveLogTransistorNode(*n._pos, n.gnd).adjust(n)
    connect(n.output, log.input[0])
    return log

@node_wrapper("ln")
def ln(n: Node) -> LinearNode:
    ''' 对数 (y=ln(x)) '''
    return (pri_log(n) + 0.69077552617129989)*-40

def inverse(func: FunctionType, vertex_id: int = 0) -> FunctionType:
    ''' 反函数，参数函数必须已经打包好，且输出为节点 '''
    def res_func(n: Node):
        v = VoidNode(*n.pos, n.gnd)
        expe = get_current_experiment()
        res = func(v)
        if not isinstance(res, Node):
            raise TypeError
        opamp = Operational_Amplifier(res.pos.x + res.width/2 + .5, res.pos.y, res.pos.z)
        wires = {
            *crt_wire(opamp.i_pos, res.output),
            *crt_wire(opamp.o, res.input[vertex_id])
            }
        node = Node(res.pos.x + .5, res.pos.y, res.pos.z, "inv", res.gnd)
        node.input = [opamp.i_neg] + res.input[:vertex_id] + res.input[vertex_id + 1:]
        node.output = opamp.o
        node.extend(res.elements + [opamp], res.wires | wires)
        connect(n.output, node.input[0])
        _gn[expe].remove(v)
        for i in _gicw[expe].copy():
            if list(i)[0] is v.output or list(i)[1] is v.output:
                _gicw[expe].remove(i)
        return node
    return res_func

@node_wrapper("primitive_exp_transistor")
def pri_exp(n: Node) -> Node:
    ''' 原始指数 (y=exp(-(x+0.69077552617129989)/0.025)) '''
    return inverse(pri_log)(n)

@node_wrapper("exp")
def exp(n: Node) -> Node:
    return inverse(ln)(n)

class IntNode(Node):
    def __init__(self, x, y, z, gnd: Ground_Component) -> None:
        ''' 积分节点 (y=∫xdt) '''
        ''' 来源：@MapMaths '''
        super().__init__(x, y, z, "int", gnd)
        x, y, z = self._pos

        oa1 = Operational_Amplifier(x + .5, y - .5, z, elementXYZ=True, max_voltage=15, min_voltage=-15)
        r1 = Resistor(x - .5, y - .5, z, elementXYZ=True)
        c1 = Basic_Capacitor(x + .5, y + 1, z, elementXYZ=True, capacitance=.1, is_ideal=True)
        crt_wire(c1.red, oa1.i_neg)
        crt_wire(c1.black, oa1.o)
        crt_wire(r1.black, oa1.i_neg)

        self.elements = [oa1, r1, c1]
        self.input = [r1.red]
        self.output = oa1.o

def integrate(n: Node) -> IntNode:
    ''' 积分 (y=∫xdt) '''
    inte = IntNode(*n._pos, n.gnd).adjust(n)
    connect(n.output, inte.input[0])
    return inte

class DifNode(Node):
    def __init__(self, x, y, z, gnd: Ground_Component) -> None:
        ''' 微分节点 (y=dx/dt) '''
        ''' 来源：@MapMaths '''
        super().__init__(x, y, z, "dif", gnd)
        x, y, z = self._pos

        oa1 = Operational_Amplifier(x + .5, y - .5, z, elementXYZ=True, max_voltage=15, min_voltage=-15)
        r1 = Resistor(x + .5, y + 1, z, elementXYZ=True)
        c1 = Basic_Capacitor(x - .5, y - .5, z, elementXYZ=True, capacitance=.1, is_ideal=True)
        crt_wire(r1.red, oa1.i_neg)
        crt_wire(r1.black, oa1.o)
        crt_wire(c1.black, oa1.i_neg)

        self.elements = [oa1, r1, c1]
        self.input = [r1.red]
        self.output = oa1.o

def differentiate(n: Node) -> DifNode:
    ''' 积分 (y=∫xdt)  '''
    diff = DifNode(*n._pos, n.gnd).adjust(n)
    connect(n.output, diff.input[0])
    return diff

def quadrant(func: FunctionType) -> FunctionType:
    ''' 四象限化，参数函数必须已经打包好，且输出为节点 '''
    def res_func(n1: Node, n2: Node):
        expe = get_current_experiment()
        v1 = VoidNode(*n1.pos, n1.gnd)
        v2 = VoidNode(*n2.pos, n2.gnd)
        res = func(v1, v2)
        if not isinstance(res, Node):
            raise TypeError
        op1_opamp = Operational_Amplifier(res.pos.x - res.width/2 - .5, res.pos.y + 1.5, res.pos.z, gain=100)
        op1_r1 = Resistor(res.pos.x - res.width/2 - .5, res.pos.y, res.pos.z, resistance=1)
        op1_r2 = Resistor(res.pos.x - res.width/2 - .5, res.pos.y - 1, res.pos.z, resistance=99)
        op2_opamp = Operational_Amplifier(res.pos.x - res.width/2 - 1.5, res.pos.y + 1.5, res.pos.z, gain=100)
        op2_r1 = Resistor(res.pos.x - res.width/2 - 1.5, res.pos.y, res.pos.z, resistance=1)
        op2_r2 = Resistor(res.pos.x - res.width/2 - 1.5, res.pos.y - 1, res.pos.z, resistance=99)
        op3_opamp = Operational_Amplifier(res.pos.x + res.width/2 + 1.5, res.pos.y + 1.5, res.pos.z, gain=100)
        op3_r1 = Resistor(res.pos.x + res.width/2 + 1.5, res.pos.y, res.pos.z, resistance=1)
        op3_r2 = Resistor(res.pos.x + res.width/2 + 1.5, res.pos.y - 1, res.pos.z, resistance=99)
        relay_i1 = Relay_Component(res.pos.x - res.width/2 - 2.5, res.pos.y + 1, res.pos.z)
        relay_i2 = Relay_Component(res.pos.x - res.width/2 - 2.5, res.pos.y - .5, res.pos.z)
        relay_o = Relay_Component(res.pos.x + res.width/2 + .5, res.pos.y + 1, res.pos.z)
        xor = Xor_Gate(res.pos.x + res.width/2 + .5, res.pos.y, res.pos.z).set_high_level_value(1e-7)
        amp = Operational_Amplifier(res.pos.x + res.width/2  + .5, res.pos.y - 1.5, res.pos.z)
        wires = {
            *crt_wire(relay_i1.mid, op1_r1.black),
            *crt_wire(relay_i2.mid, op2_r1.black),
            *crt_wire(relay_o.mid, op3_r1.black),
            *crt_wire(relay_i1.r_low, n1.gnd.i),
            *crt_wire(relay_i2.r_low, n1.gnd.i),
            *crt_wire(relay_o.r_low, n1.gnd.i),
            *crt_wire(op1_r1.black, op1_r2.red),
            *crt_wire(op2_r1.black, op2_r2.red),
            *crt_wire(op3_r1.black, op3_r2.red),
            *crt_wire(relay_i1.l_up, op1_opamp.i_neg),
            *crt_wire(relay_i2.l_up, op2_opamp.i_neg),
            *crt_wire(relay_o.l_low, op3_opamp.i_neg),
            *crt_wire(relay_i1.l_low, op1_opamp.i_pos),
            *crt_wire(relay_i2.l_low, op2_opamp.i_pos),
            *crt_wire(relay_o.l_up, op3_opamp.i_pos),
            *crt_wire(op1_r2.black, xor.i_up),
            *crt_wire(op2_r2.black, xor.i_low),
            *crt_wire(op1_r2.black, relay_i1.r_up),
            *crt_wire(op2_r2.black, relay_i2.r_up),
            *crt_wire(op1_r1.red, n1.gnd.i),
            *crt_wire(op2_r1.red, n1.gnd.i),
            *crt_wire(op3_r1.red, n1.gnd.i),
            *crt_wire(amp.i_pos, xor.o),
            *crt_wire(relay_o.r_up, amp.o),
            *crt_wire(op3_r2.black, res.output),
            *crt_wire(op1_opamp.o, res.input[0]),
            *crt_wire(op2_opamp.o, res.input[1])
        }
        node = Node(res.pos.x - .5, res.pos.y, res.pos.z, "quad", res.gnd)
        node.input = [op1_r2.black, op2_r2.black]
        node.output = op3_opamp.o
        node.extend(res.elements + [op1_opamp, op1_r1, op1_r2, op2_opamp, op2_r1, op2_r2, op3_opamp, op3_r1, op3_r2, relay_i1, relay_i2, relay_o, xor, amp], res.wires | wires)
        connect(n1.output, node.input[0])
        connect(n2.output, node.input[1])
        _gn[expe].remove(v1)
        _gn[expe].remove(v2)
        for i in _gicw[expe].copy():
            if list(i)[0] is v1.output or list(i)[1] is v1.output \
                or list(i)[0] is v2.output or list(i)[1] is v2.output:
                _gicw[expe].remove(i)
        return node
    return res_func

class MOSMultiplierNode(Node):
    def __init__(self, x, y, z, gnd: Ground_Component):
        super().__init__(x, y, z, "mos_multiplier", gnd)
        x, y, z = self._pos

        r1 = Resistor(x - 1, y + .5, z, elementXYZ=True, resistance=99999999)
        r2 = Resistor(x, y + .5, z, elementXYZ=True, resistance=1)
        oa1 = Operational_Amplifier(x, y + 2, z, elementXYZ=True, gain=100)
        battery = Battery_Source(x - 1, y - 1, z, elementXYZ=True, voltage=1.5)
        mos = N_MOSFET(x, y - 1, z, elementXYZ=True, beta=1000)
        oa2 = Operational_Amplifier(x + 1, y + .5, z, elementXYZ=True, gain=100)
        r3 = Resistor(x + 1, y + 2, z, elementXYZ=True, resistance=1000)
        r4 = Resistor(x + 1, y - 1, z, elementXYZ=True, resistance=99)
        r5 = Resistor(x + 1, y - 2, z, elementXYZ=True, resistance=1)
        crt_wire(r1.black, r2.red, oa1.i_pos)
        crt_wire(r2.black, gnd.i, r5.red)
        crt_wire(battery.red, mos.G)
        crt_wire(oa1.o, mos.S)
        crt_wire(mos.D, oa2.i_neg, r3.red)
        crt_wire(r3.black, oa2.o, r4.black)
        crt_wire(oa2.i_pos, r4.red, r5.black)

        self.elements = [r1, r2, oa1, battery, mos, oa2, r3, r4, r5]
        self.input = [r1.red, battery.black]
        self.output = oa2.o

@node_wrapper("transistor_multiplier")
def transistor_multiply(n1: Node, n2: Node) -> ComplexNode:
    return pri_exp(pri_log(n1) + pri_log(n2) + 0.69077552617129989)

@node_wrapper("mos_multiplier")
def mos_multiply(n1: Node, n2: Node) -> MOSMultiplierNode:
    mul = MOSMultiplierNode(*n1.pos, n1.gnd).adjust(n1, n2)
    connect(n1.output, mul.input[0])
    connect(n2.output, mul.input[1])
    return mul

@node_wrapper("mul")
def multiply(n1: Node, n2: Node):
    if multiply_mode == "transistor":
        return quadrant(transistor_multiply)(n1, n2)
    elif multiply_mode == "mos":
        return quadrant(mos_multiply)(n1, n2)
    else:
        raise NotImplementedError

@node_wrapper("transistor_div")
def transistor_divide(n1: Node, n2: Node):
    return pri_exp(pri_log(n1) - pri_log(n2) - 0.69077552617129989)

@node_wrapper("div")
def divide(n1: Node, n2: Node):
    return quadrant(transistor_divide)(n1, n2)

@node_wrapper("log")
def log(n1: Node, n2: Node) -> ComplexNode:
    return (pri_log(n2) + 0.69077552617129989) / (pri_log(n1) + 0.69077552617129989)
