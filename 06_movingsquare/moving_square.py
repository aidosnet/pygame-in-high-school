"""A program to move an object with the keyboard.
Credits:
[1] https://stackoverflow.com/questions/18995652/pygame-key-set-repeat-not-working?lq=1
"""
__author__ = "Maurizio Boscaini, maurizio.boscaini@gmail.com"
__date__ = "$July 18, 2019$"
__version__ = "1.0"

import pygame
from pygame.locals import *

SIZE = WIDTH, HEIGHT = (800, 600)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Moving square")
clock = pygame.time.Clock()
pygame.key.set_repeat(10, 10)

player = pygame.Rect((0, 0, 20, 20))
speed = 10
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # Move up/down/left/right by checking for pressed keys
        # and moving the player rect in-place
        keys = pygame.key.get_pressed()

        if keys[K_UP]:
            player.move_ip(0, -speed)
        if keys[K_DOWN]:
            player.move_ip(0, speed)
        if keys[K_RIGHT]:
            player.move_ip(speed, 0)
        if keys[K_LEFT]:
            player.move_ip(-speed, 0)

    # Ensure the player rect does not go out of screen
    player.clamp_ip(screen.get_rect())

    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, player)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
