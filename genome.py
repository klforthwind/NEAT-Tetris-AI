from numpy.random import random
from time import time
import numpy as np

class Genome:
    
    def __init__(self):
        self.node_count = 4
        self.node_net = np.zeros((self.node_count))
        self.output_nodes = 7

        self.yikes = False
        self.rotating = False
        self.mutate_rate = 0.2
        self.mutate_step = 0.1
        self.fitness = 0
        self.moves = []

    def mutate(self):
        for node in range(self.node_count):
            if random() < self.mutate_rate:
                self.node_net[node] += (random()-0.5) * self.mutate_step

    def handle_moves(self, capture, block_change):
        if len(self.moves) == 0 and block_change:
            data = capture.get_best_moves(self.node_net)
            self.moves.append(data[0])
            self.moves.append(data[1])
            self.moves.append(data[2])
            self.moves.append(data[3])

    def get_buttons(self, capture, block_change):
        moving_block = np.copy(capture.moving_block)
        left_most = np.amin(moving_block[1])
        self.handle_moves(capture, block_change)
        arr = np.zeros(self.output_nodes)
        self.yikes = False
        if len(self.moves) > 0:
            info = self.moves[0]
            if info[1] == -1 and info[0] == 0:
                info2 = [info, left_most, info[2]]
                info = info2
            # print(info)
            if info[0] != 0:
                self.rotating = True
                arr[6] = 1
                info2 = [(info[0] - 1), info[1], info[2]]
                info = info2
            elif info[1] < 8 and self.rotating:
                arr[3] = 1
                info2 = [info[0], (info[1] + 1), info[2]]
                info = info2
            elif (info[1] > 7 and  self.rotating) and (info[2] > 0):
                arr[1] = 1
                info2 = [info[0], info[1], (info[2] - 1)]
                info = info2
            elif not self.rotating and info[2] != info[1]:
                if info[2] > info[1]:
                    arr[1] = 1
                    info2 = [info[0], info[1], (info[2] - 1)]
                    info = info2
                else:
                    arr[3] = 1
                    info2 = [info[0], info[1], (info[2] + 1)]
                    info = info2
            else:
                self.yikes = True
                self.rotating = False
                self.moves.pop(0)
                arr[0] = 1
                self.fitness += 3
        if len(self.moves) > 0 and not self.yikes:
            self.moves[0] = info
        return arr
