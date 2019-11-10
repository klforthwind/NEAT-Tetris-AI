from emulator import Emulator
from time import time

if __name__ == '__main__':

    emulator = Emulator("COM3")
    t0 = time()
    emulator.next_genome()

    for i in range(10):
        print(time())
        while time()-t0 < 0.05:
            k = 1
        t0 = time()
        emulator.emulate_tetris([0,1,0,0,0,0,0,0,0,0])

    print("Done! Maybe....")