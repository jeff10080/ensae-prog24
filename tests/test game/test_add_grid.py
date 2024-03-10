# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from solver import Solver

class Test_add_barriers(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid4.in")
        for _ in range (10):
            grid.add_barriers()
            print(grid.barriers) 
            self.assertEqual(grid.valid_barriers(), True)

        s= Solver(grid)
        swap_sol= s.get_solution_a_star(grid)
        
        swap_set = set(swap_sol)
        if  swap_set.intersection(grid.barriers):
            AssertionError
        
       
        
        #barrière complète
        
        
        


if __name__ == '__main__':
    unittest.main()

