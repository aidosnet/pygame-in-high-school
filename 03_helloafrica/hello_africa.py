"""A basic Hello Africa with Pygame.
Credits:
[1] "Python Pygame Introduction" by Pete Shinners, https://www.pygame.org/docs/tut/PygameIntro.html
"""
__author__ = "Maurizio Boscaini, maurizio.boscaini@gmail.com"
__date__ = "$July 6, 2019$"
__version__ = "1.0"

# [0] Import general Python modules and Pygame specific modules
import sys
import os
import pygame

SIZE = WIDTH, HEIGHT = (800, 600)
WHITE = (255, 255, 255)

# [1] Initialize Pygame modules
pygame.init()

# [2] Load game resources
filename = os.path.join('res', 'images', 'logo-pycon-africa.png')
logo = pygame.image.load(filename)

# [3] Setup game objects (display, graphics, sprites,...)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Hello, Pycon Africa 2019!")
x = (WIDTH - logo.get_width()) // 2
y = (HEIGHT - logo.get_height()) // 2

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
    screen.fill(WHITE)
    screen.blit(logo, (x, y))

    # [9] Draw the game scene on the display area on the screen
    pygame.display.update()
