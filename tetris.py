from filemanager import FileManager
from switchdata import SwitchData
from emulator import Emulator
from neat import NEAT
from time import time

t0 = time()

capture = SwitchData()
capture.start()

populationSize = 50
neat = NEAT(populationSize)

fileManager = FileManager()
loadable = fileManager.loadable()
if loadable[0]:
    neat.repopulate(loadable[1])
else:
    neat.createPopulation()

port = "COM3"
emulator = Emulator(port)

while True:
    if (capture.shouldQuit()):
        emulator.stop_input()
        break

    capture.processCapture()

    if capture.shouldPressA() or capture.isDead():
        emulator.nextGenome()
        neat.loop()
        capture.clearLastBoard()

    if (time()-t0 > 0.2):
        t0 = time()
        blockChange = capture.didBlockChange()
        if blockChange:
            capture.updateLastBoard()

        if capture.existsControllablePiece():
            btnArr = neat.getMovements(capture, blockChange)
            emulator.emulateTetris(btnArr)
        else:
            emulator.stop_input()
            
        neat.printFitness()
    else:
        emulator.stop_input()

capture.stop()
emulator.close()