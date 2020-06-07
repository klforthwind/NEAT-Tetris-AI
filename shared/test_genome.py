from genome import *
import pytest

def test_genome():
    g1 = Genome()
    assert len(g1.moves) == 0
    for i in range(10):
        g1.mutate()
    g2 = Genome()
    assert g1 != g2
