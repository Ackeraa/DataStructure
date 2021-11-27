from math import sqrt, log, inf
from cartesian_stack import CartesianTreeNumber
from st import St
from dp2 import Dp

class Combine4(object):
    def __init__(self, a):
        self.a = a
        self.n = len(a)
        self.len_b = max(1, int(log(sqrt(self.n))/log(4)))
        self.hash = [-1 for _ in range(4 ** self.len_b)]
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


    def rmq(self, i, j):
        ans = inf
        ith = i // self.len_b 
        jth = j // self.len_b

        i -= ith * self.len_b
        j -= jth * self.len_b

        def find_or_set(ith, i, j):
            a = self.a[ith * self.len_b:(ith + 1) * self.len_b]
            t = CartesianTreeNumber(a).num
            if self.hash[t] == -1:
                dp = Dp(a)
                dp.preprocess()
                self.hash[t] = dp
            return a[self.hash[t].rmq(i, j)]

        if ith == jth:
            ans = min(ans, find_or_set(ith, i, j))
        else:
            ans = min(ans, find_or_set(ith, i, self.len_b - 1)) 
            ans = min(ans, find_or_set(jth, 0, j)) 

        if ith + 1 <= jth - 1:
            ans = min(ans, self.st.rmq(ith + 1, jth - 1))
        return ans

if __name__ == '__main__': 
    a = [3, 5, 4, 1, 2, 9, 7, 6, 5, 8, 2, 4, 7, 4]
    combine4 = Combine4(a)
    combine4.preprocess()
    print(combine4.rmq(1, 13))
