from swap_puzzle.grid import Grid
from swap_puzzle.game import Game


def main():
    grid = Grid(5, 5)
    game = Game(grid)
    game.display()


if __name__ == "__main__":
    main()