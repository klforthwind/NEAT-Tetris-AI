import numpy as np
from genome import Genome
from numpy.random import random
from time import time

class NEAT:

    # Initialize variables
    def __init__(self, populationSize):
        self.popSize = populationSize
        self.generation = 0
        self.genomes = []
        self.currentGenome = 0
        self.t = time()
        
    # Create the initial genomes
    def createPopulation(self):
        for g in range(self.popSize):
            temp = Genome()
            temp.mutate()
            self.genomes.append(temp)
            del temp
        #Let's save some stats
        for g in range(len(self.genomes)):
            txt = "data/"+str(self.generation)+"-"+str(g)+".txt"
            np.savetxt(txt, self.genomes[g].nodeNet, fmt="%f")
            del txt

    def repopulate(self, gen):
        for g in range(self.popSize):
            temp = Genome()
            filename = "data/"+str(gen)+"-"+str(g)+".txt"
            f = open(filename, "r")
            foo = f.read().splitlines()
            for l in range(temp.nodeCount):
                temp.nodeNet[l] = float(foo[l])
            del foo
            f.close()
            self.genomes.append(temp)
            del temp
        self.generation = gen
    
    def getCurrentNodeNet(self):
        return self.genomes[self.currentGenome].nodeNet

    def requiresMoreMoves(self):
        return self.genomes[self.currentGenome].noMoreMoves()

    def handMoves(self, moves):
        self.genomes[self.currentGenome].giveMoves(moves)

    def getGenomeActions(self, moves):
        return self.genomes[self.currentGenome].getButtons()
    
    def printFitness(self):
        self.genomes[self.currentGenome].fitness += time() - self.t
        print(" ",self.generation, " - ", self.currentGenome, " - ", self.genomes[self.currentGenome].fitness)
        self.t = time()

    def loop(self):
        self.currentGenome += 1
        self.t = time()
        if self.currentGenome == len(self.genomes):
            self.sortGenomes()
            self.increaseGeneration()
    
    # Sorts genomes by fitness, such that arr[0] has the highest fitness
    def sortGenomes(self):
        self.genomes.sort(key=lambda x: x.fitness, reverse=True)
    
    def increaseGeneration(self):
        print("Generation ", self.generation ," evaluated.")
        self.currentGenome = 0
        self.generation += 1

        while len(self.genomes) > self.popSize / 2:
            self.genomes.pop(len(self.genomes)-1)
            
        children = []
        self.genomes[0].fitness = 0
        children.append(self.genomes[0])
        for c in range(self.popSize - 1):
            children.append(self.makeChild(self.randChoice(),self.randChoice()))

        self.genomes = children
        del children

        #Let's save some stats
        for g in range(len(self.genomes)):
            txt = "data/"+str(self.generation)+"-"+str(g)+".txt"
            np.savetxt(txt, self.genomes[g].nodeNet, fmt="%f")
            del txt

    # Makes a child genome from parent genomes + random mutations
    def makeChild(self, mom, dad):
        child = Genome()
        for n in range(child.nodeCount):
            child.nodeNet[n] = mom.nodeNet[n] if random() < 0.5 else dad.nodeNet[n]
        child.mutate()
        return child

    # Returns a random genome
    def randChoice(self):
        return self.genomes[int(self.randWeightedNumBetween(0, len(self.genomes)-1))]

    # Returns a number between min and max that is more likely to be skewed towards min
    def randWeightedNumBetween(self, min, max):
        return np.floor(np.power(random(), 2) * (max - min + 1) + min)
    