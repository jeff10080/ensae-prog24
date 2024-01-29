from grid import Grid

class Solver(Grid): 
    """
    A solver class, to be implemented.
    """
    def __init__(self,m,n):
        self.m = m
        self.n = n
    

    def get_solution(self):
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        
        state_copy = self.state.copy()
        
        def move_seq(self,i1,i2,j1,j2):
            swap_h,swap_v = [],[]
            if j2-j1>0:
                swp_h = [((i1,y),(i1,y + 1)) for y in range(j1,j2)]
            if j2-j1<0:
                swp_h = [((i1,y),(i1,y - 1)) for y in range(j1,j2,-1)]
            if i2-i1>0:
                swp_v = [((x,j2),(x + 1,j2)) for x in range(i1,i2)]
            if i2-i1<0:
                swp_v = [((x,j2),(x - 1,j2)) for x in range(i1,i2,-1)]
            swap_seq = swap_h + swap_v
            return swap_seq

        def find(self,i2,j2):
            a = i2*self.n + j2 +1
            for i1 in range(self.m):
                for j1 in range(self.n):
                    if self.state[i1][j1] == a:
                        return i1,j1
            
        def fetch(self,i2,j2):
            if self.state[i2][j2] == i2*self.n + j2 +1:
                pass
            i1,j1 = find(self,i2,j2)
            swap_seq = move_seq(self,i1,i2,j1,j2)
            return swap_seq
        
        solution = []
        for i in range(self.m):
            for j in range(self.n):
                solution += fetch(self,i,j)
        return solution

        self.state = state_copy

        # TODO: implement this function (and remove the line "raise NotImplementedError").
        # NOTE: you can add other methods and subclasses as much as necessary. The only thing imposed is the format of the solution returned.
        raise NotImplementedError

