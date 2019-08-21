from numpy.random import random
import numpy as np
from time import time
import cv2

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
        self.maap = np.zeros((640, 320))
        self.needNewArray = True

    # Mutate values within the neural network
    def mutate(self):
        for n in range(self.nodeCount):
            isMutating = random()
            if isMutating < self.mutationRate:
                self.nodeNet[n] += (random()-0.5) * self.mutationStep

    # Get all buttons and whether they should be pushed
    def getButtons(self, mList):
        if self.needNewArray:
            self.moves = mList
            self.needNewArray = False
        arr = np.zeros(self.outputNodes)
        xPos = self.moves[4] + self.moves[6]
        if self.moves[1] != 0:
            self.moves[1] -= 1
            arr[6] = 1
        elif xPos > self.moves[0]:
            self.moves[4] -= 1
            arr[3] = 1
        elif xPos < self.moves[0]:
            self.moves[4] += 1
            arr[1] = 1
        else:
            self.needNewArray = True
            arr[0] = 1

        return arr

