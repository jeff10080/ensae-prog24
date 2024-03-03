"""
This is the graph module. It contains a minimalistic Graph class.
"""
from grid import Grid
from collections import deque
from heapq import *
class Graph:
    """
    A class representing undirected graphs as adjacency lists. 

    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [neighbor1, neighbor2, ...]
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    edges: list[tuple[NodeType, NodeType]]
        The list of all edges
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 

        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = {n:[] for n in nodes}
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.edges = []
        self.vertices = dict()
        
    
    def __str__(self):
        """
        Prints the graph as a list of neighbors for each node (one per line)
        """
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the graph with number of nodes and edges.
        """
        return f"<graph.Graph: nb_nodes={self.nb_nodes}, nb_edges={self.nb_edges}>"

    def add_edge(self, node1, node2):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 
        When adding an edge between two nodes, if one of the ones does not exist it is added to the list of nodes.

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append(node2)
        self.graph[node2].append(node1)
        self.nb_edges += 1
        self.edges.append((node1, node2))
    
    def construct_grid_graph(self, initial_grid):
        """
        Constructs the graph representing all possible states of the swap puzzle starting from the initial grid.

        Parameters:
        -----------
        initial_grid: Grid
            An instance of the Grid class representing the initial state of the puzzle.
        """

        if len(self.graph) == 0:
            self.graph[initial_grid.__hash__()] = []
            self.nb_nodes = 1
            self.nodes.append(initial_grid.__hash__())


        queue = deque([(initial_grid)])

        while queue:
            current_grid = queue.popleft()
            current_node = current_grid.__hash__()
            for i in range(current_grid.m):
                for j in range(current_grid.n):
                    for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                        if 0 <= ni < current_grid.m and 0 <= nj < current_grid.n:
                            new_grid = current_grid.copy()
                            new_grid.swap((i, j), (ni, nj))

                            new_node = new_grid.__hash__()
                            if new_node not in self.graph:
                                queue.append(new_grid)
                            self.add_edge(current_node, new_node)
                            # if (current_node,new_node) not in self.edges:
                            self.vertices[(current_node, new_node)] = (i,j),(ni,nj)
                            self.vertices[(new_node, current_node)] = (i,j),(ni,nj)   


    def bfs(self,src,dst):
        """
        Finds a shortest path from src to dst by BFS.  

        Parameters: 
        -----------
        src: NodeType
            The source node.
        dst: NodeType
            The destination node.

        Output: 
        -------
        path: list[NodeType] | None
            The shortest path from src to dst. Returns None if dst is not reachable from src
        """ 
        deja_vu = []
        path = dict()
        path[src] = [src]
        queue = deque([src])
        while queue != deque():
            u = queue.popleft()
            for v in self.graph[u]:
                if v == dst:
                    return path[u] + [v]
                path[v] = path[u] + [v]
                queue.append(v)
            deja_vu.append(u)
        return None
    
    def construct_grid_graph_bfs(self, initial_grid):
        """
        Constructs the graph representing all possible states of the swap puzzle starting from the initial grid.

        Parameters:
        -----------
        initial_grid: Grid
            An instance of the Grid class representing the initial state of the puzzle.
        """

        if len(self.graph) == 0:
            self.graph[initial_grid.__hash__()] = []
            self.nb_nodes = 1
            self.nodes.append(initial_grid.__hash__())
        sorted_node = Grid(initial_grid.m,initial_grid.n).__hash__()


        queue = deque([(initial_grid)])

        while queue:
            current_grid = queue.popleft()
            current_node = current_grid.__hash__()
            for i in range(current_grid.m):
                for j in range(current_grid.n):
                    for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                        if 0 <= ni < current_grid.m and 0 <= nj < current_grid.n:
                            new_grid = current_grid.copy()
                            new_grid.swap((i, j), (ni, nj))

                            new_node = new_grid.__hash__()
                            if new_node not in self.graph:
                                queue.append(new_grid)
                            self.add_edge(current_node, new_node)
                            # if (current_node,new_node) not in self.edges:
                            self.vertices[(current_node, new_node)] = (i,j),(ni,nj)
                            self.vertices[(new_node, current_node)] = (i,j),(ni,nj)
                            if new_node == sorted_node:
                                return None
                            
    #https://www.redblobgames.com/pathfinding/a-star/implementation.html                       
    
                
    def heuristic(self,node):
        heuristic = 0
        pos_m,pos_n = 0,0
        m,n= len(node),len(node[0])
        for i in range(m):
            for j in range (n):
                pos_m,pos_n = i,j
                dest_m, dest_n = (node[i][j]-1)// n, (node[i][j]-1) %n #parce qu'on commence à 1
                print(dest_m,dest_n)
                heuristic += abs(dest_m -pos_m) + abs(dest_n -pos_n)
                print(heuristic)
        return heuristic//2

        

    def a_star(self, start, goal):
        heap = []
        heappush(heap, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while heap:
            current_cost, current = heappop(heap)

            if current == goal:
                break

            for next_node in self.graph[current]:
                new_cost = cost_so_far[current] + 1  # Assuming each edge has a cost of 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(next_node)
                    heappush(heap, (priority, next_node))
                    came_from[next_node] = current

        return came_from, cost_so_far
        
    @classmethod
    def graph_from_file(cls, file_name):
        """
        Reads a text file and returns the graph as an object of the Graph class.

        The file should have the following format: 
            The first line of the file is 'n m'
            The next m lines have 'node1 node2'
        The nodes (node1, node2) should be named 1..n

        Parameters: 
        -----------
        file_name: str
            The name of the file

        Outputs: 
        -----------
        graph: Graph
            An object of the class Graph with the graph from file_name.
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            graph = Graph(range(1, n+1))
            for _ in range(m):
                edge = list(map(int, file.readline().split()))
                if len(edge) == 2:
                    node1, node2 = edge
                    graph.add_edge(node1, node2) # will add dist=1 by default
                else:
                    raise Exception("Format incorrect")
        return graph

