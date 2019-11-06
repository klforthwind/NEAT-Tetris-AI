from numpy.random import random
from genome import Genome
from time import time
import numpy as np

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

        create_next_gen()

        for g in range(len(self.genomes)):
            txt = "data/"+str(self.generation)+"-"+str(g)+".txt"
            np.savetxt(txt, self.genomes[g].node_net, fmt="%f")

    def create_next_gen():
        past_gen = self.genomes[0:int(self.pop_size / 2)]
        past_gen[0].fitness = 0
        self.genomes = []
        self.genomes.append(self.past_gen[0])
        for g in range(self.pop_size - 1):
            mom = self.rand_choice(past_gen)
            dad = self.rand_choice(past_gen)
            self.genomes.append(self.make_child(mom, dad))

    def make_child(self, mom, dad):
        child = Genome()
        for n in range(child.node_count):
            giver = mom if random() < 0.5 else dad
            child.node_net[n] = giver.node_net[n]
        child.mutate()
        return child

    def rand_choice(self, genomes):
        return genomes[self.rand_skewed_int(0, len(genomes)-1)]

    def rand_skewed_int(self, min, max):
        return int(np.floor(np.power(random(), 2) * (max - min + 1) + min))
