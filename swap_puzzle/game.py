from grid import Grid
import pygame

class Game():
    def __init__(self,grid):
        self.display = grid.display()
        self.m = grid.m
        self.n = grid.n
        self.state = grid.state
        
    
    

    def action(self):
        width = self.n * 100
        height = self.m * 100
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Vérifier si le clic de la souris est dans le rectangle du bouton Quitter
                    if 0 < event.pos[0] < width and height < event.pos[1] < height + 100:
                        pygame.quit()
                        return
        
        
        
        
        