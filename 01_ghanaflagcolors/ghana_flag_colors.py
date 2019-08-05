"""Draw of the colors of the Ghana flag"""
__author__ = "Maurizio Boscaini, maurizio.boscaini@gmail.com"
__date__ = "$August 2nd, 2019$"
__version__ = "1.0"

# [0] Import general Python and Pygame specific modules
import sys
import os
import pygame

SIZE = WIDTH, HEIGHT = (800, 600)
RED = (206, 17, 38)
YELLOW = (252, 209, 22)
GREEN = (0, 107, 63)

# [1] Initialize Pygame modules
pygame.init()

# [2] Load game resources

# [3] Setup game objects (display, graphics, sprites,...)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Colors of the Ghana flag")
height = HEIGHT // 3
red_surface = pygame.Surface((WIDTH, height))
red_surface.fill(RED)
yellow_surface = pygame.Surface((WIDTH, height))
yellow_surface.fill(YELLOW)
green_surface = pygame.Surface((WIDTH, height))
green_surface.fill(GREEN)

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
    screen.blit(red_surface, (0, 0))
    screen.blit(yellow_surface, (0, height))
    screen.blit(green_surface, (0, 2 * height))

    # [9] Draw the game scene on the display area on the screen
    pygame.display.update()
