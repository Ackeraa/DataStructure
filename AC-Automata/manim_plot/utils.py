from manim import *

class TrieNode():
    
    def __init__(self, pattern=None):
        self.children = {}
        self.pattern = None

