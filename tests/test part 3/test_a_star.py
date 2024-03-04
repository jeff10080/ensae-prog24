# This will work if ran from the root folder ensae-prog24
import sys 

sys.path.append("swap_puzzle/")

import unittest 
from graph import Graph
from grid import Grid

class Test_bfs(unittest.TestCase):
    def test_a_star(self):
        grid= Grid.grid_from_file("input/grid1.in")
        graph = Graph()
        a = graph.construct_grid_graph_bfs(grid)
        g_sorted = Grid(grid.m,grid.n)
        self.assertEqual(graph.a_star(grid,g_sorted),[grid.__hash__(),g_sorted.__hash__()] )
        self.assertEqual(graph.bfs(9,11), None)

if __name__ == '__main__':
    unittest.main()
