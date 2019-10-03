from numpy import uint8
import numpy as np

class ImageHandler:

    #Initialize if needed
    # def __init__(self):

    # Returns heights of the board, height is relative from distance between bottom and heighest filled tile (0 is empty column)
    def getHeights(self, board):
        heights = np.argmax(board, axis=0)              
        heights = np.where(heights == 0, heights, 20)
        return np.subtract(20, heights)

    # Returns a list of blocks in the Queue
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
            blocks[b] = self.analyzeQBlock(blocks[b])   # Convert block data into xy value coordinates of data ([[0,1,1,0],[1,1,0,0]] becomes [[1,1,0,0],[1,2,0,1]])
        return np.copy(blocks)                          # Return a copy of the blocks

    # Get x and y values closest to 0 without breaking formation
    def zero(self, blockData):
        data = np.copy(blockData)
        lows = np.amin(data, axis=1)
        data[0] -= lows[0]
        data[1] -= lows[1]
        return data

    def rotate(self, blockData, rotationCount):
        tempData = np.copy(blockData)
        for r in range(rotationCount):
            yTemp = tempData[0]
            tempData[0] = tempData[1]
            for index in range(len(blockData[0])):
                tempData[1][index] = 3 - yTemp[index]
        return self.zero(tempData), self.getWidth(tempData)

    def getWidth(self, blockData):
        return (np.amax(blockData[1]) - np.amin(blockData[1]) + 1)
    
    def analyzeQBlock(self, qBlock):
        newData = np.nonzero(qBlock)
        newData[0] = np.subtract(1, newData[0])
        return newData