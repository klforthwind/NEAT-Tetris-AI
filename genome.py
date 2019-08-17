import numpy as np
import random 
import numpy.random as rand

class Genome:

    # Initialize some values
    def __init__(self):

        # Set a blank neural network
        self.inputNodes = 256
        self.hiddenNodes = 18
        self.outputNodes = 7
        self.rightNeuralNet = np.zeros((self.outputNodes, self.hiddenNodes))
        self.leftNeuralNet = np.zeros((self.hiddenNodes, self.inputNodes))

        # Set mutation rate, step, and fitness
        self.mutationRate = 0.002
        self.mutationStep = 0.1
        self.fitness = -2

    # Mutate values within the neural network
    def mutate(self):
        for o in range(self.outputNodes):
            for h in range(self.hiddenNodes):
                isMutating = rand.random()
                if isMutating < self.mutationRate:
                    self.rightNeuralNet[o][h] += (rand.random()-0.5) * self.mutationStep
        for h in range(self.hiddenNodes):
            for i in range(self.inputNodes):
                isMutating = rand.random()
                if isMutating < self.mutationRate:
                    self.leftNeuralNet[h][i] += (rand.random()-0.5) * self.mutationStep

    # Get all buttons and whether they should be pushed
    def getButtons(self, inputNodes, hiddenNodes):
        arr = np.zeros(self.outputNodes)
        fitDiff = {
            0: 0,
            1: 0,
            2: 1,
            3: 0,
            4: 0,
            5: -0.3,
            6: -0.3,
            7: -1,
            8: -1,
            9: -1,
            10: -1
        }
        
        hiddenValues = np.zeros((self.hiddenNodes))
        for n in range(self.hiddenNodes):
            hiddenValues = np.sum(np.multiply(inputNodes, self.leftNeuralNet[n]))
        
        for b in range(4):
            val = np.sum(np.multiply(hiddenValues, self.rightNeuralNet[b]))
            if val > 0 and arr[0] == 0 and arr[1] == 0 and arr[2] == 0:
                arr[b] = 1
                self.fitness+=fitDiff[b]
            else:
                arr[b] = 0
        for b in range(self.outputNodes - 4):
            val = np.sum(np.multiply(hiddenValues, self.rightNeuralNet[b+4]))
            if val > 0:
                arr[b+4] = 1
                self.fitness+=fitDiff[b+4]
            else:
                arr[b+4] = 0
        return arr

