# This project is created by Michael Wang, a student from Knox Grammar School.
# With help from Edward Ji, another student from Knox Grammar School.

# modules
import pygame
import time
from data import *  # Edward this works don't change it 'cause i don't know why
from sge import *
# Loading screen
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
    def __init__(self):
        pass

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
                    if time.time() - self.spawn_protect > 3:
                        self.despawn()
                        bullet.despawn()
                    else:
                        sge_print(game_display, "spawn protection", self.x - Enemy.height, self.y)

    def despawn(self):
            Enemy.family.remove(self)

    def smart_spawn():
        if len(Enemy.family) <= Enemy.limit:
            Enemy.offset += 30
            Enemy("normal")


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


def ss_player(x, y):
    sge_rect(game_display, x, y, 20, 40)
    sge_rect(game_display, x+20, y+10, 5, 5)


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
        ss_pos = [0, 0]
        ss_cooldown = 0
        ss_score = 0

        while ss_run:
            sge_clear(game_display)
            clock.tick(60)

            sge_rect(game_display, 0, display_height - ground_height, display_width, ground_height, black)  # Ground

            ss_fire = False

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
                if ss_pos[1] > 0:
                    ss_pos[1] -= 4
            if keys[pygame.K_d]:  # Right
                if ss_pos[0] < 300:
                    ss_pos[0] += 3
            if keys[pygame.K_a]:  # Left
                if ss_pos[0] > 0:
                    ss_pos[0] -= 3
            if keys[pygame.K_s]:  # Down
                if ss_pos[1] < 560:
                    ss_pos[1] += 2
            if keys[pygame.K_SPACE]:  # Fire
                ss_fire = True
            if keys[pygame.K_p]:  # Pause
                ss_pause()

            # Gravity
            if ss_pos[1] < 560:
                ss_pos[1] += 1

            # Fire
            if ss_cooldown%5 == 0:
                if ss_fire == True:
                    if ss_cooldown < 90:
                        Bullet(ss_pos[0]+20, ss_pos[1]+10, False)
                        ss_cooldown += 20
            if ss_cooldown > 0:
                ss_cooldown -= 1

            # DISPLAY
            sge_rect(game_display, 700, 790, 100, 10, white)
            sge_rect(game_display, 700, 790, ss_cooldown, 10, red)

            for enemy in Enemy.family:
                enemy.move()
                enemy.get_hit()
                enemy.display()
                enemy.fire()

            for bullet in Bullet.good + Bullet.bad:
                bullet.display()
                bullet.move()

            Enemy.smart_spawn()

            sge_print(game_display, ss_score)
            ss_player(ss_pos[0], ss_pos[1])
            pygame.display.update()


try:
    ss()
except KeyboardInterrupt:
    pygame.display.quit()
    pygame.quit()
    quit()
