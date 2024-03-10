from grid import Grid
import pygame
import sys
from solver import Solver
import random as rd




class Game(Grid):
    def __init__(self,grid,barriers = []):
        self.m = grid.m
        self.n = grid.n
        self.state = grid.state
        self.selected_cells = []
        self.barriers =barriers
        
    
    

    def display(self, Retry = None):
        music_path ="swap_puzzle\\input_medias\\phantom-116107.mp3"
        self.music_player(music_path)
        pygame.display.quit()
        pygame.init()
        if not Retry:
            self.welcome()
        grid_heuristic = self.choose_level()
        self.level_grid(grid_heuristic)
        self.settle_barriers()
        difficulty = self.difficulty()
        init_grid= self.copy()
        grid1 = Grid(self.m,self.n,init_grid.state)
        s = Solver(grid1)
        swap_sol = s.get_solution_a_star(init_grid)
        level = len(swap_sol)
        
        
        
        
        
        

        width = self.n * 100
        height = self.m * 100

        screen = pygame.display.set_mode((width, height + 200))  # Ajout de l'espace pour le bouton

        clock = pygame.time.Clock()  # Créer une horloge pour gérer la vitesse de la boucle principale
        swap_count = 0
        
        counter = int(difficulty *level*10)# la variable timer est utilisée plus tard il faut un entier
        timer_text =f"Timer {counter // 600} : {counter % 600:02d}" 
        pygame.time.set_timer(pygame.USEREVENT, 100) # toutes les 0.5 secondes
        font = pygame.font.SysFont('cambriamath', 30)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    counter -= 1
                    timer_text = f"Timer {counter // 600} : {counter % 600:02d}" 
                    
                if event.type == pygame.QUIT or counter <=0:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 0 < event.pos[0] < width and height +100< event.pos[1] < height + 200:
                        pygame.quit()
                        sys.exit()
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
            for barrier in self.barriers:
                (i1, j1), (i2, j2) = barrier
                # Dessiner une ligne entre les cases (i1, j1) et (i2, j2)
                if i1 == i2:#même ligne
                    j =max(j1,j2)
                    pygame.draw.line(screen, (255,0,0), (j*100,(i1+1)*100 ), ( j*100,(i1+2)*100), 5)
                else:
                    i =max(i1,i2)
                    pygame.draw.line(screen, (255,0,0), (j1*100,(i+1)*100), ( (j1+1)*100,(i+1)*100), 5)

            
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
        self.BestSol(init_grid,swap_count,swap_sol)
        self.retry()
        
            
            
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
        for barrier in self.barriers:
                (i1, j1), (i2, j2) = barrier
                # Dessiner une ligne entre les cases (i1, j1) et (i2, j2)
                if i1 == i2:#même ligne
                    j =max(j1,j2)
                    pygame.draw.line(screen, (255,0,0), (j*100,(i1+1)*100 ), ( j*100,(i1+2)*100), 5)
                else:
                    i =max(i1,i2)
                    pygame.draw.line(screen, (255,0,0), (j1*100,(i+1)*100), ( (j1+1)*100,(i+1)*100), 5)
        
        
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
            music_path ="swap_puzzle\\input_medias\\neon-gaming-128925.mp3"
            text_surface = font.render("YOU WIN", True, (255, 255, 255))
        else:
            music_path ="swap_puzzle\\input_medias\\tears_withered-142384.mp3"
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
        font_path ="swap_puzzle\\input_medias\\BLADRMF_.ttf"
        font_choose = pygame.font.Font(font_path, font_size*3)
        input_text = ""

        submit_button_rect = pygame.Rect((screen_width - screen_width // 2.5) // 2, screen_height // 2, screen_width // 2.5, font_size + 20)
        quit_button_rect = pygame.Rect((screen_width - screen_width // 2.5) // 2, submit_button_rect.bottom +screen_height // 20, screen_width // 2.5, font_size + 20)

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
                text_surface = font_choose.render("Grid level", None, (255, 127, 0))
                text_rect = text_surface.get_rect(center=(screen_width // 1.9, screen_height // 4))
                screen.blit(text_surface, text_rect)

                # Champ de saisie
                input_surface = font.render(input_text, True, (255, 255, 255))
                input_rect = pygame.Rect((screen_width - screen_width // 3) // 2, screen_height // 2.7, screen_width // 3, font_size + 10)
                pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
                text_rect =input_surface.get_rect(center=input_rect.center)
                screen.blit(input_surface, text_rect)

                # Bouton "Submit"
                pygame.draw.rect(screen, (0, 255, 0), submit_button_rect)
                text = font.render("Submit", True, (255, 255, 255))
                text_rect = text.get_rect(center=submit_button_rect.center)
                screen.blit(text, text_rect)

                # Bouton "Quitter"
                pygame.draw.rect(screen, (255, 0, 0), quit_button_rect)
                text = font.render("Leave", True, (255, 255, 255))
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
        
        pygame.display.init()

        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()
        font_size = screen_height // 15
        font = pygame.font.SysFont("cambriamath", font_size)
        font_path = "swap_puzzle\\input_medias\\Game Of Squids.ttf"
        
        font_title = pygame.font.Font(font_path, font_size*2) #Création d'une police
      
        
        # Load the background image
        background_image = pygame.image.load("swap_puzzle\\input_medias\\retro-4237850_1280.jpg")  
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        play_button_rect = pygame.Rect((screen_width - screen_width // 2.5) // 2, screen_height // 1.8, screen_width // 2.5, font_size + 20)
        leave_button_rect = pygame.Rect((screen_width - screen_width // 2.5) // 2, play_button_rect.bottom + screen_height//20, screen_width // 2.5, font_size + 20)
        
        
        
        

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
                pygame.draw.rect(screen, (255, 0, 0), leave_button_rect)
                leave_text = font.render("Leave", True, (255, 255, 255))
                leave_rect = leave_text.get_rect(center=leave_button_rect.center)
                screen.blit(leave_text, leave_rect)
                title_surface = font_title.render("The Grid Master", False, (255,127,0))
                title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 3.5))
                screen.blit(title_surface, title_rect)
                pygame.display.flip()
                if play_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    running = False
                if leave_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    pygame.quit()
                    sys.exit()
                
                clock.tick(30)
                pygame.display.flip()
        pygame.time.delay(1000)
        pygame.display.quit()
        
   

    def BestSol(self,init_grid,swap_count,swap_sol):
        pygame.display.init()
        if not self.is_sorted():
            swap_count=None
        self.state =init_grid.state
        
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
            text_small = font_small.render(f"The best score possible is {optimal_swap_count}", True, (255, 255, 255))
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
            for barrier in self.barriers:
                (i1, j1), (i2, j2) = barrier
                # Dessiner une ligne entre les cases (i1, j1) et (i2, j2)
                if i1 == i2:#même ligne
                    j =max(j1,j2)
                    pygame.draw.line(screen, (255,0,0), (j*100,(i1+1)*100 ), ( j*100,(i1+2)*100), 5)
                else:
                    i =max(i1,i2)
                    pygame.draw.line(screen, (255,0,0), (j1*100,(i+1)*100), ( (j1+1)*100,(i+1)*100), 5)
        
            
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
            for barrier in self.barriers:
                (i1, j1), (i2, j2) = barrier
                # Dessiner une ligne entre les cases (i1, j1) et (i2, j2)
                if i1 == i2:#même ligne
                    j =max(j1,j2)
                    pygame.draw.line(screen, (255,0,0), (j*100,(i1+1)*100 ), ( j*100,(i1+2)*100), 5)
                else:
                    i =max(i1,i2)
                    pygame.draw.line(screen, (255,0,0), (j1*100,(i+1)*100), ( (j1+1)*100,(i+1)*100), 5)
        
            
            
            pygame.draw.rect(screen, (255, 0, 0), (0, height, width, 100))  # Rectangle rouge pour le bouton Quitter
            font = pygame.font.Font(None, 72)
            text = font.render("Quitter", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height + 50))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(1500)
        
        self.selected_cells = []
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
        for barrier in self.barriers:
                (i1, j1), (i2, j2) = barrier
                # Dessiner une ligne entre les cases (i1, j1) et (i2, j2)
                if i1 == i2:#même ligne
                    j =max(j1,j2)
                    pygame.draw.line(screen, (255,0,0), (j*100,(i1+1)*100 ), ( j*100,(i1+2)*100), 5)
                else:
                    i =max(i1,i2)
                    pygame.draw.line(screen, (255,0,0), (j1*100,(i+1)*100), ( (j1+1)*100,(i+1)*100), 5)
        
            
        pygame.display.flip()  
        pygame.time.delay(1500)
        # Stop the sound
        
        pygame.display.quit()
    
    def difficulty(self):
        pygame.display.init()

        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()
        font_size = screen_height // 15
        font = pygame.font.SysFont("cambriamath", font_size)
        font_path ="swap_puzzle\\input_medias\\BLADRMF_.ttf"
        font_dif = pygame.font.Font(font_path, font_size*3)
        input_text = ""

        # Calculate the rectangle width and buffer space
        rect_width = screen_width // 6
        buffer_space = (screen_width - 5 * rect_width) / 6  # Adjust the division factor for more/less space

        # Define the first rectangle's leftmost position (assuming left-to-right alignment)
        first_rect_left = screen_width // 30

        # Create rectangles with proper positioning
        easy_rect = pygame.Rect(first_rect_left, screen_height // 2, rect_width, font_size + 20)
        medium_rect = pygame.Rect(easy_rect.right + buffer_space, screen_height // 2, rect_width, font_size + 20)
        difficult_rect = pygame.Rect(medium_rect.right + buffer_space, screen_height // 2, rect_width, font_size + 20)
        hardcore_rect = pygame.Rect(difficult_rect.right + buffer_space, screen_height // 2, rect_width, font_size + 20)
        infernal_rect = pygame.Rect(hardcore_rect.right + buffer_space, screen_height // 2, rect_width, font_size + 20)
        
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
                text_surface = font_dif.render("Difficulty", True, (255, 127, 0))
                text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 4))
                screen.blit(text_surface, text_rect)


                # Bouton "Easy"
                pygame.draw.rect(screen, (0, 255, 0), easy_rect)
                text = font.render("Easy", True, (255, 255, 255))
                text_rect = text.get_rect(center=easy_rect.center)
                screen.blit(text, text_rect)
                
                # Bouton "Medium"
                pygame.draw.rect(screen, (255, 255, 50), medium_rect)
                text = font.render("Medium", True, (255 , 255 , 255))
                text_rect = text.get_rect(center=medium_rect.center)
                screen.blit(text, text_rect)
                
                # Bouton "Difficult"
                pygame.draw.rect(screen, (255, 127, 0), difficult_rect)
                text = font.render("Difficult", True, (255, 255, 255))
                text_rect = text.get_rect(center=difficult_rect.center)
                screen.blit(text, text_rect)
                
                # Bouton "Hardcore"
                pygame.draw.rect(screen, (86, 41, 0), hardcore_rect)
                text = font.render("Hardcore", True, (255, 255, 255))
                text_rect = text.get_rect(center=hardcore_rect.center)
                screen.blit(text, text_rect)
                
                # Bouton "Infernal"
                pygame.draw.rect(screen, (148,0,211), infernal_rect)
                text = font.render("Infernal", True, (255, 255, 255))
                text_rect = text.get_rect(center=infernal_rect.center)
                screen.blit(text, text_rect)
                
                

                # Bouton "Quitter"
                pygame.draw.rect(screen, (255, 0, 0), quit_button_rect)
                text = font.render("Leave", True, (255, 255, 255))
                text_rect = text.get_rect(center=quit_button_rect.center)
                screen.blit(text, text_rect)

                # Vérifier si le clic est dans le rectangle des bouton "Easy" ...
                if easy_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    
                    return 10
                elif medium_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    return 5
                elif difficult_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    return 2.5
                elif hardcore_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    return 1
                elif infernal_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    return 0.5
                

                # Vérifier si le clic est dans le rectangle du bouton "Quitter"
                elif quit_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    pygame.quit()
                    sys.exit()

                pygame.display.flip()
                clock.tick(30)
    def retry(self):
        
        pygame.display.init()

        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()
        font_size = screen_height // 15
        font = pygame.font.SysFont("cambriamath", font_size)
        font_path = "swap_puzzle\\input_medias\\ka1.ttf"
        
        font_title = pygame.font.Font(font_path, font_size*2) #Création d'une police
      
        
        # Load the background image
        background_image = pygame.image.load("swap_puzzle\\input_medias\\Fond_libre_droit_Pixabay.jpg")  
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        retry_button_rect = pygame.Rect(screen_width // 9, screen_height // 1.8, screen_width // 3, font_size + 20)
        leave_button_rect = pygame.Rect(retry_button_rect.right + screen_width // 8, screen_height // 1.8, screen_width // 3, font_size + 20)
        
        
        

        running = True

        while running :
            for event in pygame.event.get():
                

                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()
                screen.fill((0, 0, 0))

                
                screen.blit(background_image, (0, 0))
                 # Bouton "Play"
                pygame.draw.rect(screen, (0, 255, 0), retry_button_rect)
                
                yes_text = font.render("Yes", True, (255, 255, 255))
                yes_rect = yes_text.get_rect(center=retry_button_rect.center)
                screen.blit(yes_text, yes_rect)
                pygame.draw.rect(screen, (255, 0, 0), leave_button_rect)
                leave_text = font.render("No", True, (255, 255, 255))
                leave_rect = leave_text.get_rect(center=leave_button_rect.center)
                screen.blit(leave_text, leave_rect)
                retry_surface = font_title.render("Retry ?", False, (255,127,0))
                retry_rect = retry_surface.get_rect(center=(screen_width // 2, screen_height // 3.5))
                screen.blit(retry_surface, retry_rect)
                pygame.display.flip()
                if retry_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    pygame.time.delay(1000)
                    pygame.display.quit()
                    self.display(True)
                if leave_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    pygame.time.delay(1000)
                    pygame.display.quit()
                    sys.exit()
                    
                
                clock.tick(30)
                pygame.display.flip()
        pygame.time.delay(1000)
        pygame.display.quit()
    
    
    def settle_barriers(self):
        
        pygame.init()
        

        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()
        font_size = screen_height // 15
        font = pygame.font.SysFont("cambriamath", font_size)
        font_path = "swap_puzzle\\input_medias\\BLADRMF_.ttf"
        
        font_title = pygame.font.Font(font_path, font_size*2) #Création d'une police
      
        
       
        yes_button_rect = pygame.Rect(screen_width // 9, screen_height // 1.8, screen_width // 3, font_size + 20)
        no_button_rect = pygame.Rect(yes_button_rect.right + screen_width // 8, screen_height // 1.8, screen_width // 3, font_size + 20)
        
        
        

        running = True

        while running == True:
            for event in pygame.event.get():
                

                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()
                screen.fill((0, 0, 0))

                
                
                 # Bouton "Play"
                pygame.draw.rect(screen, (0, 255, 0), yes_button_rect)
                
                yes_text = font.render("Yes", True, (255, 255, 255))
                yes_rect = yes_text.get_rect(center=yes_button_rect.center)
                screen.blit(yes_text, yes_rect)
                pygame.draw.rect(screen, (255, 0, 0), no_button_rect)
                leave_text = font.render("No", True, (255, 255, 255))
                leave_rect = leave_text.get_rect(center=no_button_rect.center)
                screen.blit(leave_text, leave_rect)
                retry_surface = font_title.render("BARRIERS", False, (255,127,0))
                retry_rect = retry_surface.get_rect(center=(screen_width // 2, screen_height // 3.5))
                screen.blit(retry_surface, retry_rect)
                pygame.display.flip()
                if yes_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    pygame.time.delay(1000)
                    
                    self.add_barriers()
                    running = False
                    
                    
                if no_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                    pygame.time.delay(1000)
                    
                    running = False
                
                    
                
                clock.tick(30)
                pygame.display.flip()
                
        
        pygame.time.delay(1000)
        pygame.display.quit()
        
        
    
    

        
   



    
    def music_player(self, new_sound_file_path=None):
        pygame.mixer.init()

        # Arrêter la musique actuelle
        pygame.mixer.music.stop()

        if new_sound_file_path:
            # Charger et jouer la nouvelle musique
            pygame.mixer.music.load(new_sound_file_path)
            pygame.mixer.music.play(-1)
            
  



        
       
        