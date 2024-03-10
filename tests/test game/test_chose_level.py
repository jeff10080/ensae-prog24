# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from game import Game 
import pygame


class Test_Choose_Level(unittest.TestCase):
    def test_choose_level(self):
        pygame.init()
        grid = Grid(4,4)
        g = Game(grid)
        l = g.choose_level()
        print(l)
        
        

if __name__ == '__main__':
    unittest.main()
