import numpy as np

class Piece:

    def __init__(self, data=[[0,0,0,0],[0,0,0,0]]):
        mins = np.amin(data, axis=1)
        self.data = np.copy(data)
        self.data[0] = np.subtract(data[0], mins[0])
        self.data[1] = np.subtract(data[1], mins[1])
        print(self.data)

    def __eq__(self, other):
        return (isinstance(other, Piece) and (self.data == self.data))

    def __hash__(self):
        return hash((self.data[0][0],self.data[0][1],self.data[0][2],self.data[0][3],
            self.data[1][0],self.data[1][1],self.data[1][2],self.data[1][3]))