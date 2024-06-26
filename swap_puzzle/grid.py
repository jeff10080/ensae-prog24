import copy
"""
This is the grid module. It contains the Grid class and its associated methods.
"""
import pygame
import random
import sys


class Grid():
    """
    A class representing the grid from the swap puzzle. It supports rectangular grids. 

    Attributes: 
    -----------
    m: int
        Number of lines in the grid
    n: int
        Number of columns in the grid
    state: list[list[int]]
        The state of the grid, a list of list such that state[i][j] is the number in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..m and columns are numbered 0..n.
    """
    
    def __init__(self, m, n, initial_state=None):
        """
        Initializes the grid.

        Parameters:
        -----------
        m: int
            The number of rows in the grid
        n: int
            The number of columns in the grid
        initial_state: list[list[int]]
            The initial state of the grid. Default is empty (then the grid is created sorted).
        """

        

        self.m = m
        self.n = n
        if not initial_state:
            initial_state = [list(range(i * n + 1, (i + 1) * n + 1)) for i in range(m)]
        self.state = initial_state

    

    def display(self):
        pygame.init()

        width = self.n * 100
        height = self.m * 100

        screen = pygame.display.set_mode((width, height + 100))  # Ajout de l'espace pour le bouton

        for i in range(self.m):
            for j in range(self.n):
                pygame.draw.rect(screen, (255, 255, 255), (j * 100, i * 100, 100, 100))
                font = pygame.font.Font(None, 72)
                text = font.render(str(self.state[i][j]), True, (0, 0, 0))
                text_rect = text.get_rect(center=(j * 100 + 50, i * 100 + 50))
                screen.blit(text, text_rect)

        # Dessiner le bouton Quitter
        pygame.draw.rect(screen, (255, 0, 0), (0, height, width, 200))  # Rectangle rouge pour le bouton Quitter
        font = pygame.font.Font(None, 72)
        text = font.render("Quitter", True, (255, 255, 255))
        text_rect = text.get_rect(center=(width // 2, height + 50))
        screen.blit(text, text_rect)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Vérifier si le clic de la souris est dans le rectangle du bouton Quitter
                    if 0 < event.pos[0] < width and height < event.pos[1] < height + 100:
                        pygame.quit()
                        return


    def __hash__(self):
        state_tuple = tuple(tuple(self.state[i]) for i in range(self.m))
        return state_tuple #hash ne marche que sur un tuple
    def __eq__(self, other):
       return other and self.m == other.m and self.n == other.n and self.state == other.state


    
    def copy(self):
        return Grid(self.m,self.n,copy.deepcopy(self.state)) #ne marchait pas avec copy
    
    def __str__(self): 
        """
        Prints the state of the grid as text.
        """
        output = f"The grid is in the following state:\n"
        for i in range(self.m): 
            output += f"{self.state[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: m={self.m}, n={self.n}>"

    def is_sorted(self):
        """
        Checks is the current state of the grid is sorted and returns the answer as a boolean.
        """
        # TODO: implement this function (and remove the line "raise NotImplementedError").

        for i in range(self.m):
            for j in range(self.n):
                if self.state[i][j] != i*self.n + j+1: # Number in sorted grid square (i,j) = i*n + j+1
                    return False
        return True
    
    def swap(self, cell1, cell2):
        """
        Implements the swap operation between two cells. Raises an exception if the swap is not allowed.

        Parameters: 
        -----------
        cell1, cell2: tuple[int]
            The two cells to swap. They must be in the format (i, j) where i is the line and j the column number of the cell. 
        """
        i1, j1, i2, j2 = cell1[0], cell1[1], cell2[0], cell2[1]
        if self.test_valid_swap(cell1,cell2):
            self.state[i1][j1],self.state[i2][j2] = self.state[i2][j2],self.state[i1][j1]
        else:
            raise ValueError(f"Invalid swap: {cell1} and {cell2}")

    def test_valid_swap(self,cell1,cell2):
        i1,j1,i2,j2 = cell1[0],cell1[1],cell2[0],cell2[1]
        return (abs(i1-i2) == 1 and abs(j1-j2) == 0) or (abs(i1-i2) == 0 and abs(j1-j2) == 1)



    def swap_seq(self, cell_pair_list):
        """
        Executes a sequence of swaps. 

        Parameters: 
        -----------
        cell_pair_list: list[tuple[tuple[int]]]
            List of swaps, each swap being a tuple of two cells (each cell being a tuple of integers). 
            So the format should be [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """ 
        if len(cell_pair_list) < 2:
            return None
        for i in range(len(cell_pair_list)):
            self.swap(cell_pair_list[i][0], cell_pair_list[i][1])
        # for swap_call in cell_pair_list:
        #     self.swap(swap_call[0], swap_call[1])

    @classmethod
    def grid_from_file(cls, file_name): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "m n" 
            - next m lines contain n integers that represent the state of the corresponding cell

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            m, n = map(int, file.readline().split())
            initial_state = [[] for i_line in range(m)]
            for i_line in range(m):
                line_state = list(map(int, file.readline().split()))
                if len(line_state) != n: 
                    raise Exception("Format incorrect")
                initial_state[i_line] = line_state
            grid = Grid(m, n, initial_state)
        return grid
