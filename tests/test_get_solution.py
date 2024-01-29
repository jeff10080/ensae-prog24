# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from solver import Solver

class Test_IsSorted(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid3.in")
        self.assertEqual(grid.is_sorted(), False)
        sol = Solver.get_solution(grid)
        self.assertEqual(sol.is_sorted(), True)

if __name__ == '__main__':
    unittest.main()
