from node_manager import *
from file_manager import *
from switchdata import *
from emulator import *
from tetris import *
from neat import *

if __name__ == "__main__":

    emulator = Emulator("COM3")
    print("AWda")
    capture = SwitchData()
    capture.start()

    population_size = 16
    file_manager = FileManager()
    loadable = file_manager.loadable()
    neat = NEAT(population_size, loadable)

    node_manager = NodeManager()

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
            emulator.wait(0.2)
            capture.update_last_board()

        if capture.exists_controllable_piece() and capture.queue_filled():
            best_node = node_manager.analyze_switch(capture, neat.get_current_nn())

            if best_node != None:
                moves = best_node.movement 
                for move in moves:
                    emulator.perform_movement(move)
            emulator.emulate_tetris(btnArr)
            neat.print_fitness()

    capture.stop()
    emulator.close()
