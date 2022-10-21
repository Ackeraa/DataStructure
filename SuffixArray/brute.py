class Brute:
    def __init__(self, text):
        self.text = text
        self.sa = self.build()
        self.height = self.get_height()

    def build(self):
        seq = [self.text[i:] for i in range(len(self.text))]
        return sorted(range(len(seq)), key=seq.__getitem__)

    def get_height(self):
        def match(a, b):
            num = 0
            for i in range(min(len(a), len(b))):
                if a[i] == b[i]:
                    num += 1
                else:
                    break
            return num

        n = len(self.text)
        height = [0 for _ in range(n)]
        for i in range(n - 1):
            height[i] = match(self.text[self.sa[i + 1]:], self.text[self.sa[i]:])

        return height

    def lcp(self, i, j):
        ans = self.height[i]
        for k in range(i, j):
            ans = min(ans, self.height[k])

        return ans

if __name__ == '__main__':
    text = "abcabcacab"
    text = "aabaaabbabaaaba"
    brute = Brute(text)

    print(brute.height)
    print(brute.lcp(0, 2))
