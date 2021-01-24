from math import inf

class Brute(object):
    def __init__(self, a):
        self.n = len(a)
        self.a = a

    def rmq(self, i, j):
        ans = inf
        for k in range(i, j + 1):
            ans = min(ans, self.a[k])
        return ans

if __name__ == '__main__':
    a = [5, 4, 1, 3, 2]
    brute = Brute(a)
