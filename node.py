
class Node:
    x = y = rot = 0
    shape, hexcode = None, None
    height = holes = completed_lines = rating = 0
    movement = []

    def __eq__(self, other):
        return (isinstance(other, Node) and (self.x == other.x) 
            and (self.y == other.y) and (self.rot == other.rot))

    def __hash__(self):
        return hash((self.x, self.y, self.rot))