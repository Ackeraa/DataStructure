from manim import *
from utils import *
import queue


class Trie(Scene):

    def construct(self):
        self.patterns = ["ab", "about", "at", "ate", "be", "bed", "edge", "get"]
        self.root = TrieNode()
        self.build()

    def build(self):
        for pattern in self.patterns:
            u = self.root
            for c in pattern:
                if c not in u.children:
                    u.children[c] = TrieNode()
                u = u.children[c]
            u.pattern = pattern

    def match(self, text):
        m = len(text)
        for i in range(m):
            u = self.root
            for j in range(i, m):
                u = u.children.get(text[j])
                if u is None:
                    break
                else:
                    pattern = u.pattern
                    if pattern is not None:
                        print(pattern)
