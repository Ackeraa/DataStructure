from collections import defaultdict

class TrieNode(object):
    
    def __init__(self, pattern=None):
        self.children = defaultdict(TrieNode)
        self.pattern = None

class Trie(object):

    def __init__(self, patterns):
        self.patterns = patterns
        self.root = TrieNode()

    def build(self):
        for pattern in self.patterns:
            u = self.root
            for c in pattern:
                u = u.children[c]
            u.pattern = pattern

    def match(self, text):
        n = len(text)
        for i in range(n):
            u = self.root
            for j in range(i, n):
                u = u.children.get(text[j])
                if u is None:
                    break
                else:
                    pattern = u.pattern
                    if pattern is not None:
                        print(pattern)

if __name__ == '__main__':
    patterns = ["ab", "about", "at", "ate", "be", "bed", "edge", "get"]
    text = "abedget"
    trie = Trie(patterns)
    trie.build()
    trie.match(text)
