import os

from Definitions.state import State
from algorithms.search_algorithms.a_star.run_weighted_astar import run_weighted
from algorithms.search_algorithms.dfbnb.run_dfbnb import run_dfbnb
from experiments.experiment import run_other, mother_of_tests
from experiments.tests.get_max_test import test_new_spqr
from helpers import index_to_node_stuff, COMMON
from helpers.COMMON import *
from helpers.graph_builder_funcs import generate_hard_grid, parse_graph_png, crop_and_parse_graph, \
    generate_aaai_showcase, generate_aaai_showcase_original
from helpers.helper_funcs import draw_grid, flatten
from heuristics.heuristics_interface_calls import spqr_recursive_h, ex_pairs_using_spqr, ex_pairs_using_old_spqr, \
    snake_only_prune
import time as t


def run_mom_test():
    #choose hypercube or mazes

    # mother_of_tests(algorithm=run_weighted, world=CUBE_MODE, mode=SNAKE_MODE, n=6)
    mother_of_tests(algorithm=run_weighted, world=MAZE_MODE, mode=None, n=None)



def compare_alt_to_astar():
    grid, graph, start, target, index_to_node = crop_and_parse_graph('/mnt/c/Users/itay/Desktop/notebooks/all_graphs/graph_721.png', 20, 20)
    index_to_node_stuff.index_to_node = index_to_node
    index_to_node_stuff.grid = grid
    draw_grid("", graph, grid, start, target, index_to_node, path=[])

    time_start = t.time()
    path_alt = run_other(graph, start, target)
    time_alt = t.time() - time_start

    print(time_alt)
    print(len(path_alt))
    draw_grid("alt", graph, grid, start, target, index_to_node, path=path_alt)

    time_start = t.time()
    path_astar = run_weighted(ex_pairs_using_spqr, graph, start, target, 1, 50000, 2000, True, mode=LSP_MODE)[0]
    time_astar = t.time() - time_start

    print(time_astar)
    print(len(path_astar))

    draw_grid("astar", graph, grid, start, target, index_to_node, path=path_alt)


def recursive_vs_pairs():
    grid, graph, start, target, index_to_node = crop_and_parse_graph(
        '/mnt/c/Users/itay/Desktop/notebooks/all_graphs/grids_20/graph_17.png', 20, 20)
    index_to_node_stuff.index_to_node = index_to_node
    index_to_node_stuff.grid = grid
    ares = run_weighted(test_new_spqr, graph, start, target, 1, 50000, 2000, True, mode=LSP_MODE)


def showcase_work():
    _, grid, graph, start, target, index_to_node = generate_aaai_showcase_original()
    index_to_node_stuff.index_to_node = index_to_node
    index_to_node_stuff.grid = grid
    state = State(start,[],graph.nodes)
    old_val = snake_only(state, graph,target,False)
    draw_grid("old", graph, grid, start, target, index_to_node, path=flatten(COMMON.pairs_idk))
    new_val = snake_only_prune(state, graph,target,False)
    draw_grid("new", graph, grid, start, target, index_to_node, path=flatten(COMMON.pairs_idk))
    print(old_val, new_val)



if __name__ == '__main__':
    # t.sleep(7000)
    run_mom_test()
    # showcase_work()

