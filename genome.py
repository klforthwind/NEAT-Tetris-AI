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

        self.needPosition = False
        self.list = []

    # Mutate values within the neural network
    def mutate(self):
        for n in range(self.nodeCount):
            isMutating = random()
            if isMutating < self.mutationRate:
                self.nodeNet[n] += (random()-0.5) * self.mutationStep

    def handleMoves(self, capture, xPos):
        # This should only happen once
        if len(self.list) == 0:
            data = capture.getBestMoves(self.nodeNet)
            self.list.append(data[0])
            self.list.append(data[1])
        elif len(self.list) < 7:
            self.list.append(capture.getNextBestMove(self.list, self.nodeNet))

    # Get all buttons and whether they should be pushed
    def getButtons(self, capture, xPos):
        self.handleMoves(capture, xPos)
        arr = np.zeros(self.outputNodes)
        info = self.list[0]
        if info[1] != 0:
            arr[6] = 1
            info2 = [info[0], (info[1] - 1)]
            info = info2
            self.needPosition = True
        elif xPos > info[0]:
            arr[3] = 1
            info2 = [info[0] + 1, (info[1])]
            info = info2
        elif xPos < info[0]:
            arr[1] = 1
            info2 = [info[0] - 1, (info[1])]
            info = info2
        else:
            self.list.pop(0)
            arr[0] = 1
        self.list[0] = info
        return arr

