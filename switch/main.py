import sys
sys.path.append("../shared")
from node_manager import *
from file_manager import *
from switchdata import *
from emulator import *
from tetris import *
from neat import *

if __name__ == "__main__":

    emulator = Emulator("COM3")
    capture = SwitchData()
    capture.start()

    population_size = 16
    file_manager = FileManager()
    loadable = file_manager.loadable()
    neat = NEAT(population_size, loadable)

    node_manager = NodeManager()

    move_set = []
    new_board = []

    while not capture.should_quit():

        capture.process_capture()
        if capture.should_press_a() or capture.game_over():
            print('wdawd')
            emulator.press_a()
            neat.loop()
            capture.clear()

        block_change = capture.did_block_change()
        if block_change:
            emulator.wait(0.4)
            
            # capture.update_last_board()

        if len(move_set) == 0 and capture.exists_controllable_piece() and capture.queue_filled():
            if len(new_board):
                capture.past_tetris.board = list(new_board)
            best_node = node_manager.analyze_switch(capture, neat.get_current_nn())

            if best_node != None:
                move_set = best_node.movement
                new_board = list(best_node.board)
                print(move_set)

        if len(move_set):
            move = move_set.pop(0)
            emulator.perform_movement(move)
            # neat.print_fitness()

    capture.stop()
    emulator.close()
