class CartesianTreeNode(object):
    def __init__(self, index):
        self.index = index
        self.lchild = None
        self.rchild = None

class CartesianTree(object):
    def __init__(self, a):
        self.a = a
        self.root = self.build(0, len(a))
        self.traverse(self.root)

    def build(self, l, r):
        if l == r:
            return
        index = self.a[l:r].index(min(self.a[l:r])) + l
        node = CartesianTreeNode(index)
        node.lchild = self.build(l, index)
        node.rchild = self.build(index + 1, r)
        return node

    def traverse(self, node):
        if node.lchild is not None:
            self.traverse(node.lchild)
        print(node.index)
        if node.rchild is not None:
            self.traverse(node.rchild)

if __name__ == '__main__':
    a = [3, 5, 4, 1, 2, 9, 7, 6, 5, 8, 2, 4, 7, 4]
    cartesian_tree = CartesianTree(a)
