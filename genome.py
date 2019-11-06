from numpy.random import random
import numpy as np
from time import time
import cv2

class Genome:

    def __init__(self):
        self.nodeCount = 4
        self.node_net = np.zeros((self.nodeCount))
        self.output_nodes = 7

        self.mutationRate = 0.2
        self.mutation_step = 0.1
        self.fitness = 0
        self.list = []

    def mutate(self):
        for n in range(self.nodeCount):
            is_mutating = random()
            if is_mutating < self.mutationRate:
                self.node_net[n] += (random()-0.5) * self.mutation_step

    def handle_moves(self, capture, block_change):
        if len(self.list) == 0 and block_change:
            data = capture.get_best_moves(self.node_net)
            self.list.append(data[0])
            self.list.append(data[1])
        elif len(self.list) < 7:
            self.list.append(capture.get_next_best_move(self.list, self.node_net))

    def get_buttons(self, capture, block_change):
        self.handle_moves(capture, block_change)
        arr = np.zeros(self.output_nodes)
        yikes = False
        if len(self.list) > 0:
            info = self.list[0]
            if info[0] != 0:
                arr[6] = 1
                info2 = [(info[0] - 1), info[1], info[2]]
                info = info2
            elif info[1] < 8:
                arr[3] = 1
                info2 = [info[0], (info[1] + 1), info[2]]
                info = info2
            elif info[1] > 7 and info[2] > 0:
                arr[1] = 1
                info2 = [info[0], info[1], (info[2] - 1)]
                info = info2
            else:
                yikes = True
                self.list.pop(0)
                arr[0] = 1
        if len(self.list) > 0 and not yikes:
            self.list[0] = info
        return arr
