import numpy as np
import random 
import numpy.random as rand

mutationRate = 0.01
mutationStep = 0.2

class Genome:
    def __init__(self):
        self.inputNodes = 256
        self.outputNodes = 7
        self.neuralNet = np.zeros((self.outputNodes, self.inputNodes))
        self.fitness = -1

    def mutate(self):
        for o in range(self.outputNodes):
            for i in range(self.inputNodes):
                isMutating = rand.random()
                if isMutating < mutationRate:
                    # print(isMutating)
                    self.neuralNet[o][i] += (rand.random()-0.5) * mutationStep