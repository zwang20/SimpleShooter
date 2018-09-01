import pygame

print('Simple Game Engine by Michael')


def sge_print(display, string='Test', x=0, y=0, colour=(0, 0, 0)):
    display.blit(pygame.font.SysFont("arial",
        25).render(str(string), True, colour), (x, y))

def sge_rect(display, x, y, width, height, colour=(0, 0, 0)):
    if x <= 0:
        x = 1
    if y <= 0:
        y = 1
    if width <= 0:
        width = 1
    if height <= 0:
        height = 1
    pygame.draw.rect(display, colour, (x, y, width, height))


def sge_clear(display, colour=(255, 255, 255)):
    display.fill(colour)


def sge_line(
display, colour=(0,0,0), point_1=(0, 0), point_2=(10, 10), width=(10)
):
    pygame.draw.line(display, colour, point_1, point_2, width)


def sge_load():
    try:
        x = open('settings.dat', 'r')
        y = x.read()
        x.close()
        z = y.split('\n')
        e = []
        for t in z:
            if t:
                e.append(t.split(' = '))
        print(e)
        return dict(e)
    except FileNotFoundError:
        x = open('settings.dat', 'w')
        x.close()
        return None

def sge_write():
    pass
