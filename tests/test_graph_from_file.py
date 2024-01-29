# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from graph import Graph

class Test_GraphLoading(unittest.TestCase):
    def test_Graph1(self):
        g = Graph.graph_from_file("input/graph2.in")
        self.assertEqual(g.nb_nodes, 20)
        self.assertEqual(g.nb_edges, 20)
        self.assertEqual(g.graph[17],[10, 19, 7,18,2])

if __name__ == '__main__':
    unittest.main()
