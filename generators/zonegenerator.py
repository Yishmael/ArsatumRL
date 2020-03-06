import os
import sys
import time
import math
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import sign, get_direction, clear
from objects import Creature
from item import Item

class ZoneGenerator:
    def __init__(self, width, height, temperature=5):
        self.width = width
        self.height = height
        self._temperature = temperature
        self.zone = None

    def generate(self, stairs_up, stairs_down):
        raise NotImplementedError(self)

    def seed(self, s):
        random.seed(s)