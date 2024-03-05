# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid

class Test_Display(unittest.TestCase):
    def test_display(self):
        g = Grid.grid_from_file("input/grid1.in")
        g.display()
        
        

if __name__ == '__main__':
    unittest.main()


