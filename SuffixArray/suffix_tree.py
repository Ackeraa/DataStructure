from suffix_array import SuffixArray

class SuffixTreeNode:
    def __init__(self, index):
        self.index = index
        self.lchild = []
        self.rchild = []

class SuffixTree:
    def __init__(self, t):
        self.root = None
        self.t = t
        self.suffix_array = SuffixArray(t)
        self.build(self.suffix_array.height)

    def build(self, a):
        stack = []
        for i in range(len(a)):
            new_node = SuffixTreeNode(i)
            last_poped_node = None
            while len(stack) > 0 and a[stack[-1].index] > a[i]:
                last_poped_node = stack.pop()
            new_node.lchild.append(last_poped_node)
            if len(stack) > 0:
                stack[-1].rchild.append(new_node)
            else:
                self.root = new_node
            stack.append(new_node)

if __name__ == '__main__':
    text = "abcabcacab"
    suffix_tree = SuffixTree(text)
