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

    def isDead(self):
        isDead = True
        for x in range(10):
            if self.getBoardValue(0, x) == 0:
                isDead = False
                break
            if self.getBoardValue(10, x) == 0:
                isDead = False
                break
        return isDead               

    def getBoardPos(self, y, x):
        return self.__boardArr[y][x]

    def getQueuePos(self, y, x):
        return self.__queueArr[y][x]

    def getHoldPos(self, y, x):
        return self.__holdArr[y][x]

    def getInputNodes(self):

        # Begin input nodes of neat
        inputNodes = np.array([])

        # Add every tile on the board to inputNodes
        for y in range(20):
            for x in range(10):
                filled = self.getBoardValue(y, x)
                inputNodes = np.append(inputNodes, filled)
        
        # Add the important queue value tiles to inputNodes
        for i in range(17):
            for j in range(4):
                if (i + 1) % 3 == 0:
                    continue
                inputNodes = np.append(inputNodes, self.getQueueValue(i, j))
        
        # Add the hold value tiles to inputNodes
        for y in range(2):
            for x in range(4):
                inputNodes = np.append(inputNodes, self.holdArr[y][x]
        
        return inputNodes
    
    def resetBoard(self):
        self.lastBoard = np.zeros((20, 10))

    def getHiddenNodes(self, newBlock):
        # Begin input nodes of neat
        hiddenNodes = np.array([])
        xPos = -5
        yPos = -5
        if self.lastBoard.size == 0:
            self.lastBoard = np.zeros((200))
        if newBlock:
            for y in range(20):
                for x in range(10):
                    isFilled = self.getBoardValue(y, x)
                    if y < 2 and self.lastBoard[y][x] == 0 and isFilled == 1:
                        if xPos == -5:
                            xPos = x
                            yPos = y
                    else:
                        self.lastBoard[y][x] = isFilled

        for y in range(20):
            for x in range(10):
                isFilled = self.getBoardValue(y, x)
                if xPos == -5 and isFilled:
                    if self.lastBoard[y][x]==0:
                        xPos = x
                        yPos = y
        
        # Test if there is blocks to the left and down
        if xPos > 1:
            for n in range(2):
                for m in range(4):
                    if yPos + m >= 20:
                        continue
                    else:
                        lastBoardEmpty = self.lastBoard[yPos + m][xPos - n - 1] == 0
                        if lastBoardEmpty and self.getBoardValue(yPos + m, xPos - n - 1) == 1:
                            xPos -= (n + 1)
                            continue
        elif xPos == 1:
            for m in range(4):
                if yPos + m >= 20:
                    continue
                else:
                    if self.lastBoard[yPos + m][xPos - 1] == 0 and self.getBoardValue(yPos + m, xPos - 1) == 1:
                        xPos -= 1
                        continue
                
        # Add X and Y as hidden nodes
        hiddenNodes = np.append(hiddenNodes, xPos)
        hiddenNodes = np.append(hiddenNodes, yPos)

        # Add 16 input nodes for the block being placed
        for m in range(4):
            for n in range(4):
                if yPos + m >= 19 or xPos + n >= 9:
                    hiddenNodes = np.append(hiddenNodes, 0)
                elif yPos + m < 2:
                    filled = self.getBoardValue(yPos + m , xPos + n )
                    hiddenNodes = np.append(hiddenNodes, filled)
                elif yPos + m > 1:
                    filled = self.getBoardValue(yPos + m, xPos + n)
                    if filled and self.lastBoard[yPos + m][xPos + n]==1:
                        hiddenNodes = np.append(hiddenNodes, filled)
                    else:
                        hiddenNodes = np.append(hiddenNodes, 0)
        
        return hiddenNodes

    def shouldQuit(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def shouldPressA(self):
        return cv2.waitKey(1) & 0xFF == ord('a')

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()