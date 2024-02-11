# This will work if ran from the root folder ensae-prog24
import sys
sys.path.append("swap_puzzle/")
from grid import Grid

import unittest 

class Test_Swap(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid1.in")
        print(f"Initial state: {grid.state}")
        
        swaps = [((0, 0), (0, 1)), ((0, 0), (1, 0))]
        grid.swap_seq(swaps)
        
        self.assertEqual(grid.state, [[3, 1], [2, 4], [5, 6], [8, 7]])

if __name__ == '__main__':
    unittest.main()
