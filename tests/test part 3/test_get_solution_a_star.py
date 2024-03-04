# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from solver import Solver
from graph import Graph

class Test_GetSolutions(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid0.in")
        grid_sol = grid.copy()
        s = Solver(grid)
        self.assertEqual(grid.is_sorted(), False)
        swap_sol = s.get_solution_a_star(grid)
        print(swap_sol)
        graph = Graph()
        graph.construct_grid_graph(grid)
        print(graph.vertices)
        grid.swap_seq(swap_sol)
        self.assertEqual(grid.is_sorted(), True)


if __name__ == '__main__':
    unittest.main()

