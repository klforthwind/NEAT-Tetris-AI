from file_manager import *
from copy import deepcopy
from tetris import Tetris
from node import Node

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

    def new_file(self, hexcode, node):
        with open("data/"+hexcode+".txt", "w+") as hex_file:
            hex_file.write("V1\n")
            hex_file.write(str(node.height)+"\n")
            hex_file.write(str(node.holes)+"\n")
            hex_file.write(str(node.completed_lines)+"\n")
            hex_file.write(str(node.rating))
    
    def get_new_node(self):
        nn = Node()
        nn.height = self.tetris.get_height()
        nn.holes = self.tetris.get_holes()
        nn.completed_lines = self.tetris.get_completed_lines()
        nn.rating = -1
        return nn

    def analyze(self, tetris):
        self.create_copy(tetris)

        tetris = self.tetris
        board_state = tetris.get_game_state()
        hexcode = self.file_manager.get_hexcode(board_state)
        node_list = []

        if not self.file_manager.is_loadable(hexcode):
            nn = self.get_new_node()
            self.new_file(hexcode, nn)
            with open("data/"+hexcode+".txt", "a+") as hex_file:
                node_list = self.get_node_list()
                for node in node_list:
                    hex_file.write("\n"+node.hexcode+"\n")
                    lst_data = ",".join([str(x) for x in node.movement])
                    hex_file.write(lst_data)
                    if not self.file_manager.is_loadable(node.hexcode):
                        self.new_file(node.hexcode, node)
        else:
            hex_file = open("data/"+hexcode+".txt")
            file_data = hex_file.read().splitlines()
            hex_file.close()
            if len(file_data) < 6:
                hex_file = open("data/"+hexcode+".txt", "a+")
                node_list = self.get_node_list()
                for node in node_list:
                    hex_file.write("\n"+node.hexcode+"\n")
                    lst_data = ",".join([str(x) for x in node.movement])
                    hex_file.write(lst_data)
                    if not self.file_manager.is_loadable(node.hexcode):
                        self.new_file(node.hexcode, node)
                hex_file.close()
            with open("data/"+hexcode+".txt") as hex_file:
                file_data = hex_file.read().splitlines()
                node_list = []
                for n in range(int((len(file_data[5:])) // 2)):
                    node_data = file_data[5 + n * 2 : 5 + (n + 1) * 2]
                    with open("data/"+node_data[0]+".txt") as new_file:
                        new_data = new_file.read().splitlines()
                        temp_node = Node()
                        temp_node.hexcode = node_data[0]
                        temp_node.height = int(new_data[1])
                        temp_node.holes = int(new_data[2])
                        temp_node.completed_lines = int(new_data[3])
                        temp_node.rating = int(new_data[4])
                        temp_node.movement = node_data[1].split(",")
                        node_list.append(temp_node)

        score = -1000
        sel_node = None
        for n in node_list:
            temp_score = n.completed_lines + n.rating - int(n.holes // 10)
            if temp_score > score:
                score = temp_score
                sel_node = n
            if n.rating == -1:
                sel_node = n
                break
        
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
                        new_hexcode = self.file_manager.get_hexcode(new_board_state)
                        nn.hexcode = new_hexcode
                        nn.height = self.tetris.get_height()
                        nn.holes = self.tetris.get_holes()
                        nn.completed_lines = self.tetris.get_completed_lines()
                        self.tetris.remove_shape()
                        nn.rating = -1

                        final_nodes.append(nn)
                elif len(nn.movement) < len(visited[nn].movement):
                    visited[nn].movement = list(nn.movement)

        return list(final_nodes)
    
    def update_rankings(node_list)
        node_count = len(node_list)
        for i in range(node_count-1,-1,-1):
            node_file = open(node_list[i])
            lines = node_file.readlines()
            node_file.close()

            node_file = open(node_list[i], "w")
            lines[4] = min(i, 200)

            node_file.close()
