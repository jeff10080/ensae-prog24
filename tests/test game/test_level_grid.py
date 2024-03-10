import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from game import Game

class Test_level_grid(unittest.TestCase):
    def test_display(self):
        grid =Grid(5,5).level_grid(10)
        # peut ne pas marcher à tous les coups 
        self.assertEqual(grid.heuristic(), 10)
        
if __name__ == '__main__':
    unittest.main()