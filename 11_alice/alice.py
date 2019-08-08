'''Alice has to coll-ect the cherries and escape the enemies.
Credits:
[1] aliens.py, included in the Pygame examples
[2] http://www.scriptedfun.com/video-tutorial-1-making-a-barebones-pygame-program
[3] http://www.iconarchive.com/category/game/alice-game-icons-by-imil.html Free for NC use.
[4] http://www.losersjuegos.com.ar/referencia/videos/python_y_pygame_cafeconf_2007
'''
__author__ = "Maurizio Boscaini, maurizio.boscaini@gmail.com"
__date__ = "$July 28, 2019$"
__version__ = "2.0"

import os.path
from random import randint
import pygame
from pygame.locals import *

SIZE = WIDTH, HEIGHT = (640, 480)
FONT_COLOR = (10, 10, 10)
BORDER = 30
N_CHERRIES = 10
N_ENEMIES = 10
LEFT, RIGHT, UP, DOWN = range(4)
FPS = 30


class Alice(pygame.sprite.Sprite):
    '''Represents the avatar of the player'''
    speed = 12

    def __init__(self, area):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.area = area
        self.image = load_image('Alice.gif')
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT))
        self.is_moving = True

    def move(self, keystate):
        '''Move the sprite inside the area'''
        if keystate[K_LEFT]:
            x_direction, y_direction = -1, 0
        elif keystate[K_RIGHT]:
            x_direction, y_direction = 1, 0
        elif keystate[K_UP]:
            x_direction, y_direction = 0, -1
        elif keystate[K_DOWN]:
            x_direction, y_direction = 0, 1
        else:
            x_direction, y_direction = 0, 0

        if x_direction or y_direction:
            self.rect.move_ip(x_direction * self.speed, y_direction * self.speed)
            self.rect = self.rect.clamp(self.area.get_rect())


class Cherry(pygame.sprite.Sprite):
    '''Represents an object (a cherry) to collect'''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image('cherry.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect_colision = self.rect.inflate(-30, -10)

    def update(self):
        pass


class Enemy(pygame.sprite.Sprite):
    '''Represents an enemy'''
    speed = 6
    seeds = ['Cross', 'Diamond', 'Heart', 'Spade']
    current_seed = 0
    directions = {LEFT: (-1, 0), RIGHT: (1, 0), UP: (0, -1), DOWN: (0, 1)}

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        Enemy.current_seed = (Enemy.current_seed + 1) % len(Enemy.seeds)
        self.image = load_image(Enemy.seeds[Enemy.current_seed] + '.gif')
        x = randint(0, WIDTH - BORDER)
        y = BORDER
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect_collision = self.rect.inflate(-30, -30)
        self.direction = DOWN

    def update(self):
        """Control the sprite behavior"""
        if self.rect.x > WIDTH - self.rect.w:
            self.direction = LEFT
        elif self.rect.x < 0:
            self.direction = LEFT

        if self.rect.y > HEIGHT - self.rect.h:
            self.direction = UP
        elif self.rect.y < 0:
            self.direction = DOWN

        dx, dy = self.directions[self.direction]
        self.rect.move_ip(dx * self.speed, dy * self.speed)

def load_image(filename):
    '''Load and return an image from a file'''
    filename = os.path.join('res', 'images', filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image: " + filename)
        raise SystemExit(message)
    return image

def draw_info_panel(screen, font, time, score):
    '''Disegna alcune informazioni del gioco e ne ritorna i rect'''
    score_panel = font.render("Score: %d" % score, True, FONT_COLOR)
    screen.blit(score_panel, (20, 10))

    time_panel = font.render("Time: %d" % time, True, FONT_COLOR)
    screen.blit(time_panel, (screen.get_width() - 100, 10))

    return (Rect(20, 10, score_panel.get_width(), score_panel.get_height()),
        Rect(screen.get_width() - 100, 10, time_panel.get_width(), time_panel.get_height()))

def main():
    '''Game main function'''
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # To center the window, before we initialize pygame
    pygame.init() # Attempts to initialize all the Pygame modules for you
    screen = pygame.display.set_mode(SIZE) #FULLSCREEN)
    icon = pygame.transform.scale(load_image('Alice.gif'), (32, 32))
    pygame.display.set_icon(icon)  # Window icon
    pygame.display.set_caption("Alice Hunter")

    filename = os.path.join('res', 'fonts', 'LiberationMono-Bold.ttf')
    font = pygame.font.Font(filename, 16)

    if pygame.mixer:
        music = os.path.join('res', 'sounds', 'background.wav')
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1) # Background music

    background = load_image('background.png')

    # Create sprite groups
    all = pygame.sprite.Group()
    cherries = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    players = pygame.sprite.Group()

    # Assign sprites to groups
    Alice.containers = all, players
    Enemy.containers = all, enemies
    Cherry.containers = all, cherries

    player = Alice(screen)

    # Spread the cherries on the ground
    for _ in range(N_CHERRIES):
        x = randint(0, WIDTH - BORDER)
        y = randint(0, HEIGHT - BORDER)
        cherries.add(Cherry(x, y))

    clock = pygame.time.Clock()
    time = 0
    score = 0

    pygame.time.set_timer(USEREVENT + 1, 1000) # Raise an event every second

    while player.alive():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return  # Game over
            elif event.type == USEREVENT + 1:
                time += 1
                if len(enemies) < N_ENEMIES:  # Create the enemies
                    enemies.add(Enemy())
            elif event.type == KEYDOWN:
                if event.unicode == 'q' or event.key == K_ESCAPE:
                    pygame.quit()
                    return # Game over
                elif event.unicode == 'f':
                    pygame.display.toggle_fullscreen()

        keystate = pygame.key.get_pressed()
        player.move(keystate)
        all.update()

        # Collisions detection
        if pygame.sprite.groupcollide(enemies, players, 0, 1):
            pygame.quit()
            return  # Game over
        elif pygame.sprite.spritecollide(player, cherries, 1):
            score += 1

        screen.blit(background, (0, 0))
        draw_info_panel(screen, font, time, score)
        all.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
