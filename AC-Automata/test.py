import unittest
import random
from brute import Brute
from trie import Trie
from ac_automata import ACAutomata

class Test(unittest.TestCase):
    def setUp(self):
        self.chars = ["a", "b", "c", "d", "e", "f", "g"]
        n = 1000
        patterns = []
        hsh = {}
        for i in range(n):
            l = random.randint(1, 5)
            pattern = ""
            for _ in range(l):
                pattern += random.choice(self.chars)
            if pattern not in hsh.keys():
                hsh[pattern] = 1
                patterns.append(pattern)

        self.brute = Brute(patterns)
        self.trie = Trie(patterns)
        self.ac_automata = ACAutomata(patterns)

    def test_trie(self):
        t = 10
        for _ in range(t):
            n = 100
            text = ""
            for i in range(n):
                text += random.choice(self.chars)

            self.assertEqual(self.trie.match(text), self.brute.match(text))

    def test_ac_automata(self):
        t = 10
        for _ in range(t):
            n = 100
            text = ""
            for i in range(n):
                text += random.choice(self.chars)
            self.assertEqual(self.ac_automata.match(text), self.brute.match(text))

if __name__ == "__main__":
    unittest.main()
