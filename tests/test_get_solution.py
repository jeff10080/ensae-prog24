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
        print (s)
        swap_sol = s.get_solution()
        grid_sol = grid.copy()
        print (swap_sol)
        grid_sol.swap_seq(swap_sol)
        print(grid_sol)
        self.assertEqual(grid_sol.is_sorted(), True) 

if __name__ == '__main__':
    unittest.main()