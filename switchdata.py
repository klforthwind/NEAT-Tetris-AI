from time import time
import numpy as np
import threading
import cv2

# --------------------------------------------------------------------

class SwitchData:

    # Initialize variables
    def __init__(self, src=0, width=1280, height=720):

        # Set capture settings
        self.src = src
        self.cap = cv2.VideoCapture(self.src, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()
        self.debug = time()

        # Set image processing variables
        self.arr = [16,16,26,15,15,26,15,15,26,15,15,26,14,14,26,14,14]
        self.arr2 = [0,16,32,58,73,88,114,129,144,170,185,200,226,240,254,280,294]
        self.__boardArr = np.zeros((20, 10))
        self.__queueArr = np.zeros((17, 4))
        self.__holdArr = np.zeros((2, 4))

    # Start the capture thread
    def start(self):
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    # Update the capture thread
    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    # Read locked thread
    def read(self):
        with self.read_lock:
            frame = self.frame
            grabbed = self.grabbed
        return grabbed, frame

    # Stop the thread from running
    def stop(self):
        self.started = False
        self.thread.join()
        cv2.destroyAllWindows()

# --------------------------------------------------------------------

    def printTime(self):
        print(time() - self.debug)
        self.debug = time()

# --------------------------------------------------------------------
    
    def processCapture(self):
        
        self.printTime()
        # Read the capture card
        _, frame = self.cap.read()

        self.printTime()
        # Show the capture card
        cv2.imshow('Frame', frame)
        print("Frmae awdojnai")
        self.printTime()
        # Process the board, hold, and queue
        self.__makeBoard(frame[40:680, 480:800])
        self.printTime()
        self.__makeHold(frame[80:120, 396:468])
        self.printTime()
        self.__makeQueue(frame[80:390, 815:880])
        print("End of QUeuee")
        self.printTime()

    def __makeBoard(self, frame):
        board = self.__handleCanvas(frame)

        # Attempt to make a less noisy mask
        boardMat = np.zeros((640, 320))
        #Run through all 200 grid tiles
        tempArr = np.zeros((20,10))
        for y in range(20):
            for x in range(10):
                # Get correct value of the indexed tiles
                val = 1 if board[32 * y + 4][32 * x + 4] > 0 and board[32 * y + 28][32 * x + 4] > 0 and board[32 * y + 4][32 * x + 28] > 0 and board[32 * y + 28][32 * x + 28] > 0 else 0
                tempArr[y][x] = val
                # Fill in the correct tiles
                for m in range(32):
                    if val == 0:
                        break
                    for n in range(32):
                        boardMat[y * 32 + m][x * 32 + n] = 255
                # Add dotted pattern
                if x != 9 and y != 19:
                    boardMat[(y + 1) * 32 - 1][(x + 1) * 32 - 1] = 1 
        # Show the board with opencv
        self.__boardArr = np.copy(tempArr)
        cv2.imshow('Board', boardMat)
        del tempArr
        del board

    def __makeHold(self, frame):
        hold = self.__handleCanvas(frame)

        # Check every hold tile to see if its filled
        tempArr = np.zeros((2, 4))
        for y in range(2):
            for x in range(4):
                tempArr[y][x] = 1 if hold[20 * y + 10][18 * x + 9] > 0 else 0
        self.__holdArr = np.copy(tempArr)
        del tempArr
        del hold

    def __makeQueue(self, frame):
        queue = self.__handleCanvas(frame)
        
        queueMat = np.zeros((310, 65))
        tempArr = np.zeros((17, 4))
        for i in range(17):
            # level = 0
            for j in range(4):
                if (i + 1) % 3 == 0:
                    continue
                val = 1 if queue[self.arr2[i] + 8][16 * j + 8] > 0 else 0
                tempArr[i][j] = val
                for m in range(self.arr[i]):
                    if val == 0:
                        break
                    for n in range(16):
                        queueMat[self.arr2[i] + m][j * 16 + n] = 255
        self.__queueArr = np.copy(tempArr)
        cv2.imshow('Queue', queueMat)
        del tempArr
        del queue

    def __handleCanvas(self, canvas):
        # Make a mat that only shows the canvas
        tempCanvas = canvas

        # Convert the queue to Hue Luminance and Saturation Mode
        tempCanvas = cv2.cvtColor(tempCanvas, cv2.COLOR_BGR2HLS)

        # Only get the luminant parts of the board
        return cv2.inRange(tempCanvas, np.array([0,54,0]), np.array([255,255,255]))

# --------------------------------------------------------------------

    # Returns heights of the board, height is relative from distance between bottom and heighest filled tile (0 is empty column)
    def getHeights(self, board):
        heights = np.zeros((10))
        # Iterate over all of the columns
        for x in range(len(heights)):
            maxH = 0
            # Iterate over the bottom 14 rows
            for y in range(14):
                # Get the correct index for the board array
                h = 6 + y
                if board[h][x] == 1:
                    # Set the height of column to the highest filled block (bottom = 0)
                    maxH = 13 - y
                    break
            # Save the height to the heights array
            heights[x] = maxH
        return heights

    # Get x and y values closest to 0 without breaking formation
    def zeroBlock(self, blockData):
        data = np.copy(blockData)
        lows = np.amin(data, axis=1)
        data[0] -= lows[0]
        data[1] -= lows[1]
        return data

    def leftMost(self, blockData):
        return np.amin(blockData[1])

    def rotate(self, blockData, rot):
        for r in range(rot):
            yTemp = blockData[0]
            blockData[0] = blockData[1]
            for r in range(len(blockData[0])):
                blockData[1][r] = 3 - yTemp[r]
        return self.zeroBlock(blockData), self.getWidth(blockData)

    def getWidth(self, blockData):
        return (np.amax(blockData[1]) - np.amin(blockData[1]) + 1)
    
    def analyzeQBlock(self, qBlock):
        newData = np.zeros((2, 4))
        foundBlocks = 0
        for j in range(2):
            for i in range(4):
                if qBlock[j][i] == 1:
                    newData[0][foundBlocks] = 1 - j
                    newData[1][foundBlocks] = i

                if foundBlocks == 4:
                        break
        return newData

# --------------------------------------------------------------------

    def getBestMoves(self, nodeNet):
        board, hold, queue = self.__boardArr, self.__holdArr, self.__queueArr
        heights = self.getHeights(board)
        qBlocks = self.getQueueBlocks()
        movingBlock = self.zeroBlock(self.getMovingBlock())
        fitness = -1
        blocks = np.zeros(())
        arr = np.zeros((1, 2, 4))
        arr[0] = movingBlock
        arr = np.append(arr, qBlocks)
        
        moves = self.iterateMoves(7, arr)
        for r1 in range(4):
            b1, width = self.rotate(np.copy(movingBlock), r1)
            for x1 in range(int(11 - width)):
                newBoard = self.getNewBoard(heights, x1, b1, width, board)
                for r2 in range(4):
                    b2, width2 = self.rotate(np.copy(self.analyzeQBlock(qBlocks[0])), r2)
                    for x2 in range(int(11 - width2)):
                        newBoard2 = self.getNewBoard(heights, x2, b2, width2, newBoard)
                        fit = self.getFitness(newBoard2, nodeNet)
                        if  fit > fitness:
                            fitness = fit
                            arr[0] = int(x1)
                            arr[1] = int(r1)
                            arr[2] = int(self.leftMost(movingBlock))
                        del newBoard2
                    del b2
                del newBoard
            del b1
        return arr
    
    def iterateMoves(self, count, arr):
        block = 
        if count > 0:
            for r in range(4):
                block, width = self.rotate(np.copy(block), r)
                for x in range(int(11 - width)):
                    newBoard = self.getNewBoard(heights, x, block, width, board)
        else:

    
# --------------------------------------------------------------------
    
    def getFitness(self, board, nodeNet):
        fitness = 0
        heights = self.getHeights(board)

        # Aggregate Height
        heightTotal = np.sum(heights)

        # Holes (not 100% correct, but will work)
        holes = heightTotal - np.sum(board)

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

    # Returns a 2x4 array containing data on the necessary block [yCoords][xCoords], inaccurate at the moment
    def getMovingBlock(self):
        # Make a copy of the tetris board
        board = self.__boardArr
        xyVals = np.zeros((2,4))
        foundBlocks = 0
        for y in range(15):
            for x in range(10):
                if board[y][x] == 1:
                    # Save the coords of the filled block as [distance from bottom] and [x]
                    xyVals[0][foundBlocks] = 19 - y
                    xyVals[1][foundBlocks] = x
                    foundBlocks += 1
                if foundBlocks == 4:
                    return xyVals
        return xyVals

    def getLowestBlocks(self, blockData, width):
        arr = np.zeros((int(width)))
        blockData = self.zeroBlock(blockData)
        high = np.amax(blockData[0])
        for l in range(int(width)):
            low = 20
            for i in range(len(blockData[0])):
                if blockData[1][i] == l:
                    if blockData[0][i] < low:
                        low = blockData[0][i]
            arr[l] = low
        return (arr, high)

# --------------------------------------------------------------------
    
    def getNewBoard(self, heights, x, b1, width, b):
        board = np.copy(b)
        lowTuple = self.getLowestBlocks(b1, width)
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
            yAxis = int(self.zeroBlock(b1)[0][i] - yOrigin + height)
            xAxis = int(x + self.zeroBlock(b1)[1][i])
            board[19 - yAxis][xAxis] = 1
        return np.copy(board)

# --------------------------------------------------------------------

    # Returns a list of blocks in the Queue
    def getQueueBlocks(self):
        row = 0
        blocks = np.zeros((6, 2, 4))
        for i in range(17):
            for j in range(4):
                if (i + 1) % 3 == 0:
                    break
                queueNum =int((row - (row % 2)) / 2)
                rowOfBlock = int(row % 2)
                blocks[queueNum][rowOfBlock][j] = self.__queueArr[i][j]
            if (i + 1) % 3 != 0:
                row += 1
        for i in range(6):
            blocks[i] = self.analyzeQBlock(blocks[i])
        return blocks
                
# --------------------------------------------------------------------  

    def isDead(self):
        return np.amin(self.__boardArr[5]) == 1 and np.amin(self.__boardArr[10]) == 1
    
    def shouldQuit(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def shouldPressA(self):
        return cv2.waitKey(1) & 0xFF == ord('a')

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()
