from collections import defaultdict

class TrieNode:
    
    def __init__(self, pattern=None):
        self.children = defaultdict(TrieNode)
        self.pattern = None

class Trie:

    def __init__(self, patterns):
        self.patterns = patterns
        self.root = TrieNode()
        self.build()

    def build(self):
        for pattern in self.patterns:
            u = self.root
            for c in pattern:
                u = u.children[c]
            u.pattern = pattern

    def match(self, text):
        m = len(text)
        answer = defaultdict(list)
        for i in range(m):
            u = self.root
            for j in range(i, m):
                u = u.children.get(text[j])
                if u is None:
                    break
                if u.pattern is not None:
                    answer[u.pattern].append(i)

        return answer

if __name__ == '__main__':
    patterns = ["ab", "about", "at", "ate", "be", "bed", "edge", "get"]
    text = "abedget"
    patterns = ['dda', 'efgbe', 'bdd', 'abd', 'b', 'gac', 'afd', 'e', 'dgffd']
    text = "gcaebdcegg"
    trie = Trie(patterns)
    print(trie.match(text))
