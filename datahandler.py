from numpy import uint8
import numpy as np

class DataHandler:

    def get_heights(self, board):
        is_filled = np.amax(board, axis=0)
        heights = np.argmax(board, axis=0)
        heights = np.where(is_filled, heights, 20)
        return np.subtract(20, heights)
    
    def get_xy_vals(self, block_data): 
        xy_vals = np.nonzero(block_data)
        return (np.subtract(1, xy_vals[0]), xy_vals[1])
        
    def get_queue_blocks(self, queue):
        blocks = np.zeros((6, 2, 4), dtype = uint8)
        if np.sum(queue) == 24:
            for i in range(17):
                row = i % 3
                if row != 2:
                    for j in range(4):
                        block = int((i - row) / 3)
                        blocks[block][row][j] = queue[i][j]
            for b in range(6):
                blocks[b] = self.get_xy_vals(blocks[b])
        return blocks

    def zero(self, block_data):
        data = np.copy(block_data)
        lows = np.amin(data, axis=1)
        data[0] -= lows[0]
        data[1] -= lows[1]
        return data
    
    def get_lowest_blocks(self, xy_data):
        xy_zeroed = self.zero(xy_data)
        width = self.get_width(xy_zeroed)
        lowest = np.array([20]*(width), uint8)
        
        for i in range(min(len(xy_zeroed[0]),4)):
            x = xy_zeroed[1][i]
            y = xy_zeroed[0][i]
            lowest[x] = min(y, lowest[x])
        return lowest
        
    def get_width(self, xy_data):
        right_most = np.amax(xy_data[1])
        left_most = np.amin(xy_data[1])
        return (right_most - left_most + 1)
        
    def rotate(self, xy_data, rotationCount):
        xy_zeroed = self.zero(xy_data)
        for r in range(rotationCount):
            yTemp = list(xy_zeroed[0])
            xy_zeroed[0] = xy_zeroed[1]
            xy_zeroed[1] = np.subtract(3, yTemp)
        return self.zero(xy_zeroed)
        
    def did_block_change(self, last_queue, queue, next_block):
        queue_change = 0
        oldtile_count = np.sum(last_queue)
        for i in range(17):
            for j in range(4):
                if i < 2:
                    next_block[i][j] = last_queue[i][j]
                if i % 3 == 2:
                    continue
                if queue[i][j] != last_queue[i][j]:
                    last_queue[i][j] = queue[i][j]
                    queue_change += 1
        tile_count = np.sum(last_queue)
        return (queue_change > 5 and
            22 < tile_count < 26 and
            22 < oldtile_count < 26)
    
    def get_new_board(self, xVal, block, b):
        block_data = self.zero(np.copy(block))
        highest = np.amax(block_data[0])
        heights = self.get_heights(b)
        board = np.copy(b)
        lowestBlock = self.get_lowest_blocks(block_data)
        high, height = 0, 0
        for col in range(int(len(lowestBlock))):
            val = heights[xVal + col] + lowestBlock[col]
            if val > high:
                high = val
                height = heights[xVal + col] - (highest - lowestBlock[col])
        for i in range(len(block_data[0])):
            yAxis = int(block_data[0][i] + height)
            xAxis = int(xVal + self.zero(block_data)[1][i])
            board[19 - yAxis][xAxis] = 1
        return np.copy(board)
        
    def get_fitness(self, board, node_net):
        fitness = 0
        heights = self.get_heights(board)

        total_height = np.sum(heights)
        holes = total_height - np.sum(board)
        lines = np.sum(np.amin(board, axis=1))
        
        bump = 0
        for i in range(len(heights)-1):
            bump += abs(heights[i] - heights[i + 1])
        
        stats = [total_height, holes, bump, lines]
        for stat_num in range(len(stats)):
            fitness += node_net[stat_num] * stats[stat_num]
        
        return fitness
        
    def get_next_best_move(self, thelist, queue, lBoard, moving_block, node_net):
        heights = self.get_heights(lBoard)
        queue_blocks = self.get_queue_blocks(queue)
        zeroed = self.zero(moving_block)
        fitness = -1
        move = (0, 0, 0)
        
        new_board = np.copy(lBoard)
        for item in range(len(thelist)):
            if item == 0:
                block_one = self.rotate(zeroed, thelist[item][1])
                width = self.get_width(block_one)
                xval = thelist[item][0]
                if np.amax(heights[xval:xval + width]) > 16:
                    continue
                new_board = self.get_new_board(xval, block_one, new_board)
            else:
                heights = self.get_heights(new_board)
                block_one = self.rotate(queue_blocks[item - 1], thelist[item][1])
                xval = thelist[item][0]
                if np.amax(heights[xval:xval + width]) > 16:
                    continue
                new_board = self.get_new_board(xval, block_one, new_board)
        new_block = queue_blocks[len(thelist) - 1]
        heights = self.get_heights(new_board)
        good_board = lBoard
        for r1 in range(4):
            block_one = self.rotate(new_block, r1)
            width = self.get_width(block_one)
            for x1 in range(int(11 - width)):
                if np.amax(heights[x1:x1 + width]) > 16:
                    continue
                theboard = self.get_new_board(x1, block_one, new_board)
                fit = self.get_fitness(theboard, node_net)
                if  fit > fitness:
                    fitness = fit
                    move = (r1, 0 ,x1)
                    good_board = np.copy(theboard)
        return move

    def get_best_moves(self, queue, last_board, moving_block, node_net):
        heights = self.get_heights(last_board)
        queue_blocks = self.get_queue_blocks(queue)
        first_block = self.zero(moving_block)
        fitness = -100000
        move_array = []
        
        for r1 in range(4):
            block_one = self.rotate(first_block, r1)
            width = self.get_width(block_one)
            for x1 in range(int(11 - width)):
                if np.amax(heights[x1:x1 + width]) > 18:
                    continue
                new_board = self.get_new_board(x1, block_one, last_board)
                new_heights = self.get_heights(new_board)
                for r2 in range(4):
                    block_two = self.rotate(queue_blocks[0], r2)
                    width2 = self.get_width(block_two)
                    for x2 in range(int(11 - width2)):
                        if np.amax(new_heights[x2:x2 + width2]) > 18:
                            continue
                        new_board2 = self.get_new_board(x2, block_two, new_board)
                        fit = self.get_fitness(new_board2, node_net)
                        if  fit > fitness:
                            fitness = fit
                            move_array = []
                            tup1 = (r1, 0, x1)
                            move_array.append(tup1)
                            tup2 = (r2, 0, x2)
                            move_array.append(tup2)
        return move_array
