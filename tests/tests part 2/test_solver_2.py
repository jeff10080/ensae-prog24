# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from graph import Graph
from grid import Grid

class TestGraphGrid(unittest.TestCase):
    def test_construct_grid_graph(self):

        # Call the function to construct the grid graph

        graph= Graph()
        graph.construct_grid_graph(Grid.grid_from_file("input/grid1.in"))
        # Assert that the number of nodes ( 4!)

        self.assertEqual(graph.nb_nodes, 24)
        self.assertEqual(graph[])

        # Assert that the number of edges in the graph is as expected
        self.assertEqual(graph.nb_edges, expected_number_of_edges)

        # Add more assertions based on your testing requirements


if __name__ == '__main__':
    unittest.main()
