import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
import os
import time

class cube(object):
    rows = 20
    width = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(66, 244, 235)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        distance = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * distance + 1, j * distance + 1, distance - 2, distance - 2))
        if eyes:
            center = distance // 2
            radius = 3
            circleMiddle = (i * distance + center - radius, j * distance + 8)
            circleMiddle2 = (i * distance + distance - radius * 2, j * distance + 8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_ESCAPE]:
                    pygame.quit()

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= rows - 1: c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= rows - 1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows - 1)
                else: c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (128, 128, 128), (x, 0), (x, w))
        pygame.draw.line(surface, (128, 128, 128), (0, y), (w, y))

def redrawWindow(window):
    global rows, width, s, snack
    window.fill((255,255,255))
    s.draw(window)
    snack.draw(window)
    drawGrid(width, rows, window)
    pygame.display.update()

def randomSnack(rows, item):
    position = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x, y), position))) > 0:
            continue
        else:
            break
    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack
    lose = "./lose.wav&"
    eatSnack = "./eatsnack.wav&"
    width = 500
    rows = 20
    s = snake((66, 244, 235), (10,10))
    snack = cube(randomSnack(rows, s), color = (0, 255, 0))
    flag = True
    clock = pygame.time.Clock()
    while flag:
        wn = pygame.display.set_mode((500, 500))
        pygame.display.set_caption('Snake')
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            os.system("afplay " + eatSnack)
            s.addCube()
            snack = cube(randomSnack(rows, s), color = (0, 255, 0))
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x + 1 :])):
                os.system("afplay " + lose)
                s.reset((10, 10))
                time.sleep(3)
                break
        redrawWindow(wn)
    pass

main()
