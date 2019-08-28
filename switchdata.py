import numpy as np
import threading
import cv2

class SwitchData:

    # Initialize variables
    def __init__(self, src=0, width=1280, height=720):

        # Set capture settings
        self.src = src
        self.cap = cv2.VideoCapture(self.src, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.started = False

        # Set image processing variables
        self.arr = [16,16,26,15,15,26,15,15,26,15,15,26,14,14,26,14,14]
        self.arr2 = [0,16,32,58,73,88,114,129,144,170,185,200,226,240,254,280,294]
        self.__boardArr = np.zeros((20, 10))
        self.__queueArr = np.zeros((17, 4))
        self.__holdArr = np.zeros((2, 4))
        self.bestMoves = np.zeros((7))
        self.nodeNet = np.zeros((4))

    # Set a certain value on the capture
    def set(self, var1, var2):
        self.cap.set(var1, var2)

    # Start the capture thread
    def start(self):
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    # Update the capture thread
    def update(self):
        while self.started:
            
            # Read the capture card
            _, frame = self.cap.read()

            # Show the capture card
            cv2.imshow('Frame', frame)

            # Process the board, hold, and queue
            self.__makeBoard(frame)
            self.__makeHold(frame)
            self.__makeQueue(frame)

    # Stop the thread from running
    def stop(self):
        self.started = False
        self.thread.join()
        cv2.destroyAllWindows()

# --------------------------------------------------------------------
    
    def __makeBoard(self, frame):

        # Make a mat that only shows the board
        board = frame[40:680, 480:800]

        # Convert the board to Hue Luminance and Saturation Mode
        board = self.__hls(board)

        # Only get the luminant parts of the board
        board = self.__mask(board)

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
        cv2.imshow('Board', boardMat)
        self.__boardArr = tempArr
        del boardMat
        del tempArr
        del board

    def __makeHold(self, frame):
        # Make a mat that only shows the hold
        hold = frame[80:120, 396:468]

        # Convert the hold to Hue Luminance and Saturation Mode
        hold = self.__hls(hold)

        # Only get the luminant parts of the board
        hold = self.__mask(hold)

        # Check every hold tile to see if its filled
        tempArr = np.zeros((2, 4))
        for y in range(2):
            for x in range(4):
                tempArr[y][x] = 1 if hold[20 * y + 10][18 * x + 9] > 0 else 0
        self.__holdArr = tempArr
        del hold
        del tempArr

    def __makeQueue(self, frame):
        # Make a mat that only shows the queue
        queue = frame[80:390, 815:880]

        # Convert the queue to Hue Luminance and Saturation Mode
        queue = self.__hls(queue)

        # Only get the luminant parts of the board
        queue = self.__mask(queue)
        
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
        
        cv2.imshow('Queue', queueMat)
        self.__queueArr = tempArr
        del tempArr
        del queueMat
        del queue

    def __hls(self, mat):
        return cv2.cvtColor(mat, cv2.COLOR_BGR2HLS)

    def __mask(self, mat):
        return cv2.inRange(mat, np.array([0,54,0]), np.array([255,255,255]))

# --------------------------------------------------------------------

    def getHeights(self, board):
        heights = np.zeros((10))
        # Iterate over all of the columns
        for x in range(len(heights)):
            maxH = 0
            # Iterate over the bottom 15 rows
            for y in range(15):
                # Get the correct index for the board array
                h = 19 - y
                if board[h][x] == 1:
                    # Set the height of column to the highest filled block (bottom = 0)
                    maxH = y
            # Save the height to the heights array
            heights[x] = maxH
        return heights

    def pushTopLeft(self, blockData):
        left = 20
        top = 20
        for i in range(len(blockData[0])):
            if blockData[1][i] < left:
                left = blockData[1][i]
            if blockData[0][i] < top:
                top = blockData[0][i]
        for i in range(len(blockData[0])):
            blockData[0][i] -= top
            blockData[1][i] -= left
        return blockData

    def leftMost(self, blockData):
        left = 20
        for i in range(len(blockData[0])):
            if blockData[1][i] < left:
                left = blockData[1][i]
        return left 

    def rotate(self, blockData):
        yTemp = blockData[0]
        blockData[0] = blockData[1]
        for r in range(len(blockData[0])):
            blockData[1][r] = 3 - yTemp[r]
        return self.pushTopLeft(blockData)

    def getWidth(self, blockData):
        left = 20
        right = 0
        for i in range(len(blockData[1])):
            if blockData[1][i] < left:
                left = blockData[1][i]
            if blockData[1][i] > right:
                right = blockData[1][i]
        return right - left + 1

    def getBestMoves(self, nodeNet):
        board, hold, queue = self.__boardArr, self.__holdArr, self.__queueArr
        heights = self.getHeights(board)
        qBlocks = self.getQueueBlocks()
        blockData = self.getMovingBlock()
        left = self.leftMost(blockData)
        goodBoard = np.copy(board)
        fitness = -1
        arr = np.zeros((8))
        for r1 in range(4):
            b1 = blockData
            for r in range(r1 + 1):
                b1 = self.rotate(b1)
            width = self.getWidth(b1)
            for x1 in range(int(11 - width)):
                copyBoard = np.copy(board)
                newBoard = self.getNewBoard(heights, x1, b1, width, copyBoard)
                for r2 in range(4):
                    b2 = qBlocks[0]
                    for r in range(r2 + 1):
                        b2 = self.rotate(b2)
                    width2 = self.getWidth(b2)
                    for x2 in range(int(11 - width2)):
                        newBoard2 = self.getNewBoard(heights, x2, b2, width2, newBoard)
                        fit = self.getFitness(newBoard2, nodeNet)
                        if  fit > fitness:
                            goodBoard = newBoard2
                            fitness = fit
                            arr[0] = int(x1)
                            arr[1] = int(r1)
                            arr[2] = int(left)
                        del fit
                        del newBoard2
                    del b2
                del newBoard   
            del b1 
        return arr

    def getFitness(self, board, nodeNet):
        fitness = 0
        heightTotal = 0
        holes = 0
        bump = 0
        heights = self.getHeights(board)
        for i in range(len(heights)):
            # Aggregate Height
            heightTotal += heights[i]

            # Holes
            for j in range(int(heights[i])):
                if board[19-j][i] == 0:
                    holes += 1
            
            #Bumpiness
            if len(heights) > i + 2:
                bump += abs(heights[i] - heights[i + 1])

        fitness += nodeNet[0] * heightTotal
        fitness += nodeNet[1] * holes
        fitness += nodeNet[2] * bump

        # Complete Lines
        lines = 0
        for y in range(10):
            c = True
            for x in range(10):
                if board[19-y][x] == 0:
                    c = False
                    break
            if c:
                lines += 1 
        fitness += nodeNet[3] * lines

        return fitness

    def getMovingBlock(self):
        tempBoard = self.__boardArr
        xyVals = np.zeros((2,4))
        foundBlocks = 0
        for y in range(15):
            for x in range(10):
                if tempBoard[y][x] == 1:
                    xyVals[0][foundBlocks]=14 - y
                    xyVals[1][foundBlocks]=x
                    foundBlocks += 1
                if foundBlocks == 3:
                    return xyVals
        return xyVals

    def getLowestBlocks(self, blockData, width):
        arr = np.zeros((int(width)))
        lowest = 20
        leftMost = 10
        for i in range(len(blockData[0])):
            if blockData[0][i] < lowest:
                lowest = blockData[0][i]
            if blockData[1][i] < leftMost:
                leftMost = blockData[1][i]
        for i in range(len(blockData[0])):
            blockData[0][i] -= lowest
            blockData[1][i] -= leftMost
        for l in range(int(width)):
            low = 14
            for i in range(len(blockData[0])):
                if blockData[1][i] == l:
                    if blockData[0][i] < low:
                        low = blockData[0][i]
            arr[l] = low
        return arr
    
    def getNewBoard(self, heights, x, b1, width, board):
        lowestBlocks = self.getLowestBlocks(b1, width)
        high = 0
        yOrigin = 0
        for col in range(int(width)):
            val = heights[x + col] + lowestBlocks[col]
            if val > high:
                high = heights[x + col]
                yOrigin = lowestBlocks[col]
        for i in range(len(b1[0])):
            yAxis = int(b1[0][i] - yOrigin + high)
            xAxis = int(x + b1[1][i])
            board[yAxis][xAxis] = 1
        return board

    def getQueueBlocks(self):
        row = 0
        blocks = np.zeros((6, 2, 4))
        for i in range(17):
            for j in range(4):
                if (i + 1) % 3 == 0:
                    break
                queueNum =int((row - (row % 2)) / 2)
                rowOfBlock = int(row % 2)
                blocks[queueNum][rowOfBlock][j] = self.getQueuePos(i, j)
            if (i + 1) % 3 != 0:
                row += 1
        return blocks
                
# --------------------------------------------------------------------  

    def isDead(self):
        isDead = True
        for x in range(10):
            if self.getBoardPos(5, x) == 0:
                isDead = False
                break
            if self.getBoardPos(10, x) == 0:
                isDead = False
                break
        return isDead   

    def getBoard(self):
        return self.__boardArr            

    def getBoardPos(self, y, x):
        return self.__boardArr[int(y)][int(x)]

    def getQueuePos(self, y, x):
        return self.__queueArr[y][x]

    def getHoldPos(self, y, x):
        return self.__holdArr[y][x]
    
    def shouldQuit(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def shouldPressA(self):
        return cv2.waitKey(1) & 0xFF == ord('a')

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()
