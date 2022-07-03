from manim import *
from utils import *
import math
import numpy as np

class Trie(Scene):
    def construct(self):
        #self.camera.background_color = WHITE
        self.add_sound("bgm.mp3")
        self.patterns = ["ab", "about", "at", "ate", "be", "bed", "edge", "get"]
        self.root = TrieNode()
        self.nodes = VGroup(self.root)
        self.edges = VGroup()
        self.build()
        self.place(self.root)
        # self.add(self.edges)
        #self.add(self.nodes)
        self.build_animate()
        self.match_animate()
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
            e = Line(p1+dp1, p2+dp2, color=WHITE)
            self.edges.add(e)
            self.place(child)

    def build_animate(self):
        self.nodes.shift(LEFT)
        root = TrieNode()
        patterns = VGroup()
        for pattern in self.patterns:
            text = Text(pattern, font="DroidSansMono Nerd Font", font_size=22)
            patterns.add(text)
        patterns.arrange(DOWN, buff=0.5)
        patterns.shift(RIGHT*5)
        self.patterns_vg = patterns
        self.title = Text("构造", font_size=26, color=BLUE_E).shift(UP*3.5+RIGHT*5)
        self.play(FadeIn(patterns, self.title))
        ar = Triangle(color=RED_E).set_fill(RED, opacity=1).rotate(-180*DEGREES).scale(.03)
        pos = UP*0.3+LEFT*(len(self.patterns[0])//2)*0.2
        if len(self.patterns[0]) % 2 == 0:
            pos += RIGHT*0.1
        ar.move_to(patterns[0]).shift(pos)
        self.play(FadeIn(ar), FadeIn(self.root))
        self.wait()
        for i, pattern in enumerate(self.patterns):
            if i != 0:
                pos = UP*0.3+LEFT*(len(self.patterns[i])//2)*0.2
                if len(self.patterns[i]) % 2 == 0:
                    pos += RIGHT*0.1
                self.play(ar.animate.move_to(patterns[i]).shift(pos))
            u = root
            u0 = self.root
            for j, c in enumerate(pattern):
                p1 = u0.get_center()
                if c not in u.children:
                    u.children[c] = TrieNode(c, len(u.children))
                    v = u0.children[c]
                    p2 = v.get_center()
                    #e = Line(father[0], child[0], color=BLACK)
                    dp1 = np.array(p2 - p1)
                    lp = math.sqrt(dp1[0] ** 2 + dp1[1] ** 2)
                    dp1 = dp1 / lp * v[0].radius
                    dp2 = np.array(p1 - p2)
                    lp = math.sqrt(dp2[0] ** 2 + dp2[1] ** 2)
                    dp2 = dp2 / lp * v[0].radius
                    e = Line(p1+dp1, p2+dp2, color=WHITE)
                    self.play(
                            ReplacementTransform(u0.copy(), v),
                            Create(e),
                        )
                else:
                    self.play(Indicate(u0.children[c][0], color=TEAL))

                if j < len(pattern) - 1:
                    self.play(ar.animate.shift(RIGHT*0.2))

                u = u.children[c]
                u0 = u0.children[c]
            u.pattern = pattern
            self.play(u0[0].animate.set_fill(RED_E, opacity=1))
        self.remove(ar)

    def match_animate(self):
        texts = ["ate", "abou", "abc"]
        texts_vg = VGroup()
        for text in texts:
            t = Text(text, font="DroidSansMono Nerd Font", font_size=22)
            texts_vg.add(t)
        texts_vg.arrange(DOWN, buff=0.5)
        texts_vg.shift(RIGHT*5+UP*1.5)

        title = Text("查询", font_size=26, color=BLUE_E).shift(UP*3.5+RIGHT*5)
        self.play(
                self.title.animate.become(title),
                ReplacementTransform(self.patterns_vg, texts_vg),
            )

        ar = Triangle(color=RED_E).set_fill(RED, opacity=1).rotate(-180*DEGREES).scale(.03)
        ar.move_to(texts_vg[0]).shift(UP*0.3+LEFT*(len(texts[0])//2)*0.2)
        if len(texts[0]) % 2 == 0:
            arr.shift(RIGHT*0.1)
        self.play(FadeIn(ar))

        for i, text in enumerate(texts):
            u = self.root
            found = False
            if i != 0:
                pos = UP*0.3+LEFT*(len(text)//2)*0.2
                if len(text) % 2 == 0:
                    pos += RIGHT*0.1
                self.play(ar.animate.move_to(texts_vg[i]).shift(pos))
            for j, c in enumerate(text):
                u = u.children.get(c)
                if u is None:
                    break
                else:
                    self.play(Indicate(u[0], color=TEAL))
                    pattern = u.pattern
                    if pattern is not None and j == len(text) - 1:
                        found = True
                if j < len(text) - 1:
                    self.play(ar.animate.shift(RIGHT*0.2))

            if found:
                t = text = Text("", font="DroidSansMono Nerd Font", color=GREEN, font_size=22)
                t.next_to(texts_vg[i], RIGHT, buff=0.2)

            if not found:
                t = text = Text("", font="DroidSansMono Nerd Font", color=PURE_RED, font_size=22)
                t.next_to(texts_vg[i], RIGHT, buff=0.2)
            self.play(FadeIn(t))

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
        self.patterns = ["ab", "about", "at", "ate", "be", "bed", "edge", "get"]
        patterns = VGroup()
        for pattern in self.patterns:
            text = Text(pattern, font="DroidSansMono Nerd Font", font_size=22)
            patterns.add(text)
        patterns.arrange(DOWN, buff=0.5)
        patterns.shift(RIGHT*5)
        self.add(patterns)
        ar = Triangle(color=RED_E).set_fill(RED, opacity=1).rotate(-180*DEGREES).scale(.03)
        i = 1
        ar.move_to(patterns[i])
        ar.shift(UP*0.3+LEFT*(len(self.patterns[i])//2) * 0.2)
        if len(self.patterns[i]) % 2 == 0:
            ar.shift(RIGHT*0.1)
        for i in range(4):
            self.play(ar.animate.shift(RIGHT*0.2), run_time=0.8)


        self.add(ar)


        self.wait()

