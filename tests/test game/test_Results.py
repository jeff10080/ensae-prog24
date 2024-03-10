# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from game import Game 
import pygame


class Test_Display(unittest.TestCase):
    def test_display(self):
        g = Game(Grid.grid_from_file("input/grid1.in"))
        pygame.init()
        g.Result()
        g2 = Game(Grid(4,4))
        g2.Result()
        
        

if __name__ == '__main__':
    unittest.main()


