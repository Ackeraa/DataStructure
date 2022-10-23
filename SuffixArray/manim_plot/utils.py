from manim import *
import math

class Array(VGroup):

    def __init__(self, values, square_size=0.6, color=BLACK):
        size = len(values)
        super().__init__()
        for i in range(size):
            sq = Square(square_size, color=color, stroke_width=2)
            txt = Text(str(values[i]), color=color, font="DroidSansMono Nerd Font", font_size=24).scale(max(0.6, square_size))
            txt.move_to(sq.get_center())
            self.add(VGroup(sq, txt))
        self.arrange(RIGHT, buff=0)

class TrieNode(VGroup):
    
    def __init__(self, value="", idx=0, size=0.3, scale=0.6, node_color=BLACK, text_color=BLACK):
        self.children = {}
        self.l = 0
        self.w = 0
        self.dth = 0
        self.idx = idx
        self.text = None
        self.node = Circle(size).set_color(node_color).set_fill(WHITE, opacity=1)
        self.value = Text(value, color=text_color, font="DroidSansMono Nerd Font").scale(scale).move_to(self.node.get_center())
        super().__init__(self.node, self.value)

    def set_text(self, value, scale=0.4, split=False):
        color = self.value.color
        super().remove(self.value)
        if split and len(value) > 3:
            value = value[:4] + "\n" + (len(value) - 4) // 2 * " " + value[4:]
        self.value = Text(value, color=color, font="DroidSansMono Nerd Font").scale(scale).move_to(self.node.get_center())
        super().add(self.value)
