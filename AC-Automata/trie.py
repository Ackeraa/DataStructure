from collections import defaultdict
import tree

class TrieNode(object):
    
    def __init__(self, pattern=None):
        self.children = defaultdict(TrieNode)
        self.pattern = None

class Trie(object):

    def __init__(self, patterns):
        self.patterns = patterns
        self.root = TrieNode()
        self.tree_node = tree.Node(' ')

    def build(self):
        for pattern in self.patterns:
            u = self.root
            tree_u = self.tree_node
            for c in pattern:
                if c in tree_u.children.keys():
                    tree_u = tree_u.childrens[c]
                else:
                    tree_v = tree.Node(c)  
                    tree_u.connect(tree_v)
                    tree_u = tree_v
                u = u.children[c]
            u.pattern = pattern

    def match(self, text):
        m = len(text)
        for i in range(m):
            u = self.root
            for j in range(i, m):
                u = u.children.get(text[j])
                if u is None:
                    break
                else:
                    pattern = u.pattern
                    if pattern is not None:
                        print(pattern)

if __name__ == '__main__':
    patterns = ["ab", "about", "at", "ate", "be", "bed", "edge", "get"]
    patterns = ["at", "art", "oars", "soar"]
    patterns = ["i", "in", "tin", "sting"]
    text = "abedget"
    trie = Trie(patterns)
    trie.build()
    trie.match(text)
    tree.draw(trie.tree_node)
