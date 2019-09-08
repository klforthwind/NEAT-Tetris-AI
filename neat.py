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
        for genomeNum in range(self.popSize):
            genome = Genome()
            genome.mutate()
            self.genomes.append(genome)
            del genome
        #Let's save some stats
        for genomeNum in range(len(self.genomes)):
            txt = "data/"+str(self.generation)+"-"+str(genomeNum)+".txt"
            np.savetxt(txt, self.genomes[genomeNum].nodeNet, fmt="%f")
            del txt

    # Repopulate genomes from the latest generation that exists (in saved text files)
    def repopulate(self, generation):
        # Iterate over the population size
        for genomeNum in range(self.popSize):
            genome = Genome()
            filename = "data/"+str(generation)+"-"+str(genomeNum)+".txt"
            file = open(filename, "r")
            lines = file.read().splitlines()
            # Save the neural network to the genome
            for lineNum in range(genome.nodeCount):
                genome.nodeNet[lineNum] = float(lines[lineNum])
            # Clean up memory
            del lines
            file.close()
            # Add genome to the genome list
            self.genomes.append(genome)
            del genome
        self.generation = generation

    def getMovements(self, capture, xPos, blockChange):
        return self.genomes[self.currentGenome].getButtons(capture, xPos, blockChange)
    
    def printFitness(self):
        self.genomes[self.currentGenome].fitness += time() - self.t
        print(" ",self.generation, " - ", self.currentGenome, " - ", self.genomes[self.currentGenome].fitness)
        self.t = time()

    # Go to the next genome
    # If we just did the last genome of one generation, increase generation
    def loop(self):
        self.currentGenome += 1
        self.t = time()
        if self.currentGenome == len(self.genomes):
            self.sortGenomes()
            self.increaseGeneration()
    
    # Sorts genomes by fitness, such that list[0] has the highest fitness
    def sortGenomes(self):
        self.genomes.sort(key=lambda x: x.fitness, reverse=True)
    
    # Increase the generation number,
    # reset currentGenome to 0,
    # and evolve the next generation 
    def increaseGeneration(self):
        print("Generation ", self.generation ," evaluated.")
        self.currentGenome = 0
        self.generation += 1

        # Reduce the genome list to the first half
        while len(self.genomes) > self.popSize / 2:
            self.genomes.pop(len(self.genomes)-1)
            
        # Make children and append them to a new list
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
    