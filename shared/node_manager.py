from file_manager import *
from copy import deepcopy
from tetris import Tetris
from node import Node
from piece import *

class NodeManager:

    def __init__(self):
        self.file_manager = FileManager()
        self.tetris = Tetris()

    def create_copy(self, tetris):
        tetris.remove_shape()
        temp = self.tetris
        temp.board = list(tetris.board)
        temp.current = dict(tetris.current)
        temp.current["shape"] = deepcopy(tetris.current["shape"])
        temp.hold = list(tetris.hold)
        temp.queue = list(tetris.queue)
        tetris.apply_shape()

    def analyze_switch(self, capture, node_net):
        temp_tetris = capture.tetris

        p = Piece(capture.moving_block)

        dct = {
            Piece([[0,0,0,0],[0,1,2,3]]) : "I",
            Piece([[1,1,0,0],[0,1,0,1]]) : "O",
            Piece([[1,0,0,0],[2,0,1,2]]) : "L",
            Piece([[1,0,0,0],[0,0,1,2]]) : "J",
            Piece([[1,0,0,0],[1,0,1,2]]) : "T",
            Piece([[1,1,0,0],[1,2,0,1]]) : "S",
            Piece([[1,1,0,0],[0,1,1,2]]) : "Z"
        }
        try:
            key = dct[p]
            temp_tetris.current = {
            "x": 5 - int((len(temp_tetris.shapes[key]) + 1) / 2), 
            "y": 0, "r": 0, "key": key, 
            "shape": temp_tetris.shapes[key] }

            return self.analyze(capture.tetris, node_net)
        except:
            return None

    def analyze(self, tetris, node_net):
        self.create_copy(tetris)
        tetris = self.tetris
        board_state = tetris.get_game_state()

        print(sum(board_state[0:200]))

        node_list = self.get_node_list()

        score = -1000
        sel_node = None
        for n in node_list:
            temp_score = (n.completed_lines * node_net[0] + n.bumpiness * node_net[1] + 
                n.height * node_net[2] + n.holes * node_net[3])
            if temp_score > score:
                score = temp_score
                sel_node = n
        return sel_node

    def get_node_list(self):
        start_node = Node()
        curr = self.tetris.current
        start_node.x = curr["x"]
        start_node.y = curr["y"]
        start_node.shape = deepcopy(curr["shape"])

        frontier = [start_node]
        visited = {start_node: start_node}
        final_nodes = []
        while len(frontier) > 0:
            n = frontier.pop(0)
            moves = len(n.movement)
            if moves != 0 and n.movement[moves-1] == "HD":
                continue
            for dx, dy, rot in [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, 2, 0), (1, 0, 0), (-1, 0, 0)]:
                curr = self.tetris.current
                curr["x"] = n.x
                curr["y"] = n.y
                curr["r"] = n.rot
                curr["shape"] = deepcopy(n.shape)
                self.tetris.apply_shape()

                nn = Node()
                nn.movement = list(n.movement)
                if rot != 0:
                    self.tetris.try_rot(rot == 1)
                    move = ("RR", "RL")[rot == 1]
                    nn.movement.append(move)
                if dx == 1:
                    self.tetris.try_right()
                    nn.movement.append("R")
                if dx == -1:
                    self.tetris.try_left()
                    nn.movement.append("L")
                if dy == 1:
                    self.tetris.try_soft_drop()
                    nn.movement.append("SD")
                if dy == 2:
                    self.tetris.try_hard_drop()
                    nn.movement.append("HD")

                self.tetris.remove_shape()

                new = dict(self.tetris.current)
                nn.x, nn.y, nn.rot = new["x"], new["y"], new["r"]
                nn.shape = deepcopy(new["shape"])
                if nn not in visited:
                    visited[nn] = nn
                    frontier.append(nn)
                    if not self.tetris.exists_collision() and self.tetris.can_place():
                        self.tetris.apply_shape()
                        new_board_state = self.tetris.get_next_game_state()
                        nn.height = self.tetris.get_height()
                        nn.holes = self.tetris.get_holes()
                        nn.bumpiness = self.tetris.get_bumpiness()
                        nn.completed_lines = self.tetris.get_completed_lines()
                        nn.board = self.tetris.board
                        self.tetris.remove_shape()
                        final_nodes.append(nn)
                elif len(nn.movement) < len(visited[nn].movement):
                    visited[nn].movement = list(nn.movement)

        return list(final_nodes)
