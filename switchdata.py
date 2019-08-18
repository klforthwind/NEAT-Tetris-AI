import numpy as np
import threading
import cv2

class SwitchData:
    def __init__(self, src=0, width=1280, height=720):
        self.src = src
        self.cap = cv2.VideoCapture(self.src, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()
        self.lastBoard = np.zeros((20, 10))
        self.arr = [16,16,26,15,15,26,15,15,26,15,15,26,14,14,26,14,14]
        self.arr2 = [0,16,32,58,73,88,114,129,144,170,185,200,226,240,254,280,294]
        self.__boardArr = np.zeros((20, 10))
        self.__queueArr = np.zeros((17, 4))
        self.__holdArr = np.zeros((2, 4))
        self.bestMoves = np.zeros((100, 6))

    def set(self, var1, var2):
        self.cap.set(var1, var2)

    def start(self):
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.read_lock:
            frame = self.frame
            grabbed = self.grabbed
        return grabbed, frame

    def stop(self):
        self.started = False
        self.thread.join()
        cv2.destroyAllWindows()

# --------------------------------------------------------------------
    
    # Process the capture card
    def processCapture(self):
        # Read the capture card
        _, frame = self.read()

        # Show the capture card
        cv2.imshow('Frame', frame)

        # Process the board, hold, and queue
        self.__makeBoard(frame)
        self.__makeHold(frame)
        self.__makeQueue(frame)

    def __makeBoard(self, frame):
        # Make a mat that only shows the board
        board = frame[40:680, 480:800]

        # Convert the board to Hue Luminance and Saturation Mode
        board = self.__hls(board)

        # Only get the luminant parts of the board
        board = self.__mask(board)

        # Attempt to apply 
        boardMat = np.zeros((640, 320))
        for y in range(20):
            for x in range(10):
                val = 1 if board[32 * y + 4][32 * x + 4] > 0 and board[32 * y + 28][32 * x + 4] > 0 and 
                    board[32 * y + 4][32 * x + 28] > 0 and board[32 * y + 28][32 * x + 28] > 0 else 0
                self.__boardArr[y][x] = val
                for m in range(32):
                    if val == 0:
                        break
                    for n in range(32):
                        boardMat[y * 32 + m][x * 32 + n] = 255
                if x != 9 and y != 19:
                    boardMat[(y + 1) * 32 - 1][(x + 1) * 32 - 1] = 1 
        cv2.imshow('Board', boardMat)

    def __makeHold(self, frame):
        # Make a mat that only shows the hold
        hold = frame[80:120, 396:468]

        # Convert the hold to Hue Luminance and Saturation Mode
        hold = self.__hls(hold)

        # Only get the luminant parts of the board
        hold = self.__mask(hold)

        for y in range(2):
            for x in range(4):
                self.__holdArr[y][x] = 1 if hold[20 * y + 10][18 * x + 9] > 0 else 0

    def __makeQueue(self, frame):
        # Make a mat that only shows the queue
        queue = frame[80:390, 815:880]

        # Convert the queue to Hue Luminance and Saturation Mode
        queue = self.__hls(queue)

        # Only get the luminant parts of the board
        queue = self.__mask(queue)
        
        queueMat = np.zeros((310, 65))
        for i in range(17):
            # level = 0
            for j in range(4):
                if (i + 1) % 3 == 0:
                    continue
                val = 1 if queue[self.arr2[y] + 8][16 * x + 8] > 0 else 0
                self.__queueArr[i][j] = val
                for m in range(self.arr[y]):
                    if val == 0:
                        break
                    for n in range(16):
                        queueMat[self.arr2[y] + m][x * 16 + n] = 255
        
        cv2.imshow('Queue', queueMat)

    def __hls(self, mat):
        return cv2.cvtColor(mat, cv2.COLOR_BGR2HLS)

    def __mask(self, mat):
        return cv2.inRange(mat, np.array([0,54,0]), np.array([255,255,255]))

# --------------------------------------------------------------------

    def getHeights(self):
        h = 0
        for y in range(20):
            oneOnThisLevel = False
            for x in range(10):
                if self.getBoardPos(19 - y, x) == 1:
                    oneOnThisLevel = True
                    continue
            if oneOnThisLevel == False:
                h = y + 1
                break
        heights = np.zeros((10))
        for x in range(10):
            high = 0
            for y in range(h):
                high = y if self.getBoardPos(19 - y, x) == 1
            heights[x] = high
        return heights

    def getBestMoves(self, nodeNet):
        heights = self.getHeights()
        blocks = self.getQueueBlocks()
        blockBeingPlaced = self.getMovingBlock()
        for r1 in range(4):
            b1 = blocks[0]
            b1 = self.rotate(b1, r1)
            for x in range(10 - len(b1[0])):
                newBoard = self.__boardArr
                newBoard = self.getNewBoard(heights, x, b1, newBoard)
                for r2 in range(4):
                    b2 = blocks[1]
                    b2 = self.rotate(b1, r2)
                    for x in range(10 - len(b2[0])):
                        newBoard = self.getNewBoard(heights, x, b2, newBoard)

    def getMovingBlock(self):
        current = np.zeros((4,6))
        xx = -1
        yy = -1
        for y in range(10):
            for x in range(10):
                if xx == -1 and self.__boardArr[y][x] == 1:
                    xx = x
                    yy = y
                current[y - yy][x - xx + 2] = self.__boardArr[y][x]
        for y in range(4):
            for x in range(3):

    def getNewBoard(self, heights, x, b1, board):
        maxHeight = 0
        for l in range(len(b1[0])):
            maxHeight = heights[x+l] if maxHeight < heights[x+l]
        for y in range(maxHeights + 1):
            if len(b1) == 4:
                if self.checkVertical(b1, maxHeights - y, x):
                    for j in range(4):
                        for i in range(2):
                            if block[3-j][i] == 1:
                            board[maxHeights - (y + j)][x + i] = 1
                    break
            else:
                if self.checkHorizontal(b1, maxHeights - y, x):
                    for j in range(2):
                        for i in range(4):
                            if block[3-j][i] == 1:
                            board[maxHeights - (y + j)][x + i] = 1
                    break
        return board
    
    def checkVertical(self, block, y, x):
        for j in range(4):
            for i in range(2):
                if block[j][i] == 1 and self.getBoardPos(19 - (y + j), x + i) == 1:
                    return False
        for j in range(4):
            for i in range(2):
                if block[3-j][i] == 1 and (y == 0 or self.getBoardPos(19 - (y + j) + 1, x + i) == 1):
                    return True
        return False


    def checkHorizontal(self, y, x):
        for j in range(2):
            for i in range(4):
                if block[j][i] == 1 and self.getBoardPos(y + j, x + i) == 1:
                    return False
        for j in range(2):
            for i in range(4):
                if block[1-j][i] == 1 and (y == 0 or self.getBoardPos(19 - (y + j) + 1, x + i) == 1):
                    return True
        return False

    def rotate(self, block, counterRotations):
        return np.rot90(block, counterRotations)

    def getQueueBlocks(self):
        row = 0
        blocks = np.zeros((6, 2, 4))
        for i in range(17):
            for j in range(4):
                if (i + 1) % 3 == 0:
                    continue
                blocks[(row - (row % 2)) / 2][row % 2][j] = self.getQueuePos(i, j)
                row += 1
        return blocks
                
# --------------------------------------------------------------------  

    def isDead(self):
        isDead = True
        for x in range(10):
            if self.getBoardPos(0, x) == 0:
                isDead = False
                break
            if self.getBoardPos(10, x) == 0:
                isDead = False
                break
        return isDead               

    def getBoardPos(self, y, x):
        return self.__boardArr[y][x]

    def getQueuePos(self, y, x):
        return self.__queueArr[y][x]

    def getHoldPos(self, y, x):
        return self.__holdArr[y][x]
    
    def resetBoard(self):
        self.lastBoard = np.zeros((20, 10))

    def shouldQuit(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def shouldPressA(self):
        return cv2.waitKey(1) & 0xFF == ord('a')

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()