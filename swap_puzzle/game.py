from grid import Grid
import pygame
class Game():
    def __init__(self,grid):
        self.display = grid.display()
        self.m = grid.m
        self.n = grid.n
        self.state = grid.state
        
        
        