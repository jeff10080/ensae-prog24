# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from game import Game

class Test_GridLoading(unittest.TestCase):
    def test_grid1(self):
        g = Grid.grid_from_file("input/grid1.in")
        game = Game(g)
        game.display()

if __name__ == '__main__':
    unittest.main()
