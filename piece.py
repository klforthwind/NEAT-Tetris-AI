
class Piece:

    def __init__(self, data=[[0,0,0,0],[0,0,0,0]]):
        self.data = data

    def __eq__(self, other):
        return (isinstance(other, Piece) and (self.data == self.data))

    def __hash__(self):
        return hash((self.data))