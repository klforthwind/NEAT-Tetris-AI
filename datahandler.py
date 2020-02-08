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
        
    # def get_queue_blocks(self, queue):
    #     blocks = np.zeros((6, 2, 4), dtype = uint8)
    #     if np.sum(queue) == 24:
    #         for i in range(17):
    #             row = i % 3
    #             if row != 2:
    #                 for j in range(4):
    #                     block = int((i - row) / 3)
    #                     blocks[block][row][j] = queue[i][j]
    #         for board in range(6):
    #             blocks[board] = self.get_xy_vals(blocks[board])
    #     return blocks

    # def zero(self, block_data):
    #     data = np.copy(block_data)
    #     lows = np.amin(data, axis=1)
    #     data[0] -= lows[0]
    #     data[1] -= lows[1]
    #     return data
    
    # def get_lowest_blocks(self, xy_data):
    #     xy_zeroed = self.zero(xy_data)
    #     width = self.get_width(xy_zeroed)
    #     lowest = np.array([20]*(width), uint8)
        
    #     for i in range(min(len(xy_zeroed[0]),4)):
    #         x = xy_zeroed[1][i]
    #         y = xy_zeroed[0][i]
    #         lowest[x] = min(y, lowest[x])
    #     return lowest
        
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
        oldtile_count = sum(last_queue)
        for i in range(17):
            for j in range(4):
                if i % 3 != 2:
                    if i < 2:
                        next_block[i][j] = last_queue[i][j]
                        tmp_i = int(i - i//3)
                    if queue[j + tmp_i * 4] != last_queue[i][j]:
                        last_queue[i][j] = queue[j + tmp_i * 4]
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
                    tmp_i = int(i - i//3)
                    if queue[j + tmp_i * 4] == 1 and (j == 1 or j == 2):
                        middle_count += 1
        return (middle_count >= 12)
