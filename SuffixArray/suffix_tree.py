import sys
sys.path.insert(0, '../RMQ')
from cartesian_stack import CartesianTree
from suffix_array import SuffixArray

class SuffixTreeNode:
    def __init__(self, l=0, r=0):
        self.children = {} # could use hash table to get linear time.
        self.l = l
        self.r = r

class SuffixTree:
    def __init__(self, t):
        self.t = t + "$"
        suffix_array = SuffixArray(self.t)
        self.sa = suffix_array.sa
        self.height = suffix_array.height

        cartesian_tree = CartesianTree(self.height)
        
        self.cnt = 0
        self.root = SuffixTreeNode()
        self.build(cartesian_tree.root, self.root, 0)
        self.sa1 = []
        self.traverse(self.root)

    def build(self, u, node, cnt):
        for v in (u.lchild, u.rchild):
            # [l, r)
            if v is None:
                if self.cnt >= len(self.sa):
                    break
                l = self.sa[self.cnt]
                r = len(self.t)
                c = self.t[l + node.r - node.l]
                node.children[c] = SuffixTreeNode(l, r)
                self.cnt += 1
            elif self.height[u.index] == self.height[v.index]: # fusion
                self.build(v, node, cnt)
            else:
                l = self.sa[v.index]
                r = l + self.height[v.index]
                c = self.t[l + node.r - node.l]
                node.children[c] = SuffixTreeNode(l, r)
                self.build(v, node.children[c], cnt)

    def traverse(self, u):
        for c in u.children:
            v = u.children[c]
            if v.children == {}:
                self.sa1.append(v.l)
            self.traverse(v)

if __name__ == '__main__':
    text = "abcabcacab"
    suffix_tree = SuffixTree(text)
