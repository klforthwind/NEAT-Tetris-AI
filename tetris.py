# Import packages and files
from switchdata import SwitchData
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

# Main code loop
while True:
    
    # Check to see if we should end the program
    if (capture.shouldQuit()):
        break

    # Process the capture to get the images that we need
    capture.processCapture()

    # Get the needed input nodes from 
    inputNodes = capture.getInputNodes()
    
    # Check to see if genome is dead
    if capture.isDead():
        #Loop through genomes
        neat.loop()
    

# Stop the capture thread
capture.stop()
