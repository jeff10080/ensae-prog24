# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid

class Test_GetSolutions(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid4.in")
        self.assertEqual(grid.valid_barriers(), True)
        grid.barriers = set([((0,0),(0,1)),((1,0),(1,1)),((2,0),(2,1)), ((1,1),(1,2)),((2,1),(2,2)),((3,1),(3,2))])
        self.assertEqual(grid.valid_barriers(), True)
        grid.barriers.add(((3,0),(3,1)))
        #barrière complète
        self.assertNotEqual(grid.valid_barriers(), True)
        
        
        
        


if __name__ == '__main__':
    unittest.main()

