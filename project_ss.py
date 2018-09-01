# This project is created by Michael Wang, a student from Knox Grammar School.
# With help from Edward Ji, another student from Knox Grammar School.

# modules
import pygame
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
        else:
            Bullet.good.append(self)

    def move(self):
        self.x -= Bullet.speed if self.harmful else -Bullet.speed

    def display(self):
        if self.harmful:
            sge_rect(game_display, self.x, self.y, Bullet.length, Bullet.width, red)
        else:
            sge_rect(game_display, self.x, self.y, Bullet.length, Bullet.width, red)

class Enemy:
    width = 20
    height = 40
    family = []

    def __init__(self):
        self.spawn()
        Enemy.family.append(self)

    def spawn(self):
        self.x = display_width - Enemy.width - 10
        self.y = randint(0, display_height - Enemy.height)

    def display(self):
        sge_rect(game_display, self.x, self.y, Enemy.width, Enemy.height)
        sge_rect(game_display, self.x - 5, self.y + 10, 5, 5)

    def move(player_x, player_y, difficulty='normal'):
        pass


def ss_bad_ai(q,w,e,r):
    pass


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
        ss_bad_pos = [500, 500]
        ss_bullets = []
        ss_bad_bullets = []
        ss_cooldown = 0
        ss_bad_cooldown = 0
        ss_score = 0
        ss_bad_move_cooldown = 0

        while ss_run:
            sge_clear(game_display)
            clock.tick(60)
            sge_rect(game_display, 0, 600, 800, 200, black)  # Ground
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
                if ss_pos[0] < 780:
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
                        sge_print(game_display, 'Pew', ss_pos[0]+20, ss_pos[1])
                        Bullet(ss_pos[0]+20, ss_pos[1]+10, False)
                        # ss_bullets.append([ss_pos[0]+20, ss_pos[1]+10])
                        ss_cooldown += 20
            if ss_cooldown > 0:
                ss_cooldown -= 1

            # display
            for bullet in Bullet.good:
                bullet.display()
                bullet.move()

                # TODO

            # Bullets Move
            # ss_bullets_temp = []
            # ss_temp = True
            # for i in ss_bullets:
            #     ss_bullet(i[0],i[1])
            #     if i[0] in range(500, 520):
            #         if i[1] in range(500, 540):
            #             ss_score +=1
            #             ss_temp = False
            #     if i[0] < 700 and ss_temp:
            #             ss_bullets_temp.append([i[0]+10,i[1]])
            #     ss_temp = True

                # Bullets Despawn
            # del ss_temp

            # ss_bullets = ss_bullets_temp
            # del ss_bullets_temp

            # Bullet cooldowm
            sge_rect(game_display, 700, 790, 100, 10, white)
            sge_rect(game_display, 700, 790, ss_cooldown, 10, red)

            # Enemy
            # if not Enemy.family:
            #     enemy = Enemy()
            # enemy.display()

            # Bad
            # ss_bullets_temp = []
            # ss_temp = True
            # for i in ss_bad_bullets:
            #     ss_bullet(i[0], i[1], red)
            #     if i[0] in range(ss_pos[0], ss_pos[0]+20):
            #         if i[1] in range(ss_pos[1], ss_pos[1]+40):
            #             ss_score -= 10
            #             ss_temp = False
            #     if i[0] > 0 and ss_temp:
            #         ss_bullets_temp.append([i[0]-10,i[1]])
            #     ss_temp = True
            # ss_bad_bullets = ss_bullets_temp
            # del ss_temp
            # del ss_bullets_temp

            # Enemy Moves
            # if ss_bad_move_cooldown == 0:
            #     ss_temp_direction = ss_bad_ai(0, 0, ss_bad_pos[0], ss_bad_pos[1])
            #     ss_bad_move_cooldown +=30
            # if ss_score >= 100:
            #     if ss_temp_direction == 'n':
            #         ss_bad_pos = [ss_bad_pos[0], ss_bad_pos[1]-1]
            #     elif ss_temp_direction == 'e':
            #         ss_bad_pos = [ss_bad_pos[0]+1, ss_bad_pos[1]]
            #     elif ss_temp_direction == 's':
            #         ss_bad_pos = [ss_bad_pos[0], ss_bad_pos[1]+1]
            #     elif ss_temp_direction == 'w':
            #         ss_bad_pos = [ss_bad_pos[0]-1, ss_bad_pos[1]]

            # if ss_bad_cooldown == 0:
            #     ss_bad_bullets.append([randint(600,800),randint(0,600)])
            #     ss_bad_cooldown += 10
            #
            # if ss_bad_cooldown > 0:
            #     ss_bad_cooldown -= 1
            #
            # if ss_bad_move_cooldown > 0:
            #     ss_bad_move_cooldown -= 1

            sge_print(game_display, ss_score)
            ss_player(ss_pos[0], ss_pos[1])
            pygame.display.update()


try:
    ss()
except KeyboardInterrupt:
    pygame.display.quit()
    pygame.quit()
    quit()
