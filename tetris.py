# Import packages and files
from switchdata import SwitchData
from emulator import Emulator
from emulator import BTN_A
import numpy.random as rng
from neat import NEAT
import time

# Controlled randomness
rng.seed(42069666)
t0 = time.time()
t1 = time.time()
t2 = time.time()
res = False
once = False
start = True

# Connect to the Switch Capture
capture = SwitchData(0)

# Start the Switch Capture Thread, running asynchronous
capture.start()

# Begin our population
neat = NEAT(2)
neat.createPopulation()

#Get connected to an emulator
port = "COM3"
emulator = Emulator(port)

# Main code loop
while True:
    
    # Check to see if we should end the program
    if (capture.shouldQuit()):
        emulator.send_input()
        break

    # Process the capture to get the images that we need
    capture.processCapture()

    # Get the needed input nodes from 
    inputNodes = capture.getInputNodes(neat.didBlockChange())
    
    if time.time()-t2 > 1:
        # Check to see if genome is dead
        if capture.isDead():
            t2 = time.time()
            if once:
                once = False
                res = True
        else:
            if res:
                res = False
                #Loop through genomes
                neat.loop()
    
    if not capture.isDead():
        start = False
        once = True

    if res or start:
        emulator.send_input(BTN_A)
    
    if (time.time()-t0 > 0.15) and not res:
        t0 = time.time()
        # Send the correct button inputs
        btnArr = neat.processGenome(inputNodes)
        emulator.emulateTetris(btnArr)


# Stop the capture thread
capture.stop()

# Stop the emulator
emulator.close()