# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from graph import Graph
from grid import Grid

class TestGraphGrid(unittest.TestCase):
    def test_construct_grid_graph(self):
        # Create a grid from file or any other method you prefer
        initial_grid = Grid.grid_from_file("input/grid3.in")

        # Create an instance of the Graph class
        graph = Graph()

        # Call the function to construct the grid graph
        graph.construct_grid_graph(initial_grid)

        self.assertEqual(graph.nb_nodes, expected_number_of_nodes)

        # Assert that the number of edges in the graph is as expected
        self.assertEqual(graph.nb_edges, expected_number_of_edges)

        # Add more assertions based on your testing requirements

    def test_bfs(self):
        # Create a graph from file or any other method you prefer
        graph = Graph.graph_from_file("input/graph2.in")

        # Add assertions for the bfs function
        self.assertEqual(graph.bfs(9, 16), [9, 7, 17, 10, 12, 16])
        self.assertEqual(graph.bfs(9, 11), None)

if __name__ == '__main__':
    unittest.main()
