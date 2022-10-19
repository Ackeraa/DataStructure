class CartesianTreeNode(object):
    def __init__(self, index):
        self.index = index
        self.lchild = None
        self.rchild = None

class CartesianTree(object):
    def __init__(self, a):
        self.root = None
        self.build(a)
        # self.traverse(self.root)

    def build(self, a):
        stack = []
        for i in range(len(a)):
            new_node = CartesianTreeNode(i)
            last_poped_node = None
            while len(stack) > 0 and a[stack[-1].index] > a[i]:
                last_poped_node = stack.pop()
            new_node.lchild = last_poped_node
            if len(stack) > 0:
                stack[-1].rchild = new_node
            else:
                self.root = new_node
            stack.append(new_node)
    
    def traverse(self, node):
        if node.lchild is not None:
            self.traverse(node.lchild)
        print(node.index)
        if node.rchild is not None:
            self.traverse(node.rchild)

class CartesianTreeNumber(object):
    def __init__(self, a):
        self.num = self.build(a)

    def build(self, a):
        stack = []
        nums = []
        for i in range(len(a)):
            while len(stack) > 0 and a[stack[-1]] > a[i]:
                stack.pop()
                nums.append(0)
            stack.append(i)
            nums.append(1)
        while len(stack) > 0:
            stack.pop()
            nums.append(0)
        num = 0
        for x in nums:
            num = num * 2 + x
        return num

if __name__ == '__main__':
    a = [27, 18, 28, 18, 28, 45, 90, 45, 23, 53, 60, 28, 74, 71, 35]  
    cartesian_tree = CartesianTree(a)
    cartesian_tree_number = CartesianTreeNumber(a)
    print(cartesian_tree_number.num)
