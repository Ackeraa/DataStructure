from manim import *
from utils import *
import math
import numpy as np
import queue
import random

class Trie(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        self.patterns = ["ab", "about", "at", "ate", "be", "bed", "edge", "get"]
        self.root = TrieNode()
        self.nodes = VGroup(self.root)
        self.edges = VGroup()
        self.build()
        self.place(self.root)
        # self.add(self.edges)
        #self.add(self.nodes)
        #self.build_animate()
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
            self.nodes[-1][0].set_fill(RED_E, opacity=1)

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

    def build_animate(self):
        self.nodes.shift(LEFT)
        root = TrieNode()
        patterns = VGroup()
        for pattern in self.patterns:
            text = Text(pattern, color=BLACK, font="DroidSansMono Nerd Font", font_size=22)
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
                    e = Line(p1+dp1, p2+dp2, color=BLACK)
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
            t = Text(text, color=BLACK, font="DroidSansMono Nerd Font", font_size=22)
            texts_vg.add(t)
        texts_vg.arrange(DOWN, buff=0.5)
        texts_vg.shift(RIGHT*5+UP*1.5)

        title = Text("查询", font_size=26, color=BLUE_E).shift(UP*3.5+RIGHT*5)
        self.add(self.nodes, self.edges, texts_vg, title)

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

class ACAutomata(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        self.patterns = ["i", "in", "tin", "sting"]
        self.text = "sting"
        #self.patterns = ["at", "art", "oars", "soar"]
        #self.text = "soat"
        self.root = TrieNode()
        self.nodes = VGroup(self.root)
        self.edges = VGroup()
        self.suffix_links = VGroup()
        self.output_links = VGroup()
        self.build()
        self.place(self.root)
        self.bfs()
        self.add(self.edges)
        self.add(self.nodes)
        self.add(self.suffix_links)
        self.add(self.output_links)
        patterns = VGroup()
        for pattern in self.patterns:
            text = Text(pattern, color=BLACK, font="DroidSansMono Nerd Font", font_size=22)
            patterns.add(text)
        patterns.arrange(DOWN, buff=0.5)
        self.add(patterns)
        patterns.shift(RIGHT*5)
        self.nodes.shift(LEFT)
        self.edges.shift(LEFT)
        self.suffix_links.shift(LEFT)
        self.output_links.shift(LEFT)
        self.matches()
        #self.build_animate()
        #self.match_animate()
        #self.wait()

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
                    v.dth = u.dth + 1
                    self.nodes.add(v)
                u = u.children[c]
            u.pattern = pattern
            self.nodes[-1][0].set_fill(RED_E, opacity=1)

    def bfs(self):
        q = queue.Queue()
        q.put(self.root)
        while not q.empty():
            u = q.get()
            # Build suffix link.
            for a, v in u.children.items():
                if u == self.root:
                    v.suffix_link = u
                else:
                    x = u.suffix_link
                    while v.suffix_link is None:
                        if a in x.children.keys():
                            v.suffix_link = x.children[a]
                        elif x == self.root:
                            v.suffix_link = x
                        else:
                            x = x.suffix_link

                p1 = v.get_center()
                p2 = v.suffix_link.get_center()
                np1, np2 = get_p(p1, p2, v[0].radius)
                p1[1] += 0.1
                p2[1] += 0.1
                l = math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
                e = Arrow(p1, p2, color=RED_C, stroke_width=3, 
                        max_tip_length_to_length_ratio=0.2/l)
                self.suffix_links.add(e)
                v.suffix_edge = e

                # Build output link.
                if v.suffix_link.pattern is not None:
                    v.output_link = v.suffix_link
                else:
                    v.output_link = v.suffix_link.output_link
                if v.output_link is not None:
                    p1 = v.get_center()
                    p2 = v.output_link.get_center()
                    np1, np2 = get_p(p1, p2, v[0].radius)
                    rand = random.random() * 0.1
                    p1[1] -= 0.15 + rand
                    p2[1] -= 0.15 + rand
                    l = math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
                    e = Arrow(p1, p2, color=BLUE_E, stroke_width=3, 
                            max_tip_length_to_length_ratio=0.2/l)
                    self.output_links.add(e)
                    v.output_edge = e

                q.put(v)

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
            np1, np2 = get_p(p1, p2, child[0].radius)
            e = Line(np1, np2, color=BLACK)
            self.edges.add(e)
            self.place(child)

    def matches(self):
        text = Array(self.text)
        text.shift(DOWN*3.3+LEFT)
        self.add(text)
        ari = Triangle(color=RED_E).set_fill(RED, opacity=1).rotate(-180*DEGREES).scale(.03)
        pi = Text("i", color=RED_E, font="DroidSansMono Nerd Font", font_size=16)
        pi.next_to(text[0], UP, buff=0.1).shift(LEFT*0.2)
        pj = Text("j", color=RED_E, font="DroidSansMono Nerd Font", font_size=16)
        pj.next_to(text[0], DOWN, buff=0.1).shift(LEFT*0.2)
        self.add(pi, pj)

        u = self.root

        i = 0
        j = 0
        for c in self.text:
            while not c in u.children.keys():
                e = u.suffix_edge
                i = j - u.suffix_link.dth
                u = u.suffix_link
                run_time = 0.8
                self.play(ShowPassingFlash(e.copy().set_color(BLUE_E),
                    run_time=run_time,
                    time_width=run_time))
                anim  = pi.animate.next_to(text[i], UP, buff=0.1)
                self.play(anim, Indicate(u[0], color=BLUE_E), run_time=1)
                if u == self.root:
                    break
            if c in u.children.keys():
                u = u.children[c]
                anim  = pj.animate.next_to(text[j], DOWN, buff=0.1)
                j += 1
                self.play(anim, Indicate(u[0], color=BLUE_E), run_time=1)
            self.wait(0.3)
            v = u
            dth = v.dth
            while v is not None:
                if v.pattern is not None:
                    anims = []
                    for k in range(dth-v.dth, dth):
                        anims.append(Indicate(text[k][1], color=RED_E, scale_factor=2))
                    self.play(*anims)
                e = v.output_edge
                run_time=1
                if e is not None:
                    self.play(ShowPassingFlash(e.copy().set_color(PURE_RED),
                                run_time=run_time,
                                time_width=run_time))
                    self.play(Indicate(v.output_link[0], color=GREEN_E))
                v = v.output_link
                self.wait(0.3)

class Pic(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        font = "DroidSansMono Nerd Font"
        pl = Rectangle(height=1, width=3, color=BLACK)
        pl.shift(UP)
        tl = Text("w", color=BLACK, font=font, font_size=28)
        tl.move_to(pl)
        pr = Rectangle(height=0.5*2, width=0.5*2, color=BLACK)
        pr.set_fill(color=YELLOW, opacity=1)
        pr.next_to(pl, RIGHT, buff=0)
        tr = Text("a", color=BLACK, font=font, font_size=28)
        tr.move_to(pr)
        self.add(pl, tl, pr, tr)

        pl1 = Rectangle(height=0.5*2, width=1*2, color=BLACK)
        tl1 = Text("x", color=BLACK, font=font, font_size=28)
        pr1 = Rectangle(height=0.5*2, width=0.5*2, color=BLACK)
        pr1.set_fill(color=YELLOW, opacity=1)
        pr1.next_to(pr, DOWN, buff=0.5*2)
        pl1.next_to(pr1, LEFT, buff=0)
        tl1.move_to(pl1)
        tr1 = Text("a", color=BLACK, font=font, font_size=28)
        tr1.move_to(pr1)
        self.add(pl1, tl1, pr1, tr1)

class Pic2(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        font = "DroidSansMono Nerd Font"
        pl = Rectangle(height=1, width=4, color=BLACK)
        pl.shift(UP*2)
        tl = Text("w", color=BLACK, font=font, font_size=28)
        tl.move_to(pl)
        pr = Rectangle(height=0.5*2, width=0.5*2, color=BLACK)
        pr.set_fill(color=YELLOW, opacity=1)
        pr.next_to(pl, RIGHT, buff=0)
        tr = Text("a", color=BLACK, font=font, font_size=28)
        tr.move_to(pr)
        self.add(pl, tl, pr, tr)

        pl0 = Rectangle(height=0.5*2, width=1*3, color=BLACK)
        pl0.next_to(pl, DOWN, buff=1).shift(RIGHT*0.5)
        tl0 = Text("x", color=BLACK, font=font, font_size=28)
        tl0.move_to(pl0)

        pl1 = Rectangle(height=0.5*2, width=1*2, color=BLACK)
        tl1 = Text("y", color=BLACK, font=font, font_size=28)
        pr1 = Rectangle(height=0.5*2, width=0.5*2, color=BLACK)
        pr1.set_fill(color=YELLOW, opacity=1)
        pr1.next_to(pr, DOWN, buff=3)
        pl1.next_to(pr1, LEFT, buff=0)
        tl1.move_to(pl1)
        tr1 = Text("a", color=BLACK, font=font, font_size=28)
        tr1.move_to(pr1)
        self.add(pl1, tl1, pr1, tr1, pl0, tl0)

class Test(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        text = "soat"
        self.text = Array(text)
        self.text.shift(DOWN*3)
        self.add(self.text)
        ari = Triangle(color=RED_E).set_fill(RED, opacity=1).rotate(-180*DEGREES).scale(.03)
        pi = Text("i", color=RED_E, font="DroidSansMono Nerd Font", font_size=16)
        pi.next_to(self.text[0], UP, buff=0.1)
        pj = Text("j", color=RED_E, font="DroidSansMono Nerd Font", font_size=16)
        pj.next_to(self.text[2], DOWN, buff=0.1)
        self.add(pi, pj)
