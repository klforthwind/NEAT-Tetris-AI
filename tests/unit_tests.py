import sys
sys.path.append("..")
from numpy import array_equal as aequal
from file_manager import FileManager
from node_manager import NodeManager
from genome import Genome
from testarrays import *
from numpy import uint8
from neat import NEAT
import numpy as np
import unittest

class UnitTesting(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(UnitTesting, self).__init__(*args, **kwargs)
        self.node_manager = NodeManager()

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

if __name__ == '__main__':
    unittest.main()
