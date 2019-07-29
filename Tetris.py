import numpy as np
import random

class Genome:
    inputNodes = 256
    outputNodes = 7
    neuralNet = np.random.random(outputNodes, inputNodes)

populationSize = 50
generation = 0
genomes = []
currentGenome = -1
mutationRate = 0.05
mutationStep = 0.2

archive = {
    "popSize": 0,
    "currGen": 0,
    "elites": [],
    "genomes": []
}

archive["popSize"] = populationSize
for x in range(populationSize):
    genomes.append(Genome())

currentGenome+=1
