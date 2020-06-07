from random import shuffle
from random import seed

class Tetris:

    def __init__(self):
        self.board = ([99,99] + [0] * 10 + [99,99]) * 20 + [99] * 28
        self.queue = [0] * 48
        self.hold = [0] * 8

        self.shapes = {
	        "I": [[0,0,0,0], [1,1,1,1], [0,0,0,0], [0,0,0,0]],
	        "J": [[2,0,0], [2,2,2], [0,0,0]],
	        "L": [[0,0,3], [3,3,3], [0,0,0]],
	        "O": [[4,4], [4,4]],
	        "S": [[0,5,5], [5,5,0], [0,0,0]],
	        "T": [[0,6,0], [6,6,6], [0,0,0]],
	        "Z": [[7,7,0], [0,7,7], [0,0,0]]
        }
        self.shape_ids = [None] + list(self.shapes.keys())

        self.jlstz_kicks = {
            "0>R": [(0, 0), (-1, 0),(-1,-1),(0, 2), (-1, 2)],
            "R>0": [(0, 0), (1, 0), (1, 1), (0, -2),(1, -2)],
            "R>2": [(0, 0), (1, 0), (1, 1), (0, -2),(1, -2)],
            "2>R": [(0, 0), (-1, 0),(-1,-1),(0, 2), (-1, 2)],
            "2>L": [(0, 0), (1, 0), (1, -1),(0, 2), (1, -2)],
            "L>2": [(0, 0), (-1, 0),(-1, 1),(0, -2),(-1,-2)],
            "L>0": [(0, 0), (-1, 0),(-1, 1),(0, -2),(-1,-2)],
            "0>L": [(0, 0), (1, 0), (1, -1),(0, 2), (1, 2)]}

        self.i_kicks = {
            "0>R": [(0, 0), (-2, 0),(1, 0), (-2, 1),(1, -2)],
            "R>0": [(0, 0), (2, 0), (-1,0), (2, -1),(-1, 2)],
            "R>2": [(0, 0), (-1, 0),(2, 0), (-1,-2),(2, 1)],
            "2>R": [(0, 0), (1, 0), (-2,0), (1, 2), (-2,-1)],
            "2>L": [(0, 0), (2, 0), (-1,0), (2, -1),(-1, 2)],
            "L>2": [(0, 0), (-2, 0),(1, 0), (-2, 1),(1,-2)],
            "L>0": [(0, 0), (1, 0), (-2,0), (1, 2), (-2,-1)],
            "0>L": [(0, 0), (-1, 0),(2, 0), (-1,-2),(2, 1)]}

        self.current = {"x":0, "y":0, "r":0, "key":None, "shape":None}
        self.game_over = False
        self.has_held = False
        self.block_seed = 42
        self.score = 0
        self.bag = []

        self.increase_bag()
        self.next_block()

    def handle_i_piece(self, shape):
        if max(shape[0 : 4]) == 0:
            shape[0 : 4] = shape[4 : 8]
            shape[4 : 8] = [0] * 4

    def set_hold(self, key):
        self.hold = self.get_shape_data(key)[0 : 8]
        self.handle_i_piece(self.hold)

    get_hold = lambda self : self.shape_ids[max(self.hold)]

    def get_shape_data(self, key):
        lst = []
        for layer in self.shapes[key]:
            lst += [0] if len(layer) == 2 else []
            lst += layer
            lst += [0] if len(layer) != 4 else []
        return lst

    def set_queue(self):
        if len(self.bag) < 6:
            self.increase_bag()
        for s in range(6):
            block_data = self.get_shape_data(self.bag[s])
            self.handle_i_piece(block_data)
            self.queue[s * 8 : (s + 1) * 8] = block_data[0 : 8]

    board_pos = lambda self, x, y : (x + 2) + y * 14

    queue_pos = lambda self, x, y : x + y * 4

    def increase_bag(self):
        keys = list(self.shapes.keys())
        seed(self.block_seed)
        self.block_seed += 7
        shuffle(keys)
        self.bag += keys

    def next_block(self):
        self.score += 1
        next_key = self.bag.pop(0)
        self.current = {
            "x": 5 - int((len(self.shapes[next_key]) + 1) / 2), 
            "y": 0, "r": 0, "key": next_key, 
            "shape": self.shapes[next_key] }
        self.set_queue()
        self.apply_shape()

    def _mask_shape(self, being_applied):
        shape = self.current["shape"]
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                val = shape[y][x]
                if val:
                    loc = self.board_pos(self.current["x"] + x, self.current["y"] + y)
                    self.board[loc] = val if being_applied else 0

    def apply_shape(self):
        self._mask_shape(True)

    def remove_shape(self):
        self._mask_shape(False)
    
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

    def rotate(self, shape, going_left):
        return (self.transpose(self.reverse(shape)),
                self.reverse(self.transpose(shape)))[going_left]
    
    def update(self):
        self.remove_shape()
        self.current["y"] += 1
        new_block = self.exists_collision()
        self.current["y"] -= 1 if new_block else 0
        self.apply_shape()
        if new_block:
            for y in range(20):
                if min(self.board[y * 14 + 2: (y + 1) * 14 - 2]) > 0:
                    self.score += 4
                    for a in range(14):
                        self.board.pop(y * 14)
                    self.board = [99,99] + [0] * 10 + [99,99] + self.board
            self.has_held = False
            last_count = sum(self.board)
            if max(self.board[4:8]) != 0:
                self.game_over = True
            self.next_block()

    def try_rot(self, going_left):
        choices = ["0>L","R>0","2>R","L>2"] if going_left else ["0>R","R>2","2>L","L>0"]
        did_change = False
        if self.current["key"] != "O":
            self.remove_shape()
            choice = choices[self.current["r"] % 4]
            self.current["r"] += 3 if going_left else 1
            self.current["r"] %= 4
            old = dict(self.current)
            self.current["shape"] = self.rotate(self.current["shape"], going_left)
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

    def perform_movement(self, move):
        if move == "RL":
            self.try_rot_left()
        elif move == "RR":
            self.try_rot_right()
        elif move == "L":
            self.try_left()
        elif move == "R":
            self.try_right()
        elif move == "SD":
            self.try_soft_drop()
        elif move == "HD":
            self.try_hard_drop()
            self.update()
        elif move == "H":
            self.try_hold()

##################################################
# AI Code

    def get_game_state(self):
        lst = [0] * 200
        for y in range(20):
            for x in range(10):
                loc = self.board_pos(x, y)
                if self.board[loc]:
                    lst[x + y * 10] = 1
        curr_piece = self.get_shape_data(self.current["key"])[0 : 8]
        self.handle_i_piece(curr_piece)
        lst = lst + self.hold + curr_piece + self.queue[:-8]
        return list(lst)
    
    def get_next_game_state(self):
        lst = [0] * 200
        for y in range(20):
            for x in range(10):
                loc = self.board_pos(x, y)
                if self.board[loc]:
                    lst[x + y * 10] = 1
        lst = lst + self.hold + self.queue
        return list(lst)

    def can_place(self):
        shape = self.current["shape"]
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x]:
                    loc = self.board_pos(self.current["x"] + x, self.current["y"] + y + 1)
                    if self.board[loc] != 0:
                        return True
        return False

    def get_height(self):
        total = 0
        for x in range(10):
            for y in range(20):
                if self.board[self.board_pos(x, y)]:
                    total += 20 - y
                    break
        return total

    def get_bumpiness(self):
        total = 0
        left_col = -1
        for x in range(10):
            col_height = 0
            for y in range(20):
                if self.board[self.board_pos(x, y)]:
                    col_height = 20 - y
                    break
            if left_col != -1:
                total += abs(left_col - col_height)
            left_col = col_height
        return total

    def get_holes(self):
        total = 0
        for x in range(10):
            for y in range(20):
                if self.board[self.board_pos(x, y)]:
                    total += 1
        return self.get_height() - total

    def get_completed_lines(self):
        lines = 0
        for row in range(20):
            lines += min(self.board[row * 14 + 2 : row * 14 + 12]) != 0
        return lines
