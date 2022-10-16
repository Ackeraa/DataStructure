from manim import *
from utils import *
import math
import numpy as np
import queue
import random

class BuildSuffixArray(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        a = Array([0, 1, 2, 3])
        self.add(a)
        self.wait()
