from numpy import array_equal as aequal
from datahandler import DataHandler
from testarrays import *
from numpy import uint8
import numpy as np
import unittest

class TestDataHandler(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDataHandler, self).__init__(*args, **kwargs)
        self.dh = DataHandler()

    def test_getHeights(self):
        print(self.dh.getHeights(test1))
        self.assertEqual(
            aequal(self.dh.getHeights(test1), test1Compare), True, 
            "Should be {}, but was {}".format(test1Compare, self.dh.getHeights(test1)))

    def test_getQueueBlocks(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
    
    def test_zero(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_rotate(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
    
    def test_getWidth(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_analyzeQBlock(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
    
    def test_didBlockChange(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_getNextBestMove(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
    
    def test_getBestMoves(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
    
    def test_getFitness(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_getLowestBlocks(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
        
    def test_getNewBoard(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()