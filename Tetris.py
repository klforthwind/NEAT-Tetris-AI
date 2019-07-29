import numpy as np
import random

class Genome:
    inputNodes = 256
    outputNodes = 7
    neuralNet = np.random.random(outputNodes, inputNodes)
    