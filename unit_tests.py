from numpy import array_equal as aequal
from datahandler import DataHandler
from filemanager import FileManager
from genome import Genome
from testarrays import *
from numpy import uint8
from neat import NEAT
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
    
    def is_true(self, actual):
            self.assertEqual(actual, True, "Should be True but wasn't")

    def test_neat(self):
        neat = NEAT(5, (False, -1))
        neat = NEAT(5, (True, 0))
        neat.print_fitness()
        neat.loop()
        neat.loop()
        neat.loop()
        self.equality(3, neat.current_genome)

    def test_genome(self):
        genome = Genome()
        genome.mutate()

    def test_file_manager(self):
        file_manager = FileManager()
        loadable = file_manager.loadable()
        self.tup_equal((True, 0), loadable)

    def test_get_heights(self):
        self.equality(getH1C, self.dh.get_heights(getH1))
        self.equality(getH2C, self.dh.get_heights(getH2))

    def test_get_xy_vals(self):
        self.equality(getXYV1C, self.dh.get_xy_vals(getXYV1))
        self.equality(getXYV2C, self.dh.get_xy_vals(getXYV2))
        self.equality(getXYV3C, self.dh.get_xy_vals(getXYV3))

    def test_get_queue_blocks(self):
        self.equality(getQB1C, self.dh.get_queue_blocks(getQB1))
    
    def test_zero(self):
        self.equality(z1C, self.dh.zero(z1))

    def test_get_lowest_blocks(self):
        self.equality(getLB1C, self.dh.get_lowest_blocks(getLB1))
        self.equality(getLB2C, self.dh.get_lowest_blocks(getLB2))
        self.equality(getLB3C, self.dh.get_lowest_blocks(getLB3))
    
    def test_get_width(self):
        self.equality(getW1C, self.dh.get_width(getW1))
        self.equality(getW2C, self.dh.get_width(getW2))
        self.equality(getW3C, self.dh.get_width(getW3))

    def test_rotate(self):
        self.equality(r1C1, self.dh.rotate(r1, 1))
        self.equality(r1C2, self.dh.rotate(r1, 2))
        self.equality(r1C3, self.dh.rotate(r1, 3))
        self.equality(r2C1, self.dh.rotate(r2, 1))
        self.equality(r2C2, self.dh.rotate(r2, 2))
    
    def test_did_block_change(self):
        self.is_true(not self.dh.did_block_change(dBCLast2, dBCArr, dBCNext))
        self.is_true(not self.dh.did_block_change(dBCArr, dBCLast2, dBCNext))
        self.is_true(self.dh.did_block_change(dBCLast1, dBCArr, dBCNext))
        self.equality(dBCNextC, dBCNext)
    
    def test_get_new_board(self):
        self.equality(getNB1C, self.dh.get_new_board(getNB1x,getNB1bd,getNB1b))
        self.equality(getNB2C, self.dh.get_new_board(getNB2x,getNB2bd,getNB2b))
        self.equality(getNB3C, self.dh.get_new_board(getNB3x,getNB3bd,getNB3b))
    
    def test_get_fitness(self):
        self.equality(getF1FN1C, self.dh.get_fitness(getF1, getFN1))
        self.equality(getF1FN2C, self.dh.get_fitness(getF1, getFN2))
    
    def test_get_best_moves(self):
        self.equality(getBM1C, self.dh.get_best_moves(getBM1q, getBM1b, getBM1mb, getBM1nn1))
        self.equality(getBM2C, self.dh.get_best_moves(getBM1q, getBM1b, getBM1mb, getBM1nn2))

    def test_get_next_best_move(self):
        moveArr = self.dh.get_best_moves(getBM1q, getBM1b, getBM1mb, getBM1nn1)
        self.equality(getNBM1C, self.dh.get_next_best_move(moveArr, getBM1q, getBM1b, getBM1mb, getBM1nn1))
        moveArr = self.dh.get_best_moves(getBM1q, getBM1b, getBM1mb, getBM1nn2)
        self.equality(getNBM2C, self.dh.get_next_best_move(moveArr, getBM1q, getBM1b, getBM1mb, getBM1nn2))

    # def test_AllSevenMoves(self):
    #     moveArr = self.dh.get_best_moves(getASM1q, getASM1b, getASM1mb, getASM1nn1)
    #     moveArr.append(self.dh.get_next_best_move(moveArr, getASM1q, getASM1b, getASM1mb, getASM1nn1))
    #     moveArr.append(self.dh.get_next_best_move(moveArr, getASM1q, getASM1b, getASM1mb, getASM1nn1))
    #     moveArr.append(self.dh.get_next_best_move(moveArr, getASM1q, getASM1b, getASM1mb, getASM1nn1))
    #     moveArr.append(self.dh.get_next_best_move(moveArr, getASM1q, getASM1b, getASM1mb, getASM1nn1))
    #     moveArr.append(self.dh.get_next_best_move(moveArr, getASM1q, getASM1b, getASM1mb, getASM1nn1))
    #     self.equality(getASM1C, moveArr)

    # def test_dwadoiawjdoiwaj(self):
        # print("awdahdowhdiwiodjwoiajdoi")
        # print/(self.dh.get_fitness(graph1, getASM1nn1))
        # print(self.dh.get_fitness(graph2, getASM1nn1))

if __name__ == '__main__':
    unittest.main()
