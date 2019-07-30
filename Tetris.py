import numpy as np
import random 
import numpy.random as rand

class Genome:
    inputNodes = 256
    outputNodes = 7
    neuralNet = np.zeros((outputNodes, inputNodes))
    fitness = -1

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

rand.seed(0)

archive["popSize"] = populationSize
genomes = []
arr = rand.randint(10, size=populationSize)
for x in range(populationSize):
    temp = Genome()
    temp.fitness = arr[x]
    genomes.append(temp)

    
currentGenome+=1

if True:
    print("Generation ",generation," evaluated.")
    currentGenome = 0
    generation += 1
    score = 0
    moves = 0

    genomes.sort(key=lambda x: x.fitness, reverse=True)
    for x in range(populationSize):
        print(genomes[x].fitness)

