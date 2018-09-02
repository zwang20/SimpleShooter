# modules
import pygame
import time
from data import *  # Edward this works don't change it 'cause i don't know why
from sge import *

# loading screen
pygame.init()


sge_clear()
sge_print(string='Loading os')
pygame.display.update()

import os


sge_clear()
sge_print(string='Loading randint')
pygame.display.update()

from random import randint


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
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


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


sge_clear()
sge_print(string='Adjusting caption')
pygame.display.update()

pygame.display.set_caption('Simple Shooter')


sge_clear()
sge_print(string='Adding icon')
pygame.display.update()

pygame.display.set_icon(
pygame.image.load(os.path.join('assets', '32x32_project_ss.png'))
)


class Bullet:
    width = 2
    length = 20
    speed = 10
    good = []
    bad = []

    def __init__(self, x, y, harmful=True):
        self.x = x
        self.y = y
        self.harmful = harmful
        if harmful:
            Bullet.bad.append(self)
            temp = -50
        else:
            Bullet.good.append(self)
            temp = 25
        sge_print(game_display, 'Pew', x + temp, y)

    def move(self):
        self.x -= Bullet.speed if self.harmful else -Bullet.speed
        if self.x > 800 or self.x < 0:
            self.despawn()

    def display(self):
            sge_rect(game_display, self.x, self.y, Bullet.length, Bullet.width, red)

    def despawn(self):
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

    def display(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.y < 560:
            self.y += 1
        sge_rect(game_display, self.x, self.y, 20, 40)
        sge_rect(game_display, self.x + 20, self.y + 10, 5, 5)


class Enemy:
    offset = 10
    limit = 4
    width = 20
    height = 40
    family = []

    def __init__(self, difficulty='normal'):
        self.spawn()
        if difficulty == "normal":
            self.speed = 1
            self.fire_cooldown = 1
        elif difficulty == "hard":
            self.speed = 3
            self.fire_cooldown = 0.5
        elif difficulty == "hell":
            self.speed = 5
            self.fire_cooldown = 0.3
        else:
            self.speed = 0
            self.fire_cooldown = 1
        self.dir = "up"
        self.fire_timer = time.time()
        self.spawn_protect = time.time()
        Enemy.family.append(self)

    def spawn(self):
        self.x = display_width - Enemy.width - Enemy.offset
        self.y = randint(0, display_height - ground_height - Enemy.height)

    def display(self):
        sge_rect(game_display, self.x, self.y, Enemy.width, Enemy.height)
        sge_rect(game_display, self.x - 5, self.y + 10, 5, 5)

    def move(self): # this now contains enemy ai
        self.y += self.speed if self.dir == "down" else -self.speed
        if self.y < self.speed:
            self.dir = "down"
        elif self.y > 580 - self.speed:
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
                        Player.score += 10
                    else:
                        sge_print(game_display, "spawn protection", self.x - Enemy.height, self.y)
                        bullet.despawn()

    def despawn(self):
            Enemy.family.remove(self)

    def smart_spawn():
        if len(Enemy.family) <= Enemy.limit:
            Enemy.offset += 30
            Enemy("hell")


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


def ss_bullet(x, y, colour=blue):
    sge_rect(game_display, x, y, 10, 2, colour)


def ss_pause():
    ss_pause = True
    while ss_pause:
        sge_clear(game_display)
        sge_print(game_display, 'Paused')
        sge_print(game_display, 'To unpause press x', 1, 30)
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            ss_pause = False
        for event in pygame.event.get():  # Input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.display.quit()
                    pygame.quit()
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()


def ss():
    while True:

        ss_init()
        ss_run = True

        player = Player()

        while ss_run:
            sge_clear(game_display)
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
                player.move(0, -4)
            if keys[pygame.K_d]:  # Right
                player.move(3, 0)
            if keys[pygame.K_a]:  # Left
                player.move(-3, 0)
            if keys[pygame.K_s]:  # Down
                player.move(0, 2)
            if keys[pygame.K_SPACE]:  # Fire
                player.fire()
            if keys[pygame.K_p]:  # Pause
                ss_pause()

            Enemy.smart_spawn()

            # DISPLAY
            sge_rect(game_display, 700, 790, 100, 10, white)
            sge_rect(game_display, 700, 790, player.cooldown, 10, red)

            for enemy in Enemy.family:
                enemy.move()
                enemy.get_hit()
                enemy.display()
                enemy.fire()

            for bullet in Bullet.good + Bullet.bad:
                bullet.display()
                bullet.move()

            sge_print(game_display, Player.score)
            player.get_hit()
            player.display()

            pygame.display.update()


try:
    ss()
except KeyboardInterrupt:
    pygame.display.quit()
    pygame.quit()
    quit()
