import unittest
import random
from brute import Brute
from dp import Dp
from block import Block
from st import St
from combine1 import Combine1
from combine2 import Combine2
from combine3 import Combine3

class Test(unittest.TestCase):
    def setUp(self):
        self.n = random.randint(1, 100)
        a = []
        for i in range(self.n):
            a.append(random.randint(1, 100000))

        self.brute = Brute(a)
        self.dp = Dp(a)
        self.block = Block(a)
        self.st = St(a)
        self.combine1 = Combine1(a)
        self.combine2 = Combine2(a)
        self.combine3 = Combine3(a)

    def all_equal(self, func):
        for i in range(self.n):
            for j in range(i, self.n):
                self.assertEqual(func.rmq(i, j), self.brute.rmq(i, j),
                                 f"Not Equal in ({i}, {j})")

    def test_dp(self):
        self.dp.preprocess()
        self.all_equal(self.dp)

    def test_block(self):
        self.block.preprocess()
        self.all_equal(self.block)

    def test_st(self):
        self.st.preprocess()
        self.all_equal(self.st)

    def test_combine1(self):
        self.combine1.preprocess()
        self.all_equal(self.combine1)

    def test_combine2(self):
        self.combine2.preprocess()
        self.all_equal(self.combine2)

    def test_combine3(self):
        self.combine3.preprocess()
        self.all_equal(self.combine3)

if __name__ == "__main__":
    unittest.main()
