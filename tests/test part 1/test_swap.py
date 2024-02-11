# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid

class Test_Swap(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid1.in")
        grid2 = grid.copy()
        grid.swap((3, 0), (3, 1))
        self.assertEqual(grid.state, [[1, 2], [3, 4], [5, 6], [7, 8]])
        grid2.swap((0, 0), (1, 0))
        self.assertEqual(grid2.state, [[3, 2], [1, 4], [5, 6], [8, 7]])

        
if __name__ == '__main__':
    unittest.main()
