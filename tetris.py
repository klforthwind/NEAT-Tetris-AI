import numpy as np
import random 
import numpy.random as rand
from genome import Genome
from shape import Shape

# Initialize variables
populationSize = 50
generation = 0
genomes = []
currentGenome = -1

score = 0
moves = 0

# Create the initial genomes
for g in range(populationSize):
    temp = Genome()
    temp.mutate()
    genomes.append(temp)
    del temp

    

# Controlled randomness
rand.seed(0)

# Returns a number between min and max that is more likely to be skewed towards min
def randWeightedNumBetween(min, max):
    return np.floor(np.power(rand.random(), 2) * (max - min + 1) + min)

def randChoice():
    return genomes[randWeightedNumBetween(0, len(genomes))]

# Makes a child genome from parent genomes + random mutations
def makeChild(mom, dad):
    child = Genome()
    for o in range(child.outputNodes):
        for i in range(child.inputNodes):
            child.neuralNet[o][i] = mom.neuralNet[o][i] if rand.random() < 0.5 else dad.neuralNet[o][i]
    child.mutate()
    return child

# Make genome index 0
currentGenome+=1
trash = True
while (trash):
    trash = False

    


    if currentGenome == len(genomes):
        print("Generation ", generation ," evaluated.")
        currentGenome = 0
        generation += 1
        score = 0
        moves = 0

        genomes.sort(key=lambda x: x.fitness, reverse=True)
        # for x in range(populationSize):
        #     print(genomes[x].fitness)
        print("Elite Fitness: ", genomes[0].fitness)
        for o in range(7):
            print(genomes[0].neuralNet[o])

        while len(genomes) > populationSize / 2:
            genomes.pop(len(genomes)-1)

        children = []
        children.append(genomes[0])
        for c in range(populationSize - 1):
            children.append(randChoice())
        
        genomes = children
        print(genomes)
        del children
        print(genomes)




