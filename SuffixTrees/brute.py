class Brute:
    def __init__(self, text):
        self.text = text
        self.sa = []
        self.build()

    def build(self):
        seq = [self.text[i:] for i in range(len(self.text))]
        self.sa = sorted(range(len(seq)), key=seq.__getitem__)

if __name__ == '__main__':
    text = "abcabasdascacab"
    text = "bcaeaeccef"
    text = "gebaddfbafdcdebadebf"
    brute = Brute(text)

    print(brute.sa)
