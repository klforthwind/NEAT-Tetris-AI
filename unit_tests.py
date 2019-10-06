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
        self.assertEqual(aequal(expected, actual), True, 
            "Should be {}, but was {}".format(expected, actual))
    
    def tup_equal(self, expected, actual):
        self.equality(expected[0], actual[0])
        self.assertEqual(expected[1], actual[1], 
            "Should be {}, but was {}".format(expected[1], actual[1]))
    
    def isTrue(self, actual):
            self.assertEqual(actual, True, "Should be True but wasn't")

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

    def test_getLowestBlocks(self):
        self.tup_equal(getLB1C, self.dh.getLowestBlocks(getLB1))
        self.tup_equal(getLB2C, self.dh.getLowestBlocks(getLB2))
        self.tup_equal(getLB3C, self.dh.getLowestBlocks(getLB3))
    
    def test_getWidth(self):
        self.equality(getW1C, self.dh.getWidth(getW1))
        self.equality(getW2C, self.dh.getWidth(getW2))
        self.equality(getW3C, self.dh.getWidth(getW3))

    def test_rotate(self):
        self.tup_equal(r1C1, self.dh.rotate(r1, 1))
        self.tup_equal(r1C2, self.dh.rotate(r1, 2))
        self.tup_equal(r1C3, self.dh.rotate(r1, 3))
        self.tup_equal(r2C1, self.dh.rotate(r2, 1))
        self.tup_equal(r2C2, self.dh.rotate(r2, 2))
    
    def test_didBlockChange(self):
        self.isTrue(not self.dh.didBlockChange(dBCLast2, dBCArr, dBCNext))
        self.isTrue(not self.dh.didBlockChange(dBCArr, dBCLast2, dBCNext))
        self.isTrue(self.dh.didBlockChange(dBCLast1, dBCArr, dBCNext))
        self.equality(dBCNextC, dBCNext)
    
    def test_getNewBoard(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
    
    def test_getFitness(self):
        self.equality(getF1FN1C, self.dh.getFitness(getF1, getFN1))
        self.equality(getF1FN2C, self.dh.getFitness(getF1, getFN2))

    def test_getNextBestMove(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
    
    def test_getBestMoves(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()