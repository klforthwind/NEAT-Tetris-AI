import numpy as np
from genome import Genome
from numpy.random import random
from time import time

class NEAT:

    def __init__(self, populationSize):
        self.popSize = populationSize
        self.generation = 0
        self.genomes = []
        self.currentGenome = 0
        self.t = time()

    def createPopulation(self):
        for genomeNum in range(self.popSize):
            genome = Genome()
            genome.mutate()
            self.genomes.append(genome)
            txt = "data/"+str(self.generation)+"-"+str(genomeNum)+".txt"
            np.savetxt(txt, genome.nodeNet, fmt="%f")

    def repopulate(self, generation):
        for genomeNum in range(self.popSize):
            genome = Genome()
            filename = "data/"+str(generation)+"-"+str(genomeNum)+".txt"
            with open(filename) as fdata:
                lines = fdata.read().splitlines()
                for lineNum in range(genome.nodeCount):
                    genome.nodeNet[lineNum] = float(lines[lineNum])
            self.genomes.append(genome)
        self.generation = generation

    def getMovements(self, capture, blockChange):
        return self.genomes[self.currentGenome].getButtons(capture, blockChange)

    def printFitness(self):
        self.genomes[self.currentGenome].fitness += time() - self.t
        print(" {} - {} - {}".format(
            self.generation, self.currentGenome, 
            self.genomes[self.currentGenome].fitness))
        self.t = time()

    def loop(self):
        self.currentGenome += 1
        self.t = time()
        if self.currentGenome == len(self.genomes):
            self.sortGenomes()
            self.increaseGeneration()

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

        for g in range(len(self.genomes)):
            txt = "data/"+str(self.generation)+"-"+str(g)+".txt"
            np.savetxt(txt, self.genomes[g].nodeNet, fmt="%f")

    def makeChild(self, mom, dad):
        child = Genome()
        for n in range(child.nodeCount):
            child.nodeNet[n] = mom.nodeNet[n] if random() < 0.5 else dad.nodeNet[n]
        child.mutate()
        return child

    def randChoice(self):
        return self.genomes[int(self.randWeightedNumBetween(0, len(self.genomes)-1))]

    def randWeightedNumBetween(self, min, max):
        return np.floor(np.power(random(), 2) * (max - min + 1) + min)
