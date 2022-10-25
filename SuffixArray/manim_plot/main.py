from manim import *
from utils import *

class Fig1to2(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        self.texts = ["ant", "ante", "anteater", "antelope", "antique"]
        self.pattern = "ante"
        self.root = TrieNode()
        self.nodes = VGroup(self.root)
        self.edges = VGroup()
        self.build()
        self.place(self.root)
        #self.add(self.edges)
        #self.add(self.nodes)

        # Fig 1
        self.build_animate()
        # Fig 2
        # self.match_animate()

        self.wait()

    def build(self):
        w = 10
        self.root.w = w
        self.root.l = -w // 2 
        self.root.shift(UP*3.3)
        for text in self.texts:
            u = self.root
            for c in text:
                if c not in u.children:
                    v = TrieNode(c, len(u.children))
                    u.children[c] = v 
                    self.nodes.add(v)
                u = u.children[c]
            u.text = text
            self.nodes[-1][0].set_fill(RED_E, opacity=1)

    def place(self, father):
        n = max(1, len(father.children))
        l = father.l
        w = father.w
        h = father.get_center()[1]
        gap = w / n / 2 
        p1 = father.get_center()
        for child in father.children.values():
            pos = [l + (child.idx * 2 + 1) * gap, h - 0.8, 0]
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
        texts = VGroup()
        for text in self.texts:
            text = Text(text, color=BLACK, font="DroidSansMono Nerd Font", font_size=22)
            texts.add(text)
        texts.arrange(DOWN, buff=0.5)
        texts.shift(RIGHT*5)
        self.texts_vg = texts
        self.title = Text("构造", font_size=26, color=BLUE_E).shift(UP*3.5+RIGHT*5)
        self.add(texts, self.title)
        ar = Triangle(color=RED_E).set_fill(RED, opacity=1).rotate(-180*DEGREES).scale(.03)
        pos = UP*0.3+LEFT*(len(self.texts[0])//2)*0.2
        if len(self.texts[0]) % 2 == 0:
            pos += RIGHT*0.1
        ar.move_to(texts[0]).shift(pos)
        self.play(FadeIn(ar), FadeIn(self.root))
        for i, text in enumerate(self.texts):
            if i != 0:
                pos = UP*0.3+LEFT*(len(self.texts[i])//2)*0.2
                if len(self.texts[i]) % 2 == 0:
                    pos += RIGHT*0.1
                self.play(ar.animate.move_to(texts[i]).shift(pos), runn_time=0.8)
            u = root
            u0 = self.root
            for j, c in enumerate(text):
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
                        run_time=0.8
                            )
                else:
                    self.play(Indicate(u0.children[c][0], color=TEAL), run_time=0.8)

                if j < len(text) - 1:
                    self.play(ar.animate.shift(RIGHT*0.2), run_time=0.8)

                u = u.children[c]
                u0 = u0.children[c]
            u.text = text
            self.play(u0[0].animate.set_fill(RED_E, opacity=1), run_time=0.8)
        self.remove(ar)

    def match_animate(self):
        text = "ante"
        text_vg = VGroup(Text(text, color=BLACK, font="DroidSansMono Nerd Font", font_size=22))
        text_vg.shift(RIGHT*5+UP*2)

        title = Text("前缀匹配", font_size=26, color=BLUE_E).shift(UP*3.5+RIGHT*5)
        self.add(self.nodes, self.edges, text_vg, title)

        ar = Triangle(color=RED_E).set_fill(RED, opacity=1).rotate(-180*DEGREES).scale(.03)
        ar.move_to(text_vg).shift(UP*0.3+LEFT*(len(text)//2)*0.2)
        if len(text) % 2 == 0:
            ar.shift(RIGHT*0.1)
        self.play(FadeIn(ar))

        u = self.root
        for j, c in enumerate(text):
            u = u.children.get(c)
            if u is None:
                break
            else:
                self.play(Indicate(u[0], color=TEAL), run_time=0.8)
            if j < len(text) - 1:
                self.play(ar.animate.shift(RIGHT*0.2), run_time=0.8)
        self.i = 0
        def dfs(u, text):
            self.play(Indicate(u[0], color=BLUE), run_time=0.8)
            if u.text is not None:
                t = Text(text, color=RED, font="DroidSansMono Nerd Font", font_size=22)
                t.shift(RIGHT * 5, DOWN*self.i/2)
                self.add(t)
                self.i += 1
            for c in u.children:
                v = u.children[c]
                dfs(v, text + v[1].text)

        dfs(u, text)

    def match(self, text):
        m = len(text)
        for i in range(m):
            u = self.root
            for j in range(i, m):
                u = u.children.get(text[j])
                if u is None:
                    break
                else:
                    text = u.text
                    if text is not None:
                        print(text)

class Fig3to4(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        self.who = "fig3"

        if self.who == "fig3":
            self.fig3()
        else:
            self.fig4()

        self.root = TrieNode(size=self.node_size)
        self.nodes = VGroup(self.root)
        self.edges = VGroup()
        self.build()
        self.compress(self.root)

        if self.who == "fig3":
            self.place3(self.root)
        else:
            self.place4(self.root)
        
        tree = VGroup(self.root, self.nodes, self.edges)

        if self.who == "fig4":
            tree.shift(LEFT * 0.5)

        self.add(tree)

    def fig3(self):
        self.split = False
        self.node_size = 0.45
        self.scale = 0.4
        self.gap = 2.5
        self.texts = ["ant$", "ante$", "anteater$", "antelope$", "antique$"]

    def fig4(self):
        self.split = True
        self.node_size = 0.4
        self.scale = 0.4
        self.gap = 1.5
        text = "abcabcacab$"
        self.texts = [ text[i:] for i in range(len(text))]
        vg = VGroup()
        for txt in self.texts:
            t = Text(txt, color=BLACK, font="DroidSansMono Nerd Font", font_size=22)
            txt = (len(text) - len(txt)) * "*"
            t0 = Text(txt, color=WHITE, font="DroidSansMono Nerd Font", font_size=22)
            vg.add(VGroup(t, t0).arrange(RIGHT, buff=0))
        vg.arrange(DOWN, buff=0.3).shift(RIGHT * 5.5)
        self.add(vg)

    def compress(self, u):
        if len(u.children) == 1:
            text = u[1].text
            uu = u
            while len(uu.children) == 1:
                c = next(iter(uu.children))
                v = uu.children[c]
                uu.children = {}
                text += v[1].text
                uu = v
            u.set_text(text, scale=self.scale, split=self.split)
            u.children = uu.children

        self.nodes.add(u)

        for c in u.children:
            v = u.children[c]
            self.compress(v)

    def build(self):
        w = 12
        self.root.w = w
        self.root.l = -w / 2
        self.root.shift(UP*3)
        for text in self.texts:
            u = self.root
            for c in text:
                if c not in u.children:
                    v = TrieNode(c, len(u.children), size=self.node_size)
                    u.children[c] = v 
                u = u.children[c]
            u.text = text

    def place3(self, father):
        n = max(1, len(father.children))
        l = father.l
        w = father.w
        h = father.get_center()[1]
        gap = w / n / 2
        p1 = father.get_center()
        for child in father.children.values():
            pos = [l + (child.idx * 2 + 1) * gap, h - self.gap, 0]
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
            self.place3(child)

    def place4(self, father, dep=0):
        n = max(1, len(father.children))
        l = father.l
        w = father.w
        h = father.get_center()[1]
        gap = w / n / 1.8
        p1 = father.get_center()
        i = 0
        for child in father.children.values():
            pos = [l + (child.idx * 2 + 1) * gap, h - self.gap, 0]
            child.l = pos[0] - gap
            if i == 0 and dep == 3:
                pos[0] -= gap
            if i == 3 and dep == 0:
                pos[0] -= gap 

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
            i += 1
            self.edges.add(e)
            self.place4(child, dep + 1)

class Fig5(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        text = "abcabcacab"
        #text = Text(t, color=BLACK, font="DroidSansMono Nerd Font", font_size=30)
        t0 = Array([t for t in text])
        t0.shift(UP * 3.3)
        self.add(t0)    

        title1 = Text("所有后缀", color=BLUE_E, font="DroidSansMono Nerd Font", font_size=24)
        title1.shift(UP * 2.3 + LEFT * 4)
        self.add(title1)
    
        t1 = VGroup()
        for i in range(len(text)):
            a = Array([t for t in text[i:]], square_size=0.5)
            t1.add(a)
        t1.arrange(DOWN, buff=0).shift(LEFT * 3.5 + DOWN)
        for a in t1:
            a.shift((len(text) - len(a)) / 4 * LEFT)
        self.add(t1)

        for i in range(len(text)):
            id = Text(str(i), color=BLACK, font="DroidSansMono Nerd Font", font_size=24)
            id.next_to(t1[i][0], LEFT, buff=0.2)
            self.add(id)

        title2 = Text("后缀数组", color=BLUE_E, font="DroidSansMono Nerd Font", font_size=24)
        title2.shift(UP * 2.3 + RIGHT * 4)
        self.add(title2)

        texts = [text[i:] for i in range(len(text))]
        ids = sorted(range(len(texts)), key=texts.__getitem__)
        texts.sort()
        t2 = VGroup()
        for t in texts:
            a = Array(t, square_size=0.5)
            t2.add(a)
        t2.arrange(DOWN, buff=0).shift(RIGHT * 4 + DOWN)
        for a in t2:
            a.shift((len(text) - len(a)) / 4 * LEFT)
        self.add(t2)

        for i in range(len(text)):
            id = Text(str(ids[i]), color=BLACK, font="DroidSansMono Nerd Font", font_size=24)
            id.next_to(t2[i][0], LEFT, buff=0.2)
            self.add(id)

class Fig6(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        titles = ["id", "T", "T_0", "T_1", "T_2", "T_{12}", "SA_0", "SA_{12}", "R_{12}", "SA", "R"]
        titles_vg = VGroup()
        for title in titles:
            title_tex = MathTex(title, font_size=24, color=BLACK)
            title_box = Square(0.6, color=WHITE)
            title_tex.move_to(title_box.get_center())
            titles_vg.add(VGroup(title_tex, title_box))
        titles_vg.arrange(DOWN, buff=0.1).shift(LEFT * 3)

        self.add(titles_vg)

        t = [ord(x) - ord('a') + 1 for x in "abcabcacab"] + [0, 0, 0]

        n = len(t)
        n0 = (n - 1) // 3
        n1 = (n - 1) // 3
        n2 = (n - 2) // 3
        n12 = n1 + n2

        ids = VGroup()
        for i in range(n):
            tex = MathTex(str(i), font_size=22, color=BLACK)
            box = Square(0.5, color=WHITE)
            tex.move_to(box.get_center())
            ids.add(VGroup(tex, box))
        ids.arrange(RIGHT, buff=0).next_to(titles_vg[0], RIGHT, buff=0.1)
        self.add(ids)

        t0 = [i * 3 for i in range(n0)]
        t1 = [i * 3 + 1 for i in range(n1)]
        t2 = [i * 3 + 2 for i in range(n2)]
        t12 = t1 + t2
        seq0 = [t[i:] for i in t0]
        sa0 = sorted(range(len(seq0)), key=seq0.__getitem__)
        seq12 = [t[i:] for i in t12]
        sa12 = sorted(range(len(seq12)), key=seq12.__getitem__)

        r12 = [0 for _ in range(n12)]
        for i in range(n12):
            r12[sa12[i]] = i + 1

        seq = [t[i:] for i in range(n - 3)]
        sa = sorted(range(len(seq)), key=seq.__getitem__)
        r = [0 for _ in range(n - 3)]
        for i in range(n - 3):
            r[sa[i]] = i + 1

        contents = [t, t0, t1, t2, t12, sa0, sa12, r12, sa, r] 

        tmp = sa12.copy()
        for i in range(n12):
            sa12[i] = t12[tmp[i]]

        for i in range(len(contents)):
            ar = Array(contents[i], square_size=0.5)
            ar.next_to(titles_vg[i + 1], RIGHT, buff=0.1)
            self.add(ar)

class Fig7to9(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # Fig 7
        #t = [ord(x) - ord('a') + 1 for x in "abcabcacab"]
        #self.add_t_t12(t)

        # Fig 8
        #t = [ord(x) - ord('a') + 1 for x in "abcabcacab"]
        #self.add_t_t12(t)
        #self.sort(3.33, 7)

        # Fig 9
        t = [3, 3, 4, 1, 4, 5, 2]
        self.add_t_t12(t)
        self.sort(1.3, 7)

    def add_t_t12(self, t):
        square_size = 0.8
        titles = ["id", "T", "T_{12}"]
        titles_vg = VGroup()
        for title in titles:
            title_tex = MathTex(title, font_size=24, color=BLACK)
            title_box = Square(square_size, color=WHITE)
            title_tex.move_to(title_box.get_center())
            titles_vg.add(VGroup(title_tex, title_box))
        titles_vg.arrange(DOWN, buff=0.1).shift(LEFT * 5.5 + UP)
        titles_vg[0].shift(DOWN * 0.1)
        titles_vg[2].shift(DOWN)
        self.add(titles_vg)

        t += [0, 0, 0]
        n = len(t)
        n0 = (n - 1) // 3
        n1 = (n - 1) // 3
        n2 = (n - 2) // 3
        n12 = n1 + n2

        ids = Array([i for i in range(n)], square_size=square_size)
        for i in range(len(t)):
            if i < 3 * n0 and i % 3 == 0:
                ids[i][0].set_fill(PURPLE, opacity=1)
            elif i < 3 * n1 and i % 3 == 1:
                ids[i][0].set_fill(TEAL, opacity=1)
            elif i < 3 * n2:
                ids[i][0].set_fill(BLUE, opacity=1)

        tt = Array(t, square_size=square_size, color=DARK_BROWN)

        t1 = [i * 3 + 1 for i in range(n1)]
        t2 = [i * 3 + 2 for i in range(n2)]
        t12 = t1 + t2
        tt12 = Array(t12, square_size=square_size)
        for i in range(n1):
            tt12[i][0].set_fill(TEAL, opacity=1)
        for i in range(n2):
            tt12[n1 + i][0].set_fill(BLUE, opacity=1)

        contents = [ids, tt, tt12] 
        for i in range(len(contents)):
            contents[i].next_to(titles_vg[i], RIGHT, buff=0.1)
            self.add(contents[i])

        self.n, self.n0, self.n1, self.n2, self.n12 = n, n0, n1, n2, n12
        self.t, self.t12 = t, t12
        self.titles_vg = titles_vg
        self.ids, self.tt, self.tt12 = ids, tt, tt12

    def sort(self, l_offset, n):
        vg = VGroup(self.titles_vg, self.ids, self.tt, self.tt12)
        vg.shift(UP * 1.5).scale(0.8)
        self.tt12.shift(UP * 0.5)
        self.titles_vg[2].shift(UP * 0.5)

        t = VGroup()
        for i in self.t12:
            t.add(self.tt[i:i+3].copy())

        for i in range(len(t)):
            if i == 0:
                self.play(t[i].animate.shift(DOWN * 5.8 + LEFT * l_offset).scale(0.8))
            else:
                self.play(t[i].animate.next_to(t[i - 1], buff=0.2).scale(0.8))

        nums = VGroup()
        for x in t:
            num = VGroup()
            for y in x:
                num.add(y[1].copy().scale(1.5))
            num.arrange(RIGHT, buff=0.1)
            nums.add(num)
        nums.arrange(RIGHT, buff=0.4).shift(DOWN * 2)

        anims = []
        for i in range(len(t)):
            anims.append(ReplacementTransform(t[i].copy(), nums[i])) 

        buckets = VGroup()
        m = n // 2
        for i in range(n):
            buckets.add(Line([i - m, -1, 0], [i - m, 1, 0], color=BLACK, stroke_width=2))
            if i < n - 1:
                l = Line([i - m, -1, 0], [i - m + 1, -1, 0], color=BLACK, stroke_width=2)
                x = Text(str(i), font_size=16, color=BLACK).next_to(l, DOWN, buff=0.1)
                buckets.add(l, x)

        buckets.shift(DOWN * 0.3)
        anims.append(FadeIn(buckets))
        self.play(*anims)

        nums0 = nums.copy()
        ords = list(range(len(nums0)))
        for j in range(2, -1, -1):
            anims = []
            for num in nums:
                anims.append(num[j].animate.set(color=RED))
            self.play(*anims)

            queue_list = [[Line([i - m, -1.4, 0], [i - m + 1, -1.4, 0])] for i in range(100)]
            for i in range(len(nums)):
                x = int(nums[i][j].text)
                queue_list[x].append(i)

            for queue in queue_list:
                for i in range(1, len(queue)):
                    if i == 1:
                        pre = queue[i - 1]
                    else:
                        pre = nums[queue[i - 1]]
                    self.play(nums[queue[i]].animate.next_to(pre, UP, buff=0.2))

            cnt = 0
            nums1 = nums.copy()
            ordso = ords.copy()
            for queue in queue_list:
                for i in queue[1:]:
                    nums1[cnt] = nums[i]
                    ords[cnt] = ordso[i]
                    cnt += 1
            nums = nums1

            for i in range(len(nums)):
                self.play(nums[i].animate.move_to(nums0[i]))
            anims = []
            for num in nums:
                anims.append(num[j].animate.set(color=DARK_BROWN))
            self.play(*anims)
        
        rk = [1 for _ in range(len(nums))]
        cnt = 1
        for i in range(1, len(nums)):
            if (nums[i][0].text, nums[i][1].text, nums[i][2].text) !=\
               (nums[i - 1][0].text, nums[i - 1][1].text, nums[i - 1][2].text):
                cnt += 1
            rk[i] = cnt

        rkt = VGroup()
        for i in range(len(nums)):
            txt = Text(str(rk[i]), color=RED, font="DroidSansMono Nerd Font", font_size=16)
            txt.next_to(nums0[i], DOWN, buff=0.2)
            rkt.add(txt)
        for i in range(len(nums)):
            self.play(FadeIn(rkt[i], run_time=0.7))

        rkt1 = rkt.copy()
        for i in range(len(nums)):
            rkt1[i].next_to(t[ords[i]], UP, buff=0.2)

        for i in range(len(nums)):
            self.play(ReplacementTransform(VGroup(nums[i], rkt[i]), rkt1[i]))

        self.play(FadeOut(buckets))

        sa12_tex = MathTex("SA_{12}", font_size=24, color=BLACK)
        sa12_box = Square(0.8, color=WHITE)
        sa12_tex.move_to(sa12_box.get_center())
        sa12_title = VGroup(sa12_tex, sa12_box).scale(0.8)
        sa12_title.next_to(self.titles_vg[-1], DOWN, buff=0.3)

        a = [0 for _ in range(len(nums))]
        for i in range(len(nums)):
            a[i] = self.t12[ords[i]]
        sa12_content = Array(a, square_size=0.8).scale(0.8)
        sa12_content.next_to(sa12_title, RIGHT, buff=0.1)
        sa12_vg = VGroup(sa12_title, sa12_content)

        r12_tex = MathTex("R_{12}", font_size=24, color=BLACK)
        r12_box = Square(0.8, color=WHITE)
        r12_tex.move_to(r12_box.get_center())
        r12_title = VGroup(r12_tex, r12_box).scale(0.8)
        r12_title.next_to(sa12_title, DOWN, buff=0.3)

        a = [0 for _ in range(len(nums))]
        for i in range(len(nums)):
            a[ords[i]] = rk[i]
        r12_content = Array(a, square_size=0.8).scale(0.8)
        r12_content.next_to(r12_title, RIGHT, buff=0.1)
        r12_vg = VGroup(r12_title, r12_content)

        self.play(ReplacementTransform(rkt1.copy(), r12_vg))

        for i in range(len(nums)):
            if a[i] % 3 == 1:
                sa12_content[i][0].set_fill(color=TEAL, opacity=1)
            else:
                sa12_content[i][0].set_fill(color=BLUE, opacity=1)

        self.play(FadeIn(sa12_vg))

        self.wait()

class Fig10to11(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        t = [3, 3, 4, 1, 4, 5, 2]
        # Fig 10
        #self.add_t_t12(t)
        # Fig 11
        self.add_t_t12(t)
        self.sort()

    def add_t_t12(self, t):
        square_size = 0.8
        titles = ["id", "T", "T_0", "T_{12}", "SA_{12}", "R_{12}"]
        titles_vg = VGroup()
        for title in titles:
            title_tex = MathTex(title, font_size=24, color=BLACK)
            title_box = Square(square_size, color=WHITE)
            title_tex.move_to(title_box.get_center())
            titles_vg.add(VGroup(title_tex, title_box))
        titles_vg.arrange(DOWN, buff=0.5).shift(LEFT * 5.5 + UP)
        titles_vg[0].shift(DOWN*0.5)
        titles_vg.shift(DOWN*0.5)
        self.add(titles_vg)

        t += [0, 0, 0]
        n = len(t)
        n0 = (n - 1) // 3
        n1 = (n - 1) // 3
        n2 = (n - 2) // 3
        n12 = n1 + n2

        ids = Array([i for i in range(n)], square_size=square_size)
        tt = Array(t, square_size=square_size, color=DARK_BROWN)
        for i in range(len(t)):
            if i < 3 * n0 and i % 3 == 0:
                ids[i][0].set_fill(PURPLE, opacity=1)
            elif i < 3 * n1 and i % 3 == 1:
                ids[i][0].set_fill(TEAL, opacity=1)
            elif i < 3 * n2:
                ids[i][0].set_fill(TEAL, opacity=1)

        t0 = [i * 3 for i in range(n0)]
        tt0 = Array(t0, square_size=square_size)
        for i in range(n0):
            tt0[i][0].set_fill(PURPLE, opacity=1)

        t1 = [i * 3 + 1 for i in range(n1)]
        t2 = [i * 3 + 2 for i in range(n2)]
        t12 = t1 + t2
        tt12 = Array(t12, square_size=square_size)
        for i in range(n1):
            tt12[i][0].set_fill(TEAL, opacity=1)
        for i in range(n2):
            tt12[n1 + i][0].set_fill(BLUE, opacity=1)

        seq12 = [t[i:] for i in t12]
        sa12 = sorted(range(len(seq12)), key=seq12.__getitem__)
        r12 = [0 for _ in range(n12)]
        for i in range(n12):
            r12[sa12[i]] = i + 1
        rr12 = Array(r12, square_size=square_size)

        saa12 = Array([t12[i] for i in sa12], square_size=square_size)
        for i in range(n12):
            if t[sa12[i]] % 3 == 1:
                saa12[i][0].set_fill(TEAL, opacity=1)
            else:
                saa12[i][0].set_fill(BLUE, opacity=1)

        contents = [ids, tt, tt0, tt12, saa12, rr12] 
        for i in range(len(contents)):
            contents[i].next_to(titles_vg[i], RIGHT, buff=0.1)
            self.add(contents[i])
        
        self.n, self.n0, self.n1, self.n2, self.n12 = n, n0, n1, n2, n12
        self.t, self.t0, self.t12 = t, t0, t12
        self.titles_vg = titles_vg
        self.ids, self.tt, self.tt0, self.tt12, self.rr12 = ids, tt, tt0, tt12, rr12

    def sort(self):
        vg = VGroup()
        vgg = VGroup()

        vg0 = VGroup()
        for i in self.t0:
            vg0.add(self.tt[i].copy())
        
        vg1 = VGroup()
        for i in range(self.n0):
            vg1.add(self.rr12[i].copy())

        for i in range(self.n0):
            self.play(Indicate(self.tt[i * 3][0], color=BLACK),
                      Indicate(self.tt0[i][0], color=PURPLE),
                      Indicate(self.ids[i * 3][0], color=PURPLE))

            if i == 0:
                self.play(vg0[i].animate.shift(RIGHT * 6.4 + DOWN * 3))
            else:
                self.play(vg0[i].animate.next_to(vg0[i - 1], DOWN, buff=0.3))

            self.play(Indicate(self.tt12[i][0], color=TEAL),
                      Indicate(self.rr12[i][0], color=BLACK))

            self.play(vg1[i].animate.next_to(vg0[i], RIGHT, buff=0))

            vg.add(VGroup(vg0[i].copy(), vg1[i].copy()))
            vgg.add(VGroup(vg0[i], vg1[i]))

        # sort
        ords = VGroup(*[MathTex(str(i), font_size=24, color=BLACK) for i in self.t0])
        for i in range(self.n0):
            ords[i].next_to(vgg[i], LEFT, buff=0.3)
        self.play(FadeIn(ords))
        self.wait()

        sa0 = [i for i in self.t0]
        for i in range(self.n0):
            for j in range(i + 1, self.n0):
                if vg[i][0][1].text + vg[i][1][1].text > vg[j][0][1].text + vg[j][1][1].text:
                    vg[i], vg[j] = vg[j], vg[i]
                    sa0[i], sa0[j] = sa0[j], sa0[i]

        ords1 = VGroup(*[MathTex(str(i), font_size=24, color=BLACK) for i in sa0])
        for i in range(self.n0):
            ords1[i].next_to(vgg[i], LEFT, buff=0.3)

        for i in range(self.n0):
            vg[i].move_to(vgg[i])
        self.play(ReplacementTransform(vgg, vg), ReplacementTransform(ords, ords1))
        self.wait()

        title0 = MathTex("SA_0", font_size=24, color=BLACK)
        saa0 = Array(sa0, color=BLACK, square_size=0.8)
        for x in saa0:
            x[0].set_fill(PURPLE, opacity=1)

        saa0.next_to(self.tt0, RIGHT, buff=3.22)
        title0.next_to(saa0, LEFT, buff=0.3)

        self.play(ReplacementTransform(ords.copy(), VGroup(saa0, title0)))

        self.wait()

class Fig12(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # Fig 12
        t = [3, 3, 4, 1, 4, 5, 2] + [0, 0, 0]
        self.add_base(t)
        #t = [ord(x) - ord('a') + 1 for x in "abcabcacab"] + [0, 0, 0]

    def add_base(self, t):
        square_size=0.6

        titles = ["id", "T", "SA_0", "SA_{12}", "R_{12}", "SA"]
        titles_vg = VGroup()
        for title in titles:
            title_tex = MathTex(title, font_size=24, color=BLACK)
            title_box = Square(square_size, color=WHITE)
            title_tex.move_to(title_box.get_center())
            titles_vg.add(VGroup(title_tex, title_box))
        titles_vg.arrange(DOWN, buff=0.7).shift(LEFT * 6)
        titles_vg[0].shift(DOWN*0.7)
        titles_vg[4].next_to(titles_vg[3], RIGHT, buff=4.5)
        titles_vg[5].shift(UP*1.2)

        self.add(titles_vg)

        n = len(t)
        n0 = (n - 1) // 3
        n1 = (n - 1) // 3
        n2 = (n - 2) // 3
        n12 = n1 + n2

        tt = Array(t, square_size=square_size, color=DARK_BROWN)

        ids = Array([i for i in range(n)], square_size=square_size)
        for i in range(len(t)):
            if i < 3 * n0 and i % 3 == 0:
                ids[i][0].set_fill(PURPLE, opacity=1)
            elif i < 3 * n1 and i % 3 == 1:
                ids[i][0].set_fill(TEAL, opacity=1)
            elif i < 3 * n2:
                ids[i][0].set_fill(BLUE, opacity=1)

        t0 = [i * 3 for i in range(n0)]
        t1 = [i * 3 + 1 for i in range(n1)]
        t2 = [i * 3 + 2 for i in range(n2)]
        t12 = t1 + t2
        seq0 = [t[i:] for i in t0]
        sa0 = sorted(range(len(seq0)), key=seq0.__getitem__)
        seq12 = [t[i:] for i in t12]
        sa12 = sorted(range(len(seq12)), key=seq12.__getitem__)
        seq = [t[i:] for i in range(n0 + n12)]
        sa = sorted(range(len(seq)), key=seq.__getitem__)
        r12 = [0 for _ in range(n12)]
        for i in range(n12):
            r12[sa12[i]] = i + 1

        for i in range(n0):
            sa0[i] = t0[sa0[i]]
        for i in range(n12):
            sa12[i] = t12[sa12[i]]

        saa0 = Array(sa0, square_size=square_size)
        for i in range(n0):
            saa0[i][0].set_fill(PURPLE, opacity=1)

        rr12 = Array(r12, square_size=square_size)
        saa12 = Array(sa12, square_size=square_size)
        for i in range(n12):
            if sa12[i] % 3 == 1:
                saa12[i][0].set_fill(TEAL, opacity=1)
            else:
                saa12[i][0].set_fill(BLUE, opacity=1)

        saa = Array(sa, square_size=square_size)
        for i in range(len(sa)):
            if sa[i] % 3 == 0:
                saa[i][0].set_fill(PURPLE, opacity=1)
            elif i % 3 == 1:
                saa[i][0].set_fill(TEAL, opacity=1)
            else:
                saa[i][0].set_fill(BLUE, opacity=1)

        contents = [ids, tt, saa0, saa12, rr12, saa] 
        for i in range(len(contents)):
            contents[i].next_to(titles_vg[i], RIGHT, buff=0.1)
            if i < len(contents) - 1:
                self.add(contents[i])

        tt12 = Array(t12, square_size=square_size)
        for i in range(n1):
            tt12[i][0].set_fill(TEAL, opacity=1)
        for i in range(n2):
            tt12[n1+i][0].set_fill(BLUE, opacity=1)
        tt_title = MathTex("id", font_size=24, color=BLACK)
        tt12.next_to(rr12, UP, buff=0)
        tt_title.next_to(tt12, LEFT, buff=0.3)
        self.add(tt_title, tt12)

        # animation
        ar = Triangle(color=RED_E).set_fill(RED, opacity=1).rotate(-180*DEGREES).scale(.03)
        ari = VGroup(MathTex("i", font_size=20, color=BLACK), ar.copy()).arrange(DOWN, buff=0.1)
        arj = VGroup(MathTex("j", font_size=20, color=BLACK), ar.copy()).arrange(DOWN, buff=0.1)

        ari.next_to(saa0[0], UP, buff=0.1)
        arj.next_to(saa12[0], UP, buff=0.1)

        self.add(ari, arj)

        # 1
        t1_1_title = Info("T[a]", color=BLACK)
        t1_1_title.move_to(RIGHT * 4.5 + UP * 2.5)
        t1_1_value = Info()
        t1_1_value.next_to(t1_1_title, DOWN, buff=0)
        
        cmp1 = Info()
        cmp1.next_to(t1_1_value, RIGHT, buff=0.2)

        t2_1_title = Info("T[b]", color=BLACK)
        t2_1_value = Info()
        t2_1_title.next_to(t1_1_title, RIGHT, buff=1)
        t2_1_value.next_to(t2_1_title, DOWN, buff=0)

        # 2
        t1_2_title = Info()
        t1_2_value = Info()
        t1_2_title.next_to(t1_1_value, DOWN, buff=0.2)
        t1_2_value.next_to(t1_2_title, DOWN, buff=0)
        
        cmp2 = Info()
        cmp2.next_to(t1_2_value, RIGHT, buff=0.2)

        t2_2_title = Info()
        t2_2_value = Info()
        t2_2_title.next_to(t1_2_title, RIGHT, buff=1)
        t2_2_value.next_to(t2_2_title, DOWN, buff=0)

        # 3
        t1_3_title = Info()
        t1_3_value = Info()
        t1_3_title.next_to(t1_2_value, DOWN, buff=0.2)
        t1_3_value.next_to(t1_3_title, DOWN, buff=0)
        
        cmp3 = Info()
        cmp3.next_to(t1_2_value, RIGHT, buff=0.2)

        t2_3_title = Info()
        t2_3_value = Info()
        t2_3_title.next_to(t1_3_title, RIGHT, buff=1)
        t2_3_value.next_to(t2_3_title, DOWN, buff=0)

        self.add(t1_1_title, t1_1_value, t2_1_title, t2_1_value, cmp1,
                t1_2_title, t1_2_value, t2_2_title, t2_2_value, cmp2,
                t1_3_title, t1_3_value, t2_3_title, t2_3_value, cmp3)

        i = j = 0
        ssa = []
        r12 += [0, 0, 0]
        while i < n0 and j < n12:
            a = sa0[i]
            b = sa12[j]
            self.play(Indicate(tt[a][0], color=BLACK),
                      Indicate(tt[b][0], color=BLACK))
            self.play(t1_1_value.animate.update_text(t[a]),
                      t2_1_value.animate.update_text(t[b]))

            if t[a] < t[b]:
                pd = 1
                self.play(cmp1.animate.update_text("<"))
            elif t[a] > t[b]:
                pd = 0
                self.play(cmp1.animate.update_text(">"))
            elif b % 3 == 1:
                self.play(cmp1.animate.update_text("="))

                self.play(t1_2_title.animate.update_text("R_{12}[a+1]"),
                          t2_2_title.animate.update_text("R_{12}[b+1]"))

                self.play(Indicate(rr12[(a + 1) // 3][0], color=BLACK),
                          Indicate(rr12[n1 + (b + 1) // 3][0], color=BLACK))

                self.play(t1_2_value.animate.update_text(r12[(a + 1) // 3]),
                            t2_2_value.animate.update_text(r12[n1 + (b + 1) // 3]))

                if (t[a], r12[(a + 1) // 3]) < (t[b], r12[n1 + (b + 1) // 3]):
                    pd = 1
                    self.play(cmp2.animate.update_text("<"))
                else:
                    pd = 0
                    self.play(cmp2.animate.update_text(">"))
            elif b % 3 == 2:
                self.play(cmp1.animate.update_text(">"))

                self.play(t1_2_title.animate.update_text("T[a+1]"),
                            t2_2_title.animate.update_text("T[b+1]"))

                self.play(Indicate(tt[a + 1][0], color=BLACK),
                          Indicate(tt[b + 1][0], color=BLACK))

                self.play(t1_2_value.animate.update_text(t[a+1]),
                            t2_2_value.animate.update_text(t[b+1]))

                if t[a + 1] < t[b + 1]:
                    pd = 1
                    self.play(cmp2.animate.update_text("<"))
                elif t[a + 2] < t[b + 2]:
                    pd = 0
                    self.play(cmp2.animate.update_text(">"))
                else:
                    self.play(cmp2.animate.update_text("="))
                    self.play(t1_3_title.animate.update_text("R[a+2]"),
                            t2_3_title.animate.update_text("R[b+2]"))

                    self.play(Indicate(rr12[(a + 2) // 3][0], color=BLACK),
                              Indicate(rr12[n1 + (b + 2) // 3][0], color=BLACK))

                    self.play(t1_3_value.animate.update_text(r12[(a + 2) // 3]),
                            t2_3_value.animate.update_text(r12[n1 + (b + 2) // 3]))

                    if r12[n1 + (a + 2) // 3] < r12[(b + 2) // 3]:
                        pd = 1
                        self.play(cmp3.animate.update_text("<"))
                    else:
                        pd = 0
                        self.play(cmp3.animate.update_text(">"))

            if pd == 1:
                self.play(ReplacementTransform(saa0[i].copy(), saa[len(ssa)]))
                ssa.append(a)
                i += 1
                if i < n0:
                    self.play(ari.animate.next_to(saa0[i], UP, buff=0.1))
                if i == n0:
                    while j < n12:
                        self.play(arj.animate.next_to(saa12[j], UP, buff=0.1))
                        self.play(ReplacementTransform(saa12[j].copy(), saa[len(ssa)]))
                        ssa.append(sa12[j])
                        j += 1
            else: 
                self.play(ReplacementTransform(saa12[j].copy(), saa[len(ssa)]))
                ssa.append(b)
                j += 1
                if j < n12:
                    self.play(arj.animate.next_to(saa12[j], UP, buff=0.1))
                if j == n12:
                    while i < n0:
                        self.play(ari.animate.next_to(saa0[i], UP, buff=0.1))
                        self.play(ReplacementTransform(saa0[i].copy(), saa[len(ssa)]))
                        ssa.append(sa0[i])
                        i += 1
        print(ssa)
        
class BuildSuffixArray(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        self.t = list("abcabcacab")
        t = [ord(x) - ord('a') + 1 for x in self.t]
        # self.sa = self.build(t, 256)
        # self.start(t)
        self.split(t)
        self.sort()
        self.wait()

    def playa(self, anims):
        for anim in anims:
            self.play(anim)

    def start(self, t):
        mt_ = Array(self.t)
        mt = Array(t)
        self.add(mt_)
        self.play(ReplacementTransform(mt_, mt))
        self.play(mt.animate.shift(UP * 3, LEFT * 0.6 * 1.5))
        self.remove(mt, mt_)

    def split(self, t):
        t += [0, 0, 0]
        n = len(t)
        n0 = (n - 1) // 3
        n1 = (n - 1) // 3
        n2 = (n - 2) // 3
        n12 = n1 + n2
        sa12 = [i * 3 + 1 for i in range(n1)] + \
               [i * 3 + 2 for i in range(n2)]
        r12 = [0 for _ in range(len(sa12))] + [0]
        sa0 = [i * 3 for i in range(n0)]
    
        self.mt = Array(t).shift(UP * 3)
        self.msa0 = Array(t)
        self.add(self.mt[:-3])

        ''' add zeros
        self.play(FadeIn(self.mt[-3:]))
        '''

        #''' add zeros 1
        self.add(self.mt[-3:])
        #'''

        ''' set color
        anims0_0, anims0_1, anims0_2 = [], [], []
        for i in range(n):
            if i < 3 * n0 and i % 3 == 0:
                anims0_0.append(self.mt[i][0].animate.set_fill(PURPLE, opacity=1))
            elif i < 3 * n1 and i % 3 == 1:
                anims0_1.append(self.mt[i][0].animate.set_fill(TEAL, opacity=1))
            elif i < 3 * n2:
                anims0_2.append(self.mt[i][0].animate.set_fill(BLUE, opacity=1))

        self.play(*anims0_0, run_time=1)
        self.play(*anims0_1, run_time=1)
        self.play(*anims0_2, run_time=1)
        '''

        #''' set color 1
        for i in range(n):
            if i < 3 * n0 and i % 3 == 0:
                self.mt[i][0].set_fill(PURPLE, opacity=1)
            elif i < 3 * n1 and i % 3 == 1:
                self.mt[i][0].set_fill(TEAL, opacity=1)
            elif i < 3 * n2:
                self.mt[i][0].set_fill(BLUE, opacity=1)
        #'''

        self.msa1 = Array(t[1:1+n1*3]).move_to(self.mt[:-1]).shift(DOWN)
        self.msa2 = Array(t[2:2+n2*3]).move_to(self.msa1[:-1]).shift(DOWN)
        self.msa12 = Array(t[1:1+n1*3] + t[2:2+n2*3]).next_to(self.mt, DOWN * 2)
        for i in range(n1):
            self.msa12[i * 3][0].set_fill(TEAL, opacity=1)
            self.msa1[i * 3][0].set_fill(TEAL, opacity=1)
        for i in range(n2):
            self.msa12[n1 * 3 + i * 3][0].set_fill(BLUE, opacity=1)
            self.msa2[i * 3][0].set_fill(BLUE, opacity=1)

        ''' split 
        anims1_1, anims1_2 = [], []
        anims1_1.append(ReplacementTransform(self.mt[1:].copy(), self.msa1))
        anims1_1.append(ReplacementTransform(self.mt[2:].copy(), self.msa2))

        anims1_2.append(ReplacementTransform(self.msa1, self.msa12[:n1 * 3]))
        anims1_2.append(ReplacementTransform(self.msa2, self.msa12[n1 * 3:]))
        self.playa(anims1_1)
        self.play(*anims1_2)
        '''

        #''' split 1
        self.add(self.msa12)
        #'''

    def sort(self):
        buckets = VGroup()
        n = 7
        m = n // 2
        for i in range(n):
            buckets.add(Line([i - m, -2, 0], [i - m, 1, 0], color=BLACK, stroke_width=2))
            if i < 6:
                l = Line([i - m, -2, 0], [i - m + 1, -2, 0], color=BLACK, stroke_width=2)
                t = Text(str(i), font_size=16, color=BLACK).next_to(l, DOWN, buff=0.1)
                buckets.add(l, t)

        #self.play(Create(buckets))
        self.add(buckets)

        nums = VGroup()
        anims = []
        for i in range(len(self.msa12) // 3):
            num = VGroup()
            for x in self.msa12[i * 3: i * 3 + 3]:
                num.add(x[1].copy())
            nums.add(num.arrange(RIGHT, buff=0.1))
            anims.append(ReplacementTransform(self.msa12[i * 3: i * 3 + 3].copy(), num))
        nums.arrange(RIGHT, buff=0.4).shift(DOWN * 2.5)
        
        ''' divide by 3
        self.playa(anims)
        '''

        #''' divide by 3 1
        self.add(nums)
        #'''

        for j in range(1):
            anims = []
            for num in nums:
                anims.append(num[j].animate.set(color=RED))
            self.play(*anims)

            queue_list = [[Line([i - m, -2, 0], [i - m + 1, -2, 0])] for i in range(n)]
            for i in range(len(nums)):
                x = ord(nums[i][j].text) - ord('0')
                queue_list[x].append(nums[i])

            for queue in queue_list:
                for i in range(1, len(queue)):
                    self.play(queue[i].animate.next_to(queue[i - 1], UP, buff=0.2))

            '''
            cnt = 0
            for ids in queue_list:
                for i in ids:
                    b[cnt] = a[i]
                    cnt += 1
            for num in nums:
                anims1_2.append(num[j].animate.set(color=BLACK))
            '''
    
    def build(self, t, N):
        t += [0, 0, 0]
        n = len(t)
        n0 = (n - 1) // 3
        n1 = (n - 1) // 3
        n2 = (n - 2) // 3
        n12 = n1 + n2
        sa12 = [i * 3 + 1 for i in range(n1)] + \
               [i * 3 + 2 for i in range(n2)]
        r12 = [0 for _ in range(len(sa12))] + [0]

        # sort sa12
        self.radix_sort(t[2:], sa12, N)
        self.radix_sort(t[1:], sa12, N)
        self.radix_sort(t[0:], sa12, N)

        # get rank r12
        num = 0
        c0 = c1 = c2 = -1 # size is 3, so cmp 3 neibor chars
        for i in sa12:
            if t[i] != c0 or t[i + 1] != c1 or t[i + 2] != c2:
                c0, c1, c2 = t[i], t[i + 1], t[i + 2]
                num += 1
            if i % 3 == 1:
                r12[(i - 1) // 3] = num
            else:
                r12[n1 + (i - 2) // 3] = num

        # recursive build if r12 contains same order
        if num < n12:
            sa12 = self.build(r12, n12)
            # recover to the right order
            for i in range(n12):
                r12[sa12[i]] = i + 1
                if sa12[i] < n1:
                    sa12[i] = sa12[i] * 3 + 1
                else:
                    sa12[i] = (sa12[i] - n1) * 3 + 2

        # sort sa0
        sa0 = [i - 1 for i in sa12 if i % 3 == 1] # first round 
        self.radix_sort(t, sa0, N) # second round 

        # merge sa0 and sa12
        sa = []
        i = j = 0
        # delete 0s
        while t[sa0[i]] == 0:
            i += 1
        while t[sa12[j]] == 0:
            j += 1

        while i < n0 and j < n12:
            a = sa0[i]
            b = sa12[j]
            if (b % 3 == 0 and t[a] < t[b]) or \
               (b % 3 == 1 and (t[a], r12[(a + 1) // 3]) < (t[b], r12[n1 + (b + 1) // 3])) or \
               (b % 3 == 2 and (t[a], t[a + 1], r12[n1 + (a + 2) // 3]) < (t[b], t[b + 1], r12[(b + 2) // 3])):

                sa.append(a)
                i += 1
                if i == n0:
                    while j < n12:
                        sa.append(sa12[j])
                        j += 1
            else: 
                sa.append(b)
                j += 1
                if j == n12:
                    while i < n0:
                        sa.append(sa0[i])
                        i += 1
        return sa

    def radix_sort(self, t, a, N):
        queue_list = [list() for _ in range(N)]
        for i in a:
            queue_list[t[i]].append(i)

        num = 0
        for ids in queue_list:
            for i in ids:
                a[num] = i
                num += 1

        self.wait()

class Test(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        t = Info("T[a]", RIGHT * 4.5 + UP * 2.5)
        print(t.get_center() + DOWN)
        t1 = Info("T[a]")
        self.add(t)
        self.wait()
        self.play(t.animate.update_text("sd"))
        self.wait()
