'''Game quiz about nation flags with Pygame.
Credits:
[1] Linux Pro n. 65
[2] Super Trivia Challenge - 1.1 http://www.pygame.org/project/530/ [missing]
'''
__author__ = "Maurizio Boscaini, maurizio.boscaini@gmail.com"
__date__ = "$July 24, 2019$"
__version__ = "2.0"

import os
from random import randint, sample
import pygame
from pygame.locals import *

SIZE = WIDTH, HEIGHT = (640, 480)
N_QUESTIONS = 5
N_CHOICES = 3
BG_COLOR = (30)
CHOICE_COLOR = (255, 255, 255)
INTERFACE_COLOR = (244, 246, 129)
CORRECT_CHOICE_COLOR = (100, 255, 100)
WRONG_CHOICE_COLOR = (255, 50, 50)
BOX_BORDER = 40

def draw_flag(surface, name):
    '''Draw the specified flag with a border'''
    filename = os.path.join('res', 'images', 'flags', name + '.png')
    image = pygame.image.load(filename)
    border = 2
    width = image.get_rect().width + border * 2
    height = image.get_rect().height + border * 2
    x = (surface.get_width() - image.get_width()) // 2
    y = 60
    rect = pygame.Rect(x - border, y - border, width, height)
    pygame.draw.rect(surface, (255, 255, 255), rect)
    surface.blit(image, (x, y))

def draw_options(surface, options, font, index=None):
    '''Draw the possible options'''
    for i in range(N_CHOICES):
        name = options[i].replace('_', " ")
        color = CORRECT_CHOICE_COLOR if index == i else CHOICE_COLOR
        message = font.render('[{}] {}'.format(i + 1, name), True, color)
        surface.blit(message, (30, 200 + 100*i))

def draw_game_over(screen, score, font):
    screen.fill(BG_COLOR)
    info_text = []
    info_text.append(font.render('GAME OVER', True, INTERFACE_COLOR))
    info_text.append(font.render('', True, INTERFACE_COLOR))
    message = 'SCORE: '+ str(score) +'/'+ str(N_QUESTIONS)
    info_text.append(font.render(message, True, CORRECT_CHOICE_COLOR))
    info_text.append(font.render('', True, INTERFACE_COLOR))
    info_text.append(font.render('Press SPACE to play again ESC to quit', True, INTERFACE_COLOR))
    draw_info_box(screen, info_text, BOX_BORDER, BOX_BORDER)

def blit_center(surface, images):
    '''Draw a list of images centered vertically and horizonally'''
    h, w = 0, 0
    for image in images:
        w = max(w, image.get_width())
        h += image.get_height()

    y = (surface.get_height() - h) // 2

    for image in images:
        x = (surface.get_width() - image.get_width()) // 2
        surface.blit(image, (x, y))
        y += image.get_height()

def draw_info_box(surface, images, horizontal_border=0, vertical_border=0, alpha=255):
    '''Draw the game info box'''
    h, w = 0, 0
    for image in images:
        w = max(w, image.get_width())
        h += image.get_height()

    w += horizontal_border
    h += vertical_border
    box = pygame.Surface((w, h), 0, 32)
    box.set_alpha(alpha)
    blit_center(box, images)
    blit_center(surface, [box])

def get_answer():
    '''Wait until key 1, 2 or 3 or Escape are clicked'''
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                exit() # sys.exit()
            elif e.type == KEYDOWN:
                if  e.key == K_ESCAPE:
                    exit()
                elif e.key == K_1:
                    return 1
                elif e.key == K_2:
                    return 2
                elif e.key == K_3:
                    return 3

def wait_for_continue():
    '''Wait until a key (in the given list if specified) is pressed'''
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_SPACE:
                    return True

def main():
    '''Game main function'''
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # To center the window, before we initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SIZE) #, FULLSCREEN)
    pygame.display.set_caption("Guess the flag")
    font1 = pygame.font.Font(None, 30)
    font2 = pygame.font.Font(None, 40)
    filename = os.path.join('res', 'data', 'nations.txt')
    nations = [nation.strip() for nation in open(filename)]
    running = True

    while running:
        count = 0
        score = 0

        while count < N_QUESTIONS:
            screen.fill(BG_COLOR)

            # Choose without including the duplicates the options and select a nation to guess between them
            options = sample(nations, k=N_CHOICES)
            index = randint(0, N_CHOICES - 1)
            flag = options[index]
            draw_flag(screen, flag)
            draw_options(screen, options, font2)

            # Draw the question count and the score
            message = 'Question '+ str(count + 1) +" / "+ str(N_QUESTIONS)
            step_text = font1.render(message, True, INTERFACE_COLOR)
            screen.blit(step_text, (30, 20))

            message = 'Score: '+ str(score) +' / '+ str(N_QUESTIONS)
            score_text = font1.render(message, True, INTERFACE_COLOR)
            screen.blit(score_text, (500, 20))

            pygame.display.update()

            # Game logic
            answer = get_answer()
            draw_options(screen, options, font2, index)

            if answer == index + 1:
                result_text = font1.render('Correct answer!', True, CORRECT_CHOICE_COLOR)
                score += 1
            else:
                result_text = font1.render('Wrong answer!', True, WRONG_CHOICE_COLOR)

            info_text = font1.render('Press SPACE to continue', True, INTERFACE_COLOR)
            draw_info_box(screen, [result_text, info_text], BOX_BORDER, BOX_BORDER, 170)

            pygame.display.update()

            wait_for_continue()  # Wait for space bar press
            count += 1

        draw_game_over(screen, score, font1)
        pygame.display.update()
        pygame.time.delay(1000)

        running = wait_for_continue()  # Continue?

if __name__ == "__main__":
    main()
