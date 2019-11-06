import numpy as np
from genome import Genome
from numpy.random import random
from time import time

class NEAT:
    def __init__(self, population_size):
        self.pop_size = population_size
        self.generation = 0
        self.genomes = []
        self.current_genome = 0
        self.relative_time = time()

    def create_population(self):
        for genome_num in range(self.pop_size):
            genome = Genome()
            genome.mutate()
            self.genomes.append(genome)
            txt = "data/"+str(self.generation)+"-"+str(genome_num)+".txt"
            np.savetxt(txt, genome.node_net, fmt="%f")

    def repopulate(self, generation):
        for genome_num in range(self.pop_size):
            genome = Genome()
            file_name = "data/"+str(generation)+"-"+str(genome_num)+".txt"
            with open(file_name) as file_data:
                lines = file_data.read().splitlines()
                for line_num in range(genome.node_count):
                    genome.node_net[line_num] = float(lines[line_num])
            self.genomes.append(genome)
        self.generation = generation

    def get_movements(self, capture, block_change):
        return self.genomes[self.current_genome].get_buttons(capture, block_change)

    def print_fitness(self):
        self.genomes[self.current_genome].fitness += time() - self.t
        print(" {} - {} - {}".format(
            self.generation, self.current_genome, 
            self.genomes[self.current_genome].fitness))
        self.t = time()

    def loop(self):
        self.current_genome += 1
        self.t = time()
        if self.current_genome == len(self.genomes):
            self.sort_genomes()
            self.increase_generation()

    def sort_genomes(self):
        self.genomes.sort(key=lambda x: x.fitness, reverse=True)

    def increase_generation(self):
        print("Generation ", self.generation ," evaluated.")
        self.current_genome = 0
        self.generation += 1

        while len(self.genomes) > self.pop_size / 2:
            self.genomes.pop(len(self.genomes)-1)
        
        children = []
        self.genomes[0].fitness = 0
        children.append(self.genomes[0])
        for c in range(self.pop_size - 1):
            children.append(self.make_child(self.rand_choice(),self.rand_choice()))

        self.genomes = children

        for g in range(len(self.genomes)):
            txt = "data/"+str(self.generation)+"-"+str(g)+".txt"
            np.savetxt(txt, self.genomes[g].node_net, fmt="%f")

    def make_child(self, mom, dad):
        child = Genome()
        for n in range(child.node_count):
            child.node_net[n] = mom.node_net[n] if random() < 0.5 else dad.node_net[n]
        child.mutate()
        return child

    def rand_choice(self):
        return self.genomes[int(self.rand_num_weighted(0, len(self.genomes)-1))]

    def rand_num_weighted(self, min, max):
        return np.floor(np.power(random(), 2) * (max - min + 1) + min)
