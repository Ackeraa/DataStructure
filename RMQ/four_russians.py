from math import sqrt, log, pow, inf
from st import St

class FourRussians(object):
    def __init__(self, a):
        self.n = len(a)
        self.a = a
        self.len_b = max(1, int(log(self.n)/log(2)))
        self.cnt_b = (self.n - 1) // self.len_b + 1
        self.f = [[[inf for _ in range(self.len_b)]
                    for _ in range(self.len_b)]
                    for _ in range(self.cnt_b)]


    def preprocess(self):
        f = [inf for _ in range(self.cnt_b)] 
        for i in range(self.cnt_b):
            for j in range(i * self.len_b, i * self.len_b + self.len_b):
                if j >= self.n:
                    break
                f[i] = min(f[i], self.a[j])
                for k in range(i * self.len_b, j):
                    self.f[i][k][j] = min(self.f[i][k][j], self.a[k])

        self.st = St(f)
        self.st.preprocess()

    def rmq(self, i, j):
        ans = min(ans, self.st.rmq(ith + 1, jth - 1))
        return ans

if __name__ == '__main__': 
    a = [3, 5, 4, 1, 2, 9, 7, 6, 5, 8, 2, 4, 7, 4]
    combine1 = Combine1(a)
    combine1.preprocess()
    print(combine1.rmq(1, 13))
