from inspect import getfile, currentframe
from os.path import dirname, abspath
import sys

currentdir = dirname(abspath(getfile(currentframe())))
srcdir = dirname(currentdir) + "/src/"
sys.path.insert(0, srcdir) 

from neat import *
import pytest

def test_neat():
    pop_size = 4
    neat = NEAT(pop_size, (True, 0))
    assert neat.pop_size == pop_size
    assert neat.current_genome == 0
    assert len(neat.genomes) == pop_size

def test_create_population():
    pass

def test_repopulate():
    pass

def test_get_current_nn():
    pass

def test_print_fitness():
    pass

def test_loop():
    pass

def test_sort_genomes():
    pass

def test_increase_generation():
    pass

def test_create_next_gen():
    pass

def test_make_child():
    pass

def test_rand_genome():
    pass
