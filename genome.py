from numpy.random import random
from time import time
import numpy as np

class Genome:
    
    def __init__(self):
        self.node_count = 4
        self.node_net = [0] * self.node_count
        self.output_nodes = 7

        self.mutate_rate = 0.2
        self.mutate_step = 0.1
        self.fitness = 0
        self.moves = []

    def mutate(self):
        for node in range(self.node_count):
            if random() < self.mutate_rate:
                self.node_net[node] += (random()-0.5) * self.mutate_step
