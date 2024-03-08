from grid import Grid
import pygame
import sys
from solver import Solver
import random as rd
import threading



class Game(Grid):
    def __init__(self,grid,barriers = []):
        self.m = grid.m
        self.n = grid.n
        self.state = grid.state
        self.selected_cells = []
        self.barriers =barriers
        
    
    

    def display(self):
        self.welcome()
        level = self.choose_level()
        self.level_grid(level)
        init_grid= self.copy()
        pygame.display.quit()
        pygame.init()
        
        

        width = self.n * 100
        height = self.m * 100

        screen = pygame.display.set_mode((width, height + 200))  # Ajout de l'espace pour le bouton

        clock = pygame.time.Clock()  # Créer une horloge pour gérer la vitesse de la boucle principale
        swap_count = 0
        
        counter, timer_text = 5, 'Timer 1:00'
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        font = pygame.font.SysFont('cambriamath', 30)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    counter -= 1
                    timer_text = f"Timer {counter // 60} : {counter % 60:02d}" 
                    
                if event.type == pygame.QUIT or counter <=0:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 0 < event.pos[0] < width and height +100< event.pos[1] < height + 200:
                        running = False
                    clicked_row = (event.pos[1]-100) // 100
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
                                swap_count += 1
                                if self.is_sorted():
                                    print("YOU WIN")
                                    running = False
                            else:
                                print(f"Invalid swap: {clicked_cell} and {selected_cell}")
                        else:
                            self.selected_cells.append(clicked_cell)

            
            for i in range (self.m):
                for j in range(self.n):
                    cell_rect = pygame.Rect(j * 100, (i +1)* 100, 100, 100)
                    pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                    font = pygame.font.Font(None, 72)
                    text = font.render(str(self.state[i][j]), True, (0, 0, 0))
                    text_rect = text.get_rect(center=cell_rect.center)
                    screen.blit(text, text_rect)
                    if (i, j) in self.selected_cells:
                        pygame.draw.rect(screen, (255, 255, 0), cell_rect, 5)
            
            pygame.draw.rect(screen, (152, 251, 152), (0, 0, width, 100))  # Rectangle rouge pour le bouton Quitter
            font = pygame.font.Font(None, 72)
            timer = font.render(timer_text, True, (255, 255, 255))
            timer_text_rect = timer.get_rect(center=(width // 2, 50))
            screen.blit(timer, timer_text_rect)
                        

            pygame.draw.rect(screen, (255, 0, 0), (0, height + 100, width, 100))  # Rectangle rouge pour le bouton Quitter
            font = pygame.font.Font(None, 72)
            text = font.render("Leave", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height + 150))
            screen.blit(text, text_rect)
            

            pygame.display.flip()  # Mettre à jour l'affichage
            clock.tick(30)  # Limiter la vitesse de la boucle principale à 30 images par seconde
            
            
        


        
        self.Result()
        self.BestSol(init_grid,swap_count)
            
            
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
    

    def Result(self):
        
        
        
        pygame.display.quit()
        pygame.display.init()
        

        # Set the screen size
        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))

        # Define the font and text
        font = pygame.font.SysFont("Arial", 300)
        if self.is_sorted():
            music_path ="C:\\Users\\avner\\OneDrive\\Documents\\GitHub\\swap_puzzle\\input_medias\\neon-gaming-128925.mp3"
            text_surface = font.render("YOU WIN", True, (255, 255, 255))
        else:
            music_path ="C:\\Users\\avner\\OneDrive\\Documents\\GitHub\\swap_puzzle\\input_medias\\tears_withered-142384.mp3"
            text_surface = font.render("GAME OVER", True, (255, 255, 255))
        self.music_player(music_path)

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
        pygame.display.flip()

        pygame.time.delay(4000)
        
      
        # Quit Pygame
        pygame.display.quit()
    
    def choose_level(self):
        pygame.display.init()

        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()
        font_size = screen_height // 15
        font = pygame.font.SysFont("cambriamath", font_size)
        input_text = ""

        submit_button_rect = pygame.Rect((screen_width - screen_width // 2.5) // 2, screen_height // 2, screen_width // 2.5, font_size + 20)
        quit_button_rect = pygame.Rect((screen_width - screen_width // 2.5) // 2, screen_height // 1.6, screen_width // 2.5, font_size + 20)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            level = int(input_text)
                            return level
                        except ValueError:
                            print("Invalid input. Please enter a valid integer.")
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()

                screen.fill((0, 0, 0))

                # Message "Enter Level:"
                text_surface = font.render("Niveau de la Grille", None, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 4))
                screen.blit(text_surface, text_rect)

                # Champ de saisie
                input_surface = font.render(input_text, True, (255, 255, 255))
                input_rect = pygame.Rect((screen_width - screen_width // 3) // 2, screen_height // 3, screen_width // 3, font_size + 10)
                pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
                screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

                # Bouton "Submit"
                pygame.draw.rect(screen, (0, 255, 0), submit_button_rect)
                text = font.render("Valider", True, (255, 255, 255))
                text_rect = text.get_rect(center=submit_button_rect.center)
                screen.blit(text, text_rect)

                # Bouton "Quitter"
                pygame.draw.rect(screen, (255, 0, 0), quit_button_rect)
                text = font.render("Quitter", True, (255, 255, 255))
                text_rect = text.get_rect(center=quit_button_rect.center)
                screen.blit(text, text_rect)

                # Vérifier si le clic est dans le rectangle du bouton "Valider"
                if submit_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    try:
                        level = int(input_text)
                        return level
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")

                # Vérifier si le clic est dans le rectangle du bouton "Quitter"
                elif quit_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    pygame.quit()
                    sys.exit()

                pygame.display.flip()
                clock.tick(30)


    

    def welcome(self):
        music_path ="C:\\Users\\avner\\OneDrive\\Documents\\GitHub\\swap_puzzle\\input_medias\\phantom-116107.mp3"
        self.music_player(music_path)
        pygame.init()

        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()
        font_size = screen_height // 15
        font = pygame.font.SysFont("cambriamath", font_size)
      
        
        # Load the background image
        background_image = pygame.image.load("C:\\Users\\avner\\OneDrive\\Documents\\GitHub\\swap_puzzle\\input_medias\\Fond_libre_droit_Pixabay.jpg")  
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        play_button_rect = pygame.Rect((screen_width - screen_width // 2.5) // 2, screen_height // 1.8, screen_width // 2.5, font_size + 20)

        running = True

        while running == True:
            for event in pygame.event.get():
                

                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()

                screen.fill((0, 0, 0))
                screen.blit(background_image, (0, 0))
                 # Bouton "Play"
                pygame.draw.rect(screen, (0, 0, 255), play_button_rect)
                text = font.render("Play", True, (255, 255, 255))
                text_rect = text.get_rect(center=play_button_rect.center)
                screen.blit(text, text_rect)
                pygame.display.flip()
                if play_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    running = False
                
                clock.tick(30)
                pygame.display.flip()
        pygame.time.delay(1000)
        pygame.display.quit()
        
   

    def BestSol(self,init_grid,swap_count):
        pygame.display.init()
        if not self.is_sorted():
            swap_count=None
        self.state =init_grid.state
        grid1 = Grid(self.m,self.n,init_grid.state)
        s = Solver(grid1)
        swap_sol = s.get_solution_a_star(init_grid)
        optimal_swap_count = len(swap_sol)
        

        # Set the screen size
        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))

        # Define the font and text
        font = pygame.font.SysFont("Arial", 150)
        if swap_count == None:
            font = pygame.font.SysFont("Arial", 50)
            text_surface = font.render(rd.choice(["Too bad, but don't worry, you'll get it next time!"]), True, (255, 255, 255))
        elif swap_count == optimal_swap_count:
            text_surface = font.render(rd.choice(["PERFECT SCORE", "GENIUS", "EXCELLENT","CONGRATULATION"]), True, (255, 255, 255))
        elif swap_count <= optimal_swap_count +5:
            text_surface = font.render(rd.choice(["SO CLOSE", "GREAT SCORE", "WELL PLAYED", "NOT BAD"]),  True, (255, 255, 255))
        elif swap_count > optimal_swap_count + 25:
            text_surface = font.render(rd.choice(["...", "DISAPOINTING", "ARE YOU KIDDING?", " LEFT THE CHAT...","SERIOUSLY"]),  True, (255, 255, 255))
        else:
            text_surface = font.render(rd.choice(["TRY AGAIN", "NEXT TIME", "I BELIEVE IN YOU !","TOO BAD!"]),  True, (255, 255, 255))
        
        
            
            
          

        # Get the text size
        text_width, text_height = text_surface.get_size()
        
        # Calculate the offset for centering
        screen_center = (screen_width // 2, screen_height // 2)
        offset_x = screen_center[0] - text_width // 2
        offset_y = screen_center[1] - text_height // 2
        
        # Define the font and text for the score information
        font_small = pygame.font.SysFont("Arial", 50)
        if swap_count == None:
            text_small = font_small.render(f"The best score is {optimal_swap_count}", True, (255, 255, 255))
        else:
            text_small = font_small.render(f"Your score is {swap_count}. The best score is {optimal_swap_count}", True, (255, 255, 255))
            

        # Get the text size for the small phrase
        text_small_width, text_small_height = text_small.get_size()

        # Calculate the offset for centering the small phrase
        offset_x_small = screen_center[0] - text_small_width // 2
        offset_y_small = offset_y + text_height + 20  # Adjusted for spacing
        
        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Blit the text to the screen
        screen.blit(text_surface, (offset_x, offset_y))
        
        screen.blit(text_small, (offset_x_small, offset_y_small))
          # Update the display
        pygame.display.flip()
        pygame.time.delay(4500) 
        
        
        pygame.display.quit()
        pygame.display.init()

        width = self.n * 100
        height = self.m * 100

        screen = pygame.display.set_mode((width, height + 100))  # Ajout de l'espace pour le bouton
        

        for swap in swap_sol:
            self.selected_cells = [swap[0],swap[1]]
            
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
            pygame.display.flip()
            pygame.time.delay(1500)
            
            
            self.swap(swap[0],swap[1])
            for i in range(self.m):
                for j in range(self.n):
                    cell_rect = pygame.Rect(j * 100, i * 100, 100, 100)
                    pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                    font = pygame.font.Font(None, 72)
                    text = font.render(str(self.state[i][j]), True, (0, 0, 0))
                    text_rect = text.get_rect(center=cell_rect.center)
                    screen.blit(text, text_rect)
                    if (i, j) in self.selected_cells:
                        pygame.draw.rect(screen, (255, 0, 255), cell_rect, 5)
            
            
            pygame.draw.rect(screen, (255, 0, 0), (0, height, width, 100))  # Rectangle rouge pour le bouton Quitter
            font = pygame.font.Font(None, 72)
            text = font.render("Quitter", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height + 50))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(1500)
            
            
        pygame.time.delay(1500)
        # Stop the sound
        
        pygame.display.quit()
        
        
    def music_player(self, new_sound_file_path=None):
        pygame.mixer.init()

        # Arrêter la musique actuelle
        pygame.mixer.music.stop()

        if new_sound_file_path:
            # Charger et jouer la nouvelle musique
            pygame.mixer.music.load(new_sound_file_path)
            pygame.mixer.music.play(-1)
            
  



        
       
        