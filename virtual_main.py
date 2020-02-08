from node_manager import *
from filemanager import *
from graphics import *
from tetris import *
from neat import *

if __name__ == "__main__":

    population_size = 16
    file_manager = FileManager()
    loadable = file_manager.loadable()
    neat = NEAT(population_size, loadable)

    node_manager = NodeManager()
    # view = AsciimaticView()

    max_score = 0
    scores = []

    tetris = Tetris()

    for x in range(1):
        tetris = Tetris()
        node_list = []
        
        while not tetris.game_over:
            best_node = node_manager.analyze(tetris)
            node_list.append(best_node.hexcode)

            moves = best_node.movement 
            for move in moves:
                tetris.perform_movement(move)
                # view.refresh(tetris.board, moves, [move])

            tetris.update()
        
    while True:
        # print("Max score:", max_score)
        # print("Scores: ",end = "")
        # print(scores)

        if tetris.game_over:
            score = tetris.score
            max_score = score if score > max_score else max_score
            neat.genomes[neat.current_genome].fitness = score
            scores.append(score)
            print("Max score:", max_score)
            print("Scores: ",end = "")
            print(scores)
            tetris = Tetris()
            neat.loop()
            if neat.current_genome == 0 or len(scores) > 32:
                scores = []

        for i in range(8):
            input_nodes = tetris.get_input_nodes()
            block, rotation = tetris.current["key"], tetris.current["r"]
            hold, q1 = tetris.get_hold_and_q1()

            btn_array = neat.get_movements(block, rotation, hold, q1, input_nodes)

            tetris.perform_movement(btn_array)

        tetris.update()
        # clear()
        # tetris.print_data()
