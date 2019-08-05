"""A basic image animation with Pygame.
Credits:
[1] https://commons.wikimedia.org/wiki/File:Rotating_earth_(large).gif
[2] https://en.wikipedia.org/wiki/File:Rotating_globe.gif
[3] https://en.wikipedia.org/wiki/File:Blue_Marble_rotating.gif
"""
__author__ = "Maurizio Boscaini, maurizio.boscaini@gmail.com"
__date__ = "$July 23, 2019$"
__version__ = "1.0"

# [0] Import general Python and Pygame specific modules
import sys
import os
import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
SIZE = WIDTH, HEIGHT = (800, 600)

def main(name, n_images, fps=60, bg_color=BLACK, sep='-', zero_leading=False):
    '''Main function'''
    # [1] Initialize Pygame modules
    pygame.init()

    # [2] Load game resources
    images = []

    for i in range(n_images):
        num = '{:02d}'.format(i) if zero_leading else str(i)
        filename = os.path.join('res', 'images', name, name + sep + num +'.png')
        image = pygame.image.load(filename)
        images.append(image)

    # [3] Setup game objects (display, graphics, sprites,...)
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Rotating World")
    clock = pygame.time.Clock()

    # [4] Setup game specific variables (counters for lives and score,...)
    index = 0
    x = (WIDTH - images[0].get_rect().width) // 2
    y = (HEIGHT - images[0].get_rect().height) // 2

    # [5] Game Loop
    while True:
        # [6] Events management
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # [7] Game logic (collisions, movements, ...)
        image = images[index]
        index = (index + 1) % n_images

        # [9] Draw the updated game scene on the display area on the screen
        screen.fill(bg_color)
        screen.blit(image, (x, y))
        pygame.display.update()
        clock.tick(fps)

if __name__ == "__main__":
    # main("Blue_Marble_rotating", 721)
    # main("world", 20, fps=5, sep="", zero_leading=True)
    main("Rotating_globe", 299, fps=20)