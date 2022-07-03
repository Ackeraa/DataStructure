from manim import *

class TrieNode(VGroup):
    
    def __init__(self, value="", idx=0, size=0.3, node_color=WHITE, text_color=WHITE):
        self.children = {}
        self.idx = idx
        self.pattern = None
        self.node = Circle(size).set_color(node_color).set_fill(BLACK, opacity=1)
        self.value = Text(value, color=text_color, font="DroidSansMono Nerd Font").scale(0.6).move_to(self.node.get_center())
        super().__init__(self.node, self.value)

