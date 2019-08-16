# Import packages and files
from switchdata import SwitchData
from emulator import Emulator
from emulator import BTN_A
import numpy.random as rng
from neat import NEAT
import time
import os

# Controlled randomness
rng.seed(66669420)

# Get a relative point of time
t0 = time.time()
t1 = time.time()

# Connect to the Switch Capture, and run it asynchronous
capture = SwitchData()
capture.start()

# Begin our population
populationSize = 50
neat = NEAT(populationSize)

gen = 0
if os.path.isfile('data/0-0-0.txt'):
    while(os.path.isfile('data/'+str(gen)+'-0-0.txt')):
        hasData = os.path.isfile('data/'+str(gen)+'-0-0.txt')
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
    capture.processCapture(neat.genomes[neat.currentGenome].neuralNet)

    # Get the needed input nodes from 
    inputNodes = capture.getInputNodes(neat.didBlockChange())

    # Check to see if genome is dead
    if capture.isDead():
        t1 = time.time()
        emulator.nextGenome()
        neat.loop()

        
    if (time.time()-t1 > 400 and capture.isLevelingUp()):
        emulator.nextGenome()
        neat.loop()
    

    for x in range(10):
        for y in range(20):
            if(inputNodes[x + 10 * y] == 1):
                neat.genomes[neat.currentGenome].fitness += y / 2000
                break

    if (time.time()-t0 > 0.25):
        t0 = time.time()
        # Send the correct button inputs
        btnArr = neat.processGenome(inputNodes)
        emulator.emulateTetris(btnArr)

# Stop the capture thread
capture.stop()

# Stop the emulator
emulator.close()