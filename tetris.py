# Import packages and files
from filemanager import FileManager
from switchdata import SwitchData
from emulator import Emulator
from neat import NEAT
from time import time

t0 = time()                         # Get a relative point of time

capture = SwitchData()              # Connect to the Switch Capture
capture.start()                     # Run the Switch Capture asynchronously

populationSize = 50                 # Set the population size
neat = NEAT(populationSize)         # Begin our population

# Check to see if there is save data for the neural network to return to
fileManager = FileManager()         # Initialize a file manager to create / read files
loadable = fileManager.loadable()   # Get a tuple of (Boolean, Generation) as to whether the genome files are loadable
if loadable[0]:                     # Check to see if genomes files exist
    neat.repopulate(loadable[1])    # Repopulate with the oldest existent genome generation
else:
    neat.createPopulation()         # Create a new population since none exist

port = "COM3"                       # Set port for emulation
emulator = Emulator(port)           # Create emulation on the specific port

while True:                         # Main code loop :)
    if (capture.shouldQuit()):      # Check to see if the program should end (if we pressed q)
        emulator.stop_input()       # Stop any inputs to the emulator
        break                       # Break out of the while loop

    capture.processCapture()        # Make and display the board, hold, and queue, and game frame

    # Check to see if we should press A (genome over, and it won't go to next genome),
    # or check to see if genome is dead to press A
    if capture.shouldPressA() or capture.isDead():
        emulator.nextGenome()       # Hold the A button
        neat.loop()                 # Go to next genome / generation
        capture.clearLastBoard()    # Clear last board

    # Attempt a command if it has been X amount of seconds since the last command
    if (time()-t0 > 0.2):
        t0 = time()
        blockChange = capture.didBlockChange()
        if blockChange:
            capture.updateLastBoard()

        if capture.existsControllablePiece():
            btnArr = neat.getMovements(capture, blockChange)    # Get the button array of recommended moves
            emulator.emulateTetris(btnArr)  # Send the correct button inputs
        else:
            emulator.stop_input()   # Send signals to stop the emulator from sending button data

        neat.printFitness()         # Print the fitness
    else:
        emulator.stop_input()       # Send signals to stop the emulator from sending button data

capture.stop()                      # Stop the capture thread
emulator.close()                    # Stop the emulator