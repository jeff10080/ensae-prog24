# This will work if ran from the root folder ensae-prog24
import sys
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid

class Test_Heuristic(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid1.in")
        grid2 = Grid.grid_from_file("input/grid2.in")
        grid3 = Grid.grid_from_file("input/grid3.in")
        heuristic = grid.heuristic()
        heuristic2 = grid2.heuristic()
        heuristic3 = grid3.heuristic()
        self.assertEqual(heuristic, 1)
        self.assertEqual(heuristic2, 4)
        self.assertEqual(heuristic3, 4)
        
if __name__ == '__main__':
    unittest.main()
