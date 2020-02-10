from numpy import uint8
from tetris import *
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
        self.tetris = Tetris()
        self.past_tetris = Tetris()
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
        board_mat = np.zeros((640, 320), dtype = uint8)
        xy_vals = np.zeros((2,0), dtype = uint8)
        
        for y in range(20):
            for x in range(10):
                val = 1
                pixel_check = [4, 16, 28]
                for i in pixel_check:
                    for j in pixel_check:
                        if board[32 * y + i][32 * x + j] == 0:
                            val = 0
                            break
                loc = self.tetris.board_pos(x, y)
                self.tetris.board[loc] = val
                
                color_val = val * 255
                if val == 0:
                    continue
                if self.past_tetris.board[loc] == 0 and len(xy_vals[0]) < 4:
                    xy_vals = np.append(xy_vals, [[19-y],[x]], 1)
                    color_val = 128
                for m in range(32):
                    for n in range(32):
                        board_mat[y * 32 + m][x * 32 + n] = color_val
        
        self.moving_block = np.copy(xy_vals)
        cv2.imshow('Board', board_mat)

    def __make_hold(self, frame):
        hold = self.__handleCanvas(frame)
        
        for y in range(2):
            for x in range(4):
                self.tetris.hold[y * 4 + x] = (0, 1)[hold[20 * y + 10][18 * x + 9] > 0]

    def __make_queue(self, frame):
        queue = self.__handleCanvas(frame)
        
        queue_mat = np.zeros((310, 65), dtype = uint8)
        for i in range(17):
            for j in range(4):
                if i % 3 == 2:
                    continue
                val = (0,1)[queue[self.arr2[i] + 8][16 * j + 8] > 0]
                tmp_i = int(i - i // 3)
                loc = self.tetris.queue_pos(j, tmp_i)
                self.tetris.queue[loc] = val
                if val == 0:
                    continue
                for m in range(self.arr[i]):
                    for n in range(16):
                        queue_mat[self.arr2[i] + m][j * 16 + n] = 255
        cv2.imshow('Queue', queue_mat)

    def __handleCanvas(self, canvas):
        temp = cv2.cvtColor(canvas, cv2.COLOR_BGR2HLS)
        return cv2.inRange(temp, np.array([0,54,0]), np.array([255,255,255]))
        
# --------------------------------------------------------------------

    def clear(self):
        self.next_block = np.zeros((2,4), dtype = uint8)
        self.moving_block = np.zeros((2,0), dtype = uint8)

    def update_last_board(self):
        self.past_tetris.board = list(self.tetris.board)
        for i in range(2):
            for j in range(4):
                loc = self.tetris.board_pos(j + 3, i)
                if self.next_block[i][j] == 1:
                    self.last_board[loc] = 0
                    
# --------------------------------------------------------------------

    def did_block_change(self):
        past_block = np.copy(self.next_block)
        queue_change = 0
        oldtile_count = sum(self.past_tetris.queue)
        for i in range(12 * 4):
            if i < 8:
                self.next_block[int(i/4)][i%4] = self.past_tetris.queue[i]
                if self.tetris.queue[i] != self.past_tetris.queue[i]:
                    self.past_tetris.queue[i] = self.tetris.queue[i]
                    queue_change += 1
        tile_count = sum(self.tetris.queue)
        if queue_change < 6:
            self.next_block = past_block
        return (queue_change > 5 and
            22 < tile_count < 26 and
            22 < oldtile_count < 26)

    def queue_filled(self):
        middle_count = 0
        for i in range(12 * 4):
            if self.tetris.queue[i] == 1 and (i%4==1 or i%4==2):
                middle_count += 1
        return (middle_count >= 12)

# --------------------------------------------------------------------

    def exists_controllable_piece(self):
        return len(self.moving_block[0]) == 4

    def game_over(self):
        return max(self.tetris.board[2:12] + self.tetris.board[72:82]) != 0
    
    def should_quit(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def should_press_a(self):
        return cv2.waitKey(1) & 0xFF == ord('a')

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()
