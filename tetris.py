from filemanager import FileManager
from switchdata import SwitchData
from emulator import Emulator
from neat import NEAT
from time import time

t0 = time()

capture = SwitchData()
capture.start()

population_size = 50
file_manager = FileManager()
neat = NEAT(population_size, file_manager.loadable())

emulator = Emulator("COM3")

while True:
    if (capture.should_quit()):
        emulator.stop_input()
        break

    capture.process_capture()

    if capture.should_press_a() or capture.game_over():
        emulator.next_genome()
        neat.loop()
        capture.clear_last_board()

    if (time()-t0 > 0.2):
        t0 = time()
        block_change = capture.did_block_change()
        if block_change:
            capture.update_last_board()

        if capture.exists_controllable_piece():
            btnArr = neat.get_movements(capture, block_change)
            emulator.emulate_tetris(btnArr)
            
        neat.print_fitness()
    else:
        emulator.stop_input()

capture.stop()
emulator.close()