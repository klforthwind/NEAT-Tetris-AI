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
        _, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

        self.arr = [16,16,26,15,15,26,15,15,26,15,15,26,14,14,26,14,14]
        self.arr2 = [0,16,32,58,73,88,114,129,144,170,185,200,226,240,254,280,294]
        self.board_array = np.zeros((20, 10), dtype = uint8)
        self.queue_array = np.zeros((17, 4), dtype = uint8)
        self.hold_array = np.zeros((2, 4), dtype = uint8)
        self.dh = DataHandler()
        self.clear()

    def start(self):
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            _, frame = self.cap.read()
            with self.read_lock:
                self.frame = frame

    def stop(self):
        self.started = False
        self.thread.join()
        cv2.destroyAllWindows()

# --------------------------------------------------------------------
    
    def process_capture(self):
        _, frame = self.cap.read()
        cv2.imshow('Frame', frame)
        
        self.__make_board(frame[40:680, 480:800])
        self.__make_hold(frame[80:120, 396:468])
        self.__make_queue(frame[80:390, 815:880])
        
    def __make_board(self, frame):
        board = np.copy(self.__handleCanvas(frame))
        boardMat = np.zeros((640, 320), dtype = uint8)
        tempArr = np.zeros((20,10), dtype = uint8)
        last_board = np.copy(self.last_board)
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
                if val == 1 and last_board[y][x] == 0 and len(xyVals[0]) < 4:
                    xyVals = np.append(xyVals, [[19-y],[x]], 1)
                    colorVal = 128
                if val == 0:
                    continue
                for m in range(32):
                    for n in range(32):
                        boardMat[y * 32 + m][x * 32 + n] = colorVal
        
        self.moving_block = np.copy(xyVals)
        self.board_array = np.copy(tempArr)
        cv2.imshow('Board', boardMat)

    def __make_hold(self, frame):
        hold = self.__handleCanvas(frame)
        
        tempArr = np.zeros((2, 4))
        for y in range(2):
            for x in range(4):
                tempArr[y][x] = (0, 1)[hold[20 * y + 10][18 * x + 9] > 0]
                self.hold_array = np.copy(tempArr)

    def __make_queue(self, frame):
        queue = self.__handleCanvas(frame)
        
        queueMat = np.zeros((310, 65), dtype = uint8)
        tempArr = np.zeros((17, 4), dtype = uint8)
        for i in range(17):
            for j in range(4):
                if i % 3 == 2:
                    continue
                val = (0,1)[queue[self.arr2[i] + 8][16 * j + 8] > 0]
                tempArr[i][j] = val
                if val == 0:
                    continue
                for m in range(self.arr[i]):
                    for n in range(16):
                        queueMat[self.arr2[i] + m][j * 16 + n] = 255
        self.queue_array = np.copy(tempArr)
        cv2.imshow('Queue', queueMat)

    def __handleCanvas(self, canvas):
        temp = cv2.cvtColor(canvas, cv2.COLOR_BGR2HLS)
        return cv2.inRange(temp, np.array([0,54,0]), np.array([255,255,255]))
        
# --------------------------------------------------------------------

    def clear(self):
        self.last_board = np.zeros((20, 10), dtype = uint8)
        self.last_queue = np.zeros((17,4), dtype = uint8)
        self.next_block = np.zeros((2,4), dtype = uint8)
        self.moving_block = np.zeros((2,4), dtype = uint8)
        
    def update_last_board(self):
        self.last_board = np.copy(self.board_array)
        for i in range(2):
            for j in range(4):
                if self.next_block[i][j] == 1 and self.last_board[i][j + 3] == 1:
                    self.last_board[i][j + 3] = 0
                    
# --------------------------------------------------------------------

    def did_block_change(self):
        self.temp_block = np.copy(self.next_block)
        did_change = self.dh.did_block_change(self.last_queue, self.queue_array, self.temp_block)
        self.next_block = self.next_block if not did_change else self.temp_block
        return did_change

    def queue_filled(self):
        return self.dh.is_queue_filled(self.queue_array)

    def get_best_moves(self, node_net):
        return self.dh.get_best_moves(self.queue_array, self.last_board, self.moving_block, node_net)

# --------------------------------------------------------------------

    def exists_controllable_piece(self):
        return len(self.moving_block[0]) == 4

    def game_over(self):
        return np.amin(self.board_array[5]) == 1 and np.amin(self.board_array[10]) == 1
    
    def should_quit(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def should_press_a(self):
        return cv2.waitKey(1) & 0xFF == ord('a')

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()
