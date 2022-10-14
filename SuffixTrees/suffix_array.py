class SuffixArray:
    def __init__(self, text):
        self.text = text + "$"
        self.sa = []
        self.sa = sorted([self.text[i:] for i in range(len(self.text))])

    def radix_sort(self):












if __name__ == '__main__':
    text = "abcabcacab"
    suffix_array = SuffixArray(text)
    print(suffix_array.sa)

