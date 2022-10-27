from manim import *
from utils import *
sys.path.insert(0, '../../RMQ')
sys.path.insert(0, '../')
from cartesian_stack import CartesianTree
from suffix_array import SuffixArray

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
