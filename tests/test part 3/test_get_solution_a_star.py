# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from solver import Solver
from graph import Graph

class Test_GetSolutions(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid4.in")
        s = Solver(grid)
        self.assertEqual(grid.is_sorted(), False)
        swap_sol = s.get_solution_a_star(grid)
        graph = Graph()
        graph.construct_a_star(grid)
        grid.swap_seq(swap_sol)
        self.assertEqual(grid.is_sorted(), True)


if __name__ == '__main__':
    unittest.main()

