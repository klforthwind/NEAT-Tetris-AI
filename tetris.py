import numpy as np
import random 
import numpy.random as rand
from neat import NEAT
from switchdata import SwitchData

# Controlled randomness
rand.seed(0)

neat = NEAT(50)
data = SwitchData()
k = True
while k:
    # data.update()
    # data.show()
    data.update()
    k = data.specialAnalysis()
    


    




