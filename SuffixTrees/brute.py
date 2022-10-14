class Brute:
    def __init__(self, text):
        self.text = text + "$"
        self.sa = []
        self.build()

    def build(self):
        self.sa = sorted([self.text[i:] for i in range(len(self.text))])

if __name__ == '__main__':
    text = "abcabcacab"
    brute = Brute(text)

    print(brute.sa)
