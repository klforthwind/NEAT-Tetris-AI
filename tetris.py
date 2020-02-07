from random import shuffle
from random import seed

class Tetris:

    def __init__(self):
        self.board = ([99] + [0] * 10 + [99]) * 20 + [99] * 24
        self.queue = [0] * 48
        self.hold = [0] * 8

        self.shape_ids = [None, "I", "J", "L", "O", "S", "T", "Z"]
        self.shapes = {
	        "I": [[0,0,0,0], [1,1,1,1], [0,0,0,0], [0,0,0,0]],
	        "J": [[2,0,0], [2,2,2], [0,0,0]],
	        "L": [[0,0,3], [3,3,3], [0,0,0]],
	        "O": [[4,4], [4,4]],
	        "S": [[0,5,5], [5,5,0], [0,0,0]],
	        "T": [[0,6,0], [6,6,6], [0,0,0]],
	        "Z": [[7,7,0], [0,7,7], [0,0,0]]
        }

        self.jlstz_kicks = {
            "0>R": [(0, 0), (-1, 0),(-1,-1),(0, 2), (-1, 2)],
            "R>0": [(0, 0), (1, 0), (1, 1), (0, -2),(1, -2)],
            "R>2": [(0, 0), (1, 0), (1, 1), (0, -2),(1, -2)],
            "2>R": [(0, 0), (-1, 0),(-1,-1),(0, 2), (-1, 2)],
            "2>L": [(0, 0), (1, 0), (1, -1),(0, 2), (1, -2)],
            "L>2": [(0, 0), (-1, 0),(-1, 1),(0, -2),(-1,-2)],
            "L>0": [(0, 0), (-1, 0),(-1, 1),(0, -2),(-1,-2)],
            "0>L": [(0, 0), (1, 0), (1, -1),(0, 2), (1, 2)]
        }

        self.i_kicks = {
            "0>R": [(0, 0), (-2, 0),(1, 0), (-2, 1),(1, -2)],
            "R>0": [(0, 0), (2, 0), (-1,0), (2, -1),(-1, 2)],
            "R>2": [(0, 0), (-1, 0),(2, 0), (-1,-2),(2, 1)],
            "2>R": [(0, 0), (1, 0), (-2,0), (1, 2), (-2,-1)],
            "2>L": [(0, 0), (2, 0), (-1,0), (2, -1),(-1, 2)],
            "L>2": [(0, 0), (-2, 0),(1, 0), (-2, 1),(1,-2)],
            "L>0": [(0, 0), (1, 0), (-2,0), (1, 2), (-2,-1)],
            "0>L": [(0, 0), (-1, 0),(2, 0), (-1,-2),(2, 1)]
        }

        self.current = {"x":0, "y":0, "r":0, "key":None, "shape":None}
        self.game_over = False
        self.has_held = False
        self.block_count = 0
        self.score = 0
        self.bag = []
        self.shape_actions = 0

        self.increase_bag()
        self.next_block()

    def print_data(self):
        data = self.queue + self.hold
        r = 0
        print("\n\n\n")
        color = ["\033[96m","\033[31m","\033[37m","\033[91m","\033[33m","\033[32m","\033[35m","\033[31m",]
        for row in range(20):
            side_data = ""
            if row % 3 != 2:
                side_data = data[r * 4 : (r + 1) * 4]
                r += 1
            dt = [str(x) for x in self.board[row * 12 + 1: (row + 1) * 12 - 1]]
            dt = [color[int(x)] + x for x in dt]
            print("\033[96m[" + "\033[96m, ".join(dt) + "\033[96m]", end= "       ")
            print(side_data)
        print("\n")

    def set_hold(self, key):
        self.hold = self.get_shape_data(key)[0 : 8]
        if max(self.hold[0 : 4]) == 0:
            self.hold[0 : 4] = self.hold[4 : 8]
            self.hold[4 : 8] = [0] * 4

    get_hold = lambda self : self.shape_ids[max(self.hold)]

    def get_shape_data(self, key):
        block = self.shapes[key]
        lst = []
        for layer in block:
            if len(layer) == 2:
                lst.append(0)
            for val in layer:
                lst.append(val)
            if len(layer) != 4:
                lst.append(0)
        return lst

    def set_queue(self):
        if len(self.bag) < 6:
            self.increase_bag()
        for s in range(6):
            block_data = self.get_shape_data(self.bag[s])
            if max(block_data[0 : 4]) == 0:
                block_data[0 : 4] = block_data[4 : 8]
                block_data[4 : 8] = [0] * 4
            self.queue[s * 8 : (s + 1) * 8] = block_data[0 : 8]

    def board_pos(self, x, y):
        return (x + 1) + y * 12

    def queue_pos(self, x ,y):
        return x + y * 4

    def increase_bag(self):
        keys = list(self.shapes.keys())
        seed(self.block_count + 9)
        self.block_count += 7
        shuffle(keys)
        for s in keys:
            self.bag.append(s)

    def next_block(self):
        self.score += 1
        self.shape_actions = 0
        next_key = self.bag.pop(0)
        self.current = {
            "x": int(5) - int((len(self.shapes[next_key]) + 1) / 2), 
            "y": 0, "r": 0, "key": next_key, 
            "shape": self.shapes[next_key] }
        self.set_queue()
        self.apply_shape()

    def mask_shape(self, being_applied):
        shape = self.current["shape"]
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                val = shape[y][x]
                if val:
                    loc = self.board_pos(self.current["x"] + x, self.current["y"] + y)
                    self.board[loc] = val if being_applied else 0

    def apply_shape(self):
        self.mask_shape(True)

    def remove_shape(self):
        self.mask_shape(False)
    
    def exists_collision(self):
        shape = self.current["shape"]
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x]:
                    loc = self.board_pos(self.current["x"] + x, self.current["y"] + y)
                    if self.board[loc] != 0:
                        return True
        return False
    
    def width(self):
        lst = [0] * 4
        shape = self.current["shape"]
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x]:
                    lst[x] = 1
        return sum(lst)

    def height(self):
        height = 0
        shape = self.current["shape"]
        for y in range(len(shape)):
            height = y + 1 if max(shape[y]) else height
        return height

    def left_most(self):
        shape = self.current["shape"]
        for x in range(len(shape[0])):
            for y in range(len(shape)):
                if shape[y][x]:
                    return x

    reverse = lambda self, lst : lst[::-1]

    transpose = lambda self, lst : list(zip(*lst))
    
    def update(self):
        self.remove_shape()
        self.current["y"] += 1
        new_block = self.exists_collision()
        self.current["y"] -= 1 if new_block else 0
        self.apply_shape()
        for y in range(20):
            if min(self.board[y * 12  + 1: (y + 1) * 12 - 1]) > 0:
                self.score += 4
                for a in range(12):
                    self.board.pop(y * 12)
                self.board = [99] + [0] * 10 + [99] + self.board
        if new_block:
            self.has_held = False
            last_count = sum(self.board)
            if max(self.board[4:8]) != 0:
                self.game_over = True
            self.next_block()
        if self.shape_actions > 1000:
            self.try_hard_drop()

    def try_rot(self, going_left):
        choices = ["0>L","R>0","2>R","L>2"] if going_left else ["0>R","R>2","2>L","L>0"]
        did_change = False
        if self.current["key"] != "O":
            self.remove_shape()
            choice = choices[self.current["r"] % 4]
            self.current["r"] += 3 if going_left else 1
            old = dict(self.current)
            self.current["shape"] = (self.transpose(self.reverse(self.current["shape"])),
                self.reverse(self.transpose(self.current["shape"])))[going_left]
            checks = self.i_kicks[choice] if self.current["key"] == "I" else self.jlstz_kicks[choice]
            for check in checks:
                self.current["x"] = old["x"] + check[0]
                self.current["y"] = old["y"] + check[1]
                if not self.exists_collision() :
                    self.apply_shape()
                    did_change = True
                    break
            if not did_change:
                self.current = old
                self.apply_shape()

    def try_rot_left(self):
        self.try_rot(True)

    def try_rot_right(self):
        self.try_rot(False)

    def try_left(self):
        self.remove_shape()
        self.current["x"] -= 1 if (self.current["x"] + self.left_most() > 0) else 0
        self.current["x"] += 1 if self.exists_collision() else 0
        self.apply_shape()

    def try_right(self):
        self.remove_shape()
        self.current["x"] += 1 if (self.current["x"] < 10 - self.width()) else 0
        self.current["x"] -= 1 if self.exists_collision() else 0
        self.apply_shape()

    def try_soft_drop(self):
        self.remove_shape()
        self.current["y"] += 1
        self.current["y"] -= 1 if self.exists_collision() else 0
        self.apply_shape()

    def try_hard_drop(self):
        for i in range(20):
            self.try_soft_drop()
        self.update()

    def try_hold(self):
        if not self.has_held:
            self.remove_shape()
            self.current["x"] = int(5) - int((len(self.current["shape"]) + 1) / 2)
            self.current["y"] = 0
            old_held = self.get_hold()
            self.set_hold(self.current["key"])
            if old_held == None:
                self.next_block()
            else:
                self.current["key"] = old_held
                self.current["shape"] = self.shapes[old_held]
            self.has_held = True

    def get_hold_and_q_blocks(self):
        return (self.hold, self.queue[0:8], self.queue[8:16])

    def get_input_nodes(self):
        lst = [0] * 300
        s_x = self.current["x"] + self.left_most()
        s_y = self.current["y"]
        for y in range(20):
            y_deviated = s_y + y - 10
            if not (0<=y_deviated<=19):
                continue
            for x in range(15):
                x_deviated = s_y + x - 6
                if not (0<=x_deviated<=9):
                    continue
                loc = self.board_pos(x_deviated, y_deviated)
                if self.board[loc]:
                    lst[x + y * 15] = 1
                else:
                    lst[x + y * 15] = -1
        return list(lst)

    def perform_movement(self, btns):
        if btns[0] > 0:
            self.try_rot_left()
        elif btns[1] > 0:
            self.try_rot_right()
        elif btns[2] > 0:
            self.try_left()
        elif btns[3] > 0:
            self.try_right()
        elif btns[4] > 0:
            self.try_soft_drop()
        elif btns[5] > 0:
            self.try_hard_drop()
        elif btns[6] > 0:
            self.try_hold()

        self.shape_actions += 1