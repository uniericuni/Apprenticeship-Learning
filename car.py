import pygame
import numpy as np
from config import *

STARTX = 512
STARTY = 384
SCALE = 0.1
SPEED = 0.4
ACCELERATION = 1.0
SPEED_MAX = 5
DRAG = 0.3

class car:
    
    def __init__(self, fname):
        self.figure = pygame.image.load( IMAGE_PATH + fname )
        self.surface = self.figure
        self.scale(SCALE)
        self.position = np.array([STARTX,STARTY])
        self.speed = np.array([0,0])
    
    def update(self):
        self.drag()
        self.move()
   
    def move(self):
        self.position = self.position + self.speed * SPEED

    def drag(self):
        spnorm = np.linalg.norm(self.speed)
        if spnorm > 0:
            dragspeed = self.speed - self.speed * (DRAG/spnorm)
            over = dragspeed*self.speed > 0
            self.speed = dragspeed*over

    def accelerate(self, acc):
        # accelerate
        self.speed = self.speed + np.array(acc) * ACCELERATION
        spnorm = np.linalg.norm(self.speed)
        if spnorm > SPEED_MAX:
            self.speed *= SPEED_MAX/spnorm

    def scale(self, sc):
        w = int(self.surface.get_width() * sc)
        h = int(self.surface.get_height() * sc)
        self.surface = pygame.transform.scale(self.surface, (w,h))

