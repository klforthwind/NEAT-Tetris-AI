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

        self.list = []
        self.hitSeven = False

    # Mutate values within the neural network
    def mutate(self):
        for n in range(self.nodeCount):
            isMutating = random()
            if isMutating < self.mutationRate:
                self.nodeNet[n] += (random()-0.5) * self.mutationStep

    def handleMoves(self, capture, blockChange):
        # This should only happen once
        if len(self.list) == 0 and blockChange:
            data = capture.getBestMoves(self.nodeNet)
            self.list.append(data[0])
            self.list.append(data[1])
        elif len(self.list) < 7 and (not self.hitSeven or blockChange):
            self.list.append(capture.getNextBestMove(self.list, self.nodeNet))
        else:
            self.hitSeven = True

    # Get all buttons and whether they should be pushed
    def getButtons(self, capture, blockChange):
        self.handleMoves(capture, blockChange)
        arr = np.zeros(self.outputNodes)
        yikes = False
        if len(self.list)>0:
            info = self.list[0]
            if info[0] != 0:
                arr[6] = 1
                info2 = [(info[0] - 1), info[1], info[2]]
                info = info2
            elif info[1] < 8:
                arr[3] = 1
                info2 = [info[0], (info[1] + 1), info[2]]
                info = info2
            elif info[1] > 7 and info[2] > 0:
                arr[1] = 1
                info2 = [info[0], info[1], (info[2] - 1)]
                info = info2
            else:
                yikes = True
                self.list.pop(0)
                arr[0] = 1
        if len(self.list) > 0 and not yikes:
            self.list[0] = info
        return arr

