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
        width = self.getWidth(blockData)                # Get the width of the block
        highest = np.amax(blockData[0])                 # Get the height minus 1 of the block
        lowest = np.array([20]*(width), uint8)          # Create an array with width items

        for i in range(len(blockData[0])):              # Iterate over the blockdata
            x = blockData[1][i]                         # Obtain the x at the blockData index
            y = blockData[0][i]                         # Obtain the y at the blockData index
            if lowest[x] > y:                           # See if the y value is lower than the lowest one at the specific index
                lowest[x] = y                           # Put y in the lowest at matching index if y is lower
        lowest = np.subtract(highest, lowest)           # Make the lower blocks have the higher value, and vice versa
        
        return lowest                                   # Return lowest vals
     
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
        return self.zero(tempData)                          # Make sure the array is zeroed, and return the width
    
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
    
    def getNewBoard(self, xVal, block, b):
        blockData = self.zero(np.copy(block))                       # Zero blockData
        highest = np.amax(blockData[0])
        heights = self.getHeights(b)                                # Get the heights of the board
        board = np.copy(b)                                          # Create a copy of the board
        lowestBlock = self.getLowestBlocks(blockData)               # Get the lowest blocks as an inverted value
        high, height, yOrigin = 0, 0, 0                             # Initialize some variable to utilize
        for col in range(int(len(lowestBlock))):                    # Iterate over the width of the block
            val = heights[xVal + col] + lowestBlock[col]            # Determine the significance of the column
            if val > high:                                          # Check to see if this column is limiting factor in placement
                high = val                                          # Set high to this value of importance
                height = heights[xVal + col]                        # Keep track of the height of placement
                yOrigin = highest - lowestBlock[col]                # Set yorigin to lowest Block
        for i in range(len(blockData[0])):                          # Iterate over the block data
            yAxis = int(blockData[0][i] - yOrigin + height)         # Calculate the y value of tile in block
            xAxis = int(xVal + self.zero(blockData)[1][i])          # Calculate the x value of specific tile in block
            board[19 - yAxis][xAxis] = 1                            # Update the board
        return np.copy(board)                                       # Return a copy of this board

    # Get fitness of a specific board
    def getFitness(self, board, nodeNet):
        fitness = 0                                 # Start fitness at 0
        heights = self.getHeights(board)            # Get array of heights

        totalHeight = np.sum(heights)               # Aggregate Height
        holes = totalHeight - (np.sum(board) - 4)   # Holes

        bump = 0                                    # Bumpiness
        for i in range(len(heights)-1):
            bump += abs(heights[i] - heights[i + 1])
        
        lines = np.sum(np.amin(board, axis=1))      # Complete Lines

        fitness += nodeNet[0] * totalHeight         # Aggregate Height
        fitness += nodeNet[1] * holes               # Holes
        fitness += nodeNet[2] * bump                # Bumpiness
        fitness += nodeNet[3] * lines               # Complete Lines

        return fitness                              # Return total fitness

    def getNextBestMove(self, thelist, board, queue, lBoard, nodeNet):
        heights = self.getHeights(lBoard)                               # Get the heights of the board without the moving block
        qBlocks = self.getQueueBlocks()                                 # Get the queue blocks to handle
        zeroed = self.zero(self.movingBlock)                            # Get the zeroed moving block
        fitness = -1                                                    # Start fitness at -1
        move = (0, 0, 0)                                                # Create a move tracker?

        newBoard = np.copy(lBoard)                                      # Take a copy of lastBoard
        for item in range(len(thelist)):                                # Iterate over items in list
            if item == 0:                                               # Check to see if the item is the moving block
                b1 = self.rotate(zeroed, thelist[item][1])              # Rotate the block
                width = self.getWidth(b1)                               # Get the width of the block
                xval = thelist[item][0]                                 # Get the correct xvalue of the block placement
                if np.amax(heights[xval:xval + width]) > 16:            # See if the heights of the columns being placed on is too high
                    continue                                            # Continue if we should not place on those columns
                newBoard = self.getNewBoard(xval, b1, newBoard)         # Create a new board using the moving block
            else:                                                       # Iterate over the queue blocks
                heights = self.getHeights(theboard)                     # Get the heights of the new board
                b1 = self.rotate(self.getXYVals(qBlocks[item - 1]), thelist[item][1]) # Rotate the block
                xval = thelist[item][0]                                 # Get the correct xvalue of the block placement
                if np.amax(heights[xval:xval + width]) > 16:            # See if the heights of the columns being placed on is too high
                    continue                                            # Continue if we should not place on those columns
                newBoard = self.getNewBoard(xval, b1, newBoard)         # Update the newboard using a specific queue block
        newBlock = qBlocks[len(thelist) - 1]                            # Get the next queueblock in list
        heights = self.getHeights(newBoard)                             # Get the heights of the new bloard
        for r1 in range(4):
            b1, width = self.rotate(self.getXYVals(newBlock), r1)
            for x1 in range(int(11 - width)):
                if np.amax(heights[x1:x1 + width]) > 16:                # See if the heights of the columns being placed on is too high
                    continue                                            # Continue if we should not place on those columns
                theboard = self.getNewBoard(x1, b1, newBoard)           # Create a different board in order to find the fitness of it
                fit = self.getFitness(theboard, nodeNet)                # Get the fitness of this specific board
                if  fit >= fitness:                                     # Check to see if fitness beats best fitness
                    fitness = fit                                       # Set best fitness to this fitness if so
                    move = (r1, 0 ,x1)                                  # Set the preferred move to what we just did
        return move                                                     # Return the best move

    # Returns initial good placements
    def getBestMoves(self, boardArr, qArr, lastBoard, movingBlock, nodeNet):
        heights = self.getHeights(lastBoard)                                # Get the heights of the board without the moving block
        qBlocks = self.getQueueBlocks(qArr)                                 # Get the queue blocks
        firstBlock = self.zero(movingBlock)                                 # Zero the moving block
        fitness = -1                                                        # Set fitness to its initial value
        moveArr = []                                                        # Initialize a list of moves
        
        for r1 in range(4):                                                 # Iterate over all rotations
            b1 = self.rotate(firstBlock, r1)                                # Rotate the block r1 times
            width = self.getWidth(b1)                                       # Get the width of the block
            for x1 in range(int(11 - width)):                               # Iterate over all columns, skipping the right (width - 1) many (to not overflow)
                if np.amax(heights[x1:x1 + width]) > 16:                    # See if the heights of the columns being placed on is too high
                    continue                                                # Continue if we should not place on those columns
                newBoard = self.getNewBoard(x1, b1, lBoard)                 # Create the newBoard
                newHeights = self.getHeights(newBoard)                      # Get the new heights of the board
                for r2 in range(4):                                         # Iterate over all rotations
                    b2 = self.rotate(self.getXYVals(qBlocks[0]), r2)        # Rotate the block r2 times
                    width2 = self.getWidth(b2)                              # Get the width of the block
                    for x2 in range(int(11 - width2)):                      # Iterate over all columns, skipping the right (width - 1) many (to not overflow)
                        if np.amax(newHeights[x2:x2 + width2]) > 16:        # See if the heights of the columns being placed on is too high
	                        continue                                        # Continue if we should not place on those columns
                        newBoard2 = self.getNewBoard(x2, b2, newBoard)      # Create a new newboard
                        fit = self.getFitness(newBoard2, nodeNet)           # Get the fitness of said new board
                        if  fit >= fitness:                                 # Check to see if this fitness beats the best fitness
                            fitness = fit                                   # Set the best fitness to this fitness
                            moveArr = []                                    # Make moveArr empty
                            tup1 = (r1, 0, x1)                              # Create a tuple for the first move representing required actions
                            arr.append(tup1)                                # Append said tuple to the move array
                            tup2 = (r2, 0, x2)                              # Create a tuple for the second move representing required actions
                            arr.append(tup2)                                # Append said tuple to the move array
                        del newBoard2                                       # Delete newBoard2 since we wont need it
                    del b2                                                  # Delete block 2 since we won't need it
                del newBoard                                                # Delete newBoard since we won't need it
            del b1                                                          # Delete block 1 since we won't need it
        return moveArr                                                      # Return the moveArr with good moves to run
