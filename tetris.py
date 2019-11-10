from filemanager import FileManager
from switchdata import SwitchData
from emulator import Emulator
from neat import NEAT

emulator = Emulator("COM3")
capture = SwitchData()
capture.start()

population_size = 50
file_manager = FileManager()
loadable = file_manager.loadable()
neat = NEAT(population_size, loadable)

while True:
    if (capture.should_quit()):
        break

    capture.process_capture()
    if capture.should_press_a() or capture.game_over():
        emulator.press_a()
        neat.loop()
        capture.clear()

    block_change = capture.did_block_change()
    if block_change:
        capture.update_last_board()

    if capture.exists_controllable_piece() and not neat.has_placed():
        btnArr = neat.get_movements(capture, block_change)
        emulator.emulate_tetris(btnArr)
        neat.print_fitness()

capture.stop()
emulator.close()
