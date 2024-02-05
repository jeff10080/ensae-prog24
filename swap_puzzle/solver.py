from grid import Grid
from graph import Graph

class Solver(): 
    """
    A solver class, to be implemented.
    """
    def __init__(self,g): # g = grid to solve
        self.g = g.copy()
        self.state = self.g.state
        self.m = g.m
        self.n = g.n
    
    def move_seq(self, i1, i2, j1, j2):
        swap_h, swap_v = [], []

        if j2 - j1 > 0:
            swap_h.extend(((i1, y), (i1, y + 1)) for y in range(j1, j2))

        if j2 - j1 < 0:
            swap_h.extend(((i1, y), (i1, y - 1)) for y in range(j1, j2, -1))

        if i2 - i1 > 0:
            swap_v.extend(((x, j2), (x + 1, j2)) for x in range(i1, i2))

        if i2 - i1 < 0:
            swap_v.extend(((x, j2), (x - 1, j2)) for x in range(i1, i2, -1))

        swap_seq = swap_h + swap_v
        return swap_seq

    
    def find(self,i2,j2):
        a = i2*self.n + j2 +1
        for i1 in range(self.m):
            for j1 in range(self.n):
                if self.state[i1][j1] == a:
                    return i1,j1
    
    def fetch(self,i2,j2):
        i1,j1 = self.find(i2,j2)
        return self.move_seq(i1,i2,j1,j2) 
    
    def get_solution(self,g):
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        
        solution = []
        for i in range(self.m):
            for j in range(self.n):
                swapseq = self.fetch(i, j)
                solution += swapseq
                self.g.swap_seq(swapseq)

                # Check if the grid is sorted
                if self.g.is_sorted():
                    return solution  # Stop if the grid is sorted
        return solution
    
    def get_solution_bfs(self,g):
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        grid_sorted = Grid(self.m,self.n)
        G = Graph()
        G.construct_grid_graph(g)
        dst_node = grid_sorted.__hash__()
        return G.graph[dst_node]



        