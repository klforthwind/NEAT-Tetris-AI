import numpy as np
import random

class Genome:
    inputNodes = 256
    outputNodes = 7
    neuralNet = np.zeros((outputNodes, inputNodes))
    fitness = np.random.randint(10, size=1)[0]

populationSize = 50
generation = 0
genomes = []
currentGenome = -1
mutationRate = 0.05
mutationStep = 0.2

zeroShape = None
oneShape = None
twoShape = None
threeShape = None
fourShape = None
fiveShape = None

score = 0
moves = 0

archive = {
    "popSize": 0,
    "currGen": 0,
    "elites": [],
    "genomes": []
}


archive["popSize"] = populationSize
genomes = []
for x in range(populationSize):
    genomes.append(Genome())
    
currentGenome+=1

if True:
    print("Generation ",generation," evaluated.")
    currentGenome = 0
    generation += 1
    score = 0
    moves = 0

    genomes.sort(key=lambda x: x.fitness, reverse=True)
    print(genomes[0].fitness)
    print(genomes[0].fitness)

