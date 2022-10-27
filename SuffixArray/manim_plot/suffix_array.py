from manim import *
from utils import *
sys.path.insert(0, '../../RMQ')
sys.path.insert(0, '../')
from cartesian_stack import CartesianTree
from suffix_array import SuffixArray

class SuffixArray(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        self.t = list("cbacbacacb")
        t = [ord(x) - ord('a') + 1 for x in self.t]
        self.start()
        self.sa = self.build(t, 256)
        #self.split(t)
        #self.sort()
        self.wait()

    def playa(self, anims):
        for anim in anims:
            self.play(anim)

    def start(self):
        self.tt = Array(self.t)
        self.add(self.tt)
        self.play(self.tt.animate.shift(UP * 3+LEFT*0.6*1.5))

        title1 = Text("所有后缀", color=BLUE_E, font="DroidSansMono Nerd Font", font_size=24)
        title1.shift(UP * 2.1 + LEFT * 4)
    
        t1 = VGroup()
        for i in range(len(self.t)):
            a = Array([t for t in self.t[i:]], square_size=0.5)
            t1.add(a)
        t1.arrange(DOWN, buff=0).shift(LEFT * 3.5 + DOWN)
        for a in t1:
            a.shift((len(self.t) - len(a)) / 4 * LEFT)

        idd1 = VGroup()
        for i in range(len(self.t)):
            id = MathTex(str(i), color=BLACK, font_size=24)
            sq = Square(0.6).next_to(t1[i][0], LEFT, buff=0)
            id.move_to(sq.get_center())
            idd1.add(id)

        title2 = Text("后缀数组", color=BLUE_E, font="DroidSansMono Nerd Font", font_size=24)
        title2.shift(UP * 2.1 + RIGHT * 4)

        texts = [self.t[i:] for i in range(len(self.t))]
        ids = sorted(range(len(texts)), key=texts.__getitem__)
        texts.sort()
        t2 = VGroup()
        for t in texts:
            a = Array(t, square_size=0.5)
            t2.add(a)
        t2.arrange(DOWN, buff=0).shift(RIGHT * 4 + DOWN)
        for a in t2:
            a.shift((len(self.t) - len(a)) / 4 * LEFT)

        idd2 = VGroup()
        for i in range(len(self.t)):
            id = MathTex(str(ids[i]), color=BLACK, font_size=24)
            sq = Square(0.6).next_to(t2[i][0], LEFT, buff=0)
            id.move_to(sq.get_center())
            idd2.add(id)
        
        self.play(FadeIn(title1, t1, idd1))
        self.play(FadeIn(title2, t2, idd2))
        self.wait()
        self.play(FadeOut(t1, title1, t2, title2, idd1, idd2))
        
        n = len(self.t)
        t = [ord(x) - ord('a') + 1 for x in self.t]
        tt = Array(t).move_to(self.tt)
        self.play(ReplacementTransform(self.tt, tt))

    def create_basic(self, t):
        t += [0, 0, 0]
        n = len(t)
        n0 = (n - 1) // 3
        n1 = (n - 1) // 3
        n2 = (n - 2) // 3
        n12 = n1 + n2
        t0 = [i * 3 for i in range(n0)]
        t1 = [i * 3 + 1 for i in range(n1)]
        t2 = [i * 3 + 2 for i in range(n2)]
        t12 = t1 + t2

        self.idd = Array([i for i in range(n)], square_size=square_size)
        for i in range(len(t)):
            if i < 3 * n0 and i % 3 == 0:
                self.idd[i][0].set_fill(PURPLE, opacity=1)
            elif i < 3 * n1 and i % 3 == 1:
                self.idd[i][0].set_fill(TEAL, opacity=1)
            elif i < 3 * n2:
                self.idd[i][0].set_fill(BLUE, opacity=1)

        self.tt = Array(t, square_size=square_size, color=BLACK)

        self.tt12 = Array(t12, square_size=square_size)
        for i in range(n1):
            self.tt12[i][0].set_fill(TEAL, opacity=1)
        for i in range(n2):
            self.tt12[n1 + i][0].set_fill(BLUE, opacity=1)

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

    def build(self, t, N, dep=0):
        square_size=0.6
        t += [0, 0, 0]
        n = len(t)
        n0 = (n - 1) // 3
        n1 = (n - 1) // 3
        n2 = (n - 2) // 3
        n12 = n1 + n2
        sa12 = [i * 3 + 1 for i in range(n1)] + \
               [i * 3 + 2 for i in range(n2)]
        r12 = [0 for _ in range(len(sa12))] + [0]

        t0 = [i * 3 for i in range(n0)]
        t1 = [i * 3 + 1 for i in range(n1)]
        t2 = [i * 3 + 2 for i in range(n2)]
        t12 = t1 + t2

        idd = Array([i for i in range(n)], square_size=square_size)
        for i in range(n):
            if i < 3 * n0 and i % 3 == 0:
                idd[i][0].set_fill(PURPLE, opacity=1)
            elif i < 3 * n1 and i % 3 == 1:
                idd[i][0].set_fill(TEAL, opacity=1)
            elif i < 3 * n2:
                idd[i][0].set_fill(BLUE, opacity=1)

        tt = Array(t, square_size=square_size, color=BLACK)
        tt.shift(UP*3)

        tt12 = Array(t12, square_size=square_size)
        for i in range(n1):
            tt12[i][0].set_fill(TEAL, opacity=1)
        for i in range(n2):
            tt12[n1 + i][0].set_fill(BLUE, opacity=1)

        self.play(FadeIn(tt[:-3]))
        self.play(FadeIn(tt[-3:]))
        if dep == 0:
            self.remove(self.tt)

        idd.next_to(tt, UP, buff=0)
        id_title = Title("id").next_to(idd, LEFT, buff=0.2)

        t_title = Title("T").next_to(tt, LEFT, buff=0.2)

        t12_title = Title("T_{12}").next_to(t_title, DOWN, buff=0.5)
        tt12.next_to(t12_title, RIGHT, buff=0.2)

        self.play(FadeIn(idd, id_title, t_title, t12_title))
        for i in range(n12):
            self.play(ReplacementTransform(idd[t12[i]].copy(), tt12[i]))

        # sort plot
        t_ = VGroup()
        for i in t12:
            t_.add(tt[i:i+3].copy())

        for i in range(n12):
            if i == 0:
                self.play(t_[i].animate.shift(DOWN * 5.8 + LEFT * l_offset).scale(0.8))
            else:
                self.play(t_[i].animate.next_to(t[i - 1], buff=0.2).scale(0.8))

        nums = VGroup()
        for x in t_:
            num = VGroup()
            for y in x:
                num.add(y[1].copy().scale(1.5))
            num.arrange(RIGHT, buff=0.1)
            nums.add(num)
        nums.arrange(RIGHT, buff=0.4).shift(DOWN * 2)

        anims = []
        for i in range(len(t)):
            anims.append(ReplacementTransform(t_[i].copy(), nums[i])) 

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

        a = [0 for _ in range(len(nums))]
        for i in range(len(nums)):
            a[i] = t12[ords[i]]
        sa12_ttile = Title("SA_{12}").next_to(t12_title, DOWN, buff=0.5)
        saa12 = Array(a)
        sa12.next_to(sa12_title, RIGHT, buff=0.2)
        sa12_vg = VGroup(sa12_title, saa12)

        a = [0 for _ in range(len(nums))]
        for i in range(len(nums)):
            a[ords[i]] = rk[i]
        r12_ttile = Title("R_{12}").next_to(sa12_title, DOWN, buff=0.5)
        rr12 = Array(a)
        rr12.next_to(r12_title, RIGHT, buff=0.2)
        r12_vg = VGroup(r12_title, rr12)

        self.play(ReplacementTransform(rkt1.copy(), r12_vg))

        for i in range(len(nums)):
            if a[i] % 3 == 1:
                saa12[i][0].set_fill(color=TEAL, opacity=1)
            else:
                saa12[i][0].set_fill(color=BLUE, opacity=1)

        self.play(FadeIn(sa12_vg))

        self.wait()

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

        return
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

class BuildSuffixArray(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        self.t = list("cbacbacacb")
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

        #''' add zeros
        self.play(FadeIn(self.mt[-3:]))
        #'''

        ''' add zeros 1
        self.add(self.mt[-3:])
        '''

        #''' set color
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
        #'''

        ''' set color 1
        for i in range(n):
            if i < 3 * n0 and i % 3 == 0:
                self.mt[i][0].set_fill(PURPLE, opacity=1)
            elif i < 3 * n1 and i % 3 == 1:
                self.mt[i][0].set_fill(TEAL, opacity=1)
            elif i < 3 * n2:
                self.mt[i][0].set_fill(BLUE, opacity=1)
        '''

        self.msa1 = Array(t[1:1+n1*3]).move_to(self.mt[:-1]).shift(DOWN)
        self.msa2 = Array(t[2:2+n2*3]).move_to(self.msa1[:-1]).shift(DOWN)
        self.msa12 = Array(t[1:1+n1*3] + t[2:2+n2*3]).next_to(self.mt, DOWN * 2)
        for i in range(n1):
            self.msa12[i * 3][0].set_fill(TEAL, opacity=1)
            self.msa1[i * 3][0].set_fill(TEAL, opacity=1)
        for i in range(n2):
            self.msa12[n1 * 3 + i * 3][0].set_fill(BLUE, opacity=1)
            self.msa2[i * 3][0].set_fill(BLUE, opacity=1)

        #''' split 
        anims1_1, anims1_2 = [], []
        anims1_1.append(ReplacementTransform(self.mt[1:].copy(), self.msa1))
        anims1_1.append(ReplacementTransform(self.mt[2:].copy(), self.msa2))

        anims1_2.append(ReplacementTransform(self.msa1, self.msa12[:n1 * 3]))
        anims1_2.append(ReplacementTransform(self.msa2, self.msa12[n1 * 3:]))
        self.playa(anims1_1)
        self.play(*anims1_2)
        #'''

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

        self.play(Create(buckets))
        #self.add(buckets)

        nums = VGroup()
        anims = []
        for i in range(len(self.msa12) // 3):
            num = VGroup()
            for x in self.msa12[i * 3: i * 3 + 3]:
                num.add(x[1].copy())
            nums.add(num.arrange(RIGHT, buff=0.1))
            anims.append(ReplacementTransform(self.msa12[i * 3: i * 3 + 3].copy(), num))
        nums.arrange(RIGHT, buff=0.4).shift(DOWN * 2.5)
        
        #''' divide by 3
        self.playa(anims)
        #'''

        ''' divide by 3 1
        self.add(nums)
        '''

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
