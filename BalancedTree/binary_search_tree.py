class TreeNode:
    def __init__(self, value):
        self.value = value
        self.lchild = None
        self.rchild = None

class BinarySearchTree:
    def __init__(self, a):
        self.root = TreeNode(a[0])
        for x in a[1:]:
            self.insert(self.root, x)

    def insert(self, u, value):
        if value <= u.value:
            if u.lchild is None:
                u.lchild = TreeNode(value)
            else:
                self.insert(u.lchild, value)
        else:
            if u.rchild is None:
                u.rchild = TreeNode(value)
            else:
                self.insert(u.rchild, value)

    def find(self, u, value):
        if u is None:
            return False
        if u.value == value:
            return True
        if value < u.value:
            return self.find(u.lchild, value)
        else:
            return self.find(u.rchild, value)

    def delete(self, u, fa, value):
        if value == u.value:
            if u.lchild is None:
                u.lchild = TreeNode(value)
            else:
                self.insert(u.lchild, value)
        else:
            if u.rchild is None:
                u.rchild = TreeNode(value)
            else:
                self.insert(u.rchild, value)

    def traverse(self, u):
        pass
     
