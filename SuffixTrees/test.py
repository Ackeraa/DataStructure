import unittest
import random
from brute import Brute
from suffix_array import SuffixArray

class Test(unittest.TestCase):
    def setUp(self):
        self.chars = ["a", "b", "c", "d", "e", "f", "g"]

    def test_suffix_array_built(self):
        for i in range(100):
            n = 10000 + random.randint(0, 3)
            text = "".join([ random.choice(self.chars) for _ in range(n)])
            # print(text)

            brute = Brute(text)
            suffix_array = SuffixArray(text)
            self.assertEqual(brute.sa, suffix_array.sa)

if __name__ == "__main__":
    unittest.main()
