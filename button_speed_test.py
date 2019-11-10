from emulator import Emulator
from time import time

if __name__ == '__main__':

    emulator = Emulator("COM3")
    # emulator.press_a()
    for i in range(400):
        print(time())
        em = ([0,1,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0], [0,0,0,1,0,0,0,0,0,0], [0,0,0,1,0,0,0,0,0,0])[i%4]
        emulator.emulate_tetris(em)

    print("Done! Maybe....")