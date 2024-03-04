from grid import Grid
import pygame

class Game():
    def __init__(self,grid):
        self.display = grid.display()
        self.m = grid.m
        self.n = grid.n
        self.state = grid.state
    
    def display(self):
        pygame.init()
        screen = pygame.display.set_mode((1280, 853))
        background_image = "Fond_libre_droit_Pixabay.jpg"
        background = pygame.image.load(background_image).convert()

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
        
        
        