import numpy as np
import random 
import numpy.random as rand

class Genome:

    # Initialize some values
    def __init__(self):
        self.inputNodes = 256
        self.outputNodes = 11
        self.neuralNet = np.zeros((self.outputNodes, self.inputNodes))
        self.mutationRate = 0.01
        self.mutationStep = 0.2
        self.fitness = -1

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
        for b in range(self.outputNodes):
            val = np.sum(np.multiply(inputNodes, self.neuralNet[b]))
            arr[b] = 1 if val > 0 else 0
        return arr

