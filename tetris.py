from filemanager import FileManager
from switchdata import SwitchData
from emulator import Emulator
from neat import NEAT
from time import time

emulator = Emulator("COM3")
capture = SwitchData()
capture.start()
t0 = time()

population_size = 50
file_manager = FileManager()
neat = NEAT(population_size, file_manager.loadable())

while True:
    if (capture.should_quit()):
        break

    capture.process_capture()
    if capture.should_press_a() or capture.game_over():
        emulator.next_genome()
        neat.loop()
        capture.clear()

    if (time()-t0 > 0.2):
        t0 = time()
        block_change = capture.did_block_change()
        if block_change:
            capture.update_last_board()

        if capture.exists_controllable_piece():
            btnArr = neat.get_movements(capture, block_change)
            emulator.emulate_tetris(btnArr)
            
        neat.print_fitness()
    elif (time()-t0 > 0.075):
        emulator.stop_input()
capture.stop()
emulator.close()
