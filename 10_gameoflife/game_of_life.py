"""Conway Game of Life with Pygame"""
__author__ = "Alessandro Marchioro, Maurizio Boscaini, maurizio.boscaini@gmail.com"
__date__ = "$July 27, 2019$"
__version__ = "2.0"

import copy
from random import randint
import pygame
from pygame.locals import *

SIZE = WIDTH, HEIGHT = (800, 600)
FPS = 10
BG_COLOR = (0, 0, 0)
CELL_COLOR = (255, 0, 0)
CELL_DIM = 20

class Cell:
    """Represents a cell of the game"""
    def __init__(self, row, col, border=1):
        self.row = row
        self.col = col
        self.border = border
        self.state = randint(0, 1)

    def draw(self, surface):
        """Draw the cell on the given surface"""
        pygame.draw.rect(surface, CELL_COLOR, (
            self.col * CELL_DIM + self.border,
            self.row * CELL_DIM + self.border,
            CELL_DIM - self.border*2, CELL_DIM - self.border*2
            )
        )


class Grid:
    """Represents the grid of cells or the board of the game"""

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.reset()

    def reset(self):
        """Create a new grid of cells"""
        self.grid = [
            [Cell(row, col) for col in range(self.cols)] for row in range(self.rows)
        ]

    def transition(self):
        """Go to the next generation applying the Conway game of life's rules"""
        next_grid = copy.deepcopy(self.grid)

        for row in range(self.rows):
            for col in range(self.cols):
                neighbours = (  (row-1, col-1), (row-1, col), (row-1, col+1),
                                (row, col-1), (row, col), (row, col+1),
                                (row+1, col-1), (row+1, col), (row+1, col+1) )
                cell = self.grid[row][col]
                next_cell = next_grid[row][col]
                count = 0

                for neighbour in neighbours:
                    if self.is_valid(neighbour):
                        count += self.grid[neighbour[0]][neighbour[1]].state;

                if cell.state and (count < 2 or count > 3):
                    next_cell.state = 0  # Cell dies for starvation or overpopulation
                elif not cell.state and count == 3:
                    next_cell.state = 1  # Cell generation

        self.grid = next_grid

    def is_valid(self, coords):
        """Return True if the coordinates ar valid, False otherwise"""
        return 0 <= coords[0] < self.rows and 0 <= coords[1] < self.cols

    def draw(self, surface):
        """Draw the grid on the given surface"""
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]

                if cell.state:
                    cell.draw(surface)

os.environ['SDL_VIDEO_CENTERED'] = '1'  # To center the window, before we initialize pygame
pygame.init()
screen = pygame.display.set_mode(SIZE, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption('Game of Life')
clock = pygame.time.Clock()
_rows = HEIGHT // CELL_DIM
_cols = WIDTH // CELL_DIM
grid = Grid(_rows, _cols)
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_SPACE:
                grid.reset()

    # Game logic
    grid.transition()

    # Display update
    pygame.Surface.fill(screen, BG_COLOR)
    grid.draw(screen)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
