from manim import *
import math

class Array(VGroup):

    def __init__(self, values, square_size=0.6, color=BLACK):
        size = len(values)
        super().__init__()
        for i in range(size):
            sq = Square(square_size, color=BLACK, stroke_width=2)
            txt = Text(str(values[i]), color=color, font="DroidSansMono Nerd Font", font_size=24).scale(0.6)
            txt.move_to(sq.get_center())
            self.add(VGroup(sq, txt))
        self.arrange(RIGHT, buff=0)

class TrieNode(VGroup):
    
    def __init__(self, value="", idx=0, size=0.3, node_color=BLACK, text_color=BLACK):
        self.suffix_link = None
        self.output_link = None
        self.suffix_edge = None
        self.output_edge = None
        self.children = {}
        self.dth = 0
        self.idx = idx
        self.pattern = None
        self.node = Circle(size).set_color(node_color).set_fill(WHITE, opacity=1)
        self.value = Text(value, color=text_color, font="DroidSansMono Nerd Font").scale(0.6).move_to(self.node.get_center())
        super().__init__(self.node, self.value)

def get_p(p1, p2, radius):
    dp1 = np.array(p2 - p1)
    lp = math.sqrt(dp1[0] ** 2 + dp1[1] ** 2)
    dp1 = dp1 / lp * radius
    dp2 = np.array(p1 - p2)
    lp = math.sqrt(dp2[0] ** 2 + dp2[1] ** 2)
    dp2 = dp2 / lp * radius

    return p1 + dp1, p2 + dp2
