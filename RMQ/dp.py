from math import inf

class Dp(object):
    def __init__(self, a):
        self.n = len(a)
        self.a = a
        self.f = [[inf for _ in range(self.n)] for _ in range(self.n)]

    def preprocess(self):
        # Initialize the number in the diagonal.
        for i in range(self.n):
            self.f[i][i] = self.a[i]

        # Iterator the diagonals.
        # l means the index of the diagonal(start from 0).
        for l in range(1, self.n):
            for i in range(0, self.n - l):
                j = i + l
                self.f[i][j] = min(self.f[i][j - 1], self.f[i + 1][j])

    def rmq(self, i, j):
        return self.f[i][j]

if __name__ == '__main__':
    a = [3, 2, 4, 1, 5]
    dp = Dp(a)
    dp.preprocess()
    print(dp.rmq(1, 3))

