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
        self.hitSeven = False
        self.diff = 0

    # Mutate values within the neural network
    def mutate(self):
        for n in range(self.nodeCount):
            isMutating = random()
            if isMutating < self.mutationRate:
                self.nodeNet[n] += (random()-0.5) * self.mutationStep

    def handleMoves(self, capture, blockChange):
        # This should only happen once
        print(self.list)
        if len(self.list) == 0:
            if blockChange:
                data = capture.getBestMoves(self.nodeNet)
                self.list.append(data[0])
                self.list.append(data[1])
        elif len(self.list) < 7 and (not self.hitSeven or blockChange):
            self.list.append(capture.getNextBestMove(self.list, self.nodeNet))
        else:
            self.hitSeven = True

    # Get all buttons and whether they should be pushed
    def getButtons(self, capture, xPos, blockChange):
        self.handleMoves(capture, blockChange)
        arr = np.zeros(self.outputNodes)
        yikes = False
        if len(self.list)>0:
            info = self.list[0]
            print(info[0])
            print(xPos - self.diff)
            if info[1] != 0:
                arr[6] = 1
                info2 = [info[0], (info[1] - 1)]
                info = info2
                self.diff += capture.rotDiff()
            elif xPos - self.diff > info[0]:
                arr[3] = 1
                info2 = [info[0] + 1, (info[1])]
                info = info2
            elif xPos - self.diff < info[0]:
                arr[1] = 1
                info2 = [info[0] - 1, (info[1])]
                info = info2
            else:
                yikes = True
                self.list.pop(0)
                arr[0] = 1
                self.diff = 0
        if len(self.list) > 0 and not yikes:
            self.list[0] = info
        return arr

