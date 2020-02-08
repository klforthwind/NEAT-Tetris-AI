from node_manager import *
from file_manager import *
from graphics import *
from tetris import *
from neat import *

if __name__ == "__main__":

    population_size = 16
    file_manager = FileManager()
    loadable = file_manager.loadable()
    neat = NEAT(population_size, loadable)

    node_manager = NodeManager()
    view = AsciimaticView()

    # max_score = 0
    tetris = Tetris()

    while True:

        if tetris.game_over:
            score = tetris.score
            # max_score = max(score, max_score)
            neat.genomes[neat.current_genome].fitness = score
            # print("Max score:", max_score)
            tetris = Tetris()
            neat.loop()

        best_node = node_manager.analyze(tetris, neat.get_current_nn())

        if best_node != None:
            moves = best_node.movement 
            for move in moves:
                tetris.perform_movement(move)
                view.refresh(tetris.board, moves, [move])

        tetris.update()
