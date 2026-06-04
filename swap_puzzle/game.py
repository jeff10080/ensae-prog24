from __future__ import annotations
import logging
import pygame
import sys
import asyncio
import random as rd
from typing import List, Tuple, Optional, Union, Any

from .grid import Grid
from .solver import Solver

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class Game(Grid):
    """
    Main game manager class for 'The Grid Master'.
    Inherits from the Grid class and coordinates the Pygame graphical interface,
    user input capture, barrier integration, timer tracking,
    and the automated demonstration of the optimal solution computed by the A* algorithm.
    """

    def __init__(self, grid: Grid, barriers: Optional[List[Tuple[Tuple[int, int], Tuple[int, int]]]] = None) -> None:
        """
        Initializes the game instance from a reference grid.

        Args:
            grid (Grid): The initial grid instance providing dimensions and starting state.
            barriers (Optional[List[Tuple[Tuple[int, int], Tuple[int, int]]]]): Optional list of barriers.
        """
        self.m: int = grid.m
        self.n: int = grid.n
        self.state: List[List[int]] = grid.state
        self.selected_cells: List[Tuple[int, int]] = []
        self.barriers: List[Tuple[Tuple[int, int], Tuple[int, int]]] = barriers if barriers is not None else []
        logger.info(f"Game successfully initialized. Grid dimensions: {self.m}x{self.n}.")

    async def display(self, Retry: Optional[bool] = None) -> None:
        """
        Handles the main gameplay loop, cell rendering, mouse events 
        (selection/swapping of cells), and timer tracking.

        Args:
            Retry (Optional[bool]): Flag indicating if the player is restarting a game (skips the welcome screen).
        """
        music_path: str = "swap_puzzle/input_medias/phantom-116107.mp3"
        try:
            self.music_player(music_path)
        except AttributeError:
            logger.warning("The 'music_player' method is not defined in the parent class.")

        pygame.display.quit()
        pygame.init()

        if not Retry:
            await self.welcome()
            
        grid_heuristic: int = await self.choose_level()
        self.level_grid(grid_heuristic)
        await self.settle_barriers()
        difficulty: Union[int, float] = await self.difficulty()

        init_grid: Grid = self.copy()
        grid1: Grid = Grid(self.m, self.n, init_grid.state, self.barriers)
        s: Solver = Solver(grid1)
        swap_sol: List[Tuple[Tuple[int, int], Tuple[int, int]]] = s.get_solution_a_star(init_grid)
        level: int = len(swap_sol)
        
        pygame.display.quit()
        pygame.init()

        width: int = self.n * 100
        height: int = self.m * 100

        screen: pygame.Surface = pygame.display.set_mode((width, height + 200))

        clock: pygame.time.Clock = pygame.time.Clock()
        swap_count: int = 0

        counter: int = int(difficulty * level * 10)
        timer_text: str = f"Timer {counter // 600} : {counter % 600:02d}"
        pygame.time.set_timer(pygame.USEREVENT, 100)  
        font: pygame.font.Font = pygame.font.SysFont('cambriamath', 30)

        logger.info(f"Game started. Optimal solution estimated in {level} steps. Timer initialized to {counter} ticks.")

        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or counter <= 0:
                    if counter <= 0:
                        logger.info("Time's up! Game failed.")
                    running = False
                    
                if event.type == pygame.USEREVENT:
                    counter -= 1
                    timer_text = f"Timer {counter // 600} : {counter % 600:02d}"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 0 < event.pos[0] < width and height + 100 < event.pos[1] < height + 200:
                        logger.info("Player chose to leave the current game.")
                        running = False
                        return 

                    clicked_row: int = (event.pos[1] - 100) // 100
                    clicked_col: int = event.pos[0] // 100
                    
                    if 0 <= clicked_row < self.m and 0 <= clicked_col < self.n:
                        clicked_cell: Tuple[int, int] = (clicked_row, clicked_col)
                        
                        if len(self.selected_cells) == 1:
                            selected_cell: Tuple[int, int] = self.selected_cells[0]
                            if clicked_cell == selected_cell:
                                self.selected_cells = []
                            elif self.test_valid_swap(clicked_cell, selected_cell):
                                self.swap(clicked_cell, selected_cell)
                                self.selected_cells = []
                                swap_count += 1
                                logger.info(f"Swap #{swap_count} validated between {selected_cell} and {clicked_cell}.")
                                
                                if self.is_sorted():
                                    logger.info("Grid successfully sorted! Player wins the game.")
                                    running = False
                            else:
                                logger.warning(f"Invalid swap attempt between {clicked_cell} and {selected_cell}.")
                        else:
                            self.selected_cells.append(clicked_cell)

            screen.fill((0, 0, 0))
            
            for i in range(self.m):
                for j in range(self.n):
                    cell_rect: pygame.Rect = pygame.Rect(j * 100, (i + 1) * 100, 100, 100)
                    pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                    cell_font: pygame.font.Font = pygame.font.Font(None, 72)
                    text: pygame.Surface = cell_font.render(str(self.state[i][j]), True, (0, 0, 0))
                    text_rect: pygame.Rect = text.get_rect(center=cell_rect.center)
                    screen.blit(text, text_rect)
                    if (i, j) in self.selected_cells:
                        pygame.draw.rect(screen, (255, 255, 0), cell_rect, 5)

            for barrier in self.barriers:
                (i1, j1), (i2, j2) = barrier
                if i1 == i2:  
                    j: int = max(j1, j2)
                    pygame.draw.line(screen, (255, 0, 0), (j * 100, (i1 + 1) * 100), (j * 100, (i1 + 2) * 100), 5)
                else:
                    i: int = max(i1, i2)
                    pygame.draw.line(screen, (255, 0, 0), (j1 * 100, (i + 1) * 100), ((j1 + 1) * 100, (i + 1) * 100), 5)

            pygame.draw.rect(screen, (152, 251, 152), (0, 0, width, 100))
            timer_font: pygame.font.Font = pygame.font.Font(None, 72)
            timer_surf: pygame.Surface = timer_font.render(timer_text, True, (255, 255, 255))
            timer_text_rect: pygame.Rect = timer_surf.get_rect(center=(width // 2, 50))
            screen.blit(timer_surf, timer_text_rect)

            pygame.draw.rect(screen, (255, 0, 0), (0, height + 100, width, 100))
            leave_font: pygame.font.Font = pygame.font.Font(None, 72)
            leave_surf: pygame.Surface = leave_font.render("Leave", True, (255, 255, 255))
            leave_rect: pygame.Rect = leave_surf.get_rect(center=(width // 2, height + 150))
            screen.blit(leave_surf, leave_rect)

            pygame.display.flip()
            clock.tick(30)
            await asyncio.sleep(0)  

        await self.Result()
        await self.BestSol(init_grid, swap_count, swap_sol)
        await self.retry()
        pygame.quit()

    async def Result(self) -> None:
        """
        Displays the final results screen (Victory or Defeat) 
        with dedicated music and fonts.
        """
        pygame.display.quit()
        pygame.display.init()

        screen_info: pygame.display._DisplayInfo = pygame.display.Info()
        screen_width: int = screen_info.current_w
        screen_height: int = screen_info.current_h
        screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))

        if self.is_sorted():
            font: pygame.font.Font = pygame.font.Font("swap_puzzle/input_medias/Victoire.ttf", 300)
            music_path: str = "swap_puzzle/input_medias/neon-gaming-128925.mp3"
            text_surface: pygame.Surface = font.render("YOU WIN", True, (255, 127, 0))
            logger.info("Final result displayed: VICTORY.")
        else:
            font = pygame.font.Font("swap_puzzle/input_medias/Coalition_v2.ttf", 150)
            music_path = "swap_puzzle/input_medias/tears_withered-142384.mp3"
            text_surface = font.render("GAME OVER", True, (0, 128, 255))
            logger.info("Final result displayed: GAME OVER.")
            
        try:
            self.music_player(music_path)
        except AttributeError:
            pass

        text_width, text_height = text_surface.get_size()
        screen_center: Tuple[int, int] = (screen_width // 2, screen_height // 2)
        offset_x: int = screen_center[0] - text_width // 2
        offset_y: int = screen_center[1] - text_height // 2
        
        screen.fill((0, 0, 0))
        screen.blit(text_surface, (offset_x, offset_y))
        pygame.display.flip()

        await asyncio.sleep(4)
        pygame.display.quit()
    
    async def choose_level(self) -> int:
        """
        Displays a text input interface allowing the player to choose their level.

        Returns:
            int: The entered level number (defaults to 1 upon error or exit).
        """
        pygame.display.init()

        screen_info: pygame.display._DisplayInfo = pygame.display.Info()
        screen_width: int = screen_info.current_w
        screen_height: int = screen_info.current_h
        screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))
        clock: pygame.time.Clock = pygame.time.Clock()
        font_size: int = screen_height // 15
        font: pygame.font.Font = pygame.font.SysFont("cambriamath", font_size)
        font_path: str = "swap_puzzle/input_medias/BLADRMF_.ttf"
        font_choose: pygame.font.Font = pygame.font.Font(font_path, font_size * 3)
        input_text: str = ""

        submit_button_rect: pygame.Rect = pygame.Rect((screen_width - screen_width // 2.5) // 2, screen_height // 2, screen_width // 2.5, font_size + 20)
        quit_button_rect: pygame.Rect = pygame.Rect((screen_width - screen_width // 2.5) // 2, submit_button_rect.bottom + screen_height // 20, screen_width // 2.5, font_size + 20)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    logger.info("Application forcibly closed during level selection.")
                    return 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            level: int = int(input_text)
                            logger.info(f"Level {level} validated by user (Return key).")
                            return level
                        except ValueError:
                            logger.warning(f"Incorrect user input detected: '{input_text}' is not an integer.")
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
            mouse_click: Tuple[bool, bool, bool] = pygame.mouse.get_pressed()

            screen.fill((0, 0, 0))

            text_surface: pygame.Surface = font_choose.render("Grid level", None, (255, 127, 0))
            text_rect: pygame.Rect = text_surface.get_rect(center=(screen_width // 1.9, screen_height // 4))
            screen.blit(text_surface, text_rect)

            input_surface: pygame.Surface = font.render(input_text, True, (255, 255, 255))
            input_rect: pygame.Rect = pygame.Rect((screen_width - screen_width // 3) // 2, screen_height // 2.7, screen_width // 3, font_size + 10)
            pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
            text_rect = input_surface.get_rect(center=input_rect.center)
            screen.blit(input_surface, text_rect)

            pygame.draw.rect(screen, (0, 255, 0), submit_button_rect)
            text_submit: pygame.Surface = font.render("Submit", True, (255, 255, 255))
            text_rect = text_submit.get_rect(center=submit_button_rect.center)
            screen.blit(text_submit, text_rect)

            pygame.draw.rect(screen, (255, 0, 0), quit_button_rect)
            text_leave: pygame.Surface = font.render("Leave", True, (255, 255, 255))
            text_rect = text_leave.get_rect(center=quit_button_rect.center)
            screen.blit(text_leave, text_rect)

            if submit_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                try:
                    level = int(input_text)
                    logger.info(f"Level {level} validated by user (Submit button).")
                    return level
                except ValueError:
                    pass

            elif quit_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                pygame.quit()
                logger.info("User left the game from the level selection screen.")
                return 1

            pygame.display.flip()
            clock.tick(30)
            await asyncio.sleep(0)

    async def welcome(self) -> None:
        """
        Displays an interactive welcome screen with a retro background 
        and handles start buttons.
        """
        pygame.display.init()

        screen_info: pygame.display._DisplayInfo = pygame.display.Info()
        screen_width: int = screen_info.current_w
        screen_height: int = screen_info.current_h
        screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))
        clock: pygame.time.Clock = pygame.time.Clock()
        font_size: int = screen_height // 15
        font: pygame.font.Font = pygame.font.SysFont("cambriamath", font_size)
        font_path: str = "swap_puzzle/input_medias/Game Of Squids.ttf"
        font_title: pygame.font.Font = pygame.font.Font(font_path, font_size * 2)
        
        try:
            background_image: pygame.Surface = pygame.image.load("swap_puzzle/input_medias/retro-4237850_1280.jpg")  
            background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        except pygame.error:
            logger.error("Failed to load welcome background image. Falling back to a black background.")
            background_image = pygame.Surface((screen_width, screen_height))
            background_image.fill((0, 0, 0))

        play_button_rect: pygame.Rect = pygame.Rect((screen_width - screen_width // 2.5) // 2, screen_height // 1.8, screen_width // 2.5, font_size + 20)
        leave_button_rect: pygame.Rect = pygame.Rect((screen_width - screen_width // 2.5) // 2, play_button_rect.bottom + screen_height // 20, screen_width // 2.5, font_size + 20)
        
        logger.info("Displaying welcome screen.")
        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
            mouse_click: Tuple[bool, bool, bool] = pygame.mouse.get_pressed()
            screen.fill((0, 0, 0))
            screen.blit(background_image, (0, 0))
            
            pygame.draw.rect(screen, (0, 0, 255), play_button_rect)
            text_play: pygame.Surface = font.render("Play", True, (255, 255, 255))
            text_rect: pygame.Rect = text_play.get_rect(center=play_button_rect.center)
            screen.blit(text_play, text_rect)
            
            pygame.draw.rect(screen, (255, 0, 0), leave_button_rect)
            leave_text: pygame.Surface = font.render("Leave", True, (255, 255, 255))
            leave_rect: pygame.Rect = leave_text.get_rect(center=leave_button_rect.center)
            screen.blit(leave_text, leave_rect)
            
            title_surface: pygame.Surface = font_title.render("The Grid Master", False, (255, 127, 0))
            title_rect: pygame.Rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 3.5))
            screen.blit(title_surface, title_rect)
            
            if play_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                logger.info("Play button activated.")
                running = False
            if leave_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                logger.info("Leave button activated from home screen.")
                pygame.quit()
                return

            pygame.display.flip()
            clock.tick(30)
            await asyncio.sleep(0)
            
        await asyncio.sleep(1)
        pygame.display.quit()
        
    async def BestSol(self, init_grid: Grid, swap_count: Optional[int], swap_sol: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
        """
        Compares user performance against the ideal solution calculated by the Solver,
        displays a score evaluation message, and then automatically plays through
        the optimal solution steps on screen.

        Args:
            init_grid (Grid): Saved state of the grid before any modifications.
            swap_count (Optional[int]): Total moves played by the user. Set to None if defeated.
            swap_sol (List[Tuple[Tuple[int, int], Tuple[int, int]]]): Sequence of optimal moves solved by the AI.
        """
        pygame.display.init()
        if not self.is_sorted():
            swap_count = None
        self.state = init_grid.state
        optimal_swap_count: int = len(swap_sol)
        
        screen_info: pygame.display._DisplayInfo = pygame.display.Info()
        screen_width: int = screen_info.current_w
        screen_height: int = screen_info.current_h
        screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))

        if swap_count is None:
            font: pygame.font.Font = pygame.font.Font("swap_puzzle/input_medias/Coalition_v2.ttf", 50)
            text_surface: pygame.Surface = font.render("DON'T WORRY, YOU'LL GET IT NEXT TIME", True, (0, 128, 255))
            logger.info("Score evaluation: Puzzle not solved by player.")
        elif swap_count == optimal_swap_count:
            font = pygame.font.Font("swap_puzzle/input_medias/Victoire.ttf", 200)
            text_surface = font.render(rd.choice(["PERFECT SCORE", "GENIUS", "EXCELLENT", "CONGRATULATION"]), True, (255, 127, 0))
            logger.info(f"Score evaluation: Perfect score achieved ({swap_count} moves).")
        elif swap_count <= optimal_swap_count + 5:
            font = pygame.font.Font("swap_puzzle/input_medias/Victoire.ttf", 200)
            text_surface = font.render(rd.choice(["SO CLOSE", "GREAT SCORE", "WELL PLAYED", "NOT BAD"]), True, (255, 127, 0))
            logger.info(f"Score evaluation: Good score ({swap_count} moves vs {optimal_swap_count} optimal).")
        elif swap_count > optimal_swap_count + 25:
            font = pygame.font.Font("swap_puzzle/input_medias/Victoire.ttf", 200)
            text_surface = font.render(rd.choice(["...", "DISAPPOINTING", "ARE YOU KIDDING?", "LEFT THE CHAT...", "SERIOUSLY"]), True, (255, 127, 0))
            logger.warning(f"Score evaluation: Poor score ({swap_count} moves vs {optimal_swap_count} optimal).")
        else:
            font = pygame.font.Font("swap_puzzle/input_medias/Victoire.ttf", 200)
            text_surface = font.render(rd.choice(["TRY AGAIN", "NEXT TIME", "I BELIEVE IN YOU !", "TOO BAD!"]), True, (255, 127, 0))
            logger.info(f"Score evaluation: Average score ({swap_count} moves).")
        
        text_width, text_height = text_surface.get_size()
        screen_center: Tuple[int, int] = (screen_width // 2, screen_height // 2)
        offset_x: int = screen_center[0] - text_width // 2
        offset_y: int = screen_center[1] - text_height // 2
        
        if swap_count is None:
            font_small: pygame.font.Font = pygame.font.Font("swap_puzzle/input_medias/Coalition_v2.ttf", 50)
            text_small: pygame.Surface = font_small.render(f"THE BEST SCORE POSSIBLE IS {optimal_swap_count}", True, (0, 128, 255))
        else:
            font_small = pygame.font.Font("swap_puzzle/input_medias/Victoire.ttf", 90)
            text_small = font_small.render(f"Your score is {swap_count}. The best score is {optimal_swap_count}", True, (255, 127, 0))
            
        text_small_width, text_small_height = text_small.get_size()
        offset_x_small: int = screen_center[0] - text_small_width // 2
        offset_y_small: int = offset_y + text_height + 20 
        
        screen.fill((0, 0, 0))
        screen.blit(text_surface, (offset_x, offset_y))
        screen.blit(text_small, (offset_x_small, offset_y_small))
        pygame.display.flip()
        
        await asyncio.sleep(4.5)
        
        pygame.display.quit()
        pygame.display.init()

        width: int = self.n * 100
        height: int = self.m * 100
        screen = pygame.display.set_mode((width, height + 100))
        
        logger.info("Launching AI solution replay computed by A* algorithm.")
        for swap in swap_sol:
            self.selected_cells = [swap[0], swap[1]]
            screen.fill((0, 0, 0))
            for i in range(self.m):
                for j in range(self.n):
                    cell_rect: pygame.Rect = pygame.Rect(j * 100, i * 100, 100, 100)
                    pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                    cell_font: pygame.font.Font = pygame.font.Font(None, 72)
                    text_cell: pygame.Surface = cell_font.render(str(self.state[i][j]), True, (0, 0, 0))
                    text_rect = text_cell.get_rect(center=cell_rect.center)
                    screen.blit(text_cell, text_rect)
                    if (i, j) in self.selected_cells:
                        pygame.draw.rect(screen, (255, 255, 0), cell_rect, 5)
            
            for barrier in self.barriers:
                (i1, j1), (i2, j2) = barrier
                if i1 == i2:
                    j = max(j1, j2)
                    pygame.draw.line(screen, (255, 0, 0), (j * 100, i1 * 100), (j * 100, (i1 + 1) * 100), 5)
                else:
                    i = max(i1, i2)
                    pygame.draw.line(screen, (255, 0, 0), (j1 * 100, i * 100), ((j1 + 1) * 100, i * 100), 5)
        
            pygame.draw.rect(screen, (255, 0, 0), (0, height, width, 100))
            btn_font: pygame.font.Font = pygame.font.Font(None, 72)
            text_quit: pygame.Surface = btn_font.render("Quit", True, (255, 255, 255))
            text_rect = text_quit.get_rect(center=(width // 2, height + 50))
            screen.blit(text_quit, text_rect)
            pygame.display.flip()
            
            await asyncio.sleep(1.5)
            
            self.swap(swap[0], swap[1])
            screen.fill((0, 0, 0))
            for i in range(self.m):
                for j in range(self.n):
                    cell_rect = pygame.Rect(j * 100, i * 100, 100, 100)
                    pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                    text_cell = btn_font.render(str(self.state[i][j]), True, (0, 0, 0))
                    text_rect = text_cell.get_rect(center=cell_rect.center)
                    screen.blit(text_cell, text_rect)
                    if (i, j) in self.selected_cells:
                        pygame.draw.rect(screen, (255, 0, 255), cell_rect, 5)
            
            pygame.display.flip()
            await asyncio.sleep(1.5)
        
        pygame.display.quit()
    
    async def difficulty(self) -> float:
        """
        Displays a menu to select the difficulty level and determines the allocated time ratio.

        Returns:
            float: The time multiplier coefficient (lower values reduce the available time).
        """
        pygame.display.init()

        screen_info: pygame.display._DisplayInfo = pygame.display.Info()
        screen_width: int = screen_info.current_w
        screen_height: int = screen_info.current_h
        screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))
        clock: pygame.time.Clock = pygame.time.Clock()
        font_size: int = screen_height // 15
        font: pygame.font.Font = pygame.font.SysFont("cambriamath", font_size)
        font_path: str = "swap_puzzle/input_medias/BLADRMF_.ttf"
        font_dif: pygame.font.Font = pygame.font.Font(font_path, font_size * 3)

        rect_width: int = screen_width // 6
        buffer_space: float = (screen_width - 5 * rect_width) / 6
        first_rect_left: int = screen_width // 30

        easy_rect: pygame.Rect = pygame.Rect(first_rect_left, screen_height // 2, rect_width, font_size + 20)
        medium_rect: pygame.Rect = pygame.Rect(easy_rect.right + buffer_space, screen_height // 2, rect_width, font_size + 20)
        difficult_rect: pygame.Rect = pygame.Rect(medium_rect.right + buffer_space, screen_height // 2, rect_width, font_size + 20)
        hardcore_rect: pygame.Rect = pygame.Rect(difficult_rect.right + buffer_space, screen_height // 2, rect_width, font_size + 20)
        infernal_rect: pygame.Rect = pygame.Rect(hardcore_rect.right + buffer_space, screen_height // 2, rect_width, font_size + 20)
        
        quit_button_rect: pygame.Rect = pygame.Rect((screen_width - screen_width // 2.5) // 2, screen_height // 1.6, screen_width // 2.5, font_size + 20)

        logger.info("Awaiting player difficulty selection...")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    logger.info("Application closed (Default difficulty: Medium).")
                    return 5.0

            mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
            mouse_click: Tuple[bool, bool, bool] = pygame.mouse.get_pressed()
            screen.fill((0, 0, 0))

            text_surface: pygame.Surface = font_dif.render("Difficulty", True, (255, 127, 0))
            text_rect: pygame.Rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 4))
            screen.blit(text_surface, text_rect)

            pygame.draw.rect(screen, (0, 255, 0), easy_rect)
            text_easy: pygame.Surface = font.render("Easy", True, (255, 255, 255))
            screen.blit(text_easy, text_easy.get_rect(center=easy_rect.center))
            
            pygame.draw.rect(screen, (255, 255, 50), medium_rect)
            text_med: pygame.Surface = font.render("Medium", True, (255, 255, 255))
            screen.blit(text_med, text_med.get_rect(center=medium_rect.center))
            
            pygame.draw.rect(screen, (255, 127, 0), difficult_rect)
            text_diff: pygame.Surface = font.render("Difficult", True, (255, 255, 255))
            screen.blit(text_diff, text_diff.get_rect(center=difficult_rect.center))
            
            pygame.draw.rect(screen, (86, 41, 0), hardcore_rect)
            text_hard: pygame.Surface = font.render("Hardcore", True, (255, 255, 255))
            screen.blit(text_hard, text_hard.get_rect(center=hardcore_rect.center))
            
            pygame.draw.rect(screen, (148, 0, 211), infernal_rect)
            text_inf: pygame.Surface = font.render("Infernal", True, (255, 255, 255))
            screen.blit(text_inf, text_inf.get_rect(center=infernal_rect.center))
            
            pygame.draw.rect(screen, (255, 0, 0), quit_button_rect)
            text_leave: pygame.Surface = font.render("Leave", True, (255, 255, 255))
            screen.blit(text_leave, text_leave.get_rect(center=quit_button_rect.center))

            if mouse_click[0] == 1:
                if easy_rect.collidepoint(mouse_pos): 
                    logger.info("Difficulty selected: Easy.")
                    return 10.0
                elif medium_rect.collidepoint(mouse_pos): 
                    logger.info("Difficulty selected: Medium.")
                    return 5.0
                elif difficult_rect.collidepoint(mouse_pos): 
                    logger.info("Difficulty selected: Difficult.")
                    return 2.5
                elif hardcore_rect.collidepoint(mouse_pos): 
                    logger.info("Difficulty selected: Hardcore.")
                    return 1.5
                elif infernal_rect.collidepoint(mouse_pos): 
                    logger.info("Difficulty selected: Infernal.")
                    return 0.8
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    logger.info("Leave button clicked from difficulty menu.")
                    return 5.0

            pygame.display.flip()
            clock.tick(30)
            await asyncio.sleep(0)

    async def retry(self) -> None:
        """
        Displays a pop-up confirmation screen to end or restart the game.
        If accepted, asynchronously launches a new session.
        """
        pygame.display.init()

        screen_info: pygame.display._DisplayInfo = pygame.display.Info()
        screen_width: int = screen_info.current_w
        screen_height: int = screen_info.current_h
        screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))
        clock: pygame.time.Clock = pygame.time.Clock()
        font_size: int = screen_height // 15
        font: pygame.font.Font = pygame.font.SysFont("cambriamath", font_size)
        font_path: str = "swap_puzzle/input_medias/ka1.ttf"
        font_title: pygame.font.Font = pygame.font.Font(font_path, font_size * 3)
        
        try:
            background_image: pygame.Surface = pygame.image.load("swap_puzzle/input_medias/drive-8493014_1920.jpg")  
            background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
            background_image.set_alpha(200)
        except pygame.error:
            logger.error("Failed to load retry background image.")
            background_image = pygame.Surface((screen_width, screen_height))
            background_image.fill((0, 0, 0))

        retry_button_rect: pygame.Rect = pygame.Rect(screen_width // 9, screen_height // 1.8, screen_width // 3, font_size + 20)
        leave_button_rect: pygame.Rect = pygame.Rect(retry_button_rect.right + screen_width // 8, screen_height // 1.8, screen_width // 3, font_size + 20)
        
        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
            mouse_click: Tuple[bool, bool, bool] = pygame.mouse.get_pressed()
            screen.fill((0, 0, 0))
            screen.blit(background_image, (0, 0))
            
            pygame.draw.rect(screen, (0, 255, 0), retry_button_rect)
            yes_text: pygame.Surface = font.render("Yes", True, (255, 255, 255))
            yes_rect: pygame.Rect = yes_text.get_rect(center=retry_button_rect.center)
            screen.blit(yes_text, yes_rect)
            
            pygame.draw.rect(screen, (255, 0, 0), leave_button_rect)
            leave_text: pygame.Surface = font.render("No", True, (255, 255, 255))
            leave_rect: pygame.Rect = leave_text.get_rect(center=leave_button_rect.center)
            screen.blit(leave_text, leave_rect)
            
            retry_surface: pygame.Surface = font_title.render("Retry ?", False, (255, 127, 0))
            retry_rect: pygame.Rect = retry_surface.get_rect(center=(screen_width // 2 + 10, screen_height // 3.5))
            screen.blit(retry_surface, retry_rect)
            
            if mouse_click[0] == 1:
                if retry_button_rect.collidepoint(mouse_pos):
                    logger.info("Player chose to restart a game session.")
                    await asyncio.sleep(1)
                    pygame.display.quit()
                    await self.display(True)
                    return
                if leave_button_rect.collidepoint(mouse_pos):
                    logger.info("Player declined to replay and closed the session.")
                    await asyncio.sleep(1)
                    pygame.display.quit()
                    return

            pygame.display.flip()
            clock.tick(30)
            await asyncio.sleep(0)

    async def settle_barriers(self) -> None:
        """
        Displays a confirmation menu asking whether the user wants to 
        include barriers on their game board.
        """
        pygame.init()
        screen_info: pygame.display._DisplayInfo = pygame.display.Info()
        screen_width: int = screen_info.current_w
        screen_height: int = screen_info.current_h
        screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))
        clock: pygame.time.Clock = pygame.time.Clock()
        font_size: int = screen_height // 15
        font: pygame.font.Font = pygame.font.SysFont("cambriamath", font_size)
        font_path: str = "swap_puzzle/input_medias/BLADRMF_.ttf"
        font_title: pygame.font.Font = pygame.font.Font(font_path, font_size * 2)
       
        yes_button_rect: pygame.Rect = pygame.Rect(screen_width // 9, screen_height // 1.8, screen_width // 3, font_size + 20)
        no_button_rect: pygame.Rect = pygame.Rect(yes_button_rect.right + screen_width // 8, screen_height // 1.8, screen_width // 3, font_size + 20)
        
        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
            mouse_click: Tuple[bool, bool, bool] = pygame.mouse.get_pressed()
            screen.fill((0, 0, 0))
            
            title_surface: pygame.Surface = font_title.render("Settle Barriers ?", False, (255, 127, 0))
            title_rect: pygame.Rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 3.5))
            screen.blit(title_surface, title_rect)
            
            pygame.draw.rect(screen, (0, 255, 0), yes_button_rect)
            yes_text: pygame.Surface = font.render("Yes", True, (255, 255, 255))
            screen.blit(yes_text, yes_text.get_rect(center=yes_button_rect.center))
            
            pygame.draw.rect(screen, (255, 0, 0), no_button_rect)
            no_text: pygame.Surface = font.render("No", True, (255, 255, 255))
            screen.blit(no_text, no_text.get_rect(center=no_button_rect.center))
            
            if mouse_click[0] == 1:
                if yes_button_rect.collidepoint(mouse_pos):
                    logger.info("Barriers enabled for the upcoming match.")
                    running = False
                if no_button_rect.collidepoint(mouse_pos):
                    logger.info("No barriers will be applied to the grid.")
                    self.barriers = []
                    running = False
            
            pygame.display.flip()
            clock.tick(30)
            await asyncio.sleep(0)
            
        pygame.display.quit()
    
    def music_player(self, new_sound_file_path=None):
        try:
            pygame.mixer.init()
        except pygame.error:
            return

        pygame.mixer.music.stop()

        if new_sound_file_path:
            pygame.mixer.music.load(new_sound_file_path)
            pygame.mixer.music.play(-1)
                
  



        
       
        