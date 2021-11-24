from manim import *

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

    def set_color(self, color):
        self.node.set_color(color)

    def set_fill(self, color):
        self.node.set_fill(color, opacity=1)

    def add_l_child(self, l_child):
        self.l_child = l_child
    
    def add_r_child(self, r_child):
        self.r_child = r_child

class Tree(VGroup):
    def __init__(self, root):
        self.root = root
        super().__init__(self.root)

