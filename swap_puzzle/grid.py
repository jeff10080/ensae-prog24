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
        self.selected_cells = []

    

    def display(self):
        pygame.init()

        width = self.n * 100
        height = self.m * 100

        screen = pygame.display.set_mode((width, height + 100))  # Ajout de l'espace pour le bouton

        clock = pygame.time.Clock()  # Créer une horloge pour gérer la vitesse de la boucle principale

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 0 < event.pos[0] < width and height < event.pos[1] < height + 100:
                        running = False
                    clicked_row = event.pos[1] // 100
                    clicked_col = event.pos[0] // 100
                    if 0 <= clicked_row < self.m and 0 <= clicked_col < self.n:
                        clicked_cell = (clicked_row, clicked_col)
                        if len(self.selected_cells) == 1:
                            selected_cell = self.selected_cells[0]
                            if clicked_cell == selected_cell:
                                self.selected_cells = []
                            elif self.test_valid_swap(clicked_cell, selected_cell):
                                self.swap(clicked_cell, selected_cell)
                                self.selected_cells = []
                                if self.is_sorted():
                                    print("YOU WIN")
                                    running = False
                            else:
                                print(f"Invalid swap: {clicked_cell} and {selected_cell}")
                        else:
                            self.selected_cells.append(clicked_cell)

            screen.fill((0, 0, 0))  # Effacer l'écran
            for i in range(self.m):
                for j in range(self.n):
                    cell_rect = pygame.Rect(j * 100, i * 100, 100, 100)
                    pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                    font = pygame.font.Font(None, 72)
                    text = font.render(str(self.state[i][j]), True, (0, 0, 0))
                    text_rect = text.get_rect(center=cell_rect.center)
                    screen.blit(text, text_rect)
                    if (i, j) in self.selected_cells:
                        pygame.draw.rect(screen, (255, 255, 0), cell_rect, 5)

            pygame.draw.rect(screen, (255, 0, 0), (0, height, width, 100))  # Rectangle rouge pour le bouton Quitter
            font = pygame.font.Font(None, 72)
            text = font.render("Quitter", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height + 50))
            screen.blit(text, text_rect)
            

            pygame.display.flip()  # Mettre à jour l'affichage
            clock.tick(30)  # Limiter la vitesse de la boucle principale à 30 images par seconde
        
        if self.is_sorted():
            font_win = pygame.font.Font(None, 150)
            text_win = font_win.render("YOU WIN", True, (255, 255, 255))
            text_rect_win = text_win.get_rect(center=(width // 2, height // 2))
            screen.blit(text_win, text_rect_win)
            pygame.display.flip() 
        screen.fill((0, 0, 0))  # Effacer l'écran   
        screen.fill((0, 0, 0))  # Effacer l'écran

        for i in range(self.m):
            for j in range(self.n):
                cell_rect = pygame.Rect(j * 100, i * 100, 100, 100)
                pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                font = pygame.font.Font(None, 72)
                text = font.render(str(self.state[i][j]), True, (0, 0, 0))
                text_rect = text.get_rect(center=cell_rect.center)
                screen.blit(text, text_rect)
                if (i, j) in self.selected_cells:
                    pygame.draw.rect(screen, (255, 255, 0), cell_rect, 5) 
        pygame.time.delay(2000)
        pygame.quit()

    def __hash__(self):
        state_tuple = tuple(tuple(self.state[i]) for i in range(self.m))
        return state_tuple #hash ne marche que sur un tuple
    def __eq__(self, other):
       return self.m == other.m and self.n == other.n and self.state == other.state
   
    def __lt__(self,other): #quand le coût est égal pour 2 différentes grilles, on les trie par ordre croissant
        return True


    
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
    
    #def test_obstacle_swap(self,cell1,cell2,l = []):



    def swap_seq(self, cell_pair_list):
        """
        Executes a sequence of swaps. 

        Parameters: 
        -----------
        cell_pair_list: list[tuple[tuple[int]]]
            List of swaps, each swap being a tuple of two cells (each cell being a tuple of integers). 
            So the format should be [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """ 
        if len(cell_pair_list) < 1:
            raise ValueError(f"Invalid swap sequence")
        for i in range(len(cell_pair_list)):
            self.swap(cell_pair_list[i][0], cell_pair_list[i][1])
        # for swap_call in cell_pair_list:
        #     self.swap(swap_call[0], swap_call[1])

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
    
    
    def heuristic(self):
        heuristic = 0
        pos_m,pos_n = 0,0
        for i in range(self.m):
            for j in range (self.n):
                pos_m,pos_n = i,j
                dest_m, dest_n = (self.state[i][j]-1)// self.n, (self.state[i][j]-1) %self.n #parce qu'on commence à 1
                print(dest_m,dest_n)
                heuristic += abs(dest_m -pos_m) + abs(dest_n -pos_n)
                print(heuristic)
        return heuristic//2



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
