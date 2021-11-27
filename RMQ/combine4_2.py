from math import sqrt, log, inf
from st import St
from dp2 import Dp
from cartesian_stack import CartesianTreeNumber

class FischerHeun(object):
    def __init__(self, a):
        self.a = a
        self.n = len(a)
        self.len_b = max(1, int(log(sqrt(self.n))/log(4)))
        self.cnt_b = (self.n - 1) // self.len_b + 1
        self.hash = {} 

    def preprocess(self):
        f = [inf for _ in range(self.cnt_b)] 
        for i in range(self.cnt_b):
            for j in range(i * self.len_b, i * self.len_b + self.len_b):
                if j >= self.n:
                    break
                f[i] = min(f[i], self.a[j])

        self.st = St(f)
        self.st.preprocess()

    def rmq(self, i, j):
        ans = inf
        ith = i // self.len_b 
        jth = j // self.len_b
        i = i % self.len_b
        j = j % self.len_b
        i_a = self.a[ith * self.len_b : ith * self.len_b + self.len_b]
        j_a = self.a[jth * self.len_b : jth * self.len_b + self.len_b]

        ctn_i = CartesianTreeNumber(i_a).num
        ctn_j = CartesianTreeNumber(j_a).num
        if not ctn_i in self.hash:
            dp = Dp(i_a)
            dp.preprocess()
            self.hash[ctn_i] = dp.f
        if not ctn_j in self.hash:
            dp = Dp(j_a)
            dp.preprocess()
            self.hash[ctn_j] = dp.f

        recover = lambda i, ith : self.a[i + ith * self.len_b]

        if ith == jth:
            ans = min(ans, recover(self.hash[ctn_i][i][j], ith))
        else:
            ans = min(ans, recover(self.hash[ctn_i][i][self.len_b - 1], ith))
            ans = min(ans, recover(self.hash[ctn_j][0][j], jth))

        if ith + 1 <= jth - 1:
            ans = min(ans, self.st.rmq(ith + 1, jth - 1))
        return ans

if __name__ == '__main__': 
    a = [3, 5, 4, 1, 2, 9, 7, 6, 5, 8, 2, 4, 7, 4]
    fischer_heun = FischerHeun(a)
    fischer_heun.preprocess()
    print(fischer_heun.rmq(1, 13))
