import pygame
import math
import numpy as np

SPEED = 0.4
ACCELERATION = 3.0
DRAG = 1.2
SPEED_MAX = 24
SPEED_BIAS = np.array([2,0])
TARGETBUFF = 1

class car:
    
    def __init__(self, fname, posx=512, posy=384, spdx=0, spdy=0, accx=0, accy=0, sc=1, rt=0, isdrag=True):
        self.sc = sc
        self.rt = rt
        self.position = np.array([posx,posy])
        self.load(fname)
        self.speed = np.array([spdx,spdy])
        self.accelerate(np.array([accx,accy]))
        self.isdrag = isdrag
        self.targetflag = False

    def load(self, fname):
        self.figure = pygame.image.load(fname)
        self.surface = self.figure
        self.scale(self.sc)
        self.rotate(self.rt)
        self.rect = self.surface.get_rect()
        self.rect.center = tuple(self.position)
    
    def update(self):
        if self.isdrag: self.drag()
        if self.targetflag: self.targetmove()
        self.move()
        self.rect = self.surface.get_rect()
        self.rect.center = tuple(self.position)

    def settarget(self, pos):
        self.targetflag = True
        self.target = pos

    def targetmove(self):
        if np.all(np.abs(self.position-self.target)<TARGETBUFF):
            self.targetflag = False
            self.speedup(0) # immediate halt to avoid overshooting
        else:
            acc = self.target-self.position
            self.accelerate(acc/np.linalg.norm(acc))
   
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
        self.speedup(self.speed + np.array(acc)*ACCELERATION)

    def scale(self, sc):
        w = int(self.surface.get_width() * sc)
        h = int(self.surface.get_height() * sc)
        self.surface = pygame.transform.scale(self.surface, (w,h))
        self.rect = self.surface.get_rect()

    def rotate(self, rt):
        self.surface = pygame.transform.rotate(self.surface, rt)
        self.rect = self.surface.get_rect()
