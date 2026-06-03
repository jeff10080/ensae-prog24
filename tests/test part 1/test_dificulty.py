# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from  game import Game

class Test_Swap(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid2.in")
        sorted_grid = Grid(grid.m,grid.n)
        self.assertEqual(grid.compare_difficulty(sorted_grid), False)
        
        
if __name__ == '__main__':
    unittest.main()