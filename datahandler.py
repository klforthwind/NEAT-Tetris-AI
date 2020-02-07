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
            for board in range(6):
                blocks[board] = self.get_xy_vals(blocks[board])
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
                if i % 3 != 2:
                    if i < 2:
                        next_block[i][j] = last_queue[i][j]
                    if queue[i][j] != last_queue[i][j]:
                        last_queue[i][j] = queue[i][j]
                        queue_change += 1
        tile_count = np.sum(last_queue)
        return (queue_change > 5 and
            22 < tile_count < 26 and
            22 < oldtile_count < 26)

    def is_queue_filled(self, queue):
        middle_count = 0
        for i in range(17):
            for j in range(4):
                if i % 3 != 2:
                    if queue[i][j] == 1 and (j == 1 or j == 2):
                        middle_count += 1
        return (middle_count >= 12)
    
    def get_new_board(self, x_val, block, board):
        block_data = self.zero(block)
        highest = np.amax(block_data[0])
        heights = self.get_heights(board)
        temp_board = np.copy(board)
        lowest_blocks = self.get_lowest_blocks(block_data)
        invert_blocks = np.subtract(highest, lowest_blocks)
        high, height = 0, 0
        for col in range(len(lowest_blocks)):
            val = heights[x_val + col] + invert_blocks[col]
            if val > high:
                high = val
                height = heights[x_val + col] - lowest_blocks[col]
        for i in range(len(block_data[0])):
            yAxis = int(block_data[0][i] + height)
            xAxis = int(x_val + self.zero(block_data)[1][i])
            temp_board[19 - yAxis][xAxis] = 1
        return temp_board
        
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

    def rec_get_moves(self, first_block, queue_blocks, board, node_net, move_array, count, temp=[(0,0,0),(0,0,0)]):
        if count == 0:
            fit = self.get_fitness(board, node_net)
            if  fit > self.gfitness:
                self.gfitness = fit
                tmp = list(temp)
                # print(tmp)
                for i in range(len(tmp)):
                    move_array[i] = tmp[i]
        else:
            block = first_block if count == 4 else queue_blocks[3-count]
            heights = self.get_heights(board)
            r_range = 2 if sum(block[0]) == 2 else 4
            for r in range(r_range):
                cool_block = self.rotate(block, r)
                width = self.get_width(cool_block)
                for x in range(int(11 - width)):
                    if np.amax(heights[x:x + width]) > 18:
                        continue
                    new_board = self.get_new_board(x, cool_block, board)
                    tmp = list(temp)
                    tmp[2-count] = (r, -1, x)
                    self.rec_get_moves(first_block, queue_blocks, new_board, node_net, move_array, count - 1, tmp)
        
    def get_best_moves(self, queue, last_board, moving_block, node_net):
        # print(moving_block)
        heights = self.get_heights(last_board)
        queue_blocks = self.get_queue_blocks(queue)
        first_block = self.zero(moving_block)
        self.gfitness = -100000
        move_array = [(0,-1,0),(0,-1,0)]
        self.rec_get_moves(first_block, queue_blocks, last_board, node_net, move_array, 2)
        return move_array
