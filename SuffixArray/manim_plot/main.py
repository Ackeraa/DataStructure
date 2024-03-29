from manim import *
from utils import *
sys.path.insert(0, '../../RMQ')
sys.path.insert(0, '../')
from cartesian_stack import CartesianTree
from suffix_array import SuffixArray

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

        self.who = "fig4"

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
        text = "cbacbacacb$"
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
        text = "cbacbacacb"
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
            id = MathTex(str(i), color=BLACK, font_size=24)
            sq = Square(0.6).next_to(t1[i][0], LEFT, buff=0)
            id.move_to(sq.get_center())
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
            id = MathTex(str(ids[i]), color=BLACK, font_size=24)
            sq = Square(0.6).next_to(t2[i][0], LEFT, buff=0)
            id.move_to(sq.get_center())
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

        t = [ord(x) - ord('a') + 1 for x in "cbacbacacb"] + [0, 0, 0]

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
        #t = [ord(x) - ord('a') + 1 for x in "cbacbacacb"]
        #self.add_t_t12(t)
        #self.sort(3.33, 7)

        # Fig 9
        t = [3, 3, 4, 1, 4, 5, 2]
        self.add_t_t12(t)
        self.sort(1.3, 7)

    def add_t_t12(self, t):
        square_size = 0.8
        #titles = ["id", "T", "T_{12}"]
        titles = ["id", "T'", "T'_{12}"]
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

        tt = Array(t, square_size=square_size, color=BLACK)

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
                anims.append(num[j].animate.set(color=BLACK))
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

        #sa12_tex = MathTex("SA_{12}", font_size=24, color=BLACK)
        sa12_tex = MathTex("SA'_{12}", font_size=24, color=BLACK)
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

        #r12_tex = MathTex("R_{12}", font_size=24, color=BLACK)
        r12_tex = MathTex("R'_{12}", font_size=24, color=BLACK)
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

class Fig10and11and13(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        t = [4, 4, 3, 1, 3, 2, 5]
        # Fig 10
        #self.add_t_t12(t)

        # Fig 11
        #self.add_t_t12(t)
        #self.sort()

        # Fig 13
        t = [ord(x) - ord('a') + 1 for x in "cbacbacacb"]
        self.add_t_t12(t)
        self.sort()

    def add_t_t12(self, t):
        square_size = 0.8
        titles = ["id", "T", "T_0", "T_{12}", "SA_{12}", "R_{12}"]
        #titles = ["id", "T'", "T'_0", "T'_{12}", "SA'_{12}", "R'_{12}"]
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
        tt = Array(t, square_size=square_size, color=BLACK)
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
                self.play(vg0[i].animate.shift(RIGHT * 6.4 + DOWN * 2.5))
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
        #title0 = MathTex("SA'_0", font_size=24, color=BLACK)
        saa0 = Array(sa0, color=BLACK, square_size=0.8)
        for x in saa0:
            x[0].set_fill(PURPLE, opacity=1)

        saa0.next_to(self.tt0, RIGHT, buff=3.22)
        title0.next_to(saa0, LEFT, buff=0.3)

        self.play(ReplacementTransform(ords.copy(), VGroup(saa0, title0)))

        self.wait()

class Fig12and14(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # Fig 12
        t = [4, 4, 3, 1, 3, 2, 5] + [0, 0, 0]
        self.add_base(t)
        # Fig 14
        #t = [ord(x) - ord('a') + 1 for x in "cbacbacacb"] + [0, 0, 0]
        #self.add_base(t)

    def add_base(self, t):
        square_size=0.6

        #titles = ["id", "T", "SA_0", "SA_{12}", "R_{12}", "SA"]
        titles = ["id", "T'", "SA'_0", "SA'_{12}", "R'_{12}", "SA'"]
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

        tt = Array(t, square_size=square_size, color=BLACK)

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
            elif sa[i] % 3 == 1:
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
        #t1_1_title = Info("T[a]", color=BLACK)
        t1_1_title = Info("T'[a]", color=BLACK)
        t1_1_title.move_to(RIGHT * 4.5 + UP * 2.5)
        t1_1_value = Info()
        t1_1_value.next_to(t1_1_title, DOWN, buff=0)
        
        cmp1 = Info()
        cmp1.next_to(t1_1_title, RIGHT, buff=0.2)

        #t2_1_title = Info("T[b]", color=BLACK)
        t2_1_title = Info("T'[b]", color=BLACK)
        t2_1_value = Info()
        t2_1_title.next_to(t1_1_title, RIGHT, buff=1)
        t2_1_value.next_to(t2_1_title, DOWN, buff=0)

        # 2
        t1_2_title = Info()
        t1_2_value = Info()
        t1_2_title.next_to(t1_1_value, DOWN, buff=0.2)
        t1_2_value.next_to(t1_2_title, DOWN, buff=0)
        
        cmp2 = Info()
        cmp2.next_to(t1_2_title, RIGHT, buff=0.2)

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
        cmp3.next_to(t1_3_title, RIGHT, buff=0.2)

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
            self.play(Indicate(tt[a][0], color=RED),
                      Indicate(tt[b][0], color=RED))
            self.play(t1_1_value.animate.update_text(t[a]),
                      t2_1_value.animate.update_text(t[b]),
                      ReplacementTransform(tt[a].copy(), t1_1_value),
                      ReplacementTransform(tt[b].copy(), t2_1_value))

            if t[a] < t[b]:
                pd = 1
                self.play(cmp1.animate.update_text("<"))
                self.wait(0.8)
            elif t[a] > t[b]:
                pd = 0
                self.play(cmp1.animate.update_text(">"))
                self.wait(0.8)
            elif b % 3 == 1:
                self.play(cmp1.animate.update_text("="))
                self.wait(0.8)

                #self.play(t1_2_title.animate.update_text("R_{12}[a+1]"),
                #          t2_2_title.animate.update_text("R_{12}[b+1]"))
                self.play(t1_2_title.animate.update_text("R'_{12}[a+1]"),
                          t2_2_title.animate.update_text("R'_{12}[b+1]"))

                self.play(Indicate(rr12[(a + 1) // 3][0], color=RED),
                          Indicate(rr12[n1 + (b + 1) // 3][0], color=RED))


                self.play(t1_2_value.animate.update_text(r12[(a + 1) // 3]),
                          t2_2_value.animate.update_text(r12[n1 + (b + 1) // 3]),
                          ReplacementTransform(rr12[(a + 1) // 3].copy(), t1_2_value),
                          ReplacementTransform(rr12[n1 + (b + 1) // 3].copy(), t2_2_value))

                if (t[a], r12[(a + 1) // 3]) < (t[b], r12[n1 + (b + 1) // 3]):
                    pd = 1
                    self.play(cmp2.animate.update_text("<"))
                    self.wait(0.8)
                else:
                    pd = 0
                    self.play(cmp2.animate.update_text(">"))
                    self.wait(0.8)
            elif b % 3 == 2:
                self.play(cmp1.animate.update_text("="))
                self.wait(0.8)

                #self.play(t1_2_title.animate.update_text("T[a+1]"),
                #            t2_2_title.animate.update_text("T[b+1]"))
                self.play(t1_2_title.animate.update_text("T'[a+1]"),
                            t2_2_title.animate.update_text("T'[b+1]"))

                self.play(Indicate(tt[a + 1][0], color=RED),
                          Indicate(tt[b + 1][0], color=RED))

                self.play(t1_2_value.animate.update_text(t[a+1]),
                          t2_2_value.animate.update_text(t[b+1]),
                          ReplacementTransform(tt[a + 1].copy(), t1_2_value),
                          ReplacementTransform(tt[b + 1].copy(), t2_2_value))

                if t[a + 1] < t[b + 1]:
                    pd = 1
                    self.play(cmp2.animate.update_text("<"))
                    self.wait(0.8)
                elif t[a + 2] < t[b + 2]:
                    pd = 0
                    self.play(cmp2.animate.update_text(">"))
                    self.wait(0.8)
                else:
                    self.play(cmp2.animate.update_text("="))
                    self.wait(0.8)
                    #self.play(t1_3_title.animate.update_text("R[a+2]"),
                    #        t2_3_title.animate.update_text("R[b+2]"))
                    self.play(t1_3_title.animate.update_text("R'[a+2]"),
                            t2_3_title.animate.update_text("R'[b+2]"))

                    self.play(Indicate(rr12[(a + 2) // 3][0], color=RED),
                              Indicate(rr12[(b + 2) // 3][0], color=RED))

                    self.play(t1_3_value.animate.update_text(r12[(a + 2) // 3]),
                              t2_3_value.animate.update_text(r12[(b + 2) // 3]),
                              ReplacementTransform(rr12[(a + 2) // 3].copy(), t1_3_value),
                              ReplacementTransform(rr12[(b + 2) // 3].copy(), t2_3_value))

                    if r12[n1 + (a + 2) // 3] < r12[(b + 2) // 3]:
                        pd = 1
                        self.play(cmp3.animate.update_text("<"))
                        self.wait(0.8)
                    else:
                        pd = 0
                        self.play(cmp3.animate.update_text(">"))
                        self.wait(0.8)

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

            self.play(
                    t1_1_value.animate.update_text(),
                    t2_1_value.animate.update_text(),
                    t1_2_title.animate.update_text(),
                    t1_2_value.animate.update_text(),
                    t1_3_title.animate.update_text(),
                    t1_3_value.animate.update_text(),
                    t2_2_title.animate.update_text(),
                    t2_2_value.animate.update_text(),
                    t2_3_title.animate.update_text(),
                    t2_3_value.animate.update_text(),
                    cmp1.animate.update_text(),
                    cmp2.animate.update_text(),
                    cmp3.animate.update_text()
            )

class Fig15(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        t = "cbacbacacb"
        n = len(t)

        tt = Array([x for x in t], square_size=0.6)
        tt.shift(UP*3.5)
        id = MathTex("T", color=BLACK, font_size=20)
        sq = Square(0.5).next_to(tt, LEFT, buff=0)
        id.move_to(sq.get_center())
        self.add(id, tt)

        sa = [t[i:] for i in range(n)]
        ids = sorted(range(n), key=sa.__getitem__)
        sa.sort()
        
        hh = []
        for i in range(n-1):
            h = 0
            for j in range(min(len(sa[i]), len(sa[i+1]))):
                if sa[i][j] == sa[i+1][j]:
                    h += 1
                else:
                    break
            hh.append(h)
        hh.append(0)
        saa = VGroup()
        for x in sa:
            a = Array(x, square_size=0.5)
            saa.add(a)
        saa.arrange(DOWN, buff=0).shift(DOWN+RIGHT*0.5)

        rank = [0 for _ in range(n)]
        for i in range(n):
            rank[ids[i]] = i
        rr = Array(rank, square_size=0.6).shift(UP*2.5)
        id = MathTex("R", color=BLACK, font_size=20)
        sq = Square(0.5).next_to(rr, LEFT, buff=0)
        id.move_to(sq.get_center())
        self.add(id, rr)

        for a in saa:
            a.shift((n - len(a)) / 4 * LEFT)
        self.add(saa)
        
        hi = VGroup()
        for i in range(n):
            id = MathTex(str(ids[i]), color=BLACK, font_size=20)
            sq = Square(0.5).next_to(saa[i][0], LEFT, buff=0)
            id.move_to(sq.get_center())
            self.add(id)
            id1 = MathTex(str(hh[i]), color=BLACK, font_size=20)
            sq1 = Square(0.5).next_to(sq, LEFT, buff=0)
            id1.move_to(sq1.get_center())
            hi.add(id1)

        title1 = MathTex("H", color=BLACK, font_size=20).next_to(hi[0], UP, buff=0.3)
        title2 = MathTex("SA", color=BLACK, font_size=20).next_to(title1, RIGHT)
        #hi.shift(DOWN*0.2)
        self.add(title1, title2)

        hinfo = Info().shift(LEFT*3.5+UP*2.5)
        self.add(hinfo)


        h = 0
        rect = self.plot_rect(n, 0.6, tt[0].get_center(), RED)
        self.play(Create(rect))
        for i in range(n):
            ii = rank[i]
            rect1 = self.plot_rect(n-i, 0.5, saa[ii][0].get_center(), RED)
            self.play(ReplacementTransform(rect, rect1))
            
            anims1d = []
            anims1 = []
            if rank[i] == n - 1:
                h = 0
                self.play(hinfo.animate.update_text("h=0"))
                self.play(FadeIn(hi[ii]))
            else:
                k = ids[rank[i] + 1]
                for j in range(h):
                    anims1.append(saa[ii][j][0].animate.set_fill(RED_B, opacity=0.5))
                    anims1.append(saa[ii+1][j][0].animate.set_fill(RED_B, opacity=0.5))

                    anims1d.append(saa[ii][j][0])
                    anims1d.append(saa[ii+1][j][0])

                if len(anims1) > 0:
                    self.play(*anims1)
                if h < len(saa[ii]) and h < len(saa[ii+1]):
                    self.play(Indicate(saa[ii][h][1], color=RED),
                              Indicate(saa[ii+1][h][1], color=RED))
                while i + h < n and k + h < n and t[i + h] == t[k + h]:
                    self.play(saa[ii][h][0].animate.set_fill(RED_B, opacity=0.5),
                              saa[ii+1][h][0].animate.set_fill(RED_B, opacity=0.5),
                               hinfo.animate.update_text("h="+str(h+1)))

                    anims1d.append(saa[ii][h][0])
                    anims1d.append(saa[ii+1][h][0])
                    h += 1
                    if h < len(saa[ii]) and h < len(saa[ii+1]):
                        self.play(Indicate(saa[ii][h][1], color=RED),
                                  Indicate(saa[ii+1][h][1], color=RED))

                self.play(hinfo.animate.update_text("h="+str(h)))
                self.play(FadeIn(hi[ii]))
                if h > 0:
                    h -= 1

            animss = []
            for x in anims1d:
                animss.append(x.animate.set_fill(WHITE))
            orect = rect
            if i + 1 < n:
                rect = self.plot_rect(n-i-1, 0.6, tt[i + 1].get_center(), RED)
                animss.append(FadeOut(orect))
                animss.append(ReplacementTransform(rect1, rect))
                self.play(*animss)
                self.wait(0.8)
            else:
                animss.append(FadeOut(orect, rect1))
                self.play(*animss)

    def plot_rect(self, width, size, pos, color):
        rect = Rectangle(width=width*size, height=size, stroke_width=2)
        rect.move_to([pos[0] + (width - 1)*size / 2, pos[1], pos[2]])
        rect.set_stroke(color)
        return rect

class Fig16(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        t = "cbacbacacb"
        n = len(t)

        sa = [t[i:] for i in range(n)]
        ids = sorted(range(n), key=sa.__getitem__)
        sa.sort()
        
        hh = []
        for i in range(n-1):
            h = 0
            for j in range(min(len(sa[i]), len(sa[i+1]))):
                if sa[i][j] == sa[i+1][j]:
                    h += 1
                else:
                    break
            hh.append(h)
        hh.append(0)
        saa = VGroup()
        for x in sa:
            a = Array(x, square_size=0.5)
            saa.add(a)
        saa.arrange(DOWN, buff=0).shift(RIGHT*0.5)

        for a in saa:
            a.shift((n - len(a)) / 4 * LEFT)
        self.add(saa)
        
        hi = VGroup()
        for i in range(n - 1):
            id1 = MathTex(str(hh[i]), color=BLACK, font_size=20)
            sq1 = Square(0.5).next_to(saa[i][0], LEFT, buff=0)
            id1.move_to(sq1.get_center())
            hi.add(id1)
        hi.shift(DOWN*0.3)
        self.add(hi)

        self.wait()
        self.play(saa[:3].animate.shift(UP*0.6),
                  saa[6:].animate.shift(DOWN*0.6),
                  FadeOut(hi[2], hi[5]),
                  hi[:2].animate.shift(UP*0.6),
                  hi[6:].animate.shift(DOWN*0.6))

        self.wait()

class Fig17(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        self.t = "cbacbacacb$"
        suffix_array = SuffixArray(self.t)
        self.sa = suffix_array.sa
        self.height = suffix_array.height
        cartesian_tree = CartesianTree(self.height)
        rt = cartesian_tree.root

        self.hh = Array(self.height, square_size=0.8).shift(DOWN*3.2)
        self.add(self.hh)

        self.nodes = VGroup()
        self.edges = VGroup()
        root = SuffixTreeNode(str(rt.index)).move_to(self.hh[rt.index]).shift(UP*6)
        self.add_nodes1(rt, root)
        self.adjust_nodes(root)
        self.add_edges(root)
    
        self.add(self.nodes, self.edges)

        self.roots = [root]
        self.fusion(root)
        anims = []
        for u in self.roots:
            anims.append(u.animate.move_to([0, 3, 0]))
        for u in self.nodes:
            if u not in self.roots:
                anims.append(u.animate.shift(RIGHT*0.5+DOWN*0.3))
        self.play(*anims)

        self.cnt = 0
        self.play(Indicate(self.roots[-1].node, color=RED))
        self.play(self.roots[-1].animate.set_text(""))

        self.add_nodes2(rt, root)
        
    def add_nodes1(self, u, node):
        self.nodes.add(node)
        for v in (u.lchild, u.rchild):
            if v is not None:
                l = self.sa[v.index]
                r = l + self.height[v.index]
                c = self.t[l + node.r - node.l]
                print(v.index, c, l, r)
                node.children[c] = SuffixTreeNode(str(v.index), l, r)
                self.add_nodes1(v, node.children[c])

    def adjust_nodes(self, u):
        for c in u.children:
            if u.children[c] is not None:
                v = u.children[c]
                v.move_to([self.hh[v.idx].get_center()[0], u.get_center()[1] - 0.8, 0])
                self.adjust_nodes(v)

    def add_edges(self, father):
        for c in father.children:
            child = father.children[c]
            e = father.add_edge(child)
            self.edges.add(e)
            self.add_edges(child)

    def fusion(self, u):
        for c in u.children.copy():
            v = u.children[c]
            if self.height[u.idx] == self.height[v.idx]: # fusion
                anims = []
                self.play(Indicate(self.hh[u.idx], color=RED), 
                          Indicate(self.hh[v.idx], color=RED),
                          Indicate(u.node, color=RED),
                          Indicate(v.node, color=RED))
                self.play(v.animate.move_to([v.get_center()[0], u.get_center()[1], 0]))
                self.roots.append(v)

                def place(u):
                    for c in u.children:
                        v = u.children[c]
                        pos = u.get_center()[1]-0.8
                        anims.append(v)
                        place(v)
                place(v)
                self.play(VGroup(*anims).animate.shift(UP * 0.8))

                self.fusion(v)
            else:
                self.fusion(v)
        
    def add_nodes2(self, u, node, d=0):
        if node not in self.roots:
            self.play(Indicate(node.node, color=RED))
            if u.index == 9:
                text = "ac"
            else:
                text = self.t[node.l+d:node.r]
            self.play(node.animate.set_text(text))
        for v in (u.lchild, u.rchild):
            if v is None:
                if self.cnt == len(self.sa):
                    break
                l = self.sa[self.cnt]
                r = len(self.t)
                c = self.t[l + node.r - node.l]
                vnode = SuffixTreeNode("", l, r, scale=0.7)
                e = node.add_edge(vnode)
                vnode.move_to([self.hh[self.cnt].get_center()[0], node.node.get_center()[1] - 1.2, 0])
                self.play(FadeIn(vnode, e))
                text = self.t[l+node.r-node.l:]
                self.play(vnode.animate.set_text(text))
                node.children[c] = vnode
                self.cnt += 1
            else:
                l = self.sa[v.index]
                r = l + self.height[v.index]
                c = self.t[l + node.r - node.l]
                self.add_nodes2(v, node.children[c], d+node.r-node.l)

