from manim import *
from utils import *
import math
import numpy as np

class Trie(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        self.patterns = ["ab", "about", "at", "ate", "be", "bed", "edge", "get"]
        self.root = TrieNode()
        self.nodes = VGroup(self.root)
        self.edges = VGroup()
        self.build()
        self.place(self.root)
        self.add(self.edges)
        self.add(self.nodes)
        self.wait()

    def build(self):
        w = 10
        self.root.w = w
        self.root.l = -w // 2 
        self.root.shift(UP*3)
        for pattern in self.patterns:
            u = self.root
            for c in pattern:
                if c not in u.children:
                    v = TrieNode(c, len(u.children))
                    u.children[c] = v 
                    self.nodes.add(v)
                u = u.children[c]
            u.pattern = pattern

    def place(self, father):
        n = max(1, len(father.children))
        l = father.l
        w = father.w
        h = father.get_center()[1]
        gap = w / n / 2 
        p1 = father.get_center()
        for child in father.children.values():
            pos = [l + (child.idx * 2 + 1) * gap, h - 1.3, 0]
            child.l = pos[0] - gap
            child.w = 2 * gap
            child.move_to(pos)
            p2 = child.get_center()
            #e = Line(father[0], child[0], color=BLACK)
            dp1 = np.array(p2 - p1)
            lp = math.sqrt(dp1[0] ** 2 + dp1[1] ** 2)
            dp1 = dp1 / lp * child[0].radius
            dp2 = np.array(p1 - p2)
            lp = math.sqrt(dp2[0] ** 2 + dp2[1] ** 2)
            dp2 = dp2 / lp * child[0].radius
            e = Line(p1+dp1, p2+dp2, color=BLACK)
            self.edges.add(e)
            self.place(child)

    def match(self, text):
        m = len(text)
        for i in range(m):
            u = self.root
            for j in range(i, m):
                u = u.children.get(text[j])
                if u is None:
                    break
                else:
                    pattern = u.pattern
                    if pattern is not None:
                        print(pattern)
                        
class Test(Scene):
    def construct(self):
        vg = VGroup(Circle(1), Circle(2), Circle(3))
        print(vg[0].radius)
