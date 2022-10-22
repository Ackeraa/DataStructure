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
        # Fig 3
        # self.fig3()
        # Fig 4
        self.fig4()

        self.root = TrieNode(size=self.node_size)
        self.nodes = VGroup(self.root)
        self.edges = VGroup()
        self.build()
        self.compress(self.root)
        self.place(self.root)
        
        tree = VGroup(self.root, self.nodes, self.edges)

        # Fig 4
        tree.shift(LEFT)

        self.add(tree)

    def fig3(self):
        self.node_size = 0.45
        self.scale = 0.4
        self.gap = 2
        self.texts = ["ant$", "ante$", "anteater$", "antelope$", "antique$"]

    def fig4(self):
        self.node_size = 0.27
        self.scale = 0.24
        self.gap = 2
        text = "nonsense$"
        # text = "abcabcacab$"
        self.texts = [ text[i:] for i in range(len(text))]
        vg = VGroup()
        for txt in self.texts:
            t = Text(txt, color=BLACK, font="DroidSansMono Nerd Font", font_size=22)
            txt = (len(text) - len(txt)) * "*"
            t0 = Text(txt, color=WHITE, font="DroidSansMono Nerd Font", font_size=22)
            vg.add(VGroup(t, t0).arrange(RIGHT, buff=0))
        vg.arrange(DOWN, buff=0.5).shift(RIGHT * 6)
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
            u.set_text(text, scale=self.scale)
            u.children = uu.children

        self.nodes.add(u)

        for c in u.children:
            v = u.children[c]
            self.compress(v)

    def build(self):
        w = 12
        self.root.w = w
        self.root.l = -w // 2 
        self.root.shift(UP*3)
        for text in self.texts:
            u = self.root
            for c in text:
                if c not in u.children:
                    v = TrieNode(c, len(u.children), size=self.node_size)
                    u.children[c] = v 
                u = u.children[c]
            u.text = text

    def place(self, father):
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
            self.place(child)


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
            if i % 3 == 0:
                anims0_0.append(self.mt[i][0].animate.set_fill(YELLOW, opacity = 0.5))
            elif i % 3 == 1:
                anims0_1.append(self.mt[i][0].animate.set_fill(GREEN, opacity = 0.5))
            else:
                anims0_2.append(self.mt[i][0].animate.set_fill(BLUE, opacity = 0.5))

        self.play(*anims0_0, run_time=1)
        self.play(*anims0_1, run_time=1)
        self.play(*anims0_2, run_time=1)
        '''

        #''' set color 1
        for i in range(n):
            if i < 3 * n0 and i % 3 == 0:
                self.mt[i][0].set_fill(YELLOW, opacity = 0.8)
            elif i < 3 * n1 and i % 3 == 1:
                self.mt[i][0].set_fill(GREEN, opacity = 0.8)
            elif i < 3 * n2:
                self.mt[i][0].set_fill(BLUE, opacity = 0.8)
        #'''

        self.msa1 = Array(t[1:1+n1*3]).move_to(self.mt[:-1]).shift(DOWN)
        self.msa2 = Array(t[2:2+n2*3]).move_to(self.msa1[:-1]).shift(DOWN)
        self.msa12 = Array(t[1:1+n1*3] + t[2:2+n2*3]).next_to(self.mt, DOWN * 2)
        for i in range(n1):
            self.msa12[i * 3][0].set_fill(GREEN, opacity = 0.8)
            self.msa1[i * 3][0].set_fill(GREEN, opacity = 0.8)
        for i in range(n2):
            self.msa12[n1 * 3 + i * 3][0].set_fill(BLUE, opacity = 0.8)
            self.msa2[i * 3][0].set_fill(BLUE, opacity = 0.8)

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

<<<<<<< HEAD


        self.wait()

class Test(Scene):
    def construct(self):
        t = Text("a")
        t.set(text="b")
        self.add(t)

=======
>>>>>>> 5327dc6c2a0f64d20d5255b0d09208343278c51a
