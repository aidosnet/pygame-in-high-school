"""Draws random colorful squares"""
__author__ = "Maurizio Boscaini, maurizio.boscaini@gmail.com"
__date__ = "$July 29, 2019$"
__version__ = "1.0"

import os
from random import randint
import pygame
from pygame.locals import *

SIZE = WIDTH, HEIGHT = (800, 640)
FPS = 5
SIDE = 80

class Cell:
    """Represents a cell on a grid"""
    def __init__(self, row, col, border=1):
        self.row = row
        self.col = col
        self.border = border
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

    def draw(self, surface):
        """Draw the cell on the given surface"""
        pygame.draw.rect(surface, self.color, (
            self.col * SIDE + self.border,
            self.row * SIDE + self.border,
            SIDE - self.border*2, SIDE - self.border*2
            )
        )


class Grid:
    """Represents a grid of cells"""
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.reset()

    def reset(self):
        """Create a new grid of cells"""
        self.grid = [
            [Cell(row, col) for col in range(self.cols)] for row in range(self.rows)
        ]

    def draw(self, surface):
        """Draw the grid on the given surface"""
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                cell.draw(surface)

os.environ['SDL_VIDEO_CENTERED'] = '1'  # To center the window, before we initialize pygame
pygame.init()
screen = pygame.display.set_mode(SIZE, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption('Random Cells')
clock = pygame.time.Clock()
_rows = HEIGHT // SIDE
_cols = WIDTH // SIDE
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
    grid.reset()

    # Display update
    grid.draw(screen)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
