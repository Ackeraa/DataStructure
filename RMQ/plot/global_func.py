from manim import *
import math
from queue import Queue

def get_array(size, square_size=1):
    return VGroup(*[Square(square_size).set_color(BLACK) for i in range(size)]).arrange(RIGHT, buff=0)

def put_values_up_array(array, values, color=BLACK):
    return VGroup(*[Text(str(values[i]), color=color).scale(0.6).move_to(array[i].get_center()).shift(UP) for i in range(len(values))])

def put_values_down_array(array, values, color=BLACK):
    return VGroup(*[Text(str(values[i]), color=color).scale(0.6).move_to(array[i].get_center()).shift(DOWN) for i in range(len(values))])

def put_values_in_array(array, values, color=BLACK):
    return VGroup(*[Text(str(values[i]), color=color).scale(0.6).move_to(array[i].get_center()) for i in range(len(values))])

def get_node(size=1, color=BLACK):
    node = Circle(0.5).set_color(color)
    return node

class Node(VGroup):
    def __init__(self, value="", size=0.5, node_color=BLACK, text_color=BLACK):
        self.node = Circle(size).set_color(node_color)
        self.value = Text(value, color=text_color).scale(0.6).move_to(self.node.get_center())
        self.dth = 0
        self.l_child = None
        self.r_child = None
        f_always(self.value.move_to, self.node.get_center)
        super().__init__(self.node, self.value)

    def set_value(self, value):
        color = self.value.color
        super().remove(self.value)
        self.value = Text(value, color=color).scale(0.6).move_to(self.node.get_center())
        super().add(self.value)

    def trans_value(self, value):
        color = self.value.color
        new_value = Text(value, color=color).scale(0.6).move_to(self.node.get_center())
        return Transform(self.value, new_value)

    def set_value_color(self, color):
        self.value.set_color(color)

    def set_node_color(self, color):
        self.node.set_color(color)

    def set_node_fill(self, color):
        self.node.set_fill(color, opacity=1)

    def add_l_child(self, l_child):
        self.l_child = l_child
        '''
        self.l_child.next_to(self, DL*2)
        always(self.l_child.next_to, self, DL*2)
        '''
    
    def add_r_child(self, r_child):
        self.r_child = r_child
        '''
        self.r_child.next_to(self, DR*2)
        always(self.r_child.next_to, self, DR*2)
        '''

class Tree(VGroup):
    def __init__(self, root):
        super().__init__()
        self.root = root
        super().add(self.root)

    def __dfs(self, u, d):
        u.dth = d
        self.width[d] += 1
        if u.l_child != None:
            self.__dfs(u.l_child, d + 1)
        if u.r_child != None:
            self.__dfs(u.r_child, d + 1)

    def connect_l(self, u, v):
        self.__connect(u, v, 'l')

    def connect_r(self, u, v):
        self.__connect(u, v, 'r')

    def __connect(self, u, v, which):
        rad = u.node.radius * math.cos(45*math.pi/180)
        if which == 'l':
            pos = DL * 2
            vec = [[-rad, -rad, 0], [rad, rad, 0]]
        else:
            pos = DR * 2
            vec = [[rad, -rad, 0], [-rad, rad, 0]]
        v.next_to(u, pos)
        always(v.next_to, u, pos)

        p1 = u.get_center() + vec[0]
        p2 = v.get_center() + vec[1]
        e = Line(p1, p2, color=BLACK)
        self.add(v, e)

    def build(self):
        q = Queue()
        self.add(self.root)
        q.put(self.root)
        while not q.empty():
            u = q.get()
            l = u.l_child
            r = u.r_child
            if l != None:
                l.dth = u.dth + 1
                self.connect(u, l, 'l')
                q.put(l)
            if r != None:
                r.dth = u.dth + 1
                self.connect(u, r, 'r')
                q.put(r)

