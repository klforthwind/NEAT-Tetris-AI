from filemanager import FileManager
from switchdata import SwitchData
from emulator import Emulator
from neat import NEAT
from time import time

t0 = time()

capture = SwitchData()
capture.start()

population_size = 50
neat = NEAT(population_size)

file_manager = FileManager()
loadable = file_manager.loadable()
if loadable[0]:
    neat.repopulate(loadable[1])
else:
    neat.create_population()

port = "COM3"
emulator = Emulator(port)

while True:
    if (capture.should_quit()):
        emulator.stop_input()
        break

    capture.process_capture()

    if capture.should_press_a() or capture.is_dead():
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
        else:
            emulator.stop_input()
            
        neat.print_fitness()
    else:
        emulator.stop_input()

capture.stop()
emulator.close()