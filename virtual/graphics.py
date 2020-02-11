from asciimatics.screen import Screen
from time import sleep

class AsciimaticView:

    def __init__(self):
        self.screen = Screen.open()
        self.color = {
            1 : Screen.COLOUR_CYAN,
            2 : Screen.COLOUR_BLUE,
            3 : Screen.COLOUR_YELLOW,
            4 : Screen.COLOUR_YELLOW,
            5 : Screen.COLOUR_GREEN,
            6 : Screen.COLOUR_RED,
            7 : Screen.COLOUR_RED,
            8 : Screen.COLOUR_BLUE,
            99 : Screen.COLOUR_BLACK
        }

    def show_board(self, board):
        for y in range(22):
            x = 0
            for c in board[y*14 : (y+1)*14]:
                if c in self.color:
                    string = (u'[]',u'██')[c==99]
                    self.screen.print_at(string, x, y, self.color[c], Screen.A_BOLD)
                else:
                    self.screen.print_at(u'  ', x, y, Screen.COLOUR_BLUE, Screen.A_BOLD)
                x += 2

    def print(self, analysis, line):
        lst = ",".join(analysis)
        self.screen.print_at(lst, 0, line, Screen.COLOUR_RED, Screen.A_BOLD)

    def refresh(self, board, txt1, txt2):
        self.screen.clear()
        self.show_board(board)
        self.print(txt1, 25)
        self.print(txt2, 26)
        self.screen.refresh()
        sleep(0.05)
