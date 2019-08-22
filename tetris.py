# Import packages and files
from filemanager import FileManager
from switchdata import SwitchData
from emulator import Emulator
from emulator import BTN_A
import numpy.random as rng
from neat import NEAT
from time import time

# Controlled randomness, doesn't matter that much with Tetris tho
rng.seed(420)

# Get a relative point of time
t0 = time()

# Connect to the Switch Capture, and run it asynchronous
capture = SwitchData()
capture.start()

# Begin our population
populationSize = 26
neat = NEAT(populationSize)

# Check to see if there is save data for the neural network to return to
fileManager = FileManager()
loadable = fileManager.loadable()
if loadable[0]:
    neat.repopulate(loadable[1])
else:
    neat.createPopulation()

# Attempt to find the best moves
capture.setNodeNet(neat.getCurrentNodeNet())

# Start move finding
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

    # Process the capture to get the images that we need
    capture.processCapture()

    # Check to see if genome is dead
    if capture.isDead():

        # Hold the A button
        emulator.nextGenome()

        # Go to next genome / generation
        neat.loop()

        # Pass over the node net so capture can use it
        capture.setNodeNet(neat.getCurrentNodeNet())
        
    # Attempt a command if it has been X amount of seconds since the last command
    if (time()-t0 > 0.25):
        t0 = time()

        # Get the best move values
        validMoves = capture.bestMoves
        
        # Get the button array of recommended moves
        btnArr = neat.processGenome(validMoves)

        # Send the correct button inputs
        emulator.emulateTetris(btnArr)

        # Print the fitness
        neat.printFitness(capture.getFitness(capture.getBoard(), neat.getCurrentNodeNet()))

# Stop the capture thread
capture.stop()

# Stop move finding
capture.stopMoveFind()

# Stop the emulator
emulator.close()