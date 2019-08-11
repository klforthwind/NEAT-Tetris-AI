import numpy.random as rng
import time
from neat import NEAT
from switchdata import SwitchData

# Controlled randomness
rng.seed(0)

capture = SwitchData(0)
t0 = time.time()
capture.start()
while True:
    capture.handleCapture()
    inputNodes = capture.getInputNodes()
    if (capture.shouldQuit()):
        break
capture.stop()


    




