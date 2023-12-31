# snake spqr pairs
import networkx as nx
import sage.all
from sage.graphs.connectivity import spqr_tree
from sage.graphs.graph import Graph

from helpers import index_to_node_stuff
from helpers.helper_funcs import flatten, intersection, max_disj_set_upper_bound, draw_grid
from heuristics.heauristics.naive_spqr.naive_spqr import get_neighbors_pairs, \
    get_all_spqr_pairs_new


def get_path(s,t, tree):
    tree = tree.networkx_graph()
    start = [x for x in tree.nodes if s in x[1].vertices()][0]
    target = [x for x in tree.nodes if t in x[1].vertices()][0]
    return nx.shortest_path(tree, start, target)


def snake_exclusion_set_spqr(comp, in_node, out_node):
    comp_sage = Graph(comp)
    tree = spqr_tree(comp_sage)
    path = get_path(in_node, out_node, tree)
    path_nodes = set(flatten([x[1].vertices() for x in path]))
    side_nodes = set(flatten([flatten([snake_nodes_of_sn(x, p, tree, comp, in_node, out_node) for x in tree.neighbors(p) if x not in path]) for p in path]))
    nodes = path_nodes.union(side_nodes)
    return nodes

def snake_nodes_of_sn(current_sn, parent_sn, tree, g, s, t):
    nodes = list(current_sn[1].networkx_graph().nodes)
    current_sps = nodes.copy()
    for neighbor in tree.neighbors(current_sn):
        intersection_sps = intersection(neighbor[1].networkx_graph().nodes, current_sps)
        if neighbor == parent_sn or (s not in intersection_sps and t not in intersection_sps and g.has_edge(intersection_sps[0], intersection_sps[1])):
            continue
        nodes += snake_nodes_of_sn(neighbor, current_sn, tree, g, s, t)
    return nodes




def snake_exclusion_set_len_spqr(comp, in_node, out_node):
    return len(snake_exclusion_set_spqr(comp, in_node, out_node))