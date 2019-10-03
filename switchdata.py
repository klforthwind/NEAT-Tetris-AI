import numpy as np
from numpy import uint8 as uchar
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

        # Set image processing variables
        self.arr = [16,16,26,15,15,26,15,15,26,15,15,26,14,14,26,14,14]
        self.arr2 = [0,16,32,58,73,88,114,129,144,170,185,200,226,240,254,280,294]
        self.__boardArr = np.zeros((20, 10), dtype = uchar)
        self.__queueArr = np.zeros((17, 4), dtype = uchar)
        self.__holdArr = np.zeros((2, 4), dtype = uchar)
        self.clearLastBoard()

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
    
    # Make and display boardArr, holdArr, and queueArr
    def processCapture(self):
        
        # Read the capture card
        _, frame = self.cap.read()

        # Show the capture card
        cv2.imshow('Frame', frame)
        
        # Process the board, hold, and queue
        self.__makeBoard(frame[40:680, 480:800])
        self.__makeHold(frame[80:120, 396:468])
        self.__makeQueue(frame[80:390, 815:880])

    def __makeBoard(self, frame):
        board = self.__handleCanvas(frame)

        # Attempt to make a less noisy mask
        boardMat = np.zeros((640, 320), dtype = uchar)
        #Run through all 200 grid tiles
        tempArr = np.zeros((20,10), dtype = uchar)

        # Make a copy of the tetris board
        lBoard = self.lastBoard
        # Create an empty numpy array to add the locations of moving block to
        xyVals = np.zeros((2,0), dtype = uchar)

        for y in range(20):
            for x in range(10):
                # Get correct value of the indexed tiles
                val = 1
                valArr = [4, 16, 28]
                for i in valArr:
                    for j in valArr:
                        if board[32 * y + i][32 * x + j] == 0:
                            val = 0
                            break
                tempArr[y][x] = val

                colorVal = val * 255
                if val == 1 and lBoard[y][x] == 0: # Y = 0 refers to the top of the board
                    # Save the coords of the filled block as [distance from bottom] and [x]
                    xyVals = np.append(xyVals, [[19-y],[x]], 1)
                    colorVal = 128
                for m in range(32):
                    if val == 0:
                        break
                    for n in range(32):
                        boardMat[y * 32 + m][x * 32 + n] = colorVal
                # Add dotted pattern
                if x != 9 and y != 19:
                    boardMat[(y + 1) * 32 - 1][(x + 1) * 32 - 1] = 1
        
        self.movingBlock = np.copy(xyVals)
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
        
        queueMat = np.zeros((310, 65), dtype = uchar)
        tempArr = np.zeros((17, 4), dtype = uchar)
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

    def clearLastBoard(self):
        self.lastBoard = np.zeros((20, 10), dtype = uchar)
        self.lastQueue = np.zeros((17,4), dtype = uchar)
        self.nextBlock = np.zeros((2,4), dtype = uchar)
        self.movingBlock = np.zeros((2,4), dtype = uchar)

    # Make sure the block in hand doesnt show up on the board to plan things out
    def updateLastBoard(self):
        self.lastBoard = np.copy(self.__boardArr)
        for i in range(2):
            for j in range(4):
                if self.nextBlock[i][j] == 1 and self.lastBoard[i][j + 3] == 1:
                    self.lastBoard[i][j + 3] = 0

    # Returns if the block being used has been placed (queue changes)
    def didBlockChange(self):
        qChange = 0
        oldTileCount = np.sum(self.lastQueue)
        for i in range(17):
            for j in range(4):
                if i < 2:
                    self.nextBlock[i][j] = self.lastQueue[i][j]
                if (i + 1) % 3 == 0:
                    continue
                if self.__queueArr[i][j] != self.lastQueue[i][j]:
                    self.lastQueue[i][j] = self.__queueArr[i][j]
                    qChange += 1
        tileCount = np.sum(self.lastQueue)
        return qChange > 5 and tileCount > 20 and tileCount < 28 and oldTileCount > 20 and oldTileCount < 28

    # Returns heights of the board, height is relative from distance between bottom and heighest filled tile (0 is empty column)
    def getHeights(self, board):
        heights = np.argmax(board, axis=0)
        heights = np.where(heights == 0, heights, 20)
        return np.subtract(20, heights)

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

# --------------------------------------------------------------------

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

    # Determines if there is a piece that we can control
    def existsControllablePiece(self):
        return len(self.movingBlock[0]) == 4

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

    def getLowestBlocks(self, blockData, width):
        blockData = self.zero(blockData)
        maxx = np.amax(blockData[1])
        highest = np.amax(blockData[0])
        lowest = np.zeros((maxx))

        for i in range(maxx + 1):
            lowest[i] = highest
            for t in range(len(blockData[0])):
                if 


        arr = np.zeros((int(width)), dtype = uchar)
        
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
            yAxis = int(self.zero(b1)[0][i] - yOrigin + height)
            xAxis = int(x + self.zero(b1)[1][i])
            board[19 - yAxis][xAxis] = 1
        return np.copy(board)

# --------------------------------------------------------------------
                
# --------------------------------------------------------------------  

    def isDead(self):
        return np.amin(self.__boardArr[5]) == 1 and np.amin(self.__boardArr[10]) == 1
    
    def shouldQuit(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def shouldPressA(self):
        return cv2.waitKey(1) & 0xFF == ord('a')

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()
