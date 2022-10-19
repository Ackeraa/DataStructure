from manim import *
import math

class Array(VGroup):

    def __init__(self, values, square_size=0.6, color=BLACK):
        size = len(values)
        super().__init__()
        for i in range(size):
            sq = Square(square_size, color=color, stroke_width=2)
            txt = Text(str(values[i]), color=color, font="DroidSansMono Nerd Font", font_size=24).scale(0.6)
            txt.move_to(sq.get_center())
            self.add(VGroup(sq, txt))
        self.arrange(RIGHT, buff=0)

