"""A simple memory game based on pretty animals with Pygame"""
__author__ = "Maurizio Boscaini, maurizio.boscaini@gmail.com"
__date__ = "$July 10, 2019$"
__version__ = "1.0"

import os
import random
from time import time
import pygame
from pygame.locals import *

SIZE = WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (0, 255, 0)
INTRO_TIME = 2
DEC_GUESS_TIMER = 0.2
SPRITE_DIM = 85
SPRITE_MARGIN = 60

def create_characters(names, ext='.png'):
    """Load and return a list of images and their names"""
    characters = []

    for name in names:
        filename = os.path.join('res', 'images', name + ext)
        image = pygame.image.load(filename)
        characters.append({"name":name, "image":image})

    return characters

def reset_counter(images):
    """Add/reset counters to a list of images"""
    for image in images:
        image['count'] = 0

def write_message(surface, basic_font, message, x='center', y='center'):
    """Write a message on a surface"""
    text = basic_font.render(message, True, BLACK)
    text_rect = text.get_rect()
    surface_rect = surface.get_rect()

    if x == 'center':
        text_rect.centerx = surface_rect.centerx
    else:
        if x >= 0:
            text_rect.x = x
        else:
            text_rect.x = surface_rect.width - text_rect.width + x

    if y == 'center':
        text_rect.centery = surface.get_rect().centery
    else:
        text_rect.y = y

    surface.blit(text, text_rect)

def create_scene1(characters, rows, cols):
    """Create the image for the first scene"""
    surface = pygame.Surface((SPRITE_DIM*cols, rows*SPRITE_DIM))
    surface.fill(WHITE)

    for row in range(rows):
        for col in range(cols): # Print a row of random characters
            character = characters[row*cols + col]
            surface.blit(character["image"], (col*SPRITE_DIM, row*SPRITE_DIM))

    return surface

def create_scene2(characters, basic_font, cols=5, show_text=False, choice=None, answer=None):
    """Create the image for the second scene"""
    rows = int(len(characters) / cols)
    width = cols*SPRITE_DIM
    height = rows*(SPRITE_DIM + SPRITE_MARGIN)
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for row in range(rows):
        for col in range(cols):
            index = row*cols + col

            if index < len(characters):
                character = characters[index]
                x = col*SPRITE_DIM
                y = row*(SPRITE_DIM + SPRITE_MARGIN)
                character["rect"] = Rect(x + width // 2, y + height // 2, SPRITE_DIM, SPRITE_DIM)
                surface.blit(character["image"], (x, y))

                # Caption
                if not show_text:
                    text = basic_font.render("?", True, BLACK)
                else:
                    caption = ' '+ str(character["count"]) +' '
                    text = basic_font.render(caption, True, BLACK)

                    if character == choice:
                        text = basic_font.render(' ' +caption +' ', True, BLACK, RED)

                    if character["count"] == answer:
                        text = basic_font.render(' '+ caption +' ', True, BLACK, GREEN)

                x_text = x + (SPRITE_DIM - text.get_rect().width) / 2
                y_text = row * (SPRITE_DIM + SPRITE_MARGIN) + SPRITE_DIM
                surface.blit(text, (x_text, y_text))

    return surface

def check_answer(pos, characters):
    """Return the character, if any, at the given position"""
    for character in characters:
        if character["rect"].collidepoint(pos[0], pos[1]):
            return character

def main():
    '''Game main function'''
    names = "elephant", "giraffe", "hippo", "monkey", "panda", \
              "parrot", "penguin", "pig", "rabbit", "snake"

    os.environ['SDL_VIDEO_CENTERED'] = '1'  # To center the window, before we initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SIZE) #, FULLSCREEN)
    pygame.display.set_caption("Guess the most frequent animal!")
    filename = os.path.join('res', 'fonts', 'Boogaloo-Regular.ttf')
    basic_font = pygame.font.Font(filename, 40)

    rows, cols = 4, 7   # Number of rows and columns (4 x 7 = 28 characters)
    animals = create_characters(names)

    running = True
    score = 0
    prev_state = None
    state = "intro"
    frame_start = time()
    guess_timer = 2.0
    games = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                if state == 'guess the animal':
                    pos = pygame.mouse.get_pos()
                    choice = check_answer(pos, animals)

                    if choice:
                        state = "check answer"

            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE]:
                running = False
            if keys[K_SPACE]:
                if state == 'next game':
                    guess_timer -= DEC_GUESS_TIMER
                    if guess_timer > DEC_GUESS_TIMER:
                        state = 'prepare animals'
                    else:
                        state = 'end'

                    frame_start = time()

        screen.fill(WHITE)
        if state not in ('intro', 'end'):
            message = "Score: "+ str(score) +'/'+ str(games)
            write_message(screen, basic_font, message, x=-20, y=2)
            write_message(screen, basic_font, "Timer: {:.2f}".format(guess_timer), x=10, y=2)

        if state == "intro":
            write_message(screen, basic_font, "GUESS THE ANIMAL")

            if time() - frame_start > INTRO_TIME:
                state = "prepare animals"
                frame_start = time()
        elif state == "prepare animals":
            max_count = 0
            reset_counter(animals)
            games += 1
            characters = []

            for i in range(rows * cols):
                character = random.choice(animals)
                characters.append(character)
                character["count"] += 1

                if character["count"] > max_count:
                    max_count = character["count"]

            scene1 = create_scene1(characters, rows, cols)
            scene1_rect = scene1.get_rect()
            scene1_rect.center = screen.get_rect().center

            scene2 = create_scene2(animals, basic_font=basic_font)
            scene2_rect = scene2.get_rect()
            scene2_rect.center = screen.get_rect().center
            state = "show animals"
        elif state == "show animals":
            screen.blit(scene1, scene1_rect)

            if time() - frame_start > guess_timer:
                state = "guess the animal"
                write_message(screen, basic_font, "Which animal has appeared at most?", y=40)
        elif state == "guess the animal":
            screen.blit(scene2, scene2_rect)
        elif state in ('check answer', 'next game'):
            scene3 = create_scene2(animals, basic_font=basic_font, show_text=True, choice=choice, answer=max_count)
            scene3_rect = scene3.get_rect()
            scene3_rect.center = screen.get_rect().center
            screen.blit(scene3, scene3_rect)

            if choice:
                if choice['count'] == max_count:
                    write_message(screen, basic_font, "You Guessed!", y=40)

                    if state == 'check answer':
                        score += 1
                else:
                    write_message(screen, basic_font, "You Missed!", y=60)
                write_message(screen, basic_font, "Press SPACE to continue ESC to quit", y=520)

            state = 'next game'
        elif state == 'end':
            message = "Score: "+ str(score) +'/'+ str(games)
            write_message(screen, basic_font, "Game Over\nFinal score: "+ message, x='center', y='center')

        if state != prev_state:
            print("Scene:", state)
            prev_state = state

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
