from collections import defaultdict
import queue

class TrieNode:
    
    def __init__(self, pattern=None):
        self.children = defaultdict(TrieNode)
        self.pattern = None
        self.suffix_link = None
        self.output_link = None

class ACAutomata:

    def __init__(self, patterns):
        self.patterns = patterns
        self.root = TrieNode()
        self.build()
        self.bfs()

    def build(self):
        for pattern in self.patterns:
            u = self.root
            for c in pattern:
                u = u.children[c]
            u.pattern = pattern

    def bfs(self):
        q = queue.Queue()
        q.put(self.root)
        while not q.empty():
            u = q.get()
            # Build suffix link.
            for a, v in u.children.items():
                if u == self.root:
                    v.suffix_link = u
                else:
                    x = u.suffix_link
                    while v.suffix_link is None:
                        if a in x.children.keys():
                            v.suffix_link = x.children[a]
                        elif x == self.root:
                            v.suffix_link = x
                        else:
                            x = x.suffix_link

                # Build output link.
                if v.suffix_link.pattern is not None:
                    v.output_link = v.suffix_link
                else:
                    v.output_link = v.suffix_link.output_link

                q.put(v)

    def match(self, text):
        u = self.root
        answer = defaultdict(list)
        j = 0
        for c in text:
            while not c in u.children.keys():
                u = u.suffix_link
                if u == self.root or u is None:
                    break
            if u is None:
                break

            if c in u.children.keys():
                u = u.children[c]
                j += 1
            v = u
            while v is not None:
                if v.pattern is not None:
                    answer[v.pattern].append(j - len(v.pattern))
                v = v.output_link

        return answer

if __name__ == '__main__':
    patterns = ["ab", "about", "at", "ate", "be", "bed", "edge", "get"]
    text = "abedget"
    ac_automata = ACAutomata(patterns)
    print(ac_automata.match(text))
