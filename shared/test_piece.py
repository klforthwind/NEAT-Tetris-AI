from piece import *
import pytest

def test_piece():
    p1 = Piece()
    assert p1.hash == 0
    assert p1 == p1
    p2 = Piece([[1,1,1,1],[1,2,3,4]])
    assert p2 != p1
    p3 = Piece([[1,1,1,1],[2,3,4,5]])
    assert p2 == p3

