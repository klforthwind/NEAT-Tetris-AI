from inspect import getfile, currentframe
from os.path import dirname, abspath
import sys

currentdir = dirname(abspath(getfile(currentframe())))
srcdir = dirname(currentdir) + "/src/"
sys.path.insert(0, srcdir) 

from genome import *
import pytest

def test_genome():
    g1 = Genome()
    assert len(g1.moves) == 0
    for i in range(10):
        g1.mutate()
    g2 = Genome()
    assert g1 != g2
