# This will work if ran from the root folder ensae-prog24
import sys 

sys.path.append("swap_puzzle/")

import unittest 
from graph import Graph
from grid import Grid

class Test_bfs(unittest.TestCase):
    def test_a_star(self):
        grid= Grid.grid_from_file("input/grid1.in")
        initial_node = grid.__hash__()
        graph = Graph()
        a = graph.construct_grid_graph_bfs(grid)
        node_sorted = Grid(grid.m,grid.n).__hash__()
        self.assertEqual(graph.a_star(initial_node,node_sorted),[initial_node,node_sorted] )

if __name__ == '__main__':
    unittest.main()
