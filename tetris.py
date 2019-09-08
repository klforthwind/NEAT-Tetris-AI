# Import packages and files
from filemanager import FileManager
from switchdata import SwitchData
from emulator import Emulator
import numpy.random as rng
from neat import NEAT
from time import time

# Controlled randomness, doesn't matter that much with Tetris tho
rng.seed(666)

# Get a relative point of time
t0 = time()
t1 = time()

# Connect to the Switch Capture, and run it asynchronously
capture = SwitchData()
capture.start()

# Begin our population
populationSize = 50
neat = NEAT(populationSize)

# Check to see if there is save data for the neural network to return to
fileManager = FileManager()
loadable = fileManager.loadable()
if loadable[0]:
    neat.repopulate(loadable[1])
else:
    neat.createPopulation()

#Get connected to an emulator
port = "COM3"
emulator = Emulator(port)

placedBlock = False
pos = 0

# Main code loop :)
while True:
    
    # Check to see if we should end the program (if we pressed q)
    if (capture.shouldQuit()):
        emulator.stop_input()
        break

    # Make and display the board, hold, and queue, and game frame
    capture.processCapture()

    # Check to see if we should press A (genome over, and it won't go to next genome),
    # or check to see if genome is dead to press A
    if capture.shouldPressA() or capture.isDead():
        
        # Hold the A button
        emulator.nextGenome()
        
        # Go to next genome / generation
        neat.loop()

    # Attempt a command if it has been X amount of seconds since the last command
    if (time()-t0 > 0.2):
        t0 = time()
        blockChange = capture.didBlockChange()
        if placedBlock and time() - t1 > 0.5:
            placedBlock = False
            t1 = time()

        if capture.existsControllablePiece() and (not placedBlock or blockChange):
            
            # Perform movement since we can
            xPos = capture.getXPos()

            if blockChange:
                pos = xPos
                print(pos)

            # Get the button array of recommended moves
            btnArr = neat.getMovements(capture, pos, blockChange)

            if btnArr[0] == 1:
                placedBlock = True
                t1 = time()

            # Send the correct button inputs
            emulator.emulateTetris(btnArr)
        else:
            # Send signals to stop the emulator from sending button data
            emulator.stop_input()

        # Print the fitness
        neat.printFitness()
    else:
        # Send signals to stop the emulator from sending button data
        emulator.stop_input()

# Stop the capture thread
capture.stop()

# Stop the emulator
emulator.close()