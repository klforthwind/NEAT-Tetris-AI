import numpy as np
import random 
import numpy.random as rand

class Genome:

    # Initialize some values
    def __init__(self):
        self.inputNodes = 274
        self.outputNodes = 11
        self.neuralNet = np.zeros((self.outputNodes, self.inputNodes))
        self.mutationRate = 0.01
        self.mutationStep = 0.2
        self.fitness = -2

    # Mutate values within the neural network
    def mutate(self):
        for o in range(self.outputNodes):
            for i in range(self.inputNodes):
                isMutating = rand.random()
                if isMutating < self.mutationRate:
                    self.neuralNet[o][i] += (rand.random()-0.5) * self.mutationStep

    # Get all buttons and whether they should be pushed
    def getButtons(self, inputNodes):
        arr = np.empty(11)
        fitDiff = {
                    0: 25,
                    1: 0.2,
                    2: 2,
                    3: 0.2,
                    4: 0,
                    5: -0.3,
                    6: -0.3,
                    7: -1,
                    8: -1,
                    9: -1,
                    10: -1
                }
        for b in range(self.outputNodes):
            val = np.sum(np.multiply(inputNodes, self.neuralNet[b]))
            if val > 0:
                arr[b] = 1
                # print("dwajdiwoajdoi")
                self.fitness+=fitDiff[b]
            else:
                arr[b] = 0
        return arr

