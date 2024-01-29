# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from solver import Solver

class Test_GetSolutions(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid3.in")
        s = Solver(grid)
        self.assertEqual(grid.is_sorted(), False)
        swap_sol = s.get_solution()
<<<<<<< HEAD
        grid_sol = grid.copy()
        grid_sol.swap_seq(swap_sol)
        print(grid_sol)
        self.assertEqual(grid_sol.is_sorted(), True)
=======
        grid = grid.copy()
        grid.swap_seq(swap_sol)
        print(grid)
        self.assertEqual(grid.is_sorted(), True)
>>>>>>> 7909dfc3d0b7bcb6cad30bc200d4a19170b693f3

if __name__ == '__main__':
    unittest.main()
