# [0] Import general Python modules and Pygame specific modules
import sys
import pygame

WHITE = (255, 255, 255)

# [1] Initialize Pygame modules
pygame.init()

# [2] Load game resources
# [3] Setup game objects (display, graphics, sprites,...)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hello Pycon Africa 2019!")

# [4] Setup game specific variables (counters for lives and score,...)
# [5] Game Loop
while True:
    # [6] Events' handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit

    # [7] Game logic (collisions, movements, ...)
    # [8] Prepare the game scene on the image buffer
    screen.fill(WHITE)

    # [9] Draw the game scene on the display area on the screen
    pygame.display.update()

