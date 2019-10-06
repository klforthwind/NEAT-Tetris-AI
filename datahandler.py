from numpy import uint8
import numpy as np

class DataHandler:

    #Initialize if needed
    # def __init__(self):

    # Returns heights of the board, height is relative from distance between bottom and heighest filled tile (0 is empty column)
    def getHeights(self, board):
        heights = np.argmax(board, axis=0)              # Get the highest filled tile in each column
        heights = np.where(heights > 0, heights, 20)    # Replace heights that are 0 with 20 (bottom of board)
        return np.subtract(20, heights)                 # Subtract each value from 20, to flip the board to get heights correctly
    
    # Turns a grid of isFilled and notFilled tiles into relative xy coordinates
    def getXYVals(self, block):
        xyTuple = np.nonzero(block)                     # Tuple in the form (yArr, xArr)
        xyTuple = (np.subtract(1, xyTuple[0]), xyTuple[1])# Flip data so top y is 1, bottom y = 0
        return xyTuple                                  # Return the tuple

    # Returns a list of blocks in the Queue (in XY form)
    def getQueueBlocks(self, queueArr):
        blocks = np.zeros((6, 2, 4), dtype = uint8)     # Create a 3d blocks array that holds 6 tetris blocks
        for i in range(17):                             # Iterate over all 17 rows in the queue mask (2 per block, 5 empty spaces in between)
            if i % 3 == 2:                              # Check to see if i is on an empty space in between blocks
                continue                                # Go to next row, so we won't handle bad row data
            for j in range(4):                          # Iterate all four tiles in a row
                row = i % 3                             # Get relative row of current block
                block = int((i - row) / 3)              # Get block index that we are working with
                blocks[block][row][j] = queueArr[i][j]  # Plug in the (isFilled) array of data values (no xy coords yet)
        for b in range(6):                              # Iterate over all 6 blocks in queue
            blocks[b] = self.getXYVals(blocks[b])       # Convert block data into xy value coordinates of data ([[0,1,1,0],[1,1,0,0]] becomes [[1,1,0,0],[1,2,0,1]])
        return np.copy(blocks)                          # Return a copy of the blocks

    # Get x and y values closest to 0 without breaking formation
    def zero(self, blockData):
        data = np.copy(blockData)                       # Take a copy of the array / list
        lows = np.amin(data, axis=1)                    # Get the smallest value in each subarray (lowest x and lowest y from respective arrays)
        data[0] -= lows[0]                              # Subtract the lowest y value from all y values
        data[1] -= lows[1]                              # Subtract the lowest x value from all x values
        return data                                     # Return 2d array touching x = 0 y = 0, but not necessarily (0,0)
    
    def getLowestBlocks(self, blockData):
        blockData = self.zero(blockData)                # Get x and y values closest to 0 without breaking formation
        width = np.amax(blockData[1])                   # Get the width of the block
        highest = np.amax(blockData[0])                 # Get the height minus 1 of the block
        lowest = np.zeros((width), uint8)               # Create an array with width items

        for i in range(len(blockData[0])):              # Iterate over the blockdata
            x = blockData[1][i]                         # Obtain the x at the blockData index
            y = blockData[0][i]                         # Obtain the y at the blockData index
            if lowest[val] < y:                         # See if the y value is lower than the lowest one at the specific index
                lowest[val] = y                         # Put y in the lowest at matching index if y is lower
        lowest = np.subtract(highest, lowest)           # Make the lower blocks have the higher value, and vice versa
        
        return (lowest, highest)                        # Return vals, height minus one
     
    def getWidth(self, blockData):
        rightMost = np.amax(blockData[1])               # Get the rightMost X value
        leftMost = np.amin(blockData[1])                # Get the leftMost X value
        return (rightMost - leftMost + 1)               # Width = right - left + 1

    def rotate(self, blockData, rotationCount):
        tempData = self.zero(np.copy(blockData))            # Create a copy of the blockData, zeroed
        for r in range(rotationCount):                      # Rotate it r times
            yTemp = list(tempData[0])                       # Create a temp of old y data
            tempData[0] = list(tempData[1])                 # Set the y data to the x data
            tempData[1] = list(np.subtract(3, yTemp))       # Set the x data to 3 minus the old y data
        return self.zero(tempData), self.getWidth(tempData) # Make sure the array is zeroed, and return the width
    
    # Returns if the block being used has been placed (queue changes)
    def didBlockChange(self, lastQ, qArr, nextBlock):
        qChange = 0                                                 # Keep track of queue changes
        oldTileCount = np.sum(lastQ)                                # Get the old queue tile count
        for i in range(17):                                         # Iterate over all of the rows
            for j in range(4):                                      # Iterate over all of the columns
                if i < 2:                                           # Make sure data we are reading is for the next block
                    nextBlock[i][j] = lastQ[i][j]                   # Update nextblock to place
                if (i + 1) % 3 == 0:                                # Check to see if this queue row is important
                    continue                                        # Skip if queue row is not important
                if qArr[i][j] != lastQ[i][j]:                       # Check to see if new queue tile matches old queue tile
                    lastQ[i][j] = qArr[i][j]                        # Update old queue to match new queue
                    qChange += 1                                    # Increment when the old queue is not the same as the new queue
        tileCount = np.sum(lastQ)                                   # Get the new queue tile count
        return (qChange > 5 and                                     # Return true if we have moved onto the next block
            22 < tileCount < 26 and
            22 < oldTileCount < 26)

    def getNextBestMove(self, thelist, nodeNet):
        board, hold, queue, lBoard = self.__boardArr, self.__holdArr, self.__queueArr, self.lastBoard
        heights = self.getHeights(lBoard)
        qBlocks = self.getQueueBlocks()
        zeroed = self.zero(self.movingBlock)
        fitness = -1
        move = (0, 0)

        theboard = np.copy(lBoard)
        for item in range(len(thelist)):
            if item == 0:
                b1, width = self.rotate(zeroed, thelist[item][1])
                xval = thelist[item][0]
                if np.amax(heights[xval:xval + width]) > 16:
                    continue
                theboard = self.getNewBoard(heights, xval, b1, width, theboard)
            else:
                heights = self.getHeights(theboard)
                b1, width = self.rotate(self.analyzeQBlock(qBlocks[item - 1]), thelist[item][1])
                xval = thelist[item][0]
                if np.amax(heights[xval:xval + width]) > 16:
                    continue
                theboard = self.getNewBoard(heights, xval, b1, width, theboard)
        newBlock = qBlocks[len(thelist) - 1]
        heights = self.getHeights(theboard)
        for r1 in range(4):
            b1, width = self.rotate(self.analyzeQBlock(newBlock), r1)
            for x1 in range(int(11 - width)):
                if np.amax(heights[x1:x1 + width]) > 16:
                    continue
                theboard = self.getNewBoard(heights, x1, b1, width, theboard)
                fit = self.getFitness(theboard, nodeNet)
                if  fit >= fitness:
                    fitness = fit
                    move = (r1, 0 ,x1)
                    print(theboard)
        return move

    # Returns initial good placements
    def getBestMoves(self, nodeNet):
        board, hold, queue, lBoard = self.__boardArr, self.__holdArr, self.__queueArr, self.lastBoard
        heights = self.getHeights(lBoard)
        qBlocks = self.getQueueBlocks()
        firstBlock = self.zero(self.movingBlock)
        fitness = -1
        moveArr = []
        
        for r1 in range(4):
            b1, width = self.rotate(firstBlock, r1)
            for x1 in range(int(11 - width)):
                if np.amax(heights[x1:x1 + width]) > 16:
                    continue
                newBoard = self.getNewBoard(heights, x1, b1, width, lBoard)
                newHeights = self.getHeights(newBoard)
                for r2 in range(4):
                    b2, width2 = self.rotate(self.analyzeQBlock(qBlocks[0]), r2)
                    for x2 in range(int(11 - width2)):
                        if np.amax(heights[x2:x2 + width]) > 16:
	                        continue
                        newBoard2 = self.getNewBoard(newHeights, x2, b2, width2, newBoard)
                        fit = self.getFitness(newBoard2, nodeNet)
                        if  fit >= fitness:
                            fitness = fit
                            arr = []
                            tup1 = (r1, 0, x1)
                            arr.append(tup1)
                            tup2 = (r2, 0, x2)
                            arr.append(tup2)
                        del newBoard2
                    del b2
                del newBoard
            del b1
        return arr


    # --------------------------------------------------------------------
    
    def getFitness(self, board, nodeNet):
        fitness = 0
        heights = self.getHeights(board)

        # Aggregate Height
        heightTotal = np.sum(heights)

        # Holes (not 100% correct, but will work)
        sumOfBoard = np.sum(board) - 4
        holes = 0
        if heightTotal - sumOfBoard >= 0:
            holes = heightTotal - sumOfBoard

        bump = 0
        # Bumpiness
        for i in range(len(heights)-1):
            bump += abs(heights[i] - heights[i + 1])

        fitness += nodeNet[0] * heightTotal
        fitness += nodeNet[1] * holes
        fitness += nodeNet[2] * bump

        # Complete Lines
        lines = np.sum(np.amin(board, axis=1))
        fitness += nodeNet[3] * lines

        return fitness


# --------------------------------------------------------------------
    
    def getNewBoard(self, heights, x, b1, width, b):
        board = np.copy(b)
        lowTuple = self.getLowestBlocks(b1)
        lowestBlocks = lowTuple[0]
        highBoi = lowTuple[1]
        high = 0
        height = 0
        yOrigin = 0
        for col in range(int(width)):
            val = heights[x + col] + (highBoi - lowestBlocks[col])
            if val > high:
                high = val
                height = heights[x + col]
                yOrigin = lowestBlocks[col]
        for i in range(len(b1[0])):
            yAxis = int(self.zero(b1)[0][i] - yOrigin + height)
            xAxis = int(x + self.zero(b1)[1][i])
            board[19 - yAxis][xAxis] = 1
        return np.copy(board)