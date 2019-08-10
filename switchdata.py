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
    
    def handleCapture(self):
        _, frame = self.read()
        board = frame[40:680, 480:800]
        cv2.imshow('Frame', frame)
        board = cv2.cvtColor(board, cv2.COLOR_BGR2HLS)
        board = cv2.inRange(board, np.array([0,54,0]), np.array([255,255,255]))
        # cv2.imshow('Board', board)
        # hold = frame[40:180, 380:480]
        # hold = cv2.cvtColor(hold, cv2.COLOR_BGR2HLS)
        # hold = cv2.inRange(hold, np.array([0,54,0]), np.array([255,255,255]))
        # cv2.imshow('Hold', hold)
        queue = frame[60:400, 800:880]
        queue = cv2.cvtColor(queue, cv2.COLOR_BGR2HLS)
        queue = cv2.inRange(queue, np.array([0,54,0]), np.array([255,255,255]))
        # cv2.imshow('Queue', queue)
        # print(board[624][16]) #prints 255 if occupied, 0 if empty

    def shouldQuit(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()