from inspect import getfile, currentframe
from os.path import dirname, abspath
import sys

currentdir = dirname(abspath(getfile(currentframe())))
srcdir = dirname(currentdir) + "/src/"
sys.path.insert(0, srcdir) 

from node_manager import *
import pytest

def test_node_manager():
    nm = NodeManager()

def test_create_copy():
    pass

def test_analyze_switch():
    pass

def test_analyze():
    pass

def test_get_node_list():
    pass
