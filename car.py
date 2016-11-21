import pygame
import numpy as np

SPEED = 0.4
ACCELERATION = 3.0
DRAG = 1.2
SPEED_MAX = 24

class car:
    
    def __init__(self, fname, posx=512, posy=384, spdx=0, spdy=0, accx=0, accy=0, sc=1, rt=0, isdrag=True):
        self.figure = pygame.image.load(fname)
        self.surface = self.figure
        self.rect = self.surface.get_rect()
        self.position = np.array([posx,posy])
        self.scale(sc)
        self.rotate(rt)
        self.speed = np.array([spdx,spdy])
        self.accelerate(np.array([accx,accy]))
        self.isdrag = isdrag
    
    def update(self):
        if self.isdrag: self.drag()
        self.move()
        self.rect = self.surface.get_rect()
        self.rect.center = tuple(self.position)
   
    def move(self):
        self.position = self.position + self.speed * SPEED

    def drag(self):
        spnorm = np.linalg.norm(self.speed)
        if spnorm > 0:
            dragspeed = self.speed - self.speed * (DRAG/spnorm)
            over = dragspeed*self.speed > 0
            self.speed = dragspeed*over
    
    def speedup(self, spd):
        self.speed = spd
        spnorm = np.linalg.norm(self.speed)
        if spnorm > SPEED_MAX:
            self.speed *= SPEED_MAX/spnorm

    def accelerate(self, acc):
        # accelerate
        self.speedup(self.speed + np.array(acc)*ACCELERATION)

    def scale(self, sc):
        w = int(self.surface.get_width() * sc)
        h = int(self.surface.get_height() * sc)
        self.surface = pygame.transform.scale(self.surface, (w,h))

    def rotate(self, rt):
        self.surface = pygame.transform.rotate(self.surface, rt)
