from numpy import uint8
import datahandler
import unittest

class TestDataHandler(unittest.TestCase):
	def __init__(self, *args, **kwargs):
        super(TestingClass, self).__init__(*args, **kwargs)
		self.test_case = np.array([[1, 0, 0], [1, 1, 0]], uint8)
		self.dh = DataHandler()

    def test_getHeights(self):
		print(self.dh.getHeights(self.test_case))
        self.assertEqual(self.dh.getHeights(self.test_case), np.array([2,1,0]), "Should be 6")

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