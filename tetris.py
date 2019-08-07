import numpy as np
import random 
import numpy.random as rand
from genome import Genome
from shape import Shape

populationSize = 50
generation = 0
genomes = []
currentGenome = -1

def randWeightedNumBetween(min, max):
    return np.floor(np.power(rand.random(), 2) * (max - min + 1) + min)

def makeChild(mom, dad):
    child = Genome()
    for o in range(child.outputNodes):
        for i in range(child.inputNodes):
            child.neuralNet[o][i] = mom.neuralNet[o][i] if rand.random() < 0.5 else dad.neuralNet[o][i]
    child.mutate()
    return child

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
    temp.mutate()
    temp.fitness = arr[x]
    genomes.append(temp)
    del temp

    
currentGenome+=1

if currentGenome == len(genomes):
    print("Generation ",generation," evaluated.")
    currentGenome = 0
    generation += 1
    score = 0
    moves = 0

    genomes.sort(key=lambda x: x.fitness, reverse=True)
    # for x in range(populationSize):
    #     print(genomes[x].fitness)
    print("Elite Fitness: ", genomes[0].fitness)
    temp = Genome()
    temp.fitness = genomes[0].fitness
    temp.neuralNet = genomes[0].neuralNet
    archive["elites"].append(temp)

    while len(genomes) > populationSize / 2:
        genomes.pop(len(genomes)-1)

    children = []
    children.append(temp)
    del temp

    

