import os
import sys
import unittest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from receiver import receiver


class Monolithic(unittest.TestCase):
    def test_1(self):
        pass
