from math import log 

class St(object):
    def __init__(self, a):
        self.a = a
        self.n = len(a)
        self.f = [[0 for _ in range(self.n)] for _ in range(self.n)]

    def preprocess(self):
        for i in range(self.n):
            self.f[i][0] = self.a[i] 

        k = int(log(self.n) / log(2))
        for l in range(1, k + 1):
            for i in range(self.n):
                if i + int(pow(2, l)) - 1 >= self.n:
                    break
                self.f[i][l] = min(self.f[i][l - 1], self.f[i + int(pow(2, l - 1))][l - 1])

    def rmq(self, i, j):
        k = int(log(j - i + 1) / log(2))
        return min(self.f[i][k], self.f[j - int(pow(2, k)) + 1][k])

if __name__ == '__main__':
    a = [2, 9, 7, 6, 5, 1, 8, 3, 4, 6]
    st = St(a)
    st.preprocess()
    print(st.rmq(2, 8))
