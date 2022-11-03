class TreeNode:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None

class BinaryTree:
    def __init(self, a):
        self.root = None
        for x in a:
            self.insert(TreeNode(x))

    # The left most leaf of subtree rooted u
    def min(self, u):
        while u.left is not None:
            u = u.left

        return u

    # The right most heaf of subtree rooted u
    def max(self, u):
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

    def predecessor(self, u):
        if u.left is not None:
            return self.max(u.left)
        p = u.parent
        while p is not None and u == p.left:
            u = p
            p = p.parent

        return p

    def insert_after(self, u):
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

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def delete(self, u):
        if u.left is None:
            self.transplant(u, u.right)
        elif u.right is None:
            self.transplant(u, u.left)
        else:
            v = self.min(u.right)
            if v.parent != u:
                self.transplant(v, v.right)
                v.right = u.right
                v.right.parent = u
            self.transplant(u, v)
            v.left = u.left
            v.left.p = v
