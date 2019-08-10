import numpy.random as rng
import time
from neat import NEAT
from switchdata import SwitchData

# Controlled randomness
rng.seed(0)

cap = SwitchData(0)
t0 = time.time()
cap.start()
while True:
    cap.handleCapture()
    if (cap.shouldQuit()):
        break
cap.stop()


    




