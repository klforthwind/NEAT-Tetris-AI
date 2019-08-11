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
        self.lastBoard = np.array([])

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
    
    def processCapture(self):
        _, frame = self.read()
        cv2.imshow('Frame', frame)
        board = frame[40:680, 480:800]
        board = cv2.cvtColor(board, cv2.COLOR_BGR2HLS)
        self.board = cv2.inRange(board, np.array([0,54,0]), np.array([255,255,255]))
        cv2.imshow('Board', self.board)
        hold = frame[80:120, 396:468]
        hold = cv2.cvtColor(hold, cv2.COLOR_BGR2HLS)
        self.hold = cv2.inRange(hold, np.array([0,54,0]), np.array([255,255,255]))
        # cv2.imshow('Hold', self.hold)
        queue = frame[80:390, 815:880]
        queue = cv2.cvtColor(queue, cv2.COLOR_BGR2HLS)
        self.queue = cv2.inRange(queue, np.array([0,54,0]), np.array([255,255,255]))
        cv2.imshow('Queue', self.queue)
        # print(board[624][16]) #prints 255 if occupied, 0 if empty
    
    def isDead(self):
        isDead = True
        for x in range(10):
            if self.getBoardValue(18, x) == 0:
                isDead = False
                break
            if self.getBoardValue(19, x) == 0:
                isDead = False
                break
        return isDead

    def getBoardValue(self, y, x):
        return 1 if self.board[32 * y + 16][32 * x + 16] > 0 else 0
    
    def getQueueValue(self, y, x):
        # arr = [16,16,26,15,15,26,15,15,26,15,15,26,15,15,26,15,15]
        arr2 = [0,16,32,58,73,88,114,129,144,170,185,200,226,241,256,282,297]
        return 1 if self.queue[arr2[y] + 8][16 * x + 8] > 0 else 0

    def getHoldValue(self, y, x):
        return 1 if self.hold[20 * y + 10][18 * x + 9] > 0 else 0

    def getInputNodes(self, newBlock):
        # Begin input nodes of neat
        inputNodes = np.array([])
        xx = 0
        yy = 0
        if self.lastBoard.size == 0:
            newBlock = True
        if newBlock:
            self.lastBoard = np.array([])
        if newBlock:
            for y in range(20):
                for x in range(10):
                    if y > 1:
                        filled = self.getBoardValue(y, x)
                        self.lastBoard = np.append(self.lastBoard, filled)
        for y in range(20):
            for x in range(10):
                filled = self.getBoardValue(y, x)
                inputNodes = np.append(inputNodes, filled)
                if  xx == 0 and filled and y < 2:
                    xx = x + 1
                    yy = y + 1
                elif xx == 0 and filled and y > 1:
                    if self.lastBoard[(y-2)*10+x]==0:
                        xx = x + 1
                        yy = y + 1
                
        for i in range(17):
            # level = 0
            for j in range(4):
                if (i + 1) % 3 == 0:
                    continue
                # level += self.getQueueValue(i, j)
                inputNodes = np.append(inputNodes, self.getQueueValue(i, j))
            # print(level)
        for y in range(2):
            for x in range(4):
                inputNodes = np.append(inputNodes, self.getHoldValue(y, x))
        
        # Add X and Y as input nodes
        inputNodes = np.append(inputNodes, xx)
        inputNodes = np.append(inputNodes, yy)
        # Add 16 input nodes for the block being placed
        for m in range(4):
            for n in range(4):
                if yy + m - 1 >= 20 or xx + n - 1 >= 10:
                    inputNodes = np.append(inputNodes, 0)
                elif yy + m - 1 < 2:
                    filled = self.getBoardValue(yy + m - 1, xx + n - 1)
                    inputNodes = np.append(inputNodes, filled)
                elif yy + m - 1 > 1:
                    filled = self.getBoardValue(yy + m - 1, xx + n - 1)
                    if filled and self.lastBoard[(yy + m - 2)*10+xx+n-1]==1:
                        inputNodes = np.append(inputNodes, filled)
                    else:
                        inputNodes = np.append(inputNodes, 0)
        
        return inputNodes

    def shouldQuit(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()