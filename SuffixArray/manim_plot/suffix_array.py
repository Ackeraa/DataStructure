from manim import *
from utils import *
sys.path.insert(0, '../../RMQ')
sys.path.insert(0, '../')
from cartesian_stack import CartesianTree
from suffix_array import SuffixArray

class SuffixArray(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        self.add_sound("bgm.mp3")
        self.t = list("cbacbacacb")
        t = [ord(x) - ord('a') + 1 for x in self.t]
        self.start()
        self.sa = self.build(t, 256)
        self.end()

    def start(self):
        self.tt = Array(self.t)
        self.tt.shift(UP*2.5+LEFT*2.4)
        self.play(FadeIn(self.tt), run_time=2)

        title1 = Text("所有后缀", color=BLUE_E, font_size=18)
        title1.shift(UP * 1.8 + LEFT * 4)
    
        t1 = VGroup()
        for i in range(len(self.t)):
            a = Array([t for t in self.t[i:]], square_size=0.5)
            t1.add(a)
        t1.arrange(DOWN, buff=0).shift(LEFT * 3.5 + DOWN)
        for a in t1:
            a.shift((len(self.t) - len(a)) / 4 * LEFT)

        idd1 = VGroup()
        for i in range(len(self.t)):
            id = MathTex(str(i), color=BLACK, font_size=20)
            sq = Square(0.6).next_to(t1[i][0], LEFT, buff=0)
            id.move_to(sq.get_center())
            idd1.add(id)

        title2 = Text("后缀数组(SA)", color=BLUE_E, font_size=18)
        title2.shift(UP * 1.8 + RIGHT * 3.5)

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
        self.play(ReplacementTransform(title1.copy(), title2),
                  ReplacementTransform(t1.copy(), t2),
                  ReplacementTransform(idd1.copy(), idd2))
        self.wait()
        self.play(FadeOut(t1, title1, t2, title2, idd1, idd2))
        
        n = len(self.t)
        t = [ord(x) - ord('a') + 1 for x in self.t]
        tt = Array(t).move_to(self.tt)
        self.play(ReplacementTransform(self.tt, tt))
        self.tt = tt

    def end(self):
        t = Text("The End.", color=BLACK, font_size=24)
        self.play(Create(t))
        self.wait(1.5)

    def plot_rect(self, width, size, pos, color):
        rect = Rectangle(width=width*size, height=size, stroke_width=2)
        rect.move_to([pos[0] + (width - 1)*size / 2, pos[1], pos[2]])
        rect.set_stroke(color)
        return rect

    def build(self, t, N, dep=0):
        if dep == 0:
            titles_map = {
                "t": "T", "t12": "T_{12}", "t0": "T_0", 
                "r0": "R_0", "r12": "R_{12}", "sa0": "SA_0",
                "sa12": "SA_{12}", "sa": "SA",
            }
        else:
            titles_map = {
                "t": "T'", "t12": "T'_{12}", "t0": "T'_0", 
                "r0": "R'_0", "r12": "R'_{12}", "sa0": "SA'_0",
                "sa12": "SA'_{12}", "sa": "SA'"
            }
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

        tt = Array(t, square_size=square_size)
        tt.lmove_to(self.tt)

        tt12 = Array(t12, square_size=square_size)
        for i in range(n1):
            tt12[i][0].set_fill(TEAL, opacity=1)
        for i in range(n2):
            tt12[n1 + i][0].set_fill(BLUE, opacity=1)

        self.play(FadeOut(self.tt), FadeIn(tt[:-3]))
        self.play(FadeIn(tt[-3:]))

        idd.next_to(tt, UP, buff=0)
        id_title = Title("id").next_to(idd, LEFT, buff=0.2)

        t_title = Title(titles_map["t"]).next_to(tt, LEFT, buff=0.2)

        t12_title = Title(titles_map["t12"]).next_to(t_title, DOWN, buff=0.5)
        tt12.next_to(t12_title, RIGHT, buff=0.2)

        if dep == 1:
            l_offset = 0.0
            n_buckets = 7
            run_time = 0.8
        else:
            l_offset = 1.5
            n_buckets = 7
            run_time = 1

        self.wait(0.3)
        self.play(FadeIn(idd, id_title, t_title), run_time=run_time)
        self.play(FadeIn(t12_title))
        self.wait(0.3)
        for i in range(n12):
            self.play(ReplacementTransform(idd[t12[i]].copy(), tt12[i]), run_time=run_time)

        # sort plot
        t_ = VGroup()
        for i in t12:
            t_.add(tt[i:i+3].copy())

        for i in range(n12):
            if i == 0:
                self.play(t_[i].animate.shift(DOWN * 5.8 + LEFT * l_offset).scale(0.8), run_time=run_time)
            else:
                self.play(t_[i].animate.next_to(t_[i - 1], buff=0.2).scale(0.8), run_time=run_time)

        nums = VGroup()
        for x in t_:
            num = VGroup()
            for y in x:
                num.add(y[1].copy().scale(1.5))
            num.arrange(RIGHT, buff=0.1)
            nums.add(num)
        nums.arrange(RIGHT, buff=0.4).shift(DOWN * 2)

        anims = []
        for i in range(len(t_)):
            anims.append(ReplacementTransform(t_[i].copy(), nums[i])) 

        buckets = VGroup()
        m = n_buckets // 2
        for i in range(n_buckets):
            buckets.add(Line([i - m, -1, 0], [i - m, 1, 0], color=BLACK, stroke_width=2))
            if i < n_buckets - 1:
                l = Line([i - m, -1, 0], [i - m + 1, -1, 0], color=BLACK, stroke_width=2)
                x = Text(str(i), font_size=16, color=BLACK).next_to(l, DOWN, buff=0.1)
                buckets.add(l, x)

        buckets.shift(DOWN * 0.3)
        anims.append(FadeIn(buckets))
        self.play(*anims, run_time=run_time)

        nums0 = nums.copy()
        ords = list(range(len(nums0)))
        for j in range(2, -1, -1):
            anims = []
            for num in nums:
                anims.append(num[j].animate.set(color=RED))
            self.play(*anims, run_time=run_time)

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
                    self.play(nums[queue[i]].animate.next_to(pre, UP, buff=0.2), run_time=run_time)

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
                self.play(nums[i].animate.move_to(nums0[i]), run_time=run_time)
            anims = []
            for num in nums:
                anims.append(num[j].animate.set(color=BLACK))
            self.play(*anims, run_time=run_time)
        
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
            self.play(FadeIn(rkt[i], run_time=0.7), run_time=run_time)

        rkt1 = rkt.copy()
        for i in range(len(nums)):
            rkt1[i].next_to(t_[ords[i]], UP, buff=0.2)

        for i in range(len(nums)):
            self.play(ReplacementTransform(VGroup(nums[i], rkt[i]), rkt1[i]), run_time=run_time)

        self.play(FadeOut(buckets), run_time=run_time)

        a = [0 for _ in range(len(nums))]
        for i in range(len(nums)):
            a[i] = t12[ords[i]]
        sa12_title = Title(titles_map["sa12"]).next_to(t12_title, DOWN, buff=0.5)
        saa12 = Array(a)
        saa12.next_to(sa12_title, RIGHT, buff=0.2)
        sa12_vg = VGroup(sa12_title, saa12)

        a1 = [0 for _ in range(len(nums))]
        for i in range(len(nums)):
            a1[ords[i]] = rk[i]
        r12_title = Title(titles_map["r12"]).next_to(sa12_title, DOWN, buff=0.5)
        rr12 = Array(a1)
        rr12.next_to(r12_title, RIGHT, buff=0.2)
        r12_vg = VGroup(r12_title, rr12)

        self.play(ReplacementTransform(rkt1.copy(), r12_vg), run_time=run_time)

        for i in range(len(nums)):
            if a[i] % 3 == 1:
                saa12[i][0].set_fill(color=TEAL, opacity=1)
            else:
                saa12[i][0].set_fill(color=BLUE, opacity=1)

        self.wait(0.4)
        self.play(FadeIn(sa12_vg))

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
            self.play(FadeOut(tt, idd, tt12, saa12, t_, rkt1,
                              id_title, t_title, t12_title, sa12_title, r12_title))
            self.play(rr12.animate.lmove_to(tt))
            self.tt = rr12
            sa12 = self.build(r12[:-1], n12, dep+1)

            rr12.next_to(r12_title, RIGHT, buff=0.2)
            self.play(FadeIn(id_title, idd, t_title, tt, t12_title, tt12,
                             sa12_title, saa12, r12_title, rr12))                                  
                             
            # recover to the right order
            for i in range(n12):
                r12[sa12[i]] = i + 1
                if sa12[i] < n1:
                    sa12[i] = sa12[i] * 3 + 1
                else:
                    sa12[i] = (sa12[i] - n1) * 3 + 2
            self.wait(0.4)

            rr12_copy = Array(r12[:-1]).move_to(rr12)
            saa12_copy = Array(sa12).move_to(saa12)
            for i in range(len(sa12)):
                if sa12[i] % 3 == 1:
                    saa12_copy[i][0].set_fill(color=TEAL, opacity=1)
                else:
                    saa12_copy[i][0].set_fill(color=BLUE, opacity=1)

            rect1 = self.plot_rect(n12, square_size, saa12[0].get_center(), RED)
            rect2 = self.plot_rect(n12, square_size, rr12[0].get_center(), RED)
            self.play(Create(rect1), Create(rect2))
            
            self.play(ReplacementTransform(rr12, rr12_copy),
                      ReplacementTransform(saa12, saa12_copy))
            self.play(FadeOut(rect1, rect2))
            self.remove(rr12_copy, saa12_copy)
        
        # sa0 animation
        if dep == 0:
            run_time = 0.6
        else:
            run_time = 1
            self.play(FadeOut(t_, rkt1), run_time=run_time)

        tt0 = Array(t0, square_size=square_size)
        for i in range(n0):
            tt0[i][0].set_fill(PURPLE, opacity=1)
        t0_title = Title(titles_map["t0"]).next_to(t_title, DOWN, buff=0.5)
        tt0.next_to(t0_title, RIGHT, buff=0.2)
        
        vg = VGroup(tt12, t12_title, saa12, sa12_title, rr12, r12_title)
        self.play(vg.animate.shift(DOWN*(square_size+0.5)), 
                  FadeIn(tt0, t0_title), run_time=run_time)

        vg = VGroup()
        vgg = VGroup()

        vg0 = VGroup()
        for i in t0:
            vg0.add(tt[i].copy())
        
        vg1 = VGroup()
        for i in range(n0):
            vg1.add(rr12[i].copy())

        for i in range(n0):
            self.play(Indicate(tt[i * 3][0], color=BLACK),
                      Indicate(tt0[i][0], color=PURPLE),
                      Indicate(idd[i * 3][0], color=PURPLE), run_time=run_time)

            if i == 0:
                self.play(vg0[i].animate.shift(RIGHT * 6.4 + DOWN * 2.5), run_time=run_time)
            else:
                self.play(vg0[i].animate.next_to(vg0[i - 1], DOWN, buff=0.3), run_time=run_time)

            self.play(Indicate(tt12[i][0], color=TEAL),
                      Indicate(rr12[i][0], color=BLACK), run_time=run_time)

            self.play(vg1[i].animate.next_to(vg0[i], RIGHT, buff=0), run_time=run_time)

            vg.add(VGroup(vg0[i].copy(), vg1[i].copy()))
            vgg.add(VGroup(vg0[i], vg1[i]))

        # sort
        ords = VGroup(*[MathTex(str(i), font_size=24, color=BLACK) for i in t0])
        for i in range(n0):
            ords[i].next_to(vgg[i], LEFT, buff=0.3)
        self.play(FadeIn(ords), run_time=run_time)
        self.wait(0.5)

        sa0 = [i for i in t0]
        for i in range(n0):
            for j in range(i + 1, n0):
                if vg[i][0][1].text + vg[i][1][1].text > vg[j][0][1].text + vg[j][1][1].text:
                    vg[i], vg[j] = vg[j], vg[i]
                    sa0[i], sa0[j] = sa0[j], sa0[i]

        ords1 = VGroup(*[MathTex(str(i), font_size=24, color=BLACK) for i in sa0])
        for i in range(n0):
            ords1[i].next_to(vgg[i], LEFT, buff=0.3)

        for i in range(n0):
            vg[i].move_to(vgg[i])
        self.play(ReplacementTransform(vgg, vg), ReplacementTransform(ords, ords1), run_time=run_time)
        self.wait(0.3)

        #title0 = MathTex("SA'_0", font_size=24, color=BLACK)
        saa0 = Array(sa0)
        for x in saa0:
            x[0].set_fill(PURPLE, opacity=1)

        saa0.next_to(tt0, RIGHT, buff=3.22)
        sa0_title = Title(titles_map["sa0"]) 
        sa0_title.next_to(saa0, LEFT, buff=0.2)

        self.play(ReplacementTransform(ords.copy(), VGroup(saa0, sa0_title)), run_time=run_time)

        # sort sa0
        sa0 = [i - 1 for i in sa12 if i % 3 == 1] # first round 
        self.radix_sort(t, sa0, N) # second round 

        # merge animation
        # set up
        t12_title_pos = t12_title.get_center()
        tt12_pos = tt12.get_center()

        self.play(FadeOut(t0_title, tt0),
                  sa0_title.animate.move_to(t0_title),
                  saa0.animate.move_to(tt0),
                  sa12_title.animate.move_to(t12_title_pos),
                  saa12.animate.move_to(tt12_pos),
                  r12_title.animate.next_to(tt12_pos, RIGHT, buff=2.2),
                  rr12.animate.next_to(tt12_pos, RIGHT, buff=2.3+square_size),
                  t12_title.animate.next_to(tt12_pos, RIGHT, buff=2.2).shift(UP*square_size),
                  tt12.animate.next_to(tt12_pos, RIGHT, buff=2.3+square_size).shift(UP*square_size),
                  FadeOut(ords, ords1, vgg, vg), 
                  run_time=run_time)

        sa_title = Title(titles_map["sa"]).next_to(sa12_title, DOWN, buff=0.5)
        seq = [t[i:] for i in range(n0 + n12)]
        sa = sorted(range(len(seq)), key=seq.__getitem__)
        saa = Array(sa, square_size=square_size).next_to(sa_title, RIGHT, buff=0.2)
        for i in range(len(sa)):
            if sa[i] % 3 == 0:
                saa[i][0].set_fill(PURPLE, opacity=1)
            elif sa[i] % 3 == 1:
                saa[i][0].set_fill(TEAL, opacity=1)
            else:
                saa[i][0].set_fill(BLUE, opacity=1)

        ar = Triangle(color=RED_E).set_fill(RED, opacity=1).rotate(-180*DEGREES).scale(.03)
        ari = VGroup(MathTex("i", font_size=20, color=BLACK), ar.copy()).arrange(DOWN, buff=0.1)
        arj = VGroup(MathTex("j", font_size=20, color=BLACK), ar.copy()).arrange(DOWN, buff=0.1)

        ari.next_to(saa0[0], UP, buff=0.1)
        arj.next_to(saa12[0], UP, buff=0.1)

        # 1
        t1_1_title = Info(titles_map["t"]+"[a]", color=BLACK)
        t1_1_title.move_to(RIGHT * 4.5 + UP * 2.5)
        t1_1_value = Info()
        t1_1_value.next_to(t1_1_title, DOWN, buff=0)
        
        cmp1 = Info()
        cmp1.next_to(t1_1_title, RIGHT, buff=0.2)

        t2_1_title = Info(titles_map["t"]+"[b]", color=BLACK)
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

        self.play(FadeIn(sa_title, ari, arj, 
                        t1_1_title, t1_1_value, t2_1_title, t2_1_value, cmp1,
                        t1_2_title, t1_2_value, t2_2_title, t2_2_value, cmp2,
                        t1_3_title, t1_3_value, t2_3_title, t2_3_value, cmp3), run_time=run_time)
        self.wait(0.5)

        i = j = 0
        ssa = []
        r12 += [0, 0, 0]
        while i < n0 and j < n12:
            a = sa0[i]
            b = sa12[j]
            self.play(Indicate(tt[a][0], color=RED),
                      Indicate(tt[b][0], color=RED), run_time=run_time)
            self.play(t1_1_value.animate.update_text(t[a]),
                      t2_1_value.animate.update_text(t[b]),
                      ReplacementTransform(tt[a].copy(), t1_1_value),
                      ReplacementTransform(tt[b].copy(), t2_1_value), run_time=run_time)

            if t[a] < t[b]:
                pd = 1
                self.play(cmp1.animate.update_text("<"), run_time=run_time)
                self.wait(0.8)
            elif t[a] > t[b]:
                pd = 0
                self.play(cmp1.animate.update_text(">"), run_time=run_time)
                self.wait(0.8)
            elif b % 3 == 1:
                self.play(cmp1.animate.update_text("="), run_time=run_time)
                self.wait(0.8)

                self.play(t1_2_title.animate.update_text(titles_map["r12"]+"[a+1]"),
                          t2_2_title.animate.update_text(titles_map["r12"]+"[b+1]"), run_time=run_time)

                if (a + 1) // 3 < len(rr12) and n1 + (b + 1) // 3 < len(rr12):
                    self.play(Indicate(rr12[(a + 1) // 3][0], color=RED),
                              Indicate(rr12[n1 + (b + 1) // 3][0], color=RED), run_time=run_time)


                    self.play(t1_2_value.animate.update_text(r12[(a + 1) // 3]),
                              t2_2_value.animate.update_text(r12[n1 + (b + 1) // 3]),
                              ReplacementTransform(rr12[(a + 1) // 3].copy(), t1_2_value),
                              ReplacementTransform(rr12[n1 + (b + 1) // 3].copy(), t2_2_value), run_time=run_time)

                if (t[a], r12[(a + 1) // 3]) < (t[b], r12[n1 + (b + 1) // 3]):
                    pd = 1
                    self.play(cmp2.animate.update_text("<"), run_time=run_time)
                    self.wait(0.8)
                else:
                    pd = 0
                    self.play(cmp2.animate.update_text(">"), run_time=run_time)
                    self.wait(0.8)
            elif b % 3 == 2:
                self.play(cmp1.animate.update_text("="), run_time=run_time)
                self.wait(0.8)

                self.play(t1_2_title.animate.update_text(titles_map["t"]+"[a+1]"),
                            t2_2_title.animate.update_text(titles_map["t"]+"[b+1]"), run_time=run_time)

                self.play(Indicate(tt[a + 1][0], color=RED),
                          Indicate(tt[b + 1][0], color=RED), run_time=run_time)

                self.play(t1_2_value.animate.update_text(t[a+1]),
                          t2_2_value.animate.update_text(t[b+1]),
                          ReplacementTransform(tt[a + 1].copy(), t1_2_value),
                          ReplacementTransform(tt[b + 1].copy(), t2_2_value), run_time=run_time)

                if t[a + 1] < t[b + 1]:
                    pd = 1
                    self.play(cmp2.animate.update_text("<"), run_time=run_time)
                    self.wait(0.8)
                elif t[a + 2] < t[b + 2]:
                    pd = 0
                    self.play(cmp2.animate.update_text(">"), run_time=run_time)
                    self.wait(0.8)
                else:
                    self.play(cmp2.animate.update_text("="), run_time=run_time)
                    self.wait(0.8)
                    self.play(t1_3_title.animate.update_text(titles_map["r12"]+"[a+2]"),
                            t2_3_title.animate.update_text(titles_map["r12"]+"[b+2]"), run_time=run_time)

                    self.play(Indicate(rr12[(a + 2) // 3][0], color=RED),
                              Indicate(rr12[(b + 2) // 3][0], color=RED), run_time=run_time)

                    self.play(t1_3_value.animate.update_text(r12[(a + 2) // 3]),
                              t2_3_value.animate.update_text(r12[(b + 2) // 3]),
                              ReplacementTransform(rr12[(a + 2) // 3].copy(), t1_3_value),
                              ReplacementTransform(rr12[(b + 2) // 3].copy(), t2_3_value), run_time=run_time)

                    if r12[n1 + (a + 2) // 3] < r12[(b + 2) // 3]:
                        pd = 1
                        self.play(cmp3.animate.update_text("<"), run_time=run_time)
                        self.wait(0.8)
                    else:
                        pd = 0
                        self.play(cmp3.animate.update_text(">"), run_time=run_time)
                        self.wait(0.8)

            if pd == 1:
                self.play(ReplacementTransform(saa0[i].copy(), saa[len(ssa)]), run_time=run_time)
                ssa.append(a)
                i += 1
                if i < n0:
                    self.play(ari.animate.next_to(saa0[i], UP, buff=0.1), run_time=run_time)
                if i == n0:
                    while j < n12:
                        self.play(arj.animate.next_to(saa12[j], UP, buff=0.1), run_time=run_time)
                        self.play(ReplacementTransform(saa12[j].copy(), saa[len(ssa)]), run_time=run_time)
                        ssa.append(sa12[j])
                        j += 1
            else: 
                self.play(ReplacementTransform(saa12[j].copy(), saa[len(ssa)]), run_time=run_time)
                ssa.append(b)
                j += 1
                if j < n12:
                    self.play(arj.animate.next_to(saa12[j], UP, buff=0.1), run_time=run_time)
                if j == n12:
                    while i < n0:
                        self.play(ari.animate.next_to(saa0[i], UP, buff=0.1), run_time=run_time)
                        self.play(ReplacementTransform(saa0[i].copy(), saa[len(ssa)]), run_time=run_time)
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
                    cmp3.animate.update_text(),
                    run_time=run_time
            )

        self.wait()
        if dep == 0:
            tt_copy = Array(self.t+[0, 0, 0]).move_to(tt)
            self.play(ReplacementTransform(tt, tt_copy))
            self.wait()
            self.play(FadeOut(*self.mobjects))
        else:
            self.play(FadeOut(sa_title, ari, arj, idd, id_title, tt, t_title, 
                            saa0, sa0_title, saa12, sa12_title, sa_title,
                            saa, t12_title, tt12, r12_title, rr12,
                            t1_1_title, t1_1_value, t2_1_title, t2_1_value, cmp1,
                            t1_2_title, t1_2_value, t2_2_title, t2_2_value, cmp2,
                            t1_3_title, t1_3_value, t2_3_title, t2_3_value, cmp3))
        # merge sa0 and sa12
        # set up
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

