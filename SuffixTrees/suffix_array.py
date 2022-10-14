class SuffixArray:
    def __init__(self, text):
        self.k = 3
        self.N = 256 # chars are mapped to [0..N]
        self.t = text + "$$$"
        self.sa = []
        self.r0 = []
        self.r12 = []

    '''
        * split into three texts, connect last two into one, called R12.
        * recursively:
            * radix sort R12
            * use R12, sort R0.
            * combine R0 and R12.
    '''
    def build(self, t, sa):
        n = len(t)
        r0 = [i for i in range(n) if i % 3 == 0]
        r12 = [i for i in range(n) if i % 3 == 1] \
            + [i for i in range(n) if i % 3 == 2]

        sa0 = [0 for i in range(n)]
        sa12 = [0 for i in range(n)]

        self.radix_sort(t, r12, sa12)


    def radix_sort(self, a, idx, r):
        for k in range(3):
            c = [0 for _ in range(self.N)]
            for i in idx:
                c[a[i]] += 1
            sum = 0
            for i in range(self.N):
                t = c[i]
                c[i] = sum
                sum += t
            for i in idx:
                r[c[a[i]]] = i
                c[a[i]] += 1

if __name__ == '__main__':
    text = "abcabcacab"
    suffix_array = SuffixArray(text)
    print(suffix_array.sa)

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

