import unittest
import random
from brute import Brute
from suffix_array import SuffixArray

class Test(unittest.TestCase):
    def setUp(self):
        self.chars = ["a", "b", "c", "d", "e", "f", "g"]

    def test_suffix_array_built(self):
        for _ in range(100):
            n = 100 + random.randint(0, 3)
            text = "".join([ random.choice(self.chars) for _ in range(n)])
            # print(text)

            brute = Brute(text)
            suffix_array = SuffixArray(text)
            self.assertEqual(brute.sa, suffix_array.sa)

    def test_kasai(self):
        for _ in range(100):
            n = 100 + random.randint(0, 3)
            text = "".join([ random.choice(self.chars) for _ in range(n)])
   
            brute = Brute(text)
            suffix_array = SuffixArray(text)
            self.assertEqual(brute.sa, suffix_array.sa)
            self.assertEqual(brute.height, suffix_array.height)

if __name__ == "__main__":
    unittest.main()
