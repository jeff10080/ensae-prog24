# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from game import Game 
from solver import Solver


class Test_Display(unittest.TestCase):
    def test_display(self):
        grid = Grid(4,4)
        g = Game(grid)
        g.choose_level()
        grid1 = Grid(g.m,g.n,g.state)
        s = Solver(grid1)
        swap_sol = s.get_solution_a_star(grid)
        print(swap_sol)
        g.display()
        
        

if __name__ == '__main__':
    unittest.main()
