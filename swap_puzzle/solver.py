from grid import Grid

class Solver(): 
    """
    A solver class, to be implemented.
    """
    def __init__(self,g): # g = grid to solve
        self.g = g
        self.state = g.state
        self.m = g.m
        self.n = g.n
    
    def move_seq(self,i1,i2,j1,j2):
        swap_h,swap_v = [],[]
        if j2-j1>0:
            for y in range(j1,j2):
                swap_h.append((i1,y),(i1,y + 1))
            #swp_h = [((i1,y),(i1,y + 1)) for y in range(j1,j2)]
        if j2-j1<0:
            for y in range(j1,j2,-1):
                swap_h.append((i1,y),(i1,y - 1))
            #swp_h = [((i1,y),(i1,y - 1)) for y in range(j1,j2,-1)]
        if i2-i1>0:
            for x in range(i1,i2):
                swap_v.append((x,j2,),(x + 1,j2))
            #swp_v = [((x,j2),(x + 1,j2)) for x in range(i1,i2)]
        if i2-i1<0:
            for x in range(i1,i2,-1):
                swap_v.append((x,j2),(x - 1,j2))
            #swp_v = [((x,j2),(x - 1,j2)) for x in range(i1,i2,-1)]
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
        print(i1,j1)
        return self.move_seq(i1,i2,j1,j2) 
    
    def get_solution(self):
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        
        solution = []
        for i in range(self.m):
            for j in range(self.n):
                print(self.state)
                swapseq = self.fetch(i,j)
                print(swapseq)
                solution += swapseq
                self.swap_seq(swapseq)
        return solution


        