from numpy import uint8
import numpy as np

class DataHandler:

    def getHeights(self, board):
        heights = np.argmax(board, axis=0)
        heights = np.where(heights > 0, heights, 20)
        return np.subtract(20, heights)
    
    def getXYVals(self, block): 
        xyTuple = np.nonzero(block)
        xyTuple = (np.subtract(1, xyTuple[0]), xyTuple[1])
        return xyTuple
        
    def getQueueBlocks(self, queueArr):
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
                blocks[b] = self.getXYVals(blocks[b])
            return np.copy(blocks)
        else:
            return np.zeros((6, 2, 4), dtype = uint8)

    def zero(self, blockData):
        data = np.copy(blockData)
        lows = np.amin(data, axis=1)
        data[0] -= lows[0]
        data[1] -= lows[1]
        return data
    
    def getLowestBlocks(self, blockData):
        blockData = self.zero(blockData)
        width = self.getWidth(blockData)
        highest = np.amax(blockData[0])
        lowest = np.array([20]*(width), uint8)
        
        rangeee = 4 if len(blockData[0]) > 4 else len(blockData[0])
        for i in range(rangeee):
            x = blockData[1][i]
            y = blockData[0][i]
            if lowest[x] > y:
                lowest[x] = y
        lowest = np.subtract(highest, lowest)
        
        return lowest
        
    def getWidth(self, blockData):
        rightMost = np.amax(blockData[1])
        leftMost = np.amin(blockData[1])
        return (rightMost - leftMost + 1)
        
    def rotate(self, blockData, rotationCount):
        tempData = self.zero(np.copy(blockData))
        for r in range(rotationCount):
            yTemp = list(tempData[0])
            tempData[0] = list(tempData[1])
            tempData[1] = list(np.subtract(3, yTemp))
        return self.zero(tempData)
        
    def didBlockChange(self, lastQ, qArr, nextBlock):
        qChange = 0
        oldTileCount = np.sum(lastQ)
        for i in range(17):
            for j in range(4):
                if i < 2:
                    nextBlock[i][j] = lastQ[i][j]
                if (i + 1) % 3 == 0:
                    continue
                if qArr[i][j] != lastQ[i][j]:
                    lastQ[i][j] = qArr[i][j]
                    qChange += 1
        tileCount = np.sum(lastQ)
        return (qChange > 5 and
            22 < tileCount < 26 and
            22 < oldTileCount < 26)
    
    def getNewBoard(self, xVal, block, b):
        blockData = self.zero(np.copy(block))
        highest = np.amax(blockData[0])
        heights = self.getHeights(b)
        board = np.copy(b)
        lowestBlock = self.getLowestBlocks(blockData)
        high, height = 0, 0
        for col in range(int(len(lowestBlock))):
            val = heights[xVal + col] + lowestBlock[col]
            if val > high:
                high = val
                height = heights[xVal + col] - (highest - lowestBlock[col])
        for i in range(len(blockData[0])):
            yAxis = int(blockData[0][i] + height)
            xAxis = int(xVal + self.zero(blockData)[1][i])
            board[19 - yAxis][xAxis] = 1
        return np.copy(board)
        
    def getFitness(self, board, nodeNet):
        fitness = 0
        heights = self.getHeights(board)

        totalHeight = np.sum(heights)
        holes = totalHeight - (np.sum(board) - 4)
        
        bump = 0
        for i in range(len(heights)-1):
            bump += abs(heights[i] - heights[i + 1])
        
        lines = np.sum(np.amin(board, axis=1))
        fitness += nodeNet[0] * totalHeight
        fitness += nodeNet[1] * holes
        fitness += nodeNet[2] * bump
        fitness += nodeNet[3] * lines
        
        return fitness
        
    def getNextBestMove(self, thelist, queue, lBoard, movingBlock, nodeNet):
        heights = self.getHeights(lBoard)
        qBlocks = self.getQueueBlocks(queue)
        zeroed = self.zero(movingBlock)
        fitness = -1
        move = (0, 0, 0)
        
        newBoard = np.copy(lBoard)
        for item in range(len(thelist)):
            if item == 0:
                b1 = self.rotate(zeroed, thelist[item][1])
                width = self.getWidth(b1)
                xval = thelist[item][0]
                if np.amax(heights[xval:xval + width]) > 16:
                    continue
                newBoard = self.getNewBoard(xval, b1, newBoard)
            else:
                heights = self.getHeights(newBoard)
                b1 = self.rotate(qBlocks[item - 1], thelist[item][1])
                xval = thelist[item][0]
                if np.amax(heights[xval:xval + width]) > 16:
                    continue
                newBoard = self.getNewBoard(xval, b1, newBoard)
        newBlock = qBlocks[len(thelist) - 1]
        heights = self.getHeights(newBoard)
        goodBoard = lBoard
        for r1 in range(4):
            b1 = self.rotate(newBlock, r1)
            width = self.getWidth(b1)
            for x1 in range(int(11 - width)):
                if np.amax(heights[x1:x1 + width]) > 16:
                    continue
                theboard = self.getNewBoard(x1, b1, newBoard)
                fit = self.getFitness(theboard, nodeNet)
                if  fit > fitness:
                    fitness = fit
                    move = (r1, 0 ,x1)
                    goodBoard = np.copy(theboard)
        # for i in range(20):
        #     for j in range(10):
        #         val = ". " if goodBoard[i][j] == 0 else "X "
        #         print(val, end="")
        #     print("")
        return moveArr

    def getBestMoves(self, qArr, lastBoard, movingBlock, nodeNet):
        heights = self.getHeights(lastBoard)
        qBlocks = self.getQueueBlocks(qArr)
        firstBlock = self.zero(movingBlock)
        fitness = -10000
        moveArr = []
        
        for r1 in range(4):
            b1 = self.rotate(firstBlock, r1)
            width = self.getWidth(b1)
            for x1 in range(int(11 - width)):
                if np.amax(heights[x1:x1 + width]) > 16:
                    continue
                newBoard = self.getNewBoard(x1, b1, lastBoard)
                newHeights = self.getHeights(newBoard)
                for r2 in range(4):
                    b2 = self.rotate(qBlocks[0], r2)
                    width2 = self.getWidth(b2)
                    for x2 in range(int(11 - width2)):
                        if np.amax(newHeights[x2:x2 + width2]) > 16:
                            continue
                        newBoard2 = self.getNewBoard(x2, b2, newBoard)
                        fit = self.getFitness(newBoard2, nodeNet)
                        if  fit > fitness:
                            fitness = fit
                            moveArr = []
                            tup1 = (r1, 0, x1)
                            moveArr.append(tup1)
                            tup2 = (r2, 0, x2)
                            moveArr.append(tup2)
        return moveArr
