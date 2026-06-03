

import unittest 
from swap_puzzle.grid import Grid
from swap_puzzle.game import Game 


class Test_Display(unittest.TestCase):
    def test_display(self):
        g = Game(Grid(5,5))
        g.display()
        

if __name__ == '__main__':
    unittest.main()


