# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from graph import Graph
from grid import Grid

class Test_bfs(unittest.TestCase):
    def test_graph2(self):
        grid = Grid.grid_from_file("input/grid0.in")
        graph = Graph()
        graph.construct_grid_graph(grid)
        print(graph)
        # self.assertEqual(graph.construct_grid_graph(grid))


if __name__ == '__main__':
    unittest.main()
