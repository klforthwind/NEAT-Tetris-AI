import numpy as np
import numpy.random as rand
import cv2
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
    _, frame = cap.read()
    cv2.imshow('Frame', frame)
    i += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.stop()
cv2.destroyAllWindows()


    




