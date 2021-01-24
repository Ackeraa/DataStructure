from math import sqrt, inf

class Block(object):
    def __init__(self, a):
        self.n = len(a)
        self.len_b = int(sqrt(self.n))
        self.cnt_b = (self.n - 1) // self.len_b + 1
        self.a = a
        self.f = [inf for _ in range(self.cnt_b)] 

    def preprocess(self):
        # Find the minium in every blocks.
        for i in range(self.cnt_b):
            for j in range(i * self.len_b, i * self.len_b + self.len_b):
                # Maybe overflow.
                if j >= self.n:
                    break
                self.f[i] = min(self.f[i], self.a[j])

    def rmq(self, i, j):
        ans = inf
        
        # Calculate the index of block containing i/j.
        ith = i // self.len_b
        jth = j // self.len_b
        # iterator within the block to find the minium. 

        if ith == jth:
            for k in range(i, j + 1):
                ans = min(ans, self.a[k])
        else:
            for k in range(i, ith * self.len_b + self.len_b):
                ans = min(ans, self.a[k])
            for k in range(jth * self.len_b, j + 1):
                ans = min(ans, self.a[k])
            # Iterator the blocks between i and j to find the minium.
            for k in range(ith + 1, jth):
                ans = min(ans, self.f[k])
        return ans


if __name__ == '__main__':
    a = [3, 5, 4, 1, 2, 9, 7, 6, 5, 8, 2, 4, 7, 4]
    block = Block(a)
    block.preprocess()
    print(block.rmq(1, 13))
