"""An example of a random colorful squares painting"""
__author__ = "Maurizio Boscaini, maurizio.boscaini@gmail.com"
__date__ = "$August 2nd, 2019$"
__version__ = "1.0"

# [0] Import general Python modules and Pygame specific modules
import sys
import os
import pygame
from random import randrange

WHITE = (255, 255, 255)
N_SQUARES = 1000
SIZE = WIDTH, HEIGHT = (800, 600)
SIDE = 20

# [1] Initialize Pygame modules
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Random squares painting")

# [2] Load game resources
# [3] Setup game objects (display, graphics, sprites,...)
screen.fill(WHITE)
for _ in range(N_SQUARES):
    color = randrange(255), randrange(255), randrange(255)
    pos = randrange(WIDTH), randrange(HEIGHT)
    x, y = randrange(WIDTH), randrange(HEIGHT)
    pointlist = [(x, y), (x + SIDE, y), (x + SIDE, y + SIDE), (x, y + SIDE)]
    pygame.draw.polygon(screen, color, pointlist)

# [4] Setup game specific variables (counters for lives and score,...)
# [5] Game Loop
while True:
    # [6] Events' handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # [7] Game logic (collisions, movements, ...)
    # [8] Prepare the game scene on the image buffer
    # [9] Draw the game scene on the display area on the screen
    pygame.display.update()
