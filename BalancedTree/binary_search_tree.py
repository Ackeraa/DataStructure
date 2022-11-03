class TreeNode:
    def __init__(self, value):
        self.value = value
        self.lchild = None
        self.rchild = None

class BinarySearchTree:
    def __init__(self, a):
        for x in a:
            self.insert(TreeNode(x))

    def min(self):
        u = self.root
        while u.left is not None:
            u = u.left

        return u

    def max(self):
        u = self.root
        while u.right is not None:
            u = u.right

        return u

    def successor(self, u):
        if u.right is not None:
            return self.min(u.right)
        p = u.parent
        while p is not None and u == p.right:
            u = p
            p = p.parent

        return p

    def predecessor(self):
        if u.left is not None:
            return self.max(u.left)
        p = u.parent
        while p is not None and u == p.left:
            u = p
            p = p.parent

        return p

    def insert(self, v):
        u = self.root
        if u is None:
            self.root = v
            return

        while u is not None:
            if v.value < u.value:
                u = u.left
            else:
                u = u.right
        p = u.parent
        if v.value < p.value:
            p.left = v
        else:
            p.right = v

    def delete(self, value):
        pass

    def traverse(self, u):
        pass
     
