# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from game import Game 
from grid import Grid
g = Game(Grid(4,4))

g.music_player()