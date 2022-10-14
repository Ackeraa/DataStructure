import unittest
import random
from brute import Brute
from suffix_array import SuffixArray

class Test(unittest.TestCase):
    def setUp(self):
        chars = ["a", "b", "c", "d", "e", "f", "g"]
        n = 100
        text = "".join([ random.choice(chars) for _ in range(n)])

        self.brute = Brute(text)
        self.suffix_array = SuffixArray(text)

    def test_suffix_array_built(self):
        self.assertEqual(self.brute.sa, self.suffix_array.sa)

if __name__ == "__main__":
    unittest.main()
