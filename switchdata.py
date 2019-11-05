from numpy import uint8
from datahandler import DataHandler
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

        self.arr = [16,16,26,15,15,26,15,15,26,15,15,26,14,14,26,14,14]
        self.arr2 = [0,16,32,58,73,88,114,129,144,170,185,200,226,240,254,280,294]
        self.__boardArr = np.zeros((20, 10), dtype = uint8)
        self.__queueArr = np.zeros((17, 4), dtype = uint8)
        self.__holdArr = np.zeros((2, 4), dtype = uint8)
        self.dh = DataHandler()
        self.clearLastBoard()

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
    
    def processCapture(self):
        _, frame = self.cap.read()
        cv2.imshow('Frame', frame)
        
        self.__makeBoard(frame[40:680, 480:800])
        self.__makeHold(frame[80:120, 396:468])
        self.__makeQueue(frame[80:390, 815:880])
        
    def __makeBoard(self, frame):
        board = self.__handleCanvas(frame)
        boardMat = np.zeros((640, 320), dtype = uint8)
        tempArr = np.zeros((20,10), dtype = uint8)
        lBoard = self.lastBoard
        xyVals = np.zeros((2,0), dtype = uint8)
        
        for y in range(20):
            for x in range(10):
                val = 1
                valArr = [4, 16, 28]
                for i in valArr:
                    for j in valArr:
                        if board[32 * y + i][32 * x + j] == 0:
                            val = 0
                            break
                tempArr[y][x] = val
                
                colorVal = val * 255
                if val == 1 and lBoard[y][x] == 0:
                    xyVals = np.append(xyVals, [[19-y],[x]], 1)
                    colorVal = 128
                if val == 0:
                    continue
                for m in range(32):
                    for n in range(32):
                        boardMat[y * 32 + m][x * 32 + n] = colorVal
        
        self.movingBlock = np.copy(xyVals)
        self.__boardArr = np.copy(tempArr)
        cv2.imshow('Board', boardMat)
        del tempArr
        del board

    def __makeHold(self, frame):
        hold = self.__handleCanvas(frame)
        
        tempArr = np.zeros((2, 4))
        for y in range(2):
            for x in range(4):
                tempArr[y][x] = 1 if hold[20 * y + 10][18 * x + 9] > 0 else 0
                self.__holdArr = np.copy(tempArr)
        del tempArr
        del hold

    def __makeQueue(self, frame):
        queue = self.__handleCanvas(frame)
        
        queueMat = np.zeros((310, 65), dtype = uint8)
        tempArr = np.zeros((17, 4), dtype = uint8)
        for i in range(17):
            for j in range(4):
                if i % 3 == 2:
                    continue
                val = 1 if queue[self.arr2[i] + 8][16 * j + 8] > 0 else 0
                tempArr[i][j] = val
                if val == 0:
                    continue
                for m in range(self.arr[i]):
                    for n in range(16):
                        queueMat[self.arr2[i] + m][j * 16 + n] = 255
        self.__queueArr = np.copy(tempArr)
        cv2.imshow('Queue', queueMat)
        del tempArr
        del queue

    def __handleCanvas(self, canvas):
        temp = cv2.cvtColor(canvas, cv2.COLOR_BGR2HLS)
        return cv2.inRange(temp, np.array([0,54,0]), np.array([255,255,255]))
        
# --------------------------------------------------------------------

    def clearLastBoard(self):
        self.lastBoard = np.zeros((20, 10), dtype = uint8)
        self.lastQueue = np.zeros((17,4), dtype = uint8)
        self.nextBlock = np.zeros((2,4), dtype = uint8)
        self.movingBlock = np.zeros((2,4), dtype = uint8)
        
    def updateLastBoard(self):
        self.lastBoard = np.copy(self.__boardArr)
        for i in range(2):
            for j in range(4):
                if self.nextBlock[i][j] == 1 and self.lastBoard[i][j + 3] == 1:
                    self.lastBoard[i][j + 3] = 0
                    
# --------------------------------------------------------------------

    def didBlockChange(self):
        return self.dh.didBlockChange(self.lastQueue, self.__queueArr, self.nextBlock)

    def getNextBestMove(self, thelist, nodeNet):
        return self.dh.getNextBestMove(thelist, self.__queueArr, self.lastBoard, self.movingBlock, nodeNet)

    def getBestMoves(self, nodeNet):
        return self.dh.getBestMoves(self.__queueArr, self.lastBoard, self.movingBlock, nodeNet)

# --------------------------------------------------------------------

    def existsControllablePiece(self):
        return len(self.movingBlock[0]) == 4

    def isDead(self):
        return np.amin(self.__boardArr[5]) == 1 and np.amin(self.__boardArr[10]) == 1
    
    def shouldQuit(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def shouldPressA(self):
        return cv2.waitKey(1) & 0xFF == ord('a')

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()
