from node import *
import pytest

def test_node():
    node = Node()
    assert len(node.movement) == 0
    assert len(node.board) == 0
    assert node == node
    assert node.shape == None