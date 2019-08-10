import numpy.random as rand
import time
from neat import NEAT
from switchdata import SwitchData

# Controlled randomness
rand.seed(0)

cap = SwitchData(0)
t0 = time.time()
i = 0
cap.start()
while True:
    cap.handleCapture()
    i += 1
    if (cap.shouldQuit()):
        break
cap.stop()


    




