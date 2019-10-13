import numpy as np
from genome import Genome
from numpy.random import random
from time import time

class NEAT:

    def __init__(self, populationSize):                                     # Initialize variables
        self.popSize = populationSize                                       # Set the NEAT population size
        self.generation = 0                                                 # Set the generation to 0
        self.genomes = []                                                   # Create an empty list of genomes
        self.currentGenome = 0                                              # Set the currentGenome index to 0
        self.t = time()                                                     # Set self.t to a relative point in time

    def createPopulation(self):                                             # Create the initial genomes
        for genomeNum in range(self.popSize):                               # Iterate over the genome population
            genome = Genome()                                               # Make a new genome
            genome.mutate()                                                 # Mutate the genome
            self.genomes.append(genome)                                     # Append the new genome to the genome list
            txt = "data/"+str(self.generation)+"-"+str(genomeNum)+".txt"    # Create a file name
            np.savetxt(txt, genome.nodeNet, fmt="%f")                       # Save the nodenet of a genome to a file correspoding to generation and genomeNumber

    def repopulate(self, generation):                                       # Repopulate genomes from the latest generation that exists (in saved text files)
        for genomeNum in range(self.popSize):                               # Iterate over the genome population
            genome = Genome()                                               # Make a new genome
            filename = "data/"+str(generation)+"-"+str(genomeNum)+".txt"    # Create a filename to retrieve data from
            file = open(filename, "r")                                      # Open said file
            lines = file.read().splitlines()                                # Get all of the data in the file
            for lineNum in range(genome.nodeCount):                         # Iterate over all nodes in the nodeNet
                genome.nodeNet[lineNum] = float(lines[lineNum])             # Put each node from the file into the genome's node net
            file.close()                                                    # Close the file
            self.genomes.append(genome)                                     # Append the genome to the genome list
        self.generation = generation                                        # Set the generation to the correct generation

    def getMovements(self, capture, blockChange):                           # Return the correct button inputs from the currentGenome
        return self.genomes[self.currentGenome].getButtons(capture, blockChange)    # Return the genome's thoughts on what buttons to press
    
    def printFitness(self):
        self.genomes[self.currentGenome].fitness += time() - self.t         # Update the genomes fitness
        print(" {} - {} - {}".format(                                       # Print out fitness of the genome
            self.generation, self.currentGenome, 
            self.genomes[self.currentGenome].fitness))
        self.t = time()                                                     # Update the relative point of time

    def loop(self):                                                         # Go to the next genome or increase generation
        self.currentGenome += 1                                             # Increase the currentGenome index
        self.t = time()                                                     # Update the relative point of time
        if self.currentGenome == len(self.genomes):                         # Check to see if the currentGenome index is out of bounds of the genomes list
            self.sortGenomes()                                              # Sort the genomes by fitness, highest will be first in list
            self.increaseGeneration()                                       # Increase the generation

    def sortGenomes(self):
        self.genomes.sort(key=lambda x: x.fitness, reverse=True)            # Sort the genomes by fitness, highest will be first in list
    
    def increaseGeneration(self):
        print("Generation ", self.generation ," evaluated.")
        self.currentGenome = 0                                              # Reset the currentGenome index to 0
        self.generation += 1                                                # Increase the generation number

        while len(self.genomes) > self.popSize / 2:                         # Reduce the genome list to the first half
            self.genomes.pop(len(self.genomes)-1)                           # Pop off the last genome
        
        children = []                                                       # Make children and append them to a new list
        self.genomes[0].fitness = 0                                         # Set the fitness of the genome from the last generation to 0
        children.append(self.genomes[0])                                    # Append the best genome from last generation to this genome list
        for c in range(self.popSize - 1):                                   # Iterate over population size minus one
            children.append(self.makeChild(self.randChoice(),self.randChoice()))    # Append a child to the children list

        self.genomes = children                                             # Set the genome list to the children list

        for g in range(len(self.genomes)):                                  # Iterate over all of the created genomes
            txt = "data/"+str(self.generation)+"-"+str(g)+".txt"            # Create a filename to save data to
            np.savetxt(txt, self.genomes[g].nodeNet, fmt="%f")              # Save the nodenet to the txt file

    def makeChild(self, mom, dad):
        child = Genome()                                                            # Create a new child genome
        for n in range(child.nodeCount):                                            # Iterate over all nodes in the child's node net
            child.nodeNet[n] = mom.nodeNet[n] if random() < 0.5 else dad.nodeNet[n] # Set a node in the child's node net to either the mother's or father's
        child.mutate()                                                              # Mutate the node net
        return child                                                                # Return the child

    def randChoice(self):
        return self.genomes[int(self.randWeightedNumBetween(0, len(self.genomes)-1))]   # Returns a random genome

    def randWeightedNumBetween(self, min, max):
        return np.floor(np.power(random(), 2) * (max - min + 1) + min)      # Return a number between min and max, skewed towards min
    