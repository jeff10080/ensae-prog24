# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from game import Game 
from solver import Solver


class Test_Choose_Level(unittest.TestCase):
    def test_choose_level(self):
        grid = Grid(4,4)
        g = Game(grid)
        g.choose_level()
        print(g.state)
        
        

if __name__ == '__main__':
    unittest.main()
