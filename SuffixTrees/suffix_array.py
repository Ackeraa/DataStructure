class SuffixArray:
    def __init__(self, text):
        self.k = 3
        self.t = text
        # suppose char set is [a..z] -> [1..26]
        t = [ord(x) - ord('a') + 1 for x in self.t]
        self.sa = self.build(t, 27)
        print(self.sa)

    '''
        * split into three texts, connect last two into one, called R12.
        * recursively:
            * radix sort R12
            * use R12, sort R0.
            * combine R0 and R12.
    '''
    def build(self, t, N):
        t.extend([0, 0, 0])
        n = len(t)
        n0 = (n - 1) // 3
        n1 = (n - 1) // 3
        n2 = (n - 2) // 3
        n12 = n1 + n2
        sa12 = [i * 3 + 1 for i in range(n1)] \
             + [i * 3 + 2 for i in range(n2)]
        r12 = [0 for _ in range(len(sa12))]

        # sort sa12
        self.radix_pass(t[2:], sa12, N)
        self.radix_pass(t[1:], sa12, N)
        self.radix_pass(t[0:], sa12, N)

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
        sa0 = [i - 1 for i in sa12 if i % 3 == 1]
        self.radix_pass(t, sa0, N)

        # merge sa0 and sa12
        sa = []
        i = 0 if t[sa0[0]] else 1 # need to be fixed 
        j = 0 if t[sa12[0]] else 1
        while i < n0 and j < n12:
            a = sa0[i]
            b = sa12[j]
            if (b % 3 == 0 and t[a] < t[b]) or \
               (b % 3 == 1 and (t[a], r12[(a + 1) // 3]) < (t[b], r12[n1 + (b + 1) // 3])) or \
               (b % 3 == 2 and n1 + a // 3 < n12 and (t[a], t[a + 1], r12[n1 + (a + 2) // 3]) < (t[b], t[b + 1], r12[(b + 2) // 3])):

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

    def radix_pass(self, t, a, N):
        queue_list = [list() for _ in range(N)]
        for i in a:
            queue_list[t[i]].append(i)

        num = 0
        for ids in queue_list:
            for i in ids:
                a[num] = i
                num += 1

if __name__ == '__main__':
    text = "abcabcacab"
    text = "abcabasdascacab"
    text = "bcaeaeccef"
    text = "gebaddfbafdcdebadebf"
    suffix_array = SuffixArray(text)
    
    # bcaeaeccef000
    # 0123456789000
    # 0  3  6  9  
    #  1  4  7  0
    #   2  5  8  
    # 012 345 678 9 10
    # 123456000
    # 1  4  0
    #  2  5  0
    #   3  6  0

    # 12345000
    # 1  4  0
    #  2  5  0
    #   3  0

    # 1234000
    # 1  4  0
    #  2  0  
    #   3   0
