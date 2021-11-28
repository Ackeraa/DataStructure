from collections import defaultdict
import tree
import queue

class TrieNode(tree.Node):
    
    def __init__(self, text=" ", color="grey", pattern=None):
        tree.Node.__init__(self, text, color)
        self.children = {}
        self.pattern = None
        self.suffix_link = None
        self.output_link = None

class Trie(object):

    def __init__(self, patterns):
        self.patterns = patterns
        self.root = TrieNode()

    def build(self):
        for pattern in self.patterns:
            u = self.root
            for i, c in enumerate(pattern):
                if c in u.children.keys():
                    u = u.children[c]
                else:
                    if i == len(pattern) - 1:
                        v = TrieNode(c, color="green")
                    else:
                        v = TrieNode(c)
                    u.children[c] = v
                    u.connect(v)
                    u = v
            u.pattern = pattern

        tree.dfs(self.root, -1, 1)
        self.bfs()

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

                v.connect(v.suffix_link, color="red") 
                # Build output link.
                if v.suffix_link.pattern is not None:
                    v.output_link = v.suffix_link
                else:
                    v.output_link = v.suffix_link.output_link
                if v.output_link is not None:
                    v.connect(v.output_link, color="blue")
                q.put(v)

    def match(self, text):
        u = self.root
        for c in text:
            while not c in u.children.keys():
                u = u.suffix_link
                if u == self.root:
                    break
            if c in u.children.keys():
                u = u.children[c]
            v = u
            while v is not None:
                if v.pattern is not None:
                    print(v.pattern)
                v = v.output_link

if __name__ == '__main__':
    patterns = ["ab", "about", "at", "ate", "be", "bed", "edge", "get"]
    #patterns = ["i", "in", "tin", "sting"]
    text = "abedget"
    trie = Trie(patterns)
    trie.build()
    trie.match(text)
    tree.draw()
