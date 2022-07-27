from collections import defaultdict

class Brute:
    def __init__(self, patterns):
        self.patterns = patterns

    def find(self, pattern, text):
        for i in range(len(pattern)):
            if pattern[i] != text[i]:
                return False
        return True

    def match(self, text):
        m = len(text)
        answer = defaultdict(list)
        for pattern in self.patterns:
            for i in range(m - len(pattern) + 1):
                if self.find(pattern, text[i:]):
                    answer[pattern].append(i)

        return answer

if __name__ == '__main__':
    patterns = ["ab", "about", "at", "ate", "be", "bed", "edge", "get"]
    text = "abedget"
    brute = Brute(patterns)
    print(brute.match(text))

