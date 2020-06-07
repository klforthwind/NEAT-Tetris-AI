import numpy as np

class Piece:

    def __init__(self, data=[[0,0,0,0],[0,0,0,0]]):
        mins = np.amin(data, axis=1)
        data = np.copy(data)
        data[0] = np.subtract(data[0], mins[0])
        data[1] = np.subtract(data[1], mins[1])
        self.hash = (data[0][0]+data[0][1]*2+data[0][2]*4+data[0][3]*8+
            data[1][0]*16+data[1][1]*32+data[1][2]*64+data[1][3]*128)

    def __eq__(self, other):
        return (isinstance(other, Piece) and (self.hash == other.hash))

    def __hash__(self):
        return hash((self.hash))
