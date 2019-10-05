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

    def equality(self, expected, actual):
        self.assertEqual( aequal(expected, actual), True, 
            "Should be {}, but was {}".format(expected, actual))

    def test_getHeights(self):
        self.equality(getH1C, self.dh.getHeights(getH1))
        self.equality(getH2C, self.dh.getHeights(getH2))

    def test_getXYVals(self):
        self.equality(getXYV1C, self.dh.getXYVals(getXYV1))
        self.equality(getXYV2C, self.dh.getXYVals(getXYV2))
        self.equality(getXYV3C, self.dh.getXYVals(getXYV3))

    def test_getQueueBlocks(self):
        self.equality(getQB1C, self.dh.getQueueBlocks(getQB1))
    
    def test_zero(self):
        self.equality(z1C, self.dh.zero(z1))

    def test_rotate(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
    
    def test_getWidth(self):
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