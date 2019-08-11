import numpy as np
from genome import Genome
import random as rand

class NEAT:

    # Initialize variables
    def __init__(self, populationSize):
        self.popSize = populationSize
        self.generation = 0
        self.genomes = []
        self.currentGenome = 0
        self.nextBlock = np.array([])
        self.blockChanged = False
        
    # Create the initial genomes
    def createPopulation(self):
        for g in range(self.popSize):
            temp = Genome()
            temp.mutate()
            self.genomes.append(temp)
            del temp

    def processGenome(self, inputNodes):
        queueArr = np.take(inputNodes, [200,201,202,203,204,205,206,207])
        if self.nextBlock.size == 0 or not np.array_equal(self.nextBlock, queueArr):
            self.genomes[self.currentGenome].fitness += 1
            print(self.genomes[self.currentGenome].fitness)
            self.nextBlock = queueArr
            self.blockChanged = True
            del queueArr
        temp = self.genomes[self.currentGenome]
        return temp.getButtons(inputNodes)
    
    def didBlockChange(self):
        tmp = self.blockChanged
        self.blockChanged = False
        return tmp

    def loop(self):
        self.currentGenome += 1
        if self.currentGenome == len(self.genomes):
            self.sortGenomes()
            self.increaseGeneration()
    
    def sortGenomes(self):
        self.genomes.sort(key=lambda x: x.fitness, reverse=True)
        # for x in range(popSize):
        #     print(genomes[x].fitness)
    
    def increaseGeneration(self):
        print("Generation ", self.generation ," evaluated.")
        
        self.currentGenome = 0
        self.generation += 1
        self.nextBlock = np.empty(8)
            
        fitt = self.genomes[0].fitness
        print("Elite Fitness: ", fitt)
        txt = "tetris"+str(fitt)+".txt"
        np.savetxt(txt, self.genomes[0].neuralNet, fmt="%s")
    
        while len(self.genomes) > self.popSize / 2:
            self.genomes.pop(len(self.genomes)-1)
    
        children = []
        child = Genome()
        child.neuralNet = self.genomes[0].neuralNet
        children.append(child)
        for c in range(self.popSize - 1):
            children.append(self.makeChild(self.randChoice(),self.randChoice()))
            
        self.genomes = children
        del children

    # Makes a child genome from parent genomes + random mutations
    def makeChild(self, mom, dad):
        child = Genome()
        for o in range(child.outputNodes):
            for i in range(child.inputNodes):
                child.neuralNet[o][i] = mom.neuralNet[o][i] if rand.random() < 0.5 else dad.neuralNet[o][i]
        child.mutate()
        return child

    def randChoice(self):
        return self.genomes[int(self.randWeightedNumBetween(0, len(self.genomes)-1))]

    # Returns a number between min and max that is more likely to be skewed towards min
    def randWeightedNumBetween(self, min, max):
        return np.floor(np.power(rand.random(), 2) * (max - min + 1) + min)


    