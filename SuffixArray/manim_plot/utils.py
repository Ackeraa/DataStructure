from manim import *
import math

class Array(VGroup):

    def __init__(self, values, square_size=0.6, color=BLACK, line_color=BLACK):
        size = len(values)
        super().__init__()
        for i in range(size):
            sq = Square(square_size, color=line_color, stroke_width=2)
            txt = Text(str(values[i]), color=color, font="DroidSansMono Nerd Font", font_size=24).scale(max(0.6, square_size))
            txt.move_to(sq.get_center())
            self.add(VGroup(sq, txt))
        self.arrange(RIGHT, buff=0)

    def lmove_to(self, x):
        pos = x[0].get_center()
        cp = self.copy()
        for i in range(len(cp)):
            if i == 0:
                cp[i].move_to(pos)
            else:
                cp[i].next_to(cp[i - 1], RIGHT, buff=0)
        return self.move_to(cp)

class Title(VGroup):
    def __init__(self, title, square_size=0.6, color=BLACK):
        super().__init__()
        title_tex = MathTex(title, font_size=24, color=BLACK)
        title_box = Square(square_size, color=WHITE)
        title_tex.move_to(title_box.get_center())
        self.add(title_box, title_tex)

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
            value = value[:4] + "\n" + (len(value) - 4) // 2 * "\\ " + value[4:]
        self.value = Text(value, color=color, font="DroidSansMono Nerd Font").scale(scale).move_to(self.node.get_center())
        super().add(self.value)

class SuffixTreeNode(VGroup):
    def __init__(self, val="0", l=0, r=0, size=0.35, scale=1):
        self.children = {} # could use hash table to get linear time.
        self.edges = {}
        self.l = l
        self.r = r
        value = ""
        for x in val:
            if x != "$":
                value += x
            else:
                value += "\$"
        if value.isdigit():
            self.idx = int(value)
        self.node = Circle(size).set_color(BLACK).set_fill(WHITE, opacity=1)
        if value == "":
            self.value = MathTex("*", color=WHITE, font_size=22).scale(scale).move_to(self.node.get_center())
        else:
            self.value = MathTex(str(value), color=BLACK, font_size=22).scale(scale).move_to(self.node.get_center())
        super().__init__(self.node, self.value)


    def set_text(self, val, scale=0.9, split=True):
        super().remove(self.value)
        value = ""
        for x in val:
            if x != "$":
                value += x
            else:
                value += "\$"
        if value == "":
            self.value = MathTex("*", color=WHITE, font_size=22).scale(scale).move_to(self.node.get_center())
        else:
            self.value = MathTex(str(value), color=BLACK, font_size=22).scale(scale).move_to(self.node.get_center())
        super().__init__(self.node, self.value)
        super().add(self.value)

    def add_edge(self, v):
        p1 = self.node.get_center()
        p2 = v.node.get_center()
        dp1 = np.array(p2 - p1)
        lp = math.sqrt(dp1[0] ** 2 + dp1[1] ** 2)
        dp1 = dp1 / lp * v[0].radius
        dp2 = np.array(p1 - p2)
        lp = math.sqrt(dp2[0] ** 2 + dp2[1] ** 2)
        dp2 = dp2 / lp * v[0].radius
        e = Line(p1+dp1, p2+dp2, color=BLACK)

        def udt(m):
            p1 = self.node.get_center()
            p2 = v.node.get_center()
            dp1 = np.array(p2 - p1)
            lp = math.sqrt(dp1[0] ** 2 + dp1[1] ** 2)
            dp1 = dp1 / lp * v[0].radius
            dp2 = np.array(p1 - p2)
            lp = math.sqrt(dp2[0] ** 2 + dp2[1] ** 2)
            dp2 = dp2 / lp * v[0].radius

            return m.put_start_and_end_on(p1+dp1, p2+dp2)

        e.add_updater(udt)

        return e

class Info(VGroup):
    def __init__(self, txt="1", pos=DOWN*3, color=WHITE):
        self.square = Square(0.6, color=WHITE, stroke_width=2)
        self.square.move_to(pos)
        self.text = MathTex(txt, color=color, font_size=20)
        self.text.move_to(self.square.get_center())
        super().__init__(self.square, self.text)

    def update_text(self, text="*", font_size=20):
        if text == "*":
            color = WHITE
        else:
            color = BLACK
        self.text = self.text.become(MathTex(str(text), color=color, font_size=font_size))
        self.text.move_to(self.square.get_center())

        return self

