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

    # def test_getHeights(self):
    #     self.equality(getH1C, self.dh.getHeights(getH1))
    #     self.equality(getH2C, self.dh.getHeights(getH2))

    # def test_getXYVals(self):
    #     self.equality(getXYV1C, self.dh.getXYVals(getXYV1))
    #     self.equality(getXYV2C, self.dh.getXYVals(getXYV2))
    #     self.equality(getXYV3C, self.dh.getXYVals(getXYV3))

    # def test_getQueueBlocks(self):
    #     self.equality(getQB1C, self.dh.getQueueBlocks(getQB1))
    
    # def test_zero(self):
    #     self.equality(z1C, self.dh.zero(z1))

    # def test_getLowestBlocks(self):
    #     self.equality(getLB1C, self.dh.getLowestBlocks(getLB1))
    #     self.equality(getLB2C, self.dh.getLowestBlocks(getLB2))
    #     self.equality(getLB3C, self.dh.getLowestBlocks(getLB3))
    
    # def test_getWidth(self):
    #     self.equality(getW1C, self.dh.getWidth(getW1))
    #     self.equality(getW2C, self.dh.getWidth(getW2))
    #     self.equality(getW3C, self.dh.getWidth(getW3))

    # def test_rotate(self):
    #     self.equality(r1C1, self.dh.rotate(r1, 1))
    #     self.equality(r1C2, self.dh.rotate(r1, 2))
    #     self.equality(r1C3, self.dh.rotate(r1, 3))
    #     self.equality(r2C1, self.dh.rotate(r2, 1))
    #     self.equality(r2C2, self.dh.rotate(r2, 2))
    
    # def test_didBlockChange(self):
    #     self.isTrue(not self.dh.didBlockChange(dBCLast2, dBCArr, dBCNext))
    #     self.isTrue(not self.dh.didBlockChange(dBCArr, dBCLast2, dBCNext))
    #     self.isTrue(self.dh.didBlockChange(dBCLast1, dBCArr, dBCNext))
    #     self.equality(dBCNextC, dBCNext)
    
    # def test_getNewBoard(self):
    #     self.equality(getNB1C, self.dh.getNewBoard(getNB1x,getNB1bd,getNB1b))
    #     self.equality(getNB2C, self.dh.getNewBoard(getNB2x,getNB2bd,getNB2b))
    #     self.equality(getNB3C, self.dh.getNewBoard(getNB3x,getNB3bd,getNB3b))
    
    # def test_getFitness(self):
    #     self.equality(getF1FN1C, self.dh.getFitness(getF1, getFN1))
    #     self.equality(getF1FN2C, self.dh.getFitness(getF1, getFN2))
    
    # def test_getBestMoves(self):
    #     self.equality(getBM1C, self.dh.getBestMoves(getBM1q, getBM1b, getBM1mb, getBM1nn1))
    #     self.equality(getBM2C, self.dh.getBestMoves(getBM1q, getBM1b, getBM1mb, getBM1nn2))

    # def test_getNextBestMove(self):
    #     moveArr = self.dh.getBestMoves(getBM1q, getBM1b, getBM1mb, getBM1nn1)
    #     self.equality(getNBM1C, self.dh.getNextBestMove(moveArr, getBM1q, getBM1b, getBM1mb, getBM1nn1))
    #     moveArr = self.dh.getBestMoves(getBM1q, getBM1b, getBM1mb, getBM1nn2)
    #     self.equality(getNBM2C, self.dh.getNextBestMove(moveArr, getBM1q, getBM1b, getBM1mb, getBM1nn2))

    def test_AllSevenMoves(self):
        moveArr = self.dh.getBestMoves(getASM1q, getASM1b, getASM1mb, getASM1nn1)
        moveArr.append(self.dh.getNextBestMove(moveArr, getASM1q, getASM1b, getASM1mb, getASM1nn1))
        moveArr.append(self.dh.getNextBestMove(moveArr, getASM1q, getASM1b, getASM1mb, getASM1nn1))
        moveArr.append(self.dh.getNextBestMove(moveArr, getASM1q, getASM1b, getASM1mb, getASM1nn1))
        moveArr.append(self.dh.getNextBestMove(moveArr, getASM1q, getASM1b, getASM1mb, getASM1nn1))
        moveArr.append(self.dh.getNextBestMove(moveArr, getASM1q, getASM1b, getASM1mb, getASM1nn1))
        self.equality(getASM1C, moveArr)

    # def test_dwadoiawjdoiwaj(self):
        # print("awdahdowhdiwiodjwoiajdoi")
        # print/(self.dh.getFitness(graph1, getASM1nn1))
        # print(self.dh.getFitness(graph2, getASM1nn1))

if __name__ == '__main__':
    unittest.main()
