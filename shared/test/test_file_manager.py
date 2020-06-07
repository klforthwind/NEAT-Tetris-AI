from inspect import getfile, currentframe
from os.path import dirname, abspath
import sys

currentdir = dirname(abspath(getfile(currentframe())))
srcdir = dirname(currentdir) + "/src/"
sys.path.insert(0, srcdir) 

from file_manager import *
import pytest

def test_file_manager():
    fm = FileManager()
    assert fm.suffix == '-0.txt'
    assert fm.suffix != '-0.py'
    loadable = fm.loadable()
    assert len(loadable) == 2
    assert type(loadable[0]) == bool
    assert -1 <= loadable[1]