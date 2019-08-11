# Import packages and files
from switchdata import SwitchData
from emulator import Emulator
from emulator import wait
import numpy.random as rng
from neat import NEAT
import time

# Controlled randomness
rng.seed(0)

# Connect to the Switch Capture
capture = SwitchData(0)

# Start the Switch Capture Thread, running asynchronous
capture.start()

# Begin our population
neat = NEAT(50)
neat.createPopulation()

#Get connected to an emulator
port = "COM0"
emulator = Emulator(port)

# Main code loop
while True:
    
    # Check to see if we should end the program
    if (capture.shouldQuit()):
        break

    # Process the capture to get the images that we need
    capture.processCapture()

    # Get the needed input nodes from 
    inputNodes = capture.getInputNodes(neat.didBlockChange())

    # Check to see if genome is dead
    if capture.isDead():
        #Loop through genomes
        neat.loop()
        emulator.nextGenome()
    
    # Send the correct button inputs
    btnArr = neat.processGenome(inputNodes)
    emulator.emulateTetris(btnArr)
    wait(0.1)

# Stop the capture thread
capture.stop()

# Stop the emulator
emulator.close()