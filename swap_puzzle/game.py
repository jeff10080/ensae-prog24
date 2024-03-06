from grid import Grid
import pygame
import sys


class Game(Grid):
    def __init__(self,grid,barriers = []):
        self.m = grid.m
        self.n = grid.n
        self.state = grid.state
        self.selected_cells = []
        self.barriers =barriers
        
    
    

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
            # Créer une surface avec les dimensions du texte "YOU WIN"
            self.Victory()
            
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
        
        pygame.quit()
    

    def Victory(self):
        
        pygame.quit()
        pygame.init()
        

        # Set the screen size
        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))

        # Define the font and text
        font = pygame.font.SysFont("Arial", 300)
        text_surface = font.render("YOU WIN", True, (255, 255, 255))

        # Get the text size
        text_width, text_height = text_surface.get_size()

        # Calculate the offset for centering
        screen_center = (screen_width // 2, screen_height // 2)
        offset_x = screen_center[0] - text_width // 2
        offset_y = screen_center[1] - text_height // 2
        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Blit the text to the screen
        screen.blit(text_surface, (offset_x, offset_y))
          # Update the display
        pygame.display.update()

        pygame.time.delay(2000)
      
        # Quit Pygame
        pygame.quit()

    def choose_level(self):
        pygame.init()

        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 36)
        input_text = ""

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            level = int(input_text)
                            self.level_grid(level)
                            return
                        except ValueError:
                            print("Invalid input. Please enter a valid integer.")
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            screen.fill((255, 255, 255))
            text_surface = font.render("Enter Level:", True, (0, 0, 0))
            screen.blit(text_surface, (50, 50))
            input_surface = font.render(input_text, True, (0, 0, 0))
            pygame.draw.rect(screen, (0, 0, 0), (180, 50, 140, 30), 2)
            screen.blit(input_surface, (185, 55))

            pygame.display.flip()
            clock.tick(30)
    
    
    
    
    
        
        
        
        
    
    
        
        
        
        
        