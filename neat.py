import numpy as np
from genome import Genome

# Makes a child genome from parent genomes + random mutations
def makeChild(mom, dad):
    child = Genome()
    for o in range(child.outputNodes):
        for i in range(child.inputNodes):
            child.neuralNet[o][i] = mom.neuralNet[o][i] if rand.random() < 0.5 else dad.neuralNet[o][i]
    child.mutate()
    return child

class NEAT:
    # Initialize variables
    def __init__(self, populationSize):
        self.popSize = populationSize
        self.generation = 0
        self.genomes = []
        self.currentGenome = 0

        self.score = 0
        self.moves = 0
    
        
    # Create the initial genomes
    def createPopulation(self):
        for g in range(self.populationSize):
            temp = Genome()
            temp.mutate()
            self.genomes.append(temp)
            del temp

    
    # Returns a number between min and max that is more likely to be skewed towards min
    def randWeightedNumBetween(min, max):
        return np.floor(np.power(rand.random(), 2) * (max - min + 1) + min)

    def randChoice(self):
        return self.genomes[self.randWeightedNumBetween(0, len(self.genomes))]

    def sortGenomes(self):
        self.genomes.sort(key=lambda x: x.fitness, reverse=True)
        # for x in range(populationSize):
        #     print(genomes[x].fitness)

    def increaseGeneration(self):
        print("Generation ", generation ," evaluated.")
        
        self.currentGenome = 0
        self.generation += 1
        self.score = 0
        self.moves = 0
            
        print("Elite Fitness: ", self.genomes[0].fitness)
        for o in range(7):
            print(self.genomes[0].neuralNet[o])
    
        while len(self.genomes) > self.populationSize / 2:
            self.genomes.pop(len(self.genomes)-1)
    
        children = []
        children.append(genomes[0])
        for c in range(self.populationSize - 1):
            children.append(makeChild(self.randChoice(),self.randChoice()))
            
        self.genomes = children
        del children

        def loop(self):
            self.currentGenome += 1
            if self.currentGenome == len(self.genomes):
                increaseGeneration()