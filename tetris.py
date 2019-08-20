# Import packages and files
from filemanager import FileManager
from switchdata import SwitchData
from emulator import Emulator
from emulator import BTN_A
import numpy.random as rng
from neat import NEAT
import time
from os.path import isfile

# Controlled randomness
rng.seed(420)

# Get a relative point of time
t0 = time.time()

# Connect to the Switch Capture, and run it asynchronous
capture = SwitchData()
capture.start()

# Begin our population
populationSize = 26
neat = NEAT(populationSize)

# Check to see if there is save data for the neural network to return to
fileManager = FileManager()
canRepopulate = fileManager.canRepopulate()
if canRepopulate[0]:
    neat.repopulate(canRepopulate[1])
else:
    neat.createPopulation()

capture.setNodeNet(neat.getCurrentNodeNet())
capture.startMoveFind()

#Get connected to an emulator
port = "COM3"
emulator = Emulator(port)

# Main code loop
while True:
    
    # Check to see if we should end the program (if we pressed q)
    if (capture.shouldQuit()):
        emulator.send_input()
        break

    # Check to see if we should press A (genome over, and it won't go to next genome)
    if (capture.shouldPressA()):
        emulator.nextGenome()
        neat.loop()
    
    capture.setNodeNet(neat.getCurrentNodeNet())

    # Process the capture to get the images that we need
    capture.processCapture()

    # Check to see if genome is dead
    if capture.isDead():
        t1 = time.time()
        emulator.nextGenome()
        neat.loop()
        capture.resetBoard()

    if (time.time()-t0 > 0.25):
        t0 = time.time()

        # Get the best move values
        validMoves = capture.bestMoves
        
        # Send the correct button inputs
        btnArr = neat.processGenome(validMoves)
        # print(btnArr)
        emulator.emulateTetris(btnArr)
        neat.printFitness(capture.getFitness(capture.getBoard(), neat.getCurrentNodeNet()))

# Stop the capture thread
capture.stop()

capture.stopMoveFind()

# Stop the emulator
emulator.close()