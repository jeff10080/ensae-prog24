# This will work if ran from the root folder ensae-prog24
import sys 

sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from game import Game 


class Test_Display(unittest.TestCase):
    def test_display(self):
        g = Game(Grid(5,5))
        g.display()
        
        

if __name__ == '__main__':
    unittest.main()


