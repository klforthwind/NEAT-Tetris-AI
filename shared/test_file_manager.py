from file_manager import *
import pytest

def test_file_manager():
    fm = FileManager()
    assert fm.suffix == '-0.txt'
    assert fm.suffix != '-0.py'
    loadable = fm.loadable()
    assert len(loadable) == 2
    assert type(loadable[0]) == bool
    assert 0 <= loadable[1]