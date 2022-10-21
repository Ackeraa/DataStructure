import sys
sys.path.insert(0, '../RMQ')
from cartesian_stack import CartesianTree
from import SuffixArray
from collections import defaultdict

class SuffixTreeNode:
    def __init__(self, l=0, r=0):
        self.children = defaultdict(SuffixTreeNode)
        self.l = l
        self.r = r

class SuffixTree:
    def __init__(self, t):
        self.root = None
        self.t = t
        suffix_array = SuffixArray(t)
        self.sa = suffix_array.sa
        self.height = suffix_array.height

        cartesian_tree = CartesianTree(self.height)
        #self.traverse(self.cartesian_tree.root)
        self.cnt = 0
        self.build(cartesian_tree.root, self.root)


    def build(self, u, node):
        if u.lchild is None:
            l = self.sa[self.cnt]
            r = len(self.t)
            c = self.t[l]
            node[c] = SuffixTreeNode(l, r)
            self.cnt += 1
        else:
            l = self.sa[u.lchild.index]
            r = l + self.height[u.lchild.index]
            c = self.t[l]
            node[c] = SuffixTreeNode(l, r)
            self.build(u.lchild, node[c])

        if u.rchild is None:
            l = self.sa[self.cnt]
            r = len(self.t)
            c = self.t[l]
            node[c] = SuffixTreeNode(l, r)
            self.cnt += 1
        else:
            l = self.sa[u.rchild.index]
            r = l + self.height[u.rchild.index]
            c = self.t[l]
            node[c] = SuffixTreeNode(l, r)
            self.build(u.rchild, node[c])

    def traverse(self, node):
        print(node.index)
        if node.lchild is not None:
            self.traverse(node.lchild)
        if node.rchild is not None:
            self.traverse(node.rchild)

if __name__ == '__main__':
    text = "abcabcacab"
    suffix_tree = SuffixTree(text)

