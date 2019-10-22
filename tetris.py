# Import packages and files
from filemanager import FileManager
from switchdata import SwitchData
from emulator import Emulator
import numpy.random as rng
from neat import NEAT
from time import time

rng.seed(666)               # Controlled randomness, although Tetris blocks are random :P

t0 = time()                 # Get a relative point of time

capture = SwitchData()      # Connect to the Switch Capture
capture.start()             # Run the Switch Capture asynchronously

populationSize = 50         # Set the population size
neat = NEAT(populationSize) # Begin our population

# Check to see if there is save data for the neural network to return to
fileManager = FileManager() # Initialize a file manager to create / read files
loadable = fileManager.loadable()   # Get a tuple of (Boolean, Generation) as to whether the genome files are loadable
if loadable[0]:             # Check to see if genomes files exist
    neat.repopulate(loadable[1])    # Repopulate with the oldest existent genome generation
else:
    neat.createPopulation() # Create a new population since none exist

#Get connected to an emulator
port = "COM3"
emulator = Emulator(port)

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

        # Clear last board
        capture.clearLastBoard()

    # Attempt a command if it has been X amount of seconds since the last command
    if (time()-t0 > 0.2):
        t0 = time()
        blockChange = capture.didBlockChange()
        if blockChange:
            capture.updateLastBoard()

        if capture.existsControllablePiece():

            # Get the button array of recommended moves
            btnArr = neat.getMovements(capture, blockChange)

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