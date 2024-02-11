# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid
from solver import Solver
from graph import Graph

class Test_GetSolutions(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid3.in")
        G = Graph()
        G.construct_grid_graph(grid)
        print(G.nb_edges)

        # s = Solver(grid)
        # self.assertEqual(grid.is_sorted(), False)
        # swap_sol = s.get_solution_bfs(grid)
        # grid_sol.swap_seq(swap_sol)
        # self.assertEqual(grid_sol.is_sorted(), True) 


if __name__ == '__main__':
    unittest.main()

