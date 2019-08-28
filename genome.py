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

    # Mutate values within the neural network
    def mutate(self):
        for n in range(self.nodeCount):
            isMutating = random()
            if isMutating < self.mutationRate:
                self.nodeNet[n] += (random()-0.5) * self.mutationStep

    # Get all buttons and whether they should be pushed
    def getButtons(self, mList):
        arr = np.zeros(self.outputNodes)
        xPos = mList[2]
        if mList[1] != 0:
            arr[6] = 1
        elif xPos > mList[0]:
            arr[3] = 1
        elif xPos < mList[0]:
            arr[1] = 1
        else:
            arr[0] = 1
        return arr

