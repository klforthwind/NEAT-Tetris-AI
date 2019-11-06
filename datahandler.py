from numpy import uint8
import numpy as np

class DataHandler:

    def get_heights(self, board):
        heights = np.argmax(board, axis=0)
        heights = np.where(heights > 0, heights, 20)
        return np.subtract(20, heights)
    
    def get_xy_vals(self, block): 
        xyTuple = np.nonzero(block)
        xyTuple = (np.subtract(1, xyTuple[0]), xyTuple[1])
        return xyTuple
        
    def get_queue_blocks(self, queueArr):
        if np.sum(queueArr) == 24:
            blocks = np.zeros((6, 2, 4), dtype = uint8)
            for i in range(17):
                if i % 3 == 2:
                    continue
                for j in range(4):
                    row = i % 3
                    block = int((i - row) / 3)
                    blocks[block][row][j] = queueArr[i][j]
            for b in range(6):
                blocks[b] = self.get_xy_vals(blocks[b])
            return np.copy(blocks)
        else:
            return np.zeros((6, 2, 4), dtype = uint8)

    def zero(self, block_data):
        data = np.copy(block_data)
        lows = np.amin(data, axis=1)
        data[0] -= lows[0]
        data[1] -= lows[1]
        return data
    
    def get_lowest_blocks(self, block_data):
        block_data = self.zero(block_data)
        width = self.get_width(block_data)
        highest = np.amax(block_data[0])
        lowest = np.array([20]*(width), uint8)
        
        rangeee = (len(block_data[0]),4)[len(block_data[0]) > 4]
        for i in range(rangeee):
            x = block_data[1][i]
            y = block_data[0][i]
            if lowest[x] > y:
                lowest[x] = y
        lowest = np.subtract(highest, lowest)
        
        return lowest
        
    def get_width(self, block_data):
        rightMost = np.amax(block_data[1])
        leftMost = np.amin(block_data[1])
        return (rightMost - leftMost + 1)
        
    def rotate(self, block_data, rotationCount):
        tempData = self.zero(np.copy(block_data))
        for r in range(rotationCount):
            yTemp = list(tempData[0])
            tempData[0] = list(tempData[1])
            tempData[1] = list(np.subtract(3, yTemp))
        return self.zero(tempData)
        
    def did_block_change(self, last_queue, queue_array, next_block):
        queue_change = 0
        oldtile_count = np.sum(last_queue)
        for i in range(17):
            for j in range(4):
                if i < 2:
                    next_block[i][j] = last_queue[i][j]
                if (i + 1) % 3 == 0:
                    continue
                if queue_array[i][j] != last_queue[i][j]:
                    last_queue[i][j] = queue_array[i][j]
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
        
    def get_fitness(self, board, nodeNet):
        fitness = 0
        heights = self.get_heights(board)

        total_height = np.sum(heights)
        holes = total_height - (np.sum(board) - 4)
        
        bump = 0
        for i in range(len(heights)-1):
            bump += abs(heights[i] - heights[i + 1])
        
        lines = np.sum(np.amin(board, axis=1))
        fitness += nodeNet[0] * total_height
        fitness += nodeNet[1] * holes
        fitness += nodeNet[2] * bump
        fitness += nodeNet[3] * lines
        
        return fitness
        
    def get_next_best_move(self, thelist, queue, lBoard, movingBlock, nodeNet):
        heights = self.get_heights(lBoard)
        qBlocks = self._q(que_be)
        zeroed = self.zero(movingBlock)
        fitness = -1
        move = (0, 0, 0)
        
        newBoard = np.copy(lBoard)
        for item in range(len(thelist)):
            if item == 0:
                b1 = self.rotate(zeroed, thelist[item][1])
                width = self.get_width(b1)
                xval = thelist[item][0]
                if np.amax(heights[xval:xval + width]) > 16:
                    continue
                newBoard = self.get_new_board(xval, b1, newBoard)
            else:
                heights = self.get_heights(newBoard)
                b1 = self.rotate(qBlocks[item - 1], thelist[item][1])
                xval = thelist[item][0]
                if np.amax(heights[xval:xval + width]) > 16:
                    continue
                newBoard = self.get_new_board(xval, b1, newBoard)
        newBlock = qBlocks[len(thelist) - 1]
        heights = self.get_heights(newBoard)
        goodBoard = lBoard
        for r1 in range(4):
            b1 = self.rotate(newBlock, r1)
            width = self.get_width(b1)
            for x1 in range(int(11 - width)):
                if np.amax(heights[x1:x1 + width]) > 16:
                    continue
                theboard = self.get_new_board(x1, b1, newBoard)
                fit = self.get_fitness(theboard, nodeNet)
                if  fit > fitness:
                    fitness = fit
                    move = (r1, 0 ,x1)
                    goodBoard = np.copy(theboard)
        return move_array

    def getBestMoves(self, queue_array, lastBoard, movingBlock, nodeNet):
        heights = self.get_heights(lastBoard)
        qBlocks = self._q(qAr_b)
        firstBlock = self.zero(movingBlock)
        fitness = -10000
        move_array = []
        
        for r1 in range(4):
            b1 = self.rotate(firstBlock, r1)
            width = self.get_width(b1)
            for x1 in range(int(11 - width)):
                if np.amax(heights[x1:x1 + width]) > 16:
                    continue
                newBoard = self.get_new_board(x1, b1, lastBoard)
                newHeights = self.get_heights(newBoard)
                for r2 in range(4):
                    b2 = self.rotate(qBlocks[0], r2)
                    width2 = self.get_width(b2)
                    for x2 in range(int(11 - width2)):
                        if np.amax(newHeights[x2:x2 + width2]) > 16:
                            continue
                        newBoard2 = self.get_new_board(x2, b2, newBoard)
                        fit = self.get_fitness(newBoard2, nodeNet)
                        if  fit > fitness:
                            fitness = fit
                            move_array = []
                            tup1 = (r1, 0, x1)
                            move_array.append(tup1)
                            tup2 = (r2, 0, x2)
                            move_array.append(tup2)
        return move_array
