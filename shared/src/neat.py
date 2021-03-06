from numpy.random import random
from numpy import savetxt
from genome import Genome
from time import time

class NEAT:
    
    def __init__(self, population_size, loadable):
        self.pop_size = population_size
        self.current_genome = 0
        self.genomes = []
        self.t = time()
        if loadable[0]:
            self.repopulate(loadable[1])
        else:
            self.create_population()

    def data_loc(self, generation, genome_num):
        return f"../data/%d-%d.txt"%(generation, genome_num)

    def create_population(self):
        """
        Creates a genome population using self.pop_size
        """
        self.generation = 0
        for genome_num in range(self.pop_size):
            genome = Genome()
            genome.mutate()
            self.genomes.append(genome)
            txt = self.data_loc(self.generation, genome_num)
            savetxt(txt, genome.node_net, fmt="%f")

    def repopulate(self, generation):
        """
        Repopulates genomes
        """
        self.generation = generation
        for genome_num in range(self.pop_size):
            genome = Genome()
            file_name = self.data_loc(generation, genome_num)
            with open(file_name) as file_data:
                lines = file_data.read().splitlines()
                for line_num in range(genome.node_count):
                    genome.node_net[line_num] = float(lines[line_num])
            self.genomes.append(genome)

    def get_current_nn(self):
        return self.genomes[self.current_genome].node_net

    def print_fitness(self):
        self.genomes[self.current_genome].fitness += time() - self.t
        print(f" %d - %d - %d" % (
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

        self.create_next_gen()

        for g in range(len(self.genomes)):
            txt = self.data_loc(self.generation, g)
            savetxt(txt, self.genomes[g].node_net, fmt="%f")

    def create_next_gen(self):
        past_gen = self.genomes[0:int(self.pop_size / 2)]
        past_gen[0].fitness = 0
        self.genomes = []
        self.genomes.append(past_gen[0])
        for g in range(self.pop_size - 1):
            mom = self.rand_genome(past_gen)
            dad = self.rand_genome(past_gen)
            self.genomes.append(self.make_child(mom, dad))

    def make_child(self, mom, dad):
        child = Genome()
        for n in range(child.node_count):
            giver = (mom, dad)[random() > 0.5]
            child.node_net[n] = giver.node_net[n]
        child.mutate()
        return child

    def rand_genome(self, genomes):
        return genomes[int((random() ** 2) * (len(genomes)))]
