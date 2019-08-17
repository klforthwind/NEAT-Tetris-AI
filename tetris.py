# Import packages and files
from switchdata import SwitchData
from emulator import Emulator
from emulator import BTN_A
import numpy.random as rng
from neat import NEAT
import time
from os.path import isfile

# Controlled randomness
rng.seed(66669420)

# Get a relative point of time
t0 = time.time()
t1 = time.time()

# Connect to the Switch Capture, and run it asynchronous
capture = SwitchData()
capture.start()

# Add height variable
maxHeight = 0

# Begin our population
populationSize = 50
neat = NEAT(populationSize)

# Check to see if there is save data for the neural network to return to
gen = 0
zeroGenome = '0-0-h-0.txt'
if isfile('data/0'+zeroGenome):
    while(isfile('data/'+str(gen)+zeroGenome)):
        hasData = isfile('data/'+str(gen)+zeroGenome)
        if hasData:
            gen += 1
    gen -= 1
    neat.repopulate(gen)
else:
    neat.createPopulation()

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

    change = neat.didBlockChange(capture)

    # Get the needed input nodes from 
    inputNodes = capture.getInputNodes()
    hiddenNodes = capture.getHiddenNodes(change)
    if change:
        change = False
        hitWhite = False
        heightFromTop = 20
        for x in range(10):
            for y in range(20):
                if y > 1 and capture.lastBoard[y][x] == 1 and y < heightFromTop:
                    y = heightFromTop
                if(capture.lastBoard[y][x] == 1):
                    neat.genomes[neat.currentGenome].fitness += y / 20
                    break
        if (20 - heightFromTop < maxHeight and maxHeight - (20 - heightFromTop) <= 4):
            neat.genomes[neat.currentGenome].fitness += 50
            maxHeight = 20 - heightFromTop

    # Check to see if genome is dead
    if capture.isDead():
        t1 = time.time()
        emulator.nextGenome()
        neat.loop()
        capture.resetBoard()

        
    if (time.time()-t1 > 400 and capture.isLevelingUp()):
        emulator.nextGenome()
        neat.loop()

    if (time.time()-t0 > 0.25):
        t0 = time.time()
        # Send the correct button inputs
        btnArr = neat.processGenome(inputNodes, hiddenNodes)
        emulator.emulateTetris(btnArr)

# Stop the capture thread
capture.stop()

# Stop the emulator
emulator.close()