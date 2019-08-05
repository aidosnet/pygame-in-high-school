"""A basic bouncing ball with Pygame."""
__author__ = "Maurizio Boscaini, maurizio.boscaini@gmail.com"
__date__ = "$July 6, 2019$"
__version__ = "1.0"

# [0] Import general Python and Pygame specific modules
import sys
import os
from random import randint
import pygame

BLACK = (0, 0, 0)
SIZE = WIDTH, HEIGHT = (800, 600)

def main():
    '''Main function'''
    # [1] Initialize Pygame modules
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # To center the window, before we initialize pygame
    pygame.init()

    # [2] Load game resources
    filename = os.path.join('res', 'images', 'ball.gif')
    ball = pygame.image.load(filename)

    # [3] Setup game objects (display, graphics, sprites,...)
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Bouncing Ball")

    # [4] Setup game specific variables (counters for lives and score,...)
    ball_rect = ball.get_rect() # Rect object for the ball
    speed = [2, 2] # Vectorial speed

    # [5] Game Loop
    while True:
        screen.fill(BLACK)
        ball_rect = ball_rect.move(speed)

        # [6] Events management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # [7] Game logic (collisions, movements, ...)
        if ball_rect.left < 0 or ball_rect.right > WIDTH:
            speed[0] = -speed[0]
        if ball_rect.top < 0 or ball_rect.bottom > HEIGHT:
            speed[1] = -speed[1]

        # [8] Prepare the game scene on the image buffer
        screen.blit(ball, ball_rect)

        # [9] Draw the game scene on the display area on the screen
        pygame.display.update()
        pygame.time.delay(5)

if __name__ == "__main__":
    main()
