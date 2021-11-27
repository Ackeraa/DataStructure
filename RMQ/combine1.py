from math import sqrt, log, inf
from st import St

class Combine1(object):
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

        self.st = St(f)
        self.st.preprocess()

    def rmq(self, i, j):
        ans = inf
        ith = i // self.len_b 
        jth = j // self.len_b

        if ith == jth:
            for k in range(i, j + 1):
                ans = min(ans, self.a[k])
        else:
            for k in range(i, ith * self.len_b + self.len_b):
                ans = min(ans, self.a[k])
            for k in range(jth * self.len_b, j + 1):
                ans = min(ans, self.a[k])

        if ith + 1 <= jth - 1:
            ans = min(ans, self.st.rmq(ith + 1, jth - 1))
        return ans

if __name__ == '__main__': 
    a = [3, 5, 4, 1, 2, 9, 7, 6, 5, 8, 2, 4, 7, 4]
    combine1 = Combine1(a)
    combine1.preprocess()
    print(combine1.rmq(1, 13))
