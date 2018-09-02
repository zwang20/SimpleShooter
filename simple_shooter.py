# modules
import pygame
from data import *
from sge import *

# loading screen
pygame.init()

sge_clear()
sge_print(string='Loading time')
pygame.display.update()

import time


sge_clear()
sge_print(string='Loading os')
pygame.display.update()

import os


sge_clear()
sge_print(string='Loading randint')
pygame.display.update()

from random import randint, choice


sge_clear()
sge_print(string='Loading data')
pygame.display.update()

game_data = sge_load()


sge_clear()
sge_print(string='Loading clock')
pygame.display.update()

clock = pygame.time.Clock()


sge_clear()
sge_print(string='Loading colours')
pygame.display.update()

white = (255, 255, 255)
black = (0, 0, 0)
red = (204, 51, 0)
orange = (255, 153, 0)
green = (51, 204, 51)
blue = (0, 102, 255)
grey = (40, 40, 50)


sge_clear()
sge_print(string='Adjusting height')
pygame.display.update()

try:
    if int(game_data['display_height']) > 0:
        display_height = int(game_data['display_height'])
    else:
        display_height = 800
except:
    display_height = 800


sge_clear()
sge_print(string='Adjusting width')
pygame.display.update()

try:
    if int(game_data['display_width']) > 0:
        display_width = int(game_data['display_width'])
    else:
        display_width = 800
except:
    display_width = 800


sge_clear()
sge_print(string='Adjusting ground height')
pygame.display.update()

try:
    if int(game_data['ground_height']) > 0:
        ground_height = int(game_data['ground_height'])
    else:
        ground_height = 200
except:
    ground_height = 200 # try not to hard code


sge_clear()
sge_print(string='Adjusting size')
pygame.display.update()

game_display = pygame.display.set_mode([display_width, display_height])


# sge_clear()
# sge_print(string='Loading background')
# pygame.display.update()
#
# background_image = pygame.image.load(os.path.join('assets', 'background_image.png'))
# background_image = pygame.transform.scale(background_image, (display_width, display_height))


sge_clear()
sge_print(string='Loading instructions')
pygame.display.update()

instruction_image = pygame.image.load(os.path.join('assets', 'instruction.png'))
instruction_image = pygame.transform.scale(instruction_image, (display_width, display_height))


sge_clear()
sge_print(string='Loading explosions')
pygame.display.update()

explosion = pygame.image.load(os.path.join('assets', 'explosion.png'))


sge_clear()
sge_print(string='Adjusting caption')
pygame.display.update()

pygame.display.set_caption('Simple Shooter')


sge_clear()
sge_print(string='Adding icon')
pygame.display.update()

pygame.display.set_icon(
pygame.image.load(os.path.join('assets', '32x32_simple_shooter.png'))
)


sge_clear()
sge_print(string='Loading laser sounds')
pygame.display.update()

laser_sound_1 = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'sfx_laser1.ogg'))
laser_sound_2 = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'sfx_laser2.ogg'))


class Bullet:
    width = 2
    length = 20
    speed = 8
    good = []
    bad = []

    def __init__(self, x, y, harmful=True):
        pygame.mixer.Sound.play(laser_sound_1) if randint(0,1) == 0 else pygame.mixer.Sound.play(laser_sound_2)
        self.x = x
        self.y = y
        self.harmful = harmful
        if harmful:
            Bullet.bad.append(self)
            temp = -50
        else:
            Bullet.good.append(self)
            temp = 25
        sge_print(game_display, 'Pew', x + temp, y, colour=white)

    def move(self):
        self.x -= Bullet.speed if self.harmful else -Bullet.speed
        if self.x > display_width-25 or self.x < 0:
            self.despawn()

    def display(self):
        if self.harmful:
            sge_rect(game_display, self.x, self.y, Bullet.length, Bullet.width, red)
        else:
            sge_rect(game_display, self.x, self.y, Bullet.length, Bullet.width, blue)

    def despawn(self):
        game_display.blit(explosion, (self.x, self.y))
        if self.harmful:
            Bullet.bad.remove(self)
        else:
            Bullet.good.remove(self)


class Player:
    width = 20
    height = 40
    score = 0

    def __init__(self):
        self.x = 0
        self.y = 0
        self.cooldown = 0

    def move(self, move_x, move_y):
        self.x += move_x
        self.y += move_y
        if self.x < 0:
            self.x = 0
        elif self.x > 300:
            self.x = 300
        if self.y < 0:
            self.y = 0
        elif self.y > display_height - ground_height - Player.height:
            self.y = display_height - ground_height - Player.height

    def fire(self):
        if self.cooldown % 5 == 0:
            if self.cooldown < 90:
                Bullet(self.x + 20, self.y + 10, False)
                self.cooldown += 20

    def get_hit(self): # checks if an enemy gets hit and respond accordingly
        for bullet in Bullet.bad:
            if self.x <= bullet.x <= self.x + Player.width:
                if self.y <= bullet.y <= self.y + Player.height:
                    bullet.despawn()
                    Player.score -= 10

    def renew(self):
        # cooldown recover
        if self.cooldown > 0:
            self.cooldown -= 1
        # gravity
        if self.y < display_height - ground_height - Player.height:
            self.y += 1
        # score above 0
        if Player.score < 0:
            Player.score = 0
        # difficulty renew
        if Player.score == 0:
            Enemy.limit = 1
        elif Player.score <= 30:
            Enemy.limit = 2
        elif Player.score <= 50:
            Enemy.limit = 3
        elif Player.score <= 70:
            Enemy.limit = 4
        elif Player.score <= 80:
            Enemy.limit = 5
        else:
            Enemy.limit = 6

    def display(self):
        sge_rect(game_display, self.x, self.y, Player.width, Player.height, white)
        sge_rect(game_display, self.x + Player.width, self.y + 10, 5, 5, white)


class Enemy:
    spawn_range = 500
    limit = 2
    width = 20
    height = 40
    family = []
    _difficulty = ("normal", "hard", "hell")

    def __init__(self, difficulty=None):
        self.spawn()
        if difficulty == None:
            difficulty = choice(Enemy._difficulty)
        if difficulty == "normal":
            self.speed = randint(1, 2)
            self.fire_cooldown = 1
        elif difficulty == "hard":
            self.speed = randint(2, 4)
            self.fire_cooldown = 0.5
        elif difficulty == "hell":
            self.speed = randint(4, 7)
            self.fire_cooldown = 0.3
        elif difficulty == "dummy":
            self.speed = 0
            self.fire_cooldown = 99999
        self.difficulty = difficulty
        self.dir = "up"
        self.fire_timer = time.time()
        self.spawn_protect = time.time()
        Enemy.family.append(self)

    def spawn(self):
        self.x = randint(Enemy.spawn_range, display_width - Enemy.width)
        self.y = randint(0, display_height - ground_height - Enemy.height)

    def display(self):
        if self.difficulty == "normal":
            color = green
        elif self.difficulty == "hard":
            color = orange
        elif self.difficulty == "hell":
            color = red
        elif self.difficulty == "dummy":
            color = white
        sge_rect(game_display, self.x, self.y, Enemy.width, Enemy.height, color)
        sge_rect(game_display, self.x - 5, self.y + 10, 5, 5, color)

    def move(self): # this now contains enemy ai
        self.y += self.speed if self.dir == "down" else -self.speed
        if self.y < self.speed:
            self.dir = "down"
        elif self.y > display_height - ground_height - Enemy.height - self.speed:
            self.dir = "up"

    def fire(self):
        if time.time() - self.fire_timer >= self.fire_cooldown:
            self.fire_timer = time.time()
            Bullet(self.x - 5, self.y + 7, True)

    def get_hit(self): # checks if an enemy gets hit and respond accordingly
        for bullet in Bullet.good:
            if self.x <= bullet.x <= self.x + Enemy.width and self.y <= bullet.y <= self.y + Enemy.height:
                if time.time() - self.spawn_protect > 1:
                    self.despawn()
                    bullet.despawn()
                    if self.difficulty == "normal":
                        Player.score += 10
                    elif self.difficulty == "hard":
                        Player.score += 15
                    elif self.difficulty == "hell":
                        Player.score += 20
                else:
                    sge_print(game_display,
                              "spawn protection",
                              self.x - Enemy.height,
                              self.y,
                              colour=white)
                    bullet.despawn()

    def despawn(self):
            Enemy.family.remove(self)

    def smart_spawn():
        while len(Enemy.family) < Enemy.limit:
            Enemy()


def ss_init():
    sge_clear()
    sge_print(game_display, 'This is a simple shooter')
    # TODO: complete this description
    ss_initial = True
    while ss_initial:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.display.quit()
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_SPACE:
                    ss_initial = False
        pygame.display.update()


def ss_pause():
    ss_pause = True
    while ss_pause:
        # sge_clear(game_display)
        game_display.blit(instruction_image, (0,0))
        sge_print(string='Paused', colour = white)
        sge_print(string = 'To unpause press keyboard "X"',y=30, colour = white)
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            ss_pause = False
        for event in pygame.event.get():  # Input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.display.quit()
                    pygame.quit()
                    quit()
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                quit()


def ss():
    while True:

        ss_init()
        ss_run = True

        player = Player()

        while ss_run:
            game_display.fill(grey)
            clock.tick(60)

            sge_rect(game_display, 0, display_height - ground_height, display_width, ground_height, black)  # Ground

            for event in pygame.event.get():  # Input
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    quit()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_q]:  # Quit
                pygame.display.quit()
                pygame.quit()
                quit()
            if keys[pygame.K_w]:  # Up
                player.move(0, -6)
            if keys[pygame.K_d]:  # Right
                player.move(4, 0)
            if keys[pygame.K_a]:  # Left
                player.move(-4, 0)
            if keys[pygame.K_s]:  # Down
                player.move(0, 3)
            if keys[pygame.K_SPACE]:  # Fire
                player.fire()
            if keys[pygame.K_p]:  # Pause
                ss_pause()

            # CALCULATIONS
            for enemy in Enemy.family:
                enemy.move()
                enemy.get_hit()
                enemy.fire()

            for bullet in Bullet.good + Bullet.bad:
                bullet.move()

            player.get_hit()
            player.renew()

            Enemy.smart_spawn()

            for enemy in Enemy.family:
                enemy.display()
            for bullet in Bullet.good + Bullet.bad:
                bullet.display()
            player.display()

            sge_rect(game_display, display_width-100, display_height-10, 100, 10, white)
            sge_rect(game_display, display_width-100, display_height-10, player.cooldown, 10, red)
            sge_print(game_display, Player.score, colour=white)

            pygame.display.update()


try:
    ss()
except KeyboardInterrupt:
    pygame.display.quit()
    pygame.quit()
    quit()
