import numpy as np
import random 
import numpy.random as rand

class Genome:
    def __init__(self):
        self.inputNodes = 272
        self.outputNodes = 7
        self.neuralNet = np.zeros((self.outputNodes, self.inputNodes))
        self.mutationRate = 0.01
        self.mutationStep = 0.2
        self.fitness = -1

    def mutate(self):
        for o in range(self.outputNodes):
            for i in range(self.inputNodes):
                isMutating = rand.random()
                if isMutating < self.mutationRate:
                    self.neuralNet[o][i] += (rand.random()-0.5) * self.mutationStep