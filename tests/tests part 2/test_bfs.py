# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from graph import Graph

class Test_bfs(unittest.TestCase):
    def test_graph2(self):
        graph = Graph.graph_from_file("input/graph2.in")
        self.assertEqual(graph.bfs(9,16)[1], [9, 7, 17, 10, 12, 16])
        self.assertEqual(graph.bfs(9,11), None)

if __name__ == '__main__':
    unittest.main()
