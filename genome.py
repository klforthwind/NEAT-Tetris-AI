import numpy as np
from numpy.random import random
import time

class Genome:

    # Initialize some values
    def __init__(self):

        # Make Node Net
        self.nodeCount = 4
        self.nodeNet = np.zeros((self.nodeCount))
        self.outputNodes = 7

        # Set mutation rate, step, and fitness
        self.mutationRate = 0.2
        self.mutationStep = 0.1
        self.fitness = 0

        self.moves = np.array([0])
        self.needNewArray = True

        self.wao = time.time()

    # Mutate values within the neural network
    def mutate(self):
        for n in range(self.nodeCount):
            isMutating = random()
            if isMutating < self.mutationRate:
                self.nodeNet[n] += (random()-0.5) * self.mutationStep

    # Get all buttons and whether they should be pushed
    def getButtons(self, mList):
        if self.needNewArray:
            # print("getting another block")
            self.moves = mList
            self.needNewArray = False
        # print(moves)
        arr = np.zeros(self.outputNodes)
        xPos = self.moves[4] + self.moves[6]
        # print(str(xPos)," going to ", str(arr[0]))
        if self.moves[1] != 0:
            # print("rotating")
            self.moves[1] -= 1
            arr[6] = 1
        elif xPos > self.moves[0]:
            # print("moving left")
            self.moves[4] -= 1
            arr[3] = 1
        elif xPos < self.moves[0]:
            # print("moving right")
            self.moves[4] += 1
            arr[1] = 1
        elif time.time() - self.wao > 3:
            # print("moving down")
            self.wao = time.time()
            self.needNewArray = True
            arr[0] = 1
        return arr

