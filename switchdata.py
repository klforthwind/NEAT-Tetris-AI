from numpy import uint8
from datahandler import DataHandler
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
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

        # Set image processing variables
        self.arr = [16,16,26,15,15,26,15,15,26,15,15,26,14,14,26,14,14]
        self.arr2 = [0,16,32,58,73,88,114,129,144,170,185,200,226,240,254,280,294]
        self.__boardArr = np.zeros((20, 10), dtype = uint8)
        self.__queueArr = np.zeros((17, 4), dtype = uint8)
        self.__holdArr = np.zeros((2, 4), dtype = uint8)
        self.dh = DataHandler()
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
    
    def processCapture(self):                                                   # Make and display boardArr, holdArr, and queueArr
        _, frame = self.cap.read()                                              # Read the capture card
        cv2.imshow('Frame', frame)                                              # Show the capture card

        self.__makeBoard(frame[40:680, 480:800])                                # Process and show the board
        self.__makeHold(frame[80:120, 396:468])                                 # Process the hold
        self.__makeQueue(frame[80:390, 815:880])                                # Process the queue

    def __makeBoard(self, frame):
        board = self.__handleCanvas(frame)                                      # Add a luminance mask to the board mat
        boardMat = np.zeros((640, 320), dtype = uint8)                          # Attempt to make a less noisy mask
        tempArr = np.zeros((20,10), dtype = uint8)                              #Run through all 200 grid tiles
        lBoard = self.lastBoard                                                 # Make a copy of the tetris board
        xyVals = np.zeros((2,0), dtype = uint8)                                 # Create an empty numpy array to add the locations of moving block to

        for y in range(20):                                                     # Iterate over each row of the board
            for x in range(10):                                                 # Iterate over each tile in a row    
                val = 1                                                         # Get correct value of the indexed tiles
                valArr = [4, 16, 28]
                for i in valArr:
                    for j in valArr:
                        if board[32 * y + i][32 * x + j] == 0:                  # See if tile as specific pixel is filled or not
                            val = 0
                            break
                tempArr[y][x] = val                                             # Add to board array whether the tile was filled or not

                colorVal = val * 255
                if val == 1 and lBoard[y][x] == 0:                              # Y = 0 refers to the top of the board
                    xyVals = np.append(xyVals, [[19-y],[x]], 1)                 # Save the coords of the filled block as [distance from bottom] and [x]
                    colorVal = 128                                              # Set the color of the moving block to grey, so it is much more visible on the mat
                if val == 0:                                                    # Skip coloring if tile is empty
                    continue
                for m in range(32):                                             # Color the tile if it is filled
                    for n in range(32):
                        boardMat[y * 32 + m][x * 32 + n] = colorVal
        
        self.movingBlock = np.copy(xyVals)                                      # Create a copy of xyVals that other functions can access
        self.__boardArr = np.copy(tempArr)                                      # Show the board with opencv
        cv2.imshow('Board', boardMat)                                           # Show the board
        del tempArr                                                             # Delete the temporary array
        del board

    def __makeHold(self, frame):
        hold = self.__handleCanvas(frame)                                       # Add a luminance mask to the hold mat

        tempArr = np.zeros((2, 4))                                              # Array to hold which tiles in hold are filled
        for y in range(2):                                                      # Iterate over the two rows of the hold block
            for x in range(4):                                                  # Iterate over the four tiles in a row
                tempArr[y][x] = 1 if hold[20 * y + 10][18 * x + 9] > 0 else 0   # Set the value in the temp array to whether the hold block was filled at the specific tile
        self.__holdArr = np.copy(tempArr)                                       # Create a copy of temp array that other functions can access
        del tempArr                                                             # Delete the temporary array
        del hold

    def __makeQueue(self, frame):
        queue = self.__handleCanvas(frame)                                      # Add a luminance mask to the queue mat
        
        queueMat = np.zeros((310, 65), dtype = uint8)                           # Queue Mat to display to the screen
        tempArr = np.zeros((17, 4), dtype = uint8)                              # Array to hold which tiles in queue are filled
        for i in range(17):                                                     # Iterate over all of the rows
            for j in range(4):                                                  # Iterate over the four tiles in a row
                if i % 3 == 2:                                                  # Check to see if i is on an empty space in between blocks
                    continue                                                    # Go to next row, so we don't handle bad row data
                val = 1 if queue[self.arr2[i] + 8][16 * j + 8] > 0 else 0       # Obtain whether a given tile is filled or not
                tempArr[i][j] = val                                             # Add tile status to queue array
                if val == 0:                                                    # Check to see if the tile is not filled
                    continue                                                    # Continue to the next tile, since we don't need to draw in the tile
                for m in range(self.arr[i]):                                    # Iterate over the tile in queueMat and draw a square where a tile exists
                    for n in range(16):
                        queueMat[self.arr2[i] + m][j * 16 + n] = 255
        self.__queueArr = np.copy(tempArr)                                      # Create a copy of temp array that other functions can access
        cv2.imshow('Queue', queueMat)                                           # Show the queue
        del tempArr                                                             # Delete the temporary array
        del queue

    def __handleCanvas(self, canvas):
        temp = cv2.cvtColor(canvas, cv2.COLOR_BGR2HLS)                          # Convert the queue to Hue Luminance and Saturation Mode
        return cv2.inRange(temp, np.array([0,54,0]), np.array([255,255,255]))   # Only get the luminant parts of the board

# --------------------------------------------------------------------

    def clearLastBoard(self):                                                   # Clear the last board data
        self.lastBoard = np.zeros((20, 10), dtype = uint8)                      # Reset values for the last board
        self.lastQueue = np.zeros((17,4), dtype = uint8)                        # Reset values for the last queue
        self.nextBlock = np.zeros((2,4), dtype = uint8)                         # Reset values for the next block
        self.movingBlock = np.zeros((2,4), dtype = uint8)                       # Reset values for the moving block

    def updateLastBoard(self):
        self.lastBoard = np.copy(self.__boardArr)                               # Copy over the board array into the last board, since the current block just got placed
        for i in range(2):                                                      # Iterate over the tiles that the new tetris block spawns at
            for j in range(4):
                if self.nextBlock[i][j] == 1 and self.lastBoard[i][j + 3] == 1: # If the tile exists on the new block in hand, and it is filled on the last board, it should not be filled on the last board
                    self.lastBoard[i][j + 3] = 0                                # Set the conflicting tile to not filled

# --------------------------------------------------------------------

    def didBlockChange(self):
        return self.dh.didBlockChange(self.lastQueue, self.__queueArr, self.nextBlock)

    def getNextBestMove(self, thelist, nodeNet):
        return self.dh.getNextBestMove(thelist, self.__queueArr, self.lastBoard, self.movingBlock, nodeNet)

    def getBestMoves(self, nodeNet):
        return self.dh.getBestMoves(self.__queueArr, self.lastBoard, self.movingBlock, nodeNet)

# --------------------------------------------------------------------

    # Determines if there is a piece that we can control
    def existsControllablePiece(self):
        return len(self.movingBlock[0]) == 4

    def isDead(self):                                                           # Returns true if row 5 and row 10 (top starting at row 0) are both filled
        return np.amin(self.__boardArr[5]) == 1 and np.amin(self.__boardArr[10]) == 1
    
    def shouldQuit(self):                                                       # Returns true if the q button is pressed
        return cv2.waitKey(1) & 0xFF == ord('q')

    def shouldPressA(self):                                                     # Returns true if the a button is pressed
        return cv2.waitKey(1) & 0xFF == ord('a')

    def __exit__(self, exec_type, exc_value, traceback):                        # Exits out of the opencv capture once program is over
        self.cap.release()
