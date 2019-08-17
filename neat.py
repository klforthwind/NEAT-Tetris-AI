import numpy as np
from genome import Genome
import random as rand
import time

class NEAT:

    # Initialize variables
    def __init__(self, populationSize):
        self.popSize = populationSize
        self.generation = 0
        self.genomes = []
        self.currentGenome = 0
        self.lastQueue = np.zeros((17, 4))
        self.t = time.time()
        
    # Create the initial genomes
    def createPopulation(self):
        for g in range(self.popSize):
            temp = Genome()
            temp.mutate()
            self.genomes.append(temp)
            del temp
        #Let's save some stats
        for g in range(len(self.genomes)):
            for h in range(self.genomes[0].outputNodes): 
                txt = "data/"+str(self.generation)+"-"+str(g)+"-h-"+str(h)+".txt"
                np.savetxt(txt, self.genomes[g].leftNeuralNet[h], fmt="%f")
            for o in range(self.genomes[0].outputNodes): 
                txt = "data/"+str(self.generation)+"-"+str(g)+"-o-"+str(o)+".txt"
                np.savetxt(txt, self.genomes[g].rightNeuralNet[o], fmt="%f")

    def repopulate(self, gen):
        for g in range(self.popSize):
            temp = Genome()
            for h in range(temp.hiddenNodes):
                filename = "data/"+str(gen)+"-"+str(g)+"-o-"+str(h)+".txt"
                f = open(filename, "r")
                dttt = f.read().splitlines()
                for l in range(temp.inputNodes):
                    temp.leftNeuralNet[h][l] = float(dttt[l])
                del dttt
                f.close()
            for o in range(temp.outputNodes):
                filename = "data/"+str(gen)+"-"+str(g)+"-o-"+str(o)+".txt"
                f = open(filename, "r")
                dttt = f.read().splitlines()
                for l in range(temp.hiddenNodes):
                    temp.rightNeuralNet[o][l] = float(dttt[l])
                del dttt
                f.close()
            self.genomes.append(temp)
            del temp
        self.generation = gen

    def processGenome(self, inputNodes, hiddenNodes):
        self.genomes[self.currentGenome].fitness += time.time()-self.t
        self.t = time.time()

        print(" ",self.generation, " - ", self.currentGenome, " - ", self.genomes[self.currentGenome].fitness)
        temp = self.genomes[self.currentGenome]
        return temp.getButtons(inputNodes, hiddenNodes)
    
    def didBlockChange(self, captura):
        qChange = 0
        for i in range(17):
            for j in range(4):
                if (i + 1) % 3 == 0:
                    continue
                if captura.getQueueValue(i, j) != self.lastQueue[i][j]:
                    self.lastQueue[i][j] = captura.getQueueValue(i, j)
                    qChange += 1
        tmp = qChange > 10
        return tmp

    def loop(self):
        self.currentGenome += 1
        if self.currentGenome == len(self.genomes):
            self.sortGenomes()
            self.increaseGeneration()
        self.t = time.time()
    
    # Sorts genomes by fitness, such that arr[0] has the highest fitness
    def sortGenomes(self):
        self.genomes.sort(key=lambda x: x.fitness, reverse=True)
        # for x in range(popSize):
        #     print(genomes[x].fitness)
    
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

        #Let's save some stats
        for g in range(len(self.genomes)):
            for o in range(self.genomes[0].outputNodes): 
                txt = "data/"+str(self.generation)+"-"+str(g)+"-o-"+str(o)+".txt"
                np.savetxt(txt, self.genomes[g].neuralNet[z], fmt="%f")
            for h in range(self.genomes[0].hiddenNodes): 
                txt = "data/"+str(self.generation)+"-"+str(g)+"-h-"+str(o)+".txt"
                np.savetxt(txt, self.genomes[g].neuralNet[z], fmt="%f")


    # Makes a child genome from parent genomes + random mutations
    def makeChild(self, mom, dad):
        child = Genome()
        for o in range(child.outputNodes):
            for h in range(child.hiddenNodes):
                child.rightNeuralNet[o][h] = mom.rightNeuralNet[o][h] if rand.random() < 0.5 else dad.rightNeuralNet[o][h]
        for h in range(child.hiddenNodes):
            for i in range(child.inputNodes):
                child.rightNeuralNet[h][i] = mom.leftNeuralNet[h][i] if rand.random() < 0.5 else dad.leftNeuralNet[h][i]    
        child.mutate()
        return child

    def randChoice(self):
        return self.genomes[int(self.randWeightedNumBetween(0, len(self.genomes)-1))]

    # Returns a number between min and max that is more likely to be skewed towards min
    def randWeightedNumBetween(self, min, max):
        return np.floor(np.power(rand.random(), 2) * (max - min + 1) + min)


    