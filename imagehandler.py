from numpy import uint8
import numpy as np

class ImageHandler:

    #Initialize if needed
    # def __init__(self):

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