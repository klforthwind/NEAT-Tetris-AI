from inspect import getfile, currentframe
from os.path import dirname, abspath
import sys

currentdir = dirname(abspath(getfile(currentframe())))
srcdir = dirname(currentdir) + "/src/"
sys.path.insert(0, srcdir) 

from node import *
import pytest

def test_node():
    node = Node()
    assert len(node.movement) == 0
    assert len(node.board) == 0
    assert node == node
    assert node.shape == None