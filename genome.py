from numpy.random import random
import numpy as np
from time import time
import cv2

class Genome:

    # Initialize some values
    def __init__(self):

        # Make node net
        self.nodeCount = 4
        self.nodeNet = np.zeros((self.nodeCount))
        self.outputNodes = 7

        # Set mutation rate, step, and fitness
        self.mutationRate = 0.2
        self.mutationStep = 0.1
        self.fitness = 0
        
        self.needNew = False
        self.list = np.zeros((6))

    # Mutate values within the neural network
    def mutate(self):
        for n in range(self.nodeCount):
            isMutating = random()
            if isMutating < self.mutationRate:
                self.nodeNet[n] += (random()-0.5) * self.mutationStep

    # Get all buttons and whether they should be pushed
    def getButtons(self, mList):
        if self.needNew:
            self.needNew = False
            self.list = mList
        arr = np.zeros(self.outputNodes)
        xPos = self.list[2]
        if self.list[1] != 0:
            arr[6] = 1
            self.list[1] -= 1
        elif xPos > self.list[0]:
            arr[3] = 1
            self.list[2] -= 1
        elif xPos < self.list[0]:
            arr[1] = 1
            self.list[2] += 1
        else:
            self.needNew = True
            arr[0] = 1
        return arr

