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
    def __init__(self, value="", size=0.3, node_color=BLACK, text_color=BLACK):
        self.node = Circle(size).set_color(node_color)
        self.value = Text(value, color=text_color).scale(0.6).move_to(self.node.get_center())
        self.dth = 0
        self.index = int(value)
        self.l_child = None
        self.r_child = None
        self.l_line = None
        self.r_line = None
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

    def set_node_fill(self, color, opacity):
        self.node.set_fill(color, opacity=opacity)

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
        self.add(self.root)

    def connect_l(self, u, v):
        self.__connect(u, v, v.dth, 'l')

    def connect_r(self, u, v):
        self.__connect(u, v, v.dth, 'r')

    def __connect(self, u, v, d, which):
        w = config['frame_width'] / pow(2, d + 1)
        if which == 'l':
            dirs = DOWN + LEFT * w
            rad = u.node.radius / math.sqrt(dirs[0] ** 2 + dirs[1] ** 2)
            dx = rad * dirs[0]
            dy = rad * dirs[1]
            vec = [[dx , dy, 0], [-dx, -dy, 0]]
        else:
            dirs = DOWN * 1.5 + RIGHT * w
            rad = u.node.radius / math.sqrt(dirs[0] ** 2 + dirs[1] ** 2)
            dx = rad * dirs[0]
            dy = rad * dirs[1]
            vec = [[dx, dy, 0], [-dx, -dy, 0]]
        pos = u.get_center() + dirs
        v.move_to(pos)
        #v.add_updater(lambda m: m.move_to(u.get_center() + dirs))

        p1 = u.get_center() + vec[0]
        p2 = v.get_center() + vec[1]
        e = Line(p1, p2, color=BLACK)
        e.add_updater(lambda m: m.put_start_and_end_on(u.get_center() + vec[0],
                                                       v.get_center() + vec[1]))
        self.add(v)

    def build(self):
        q = Queue()
        q.put(self.root)
        while not q.empty():
            u = q.get()
            l = u.l_child
            r = u.r_child
            if l != None:
                l.dth = u.dth + 1
                self.__connect(u, l, l.dth, 'l')
                q.put(l)
            if r != None:
                r.dth = u.dth + 1
                self.__connect(u, r, r.dth, 'r')
                q.put(r)

