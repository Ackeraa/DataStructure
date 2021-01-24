from math import sqrt, log, pow, inf
from st import St
from combine1 import Combine1

class Combine3(object):
    def __init__(self, a):
        self.a = a
        self.n = len(a)
        self.len_b = max(1, int(log(self.n)/log(2)))
        self.cnt_b = (self.n - 1) // self.len_b + 1

    def preprocess(self):
        f = [inf for _ in range(self.cnt_b)] 
        for i in range(self.cnt_b):
            for j in range(i * self.len_b, i * self.len_b + self.len_b):
                if j >= self.n:
                    break
                f[i] = min(f[i], self.a[j])

        # ST between blocks.
        self.st = St(f)
        self.st.preprocess()

        # ST winth block.
        self.combine1s = []
        for i in range(self.cnt_b):
            tmp = self.a[i * self.len_b : min(self.n, i * self.len_b + self.len_b)]
            self.combine1s.append(Combine1(tmp))
            self.combine1s[i].preprocess()

    def rmq(self, i, j):
        ans = inf
        ith = i // self.len_b 
        jth = j // self.len_b

        i -= ith * self.len_b
        j -= jth * self.len_b
        if ith == jth:
            ans = min(ans, self.combine1s[ith].rmq(i, j))  
        else:
            ans = min(ans, self.combine1s[ith].rmq(i, self.len_b - 1))
            ans = min(ans, self.combine1s[jth].rmq(0, j))

        if ith + 1 <= jth - 1:
            ans = min(ans, self.st.rmq(ith + 1, jth - 1))
        return ans

if __name__ == '__main__': 
    a = [3, 5, 4, 1, 2, 9, 7, 6, 5, 8, 2, 4, 7, 4]
    combine1 = Combine1(a)
    combine1.preprocess()
    print(combine1.rmq(1, 13))
