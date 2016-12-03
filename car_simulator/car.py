import pygame
import math
import numpy as np

SPEED = 0.4                     # speed multiplier
ACCELERATION = 3.0              # acceleration multiplier
DRAG = 1.0                      # drag multiplier
SPEED_MAX = 14                  # max speed
TARGETBUFF = 1                  # target tolerance, in avoidance of oscillation

class car:
#####################################################################################################
# methods:      __init__(self, fanme, posx, posy, spdx, spdy, accx, accy, sc, rt): init acr object  #
#               load(self, fname): load figure fname to the object                                  #
#               update(self): update attributes of car object                                       #
#               settarget(self, pos): set target to move foward                                     #
#               targetmove(self): change position foward target                                     #
#               move(self): change position by speed                                                # 
#               speedup(self, spd): change speed by spd                                             #
#               accelerate(self, acc): change speed by acc                                          #
#               drag(self): gradually decrease speed until zero                                     #
#               rotate(self, rt): rotate surface by rt                                              #
#               scale(self, sc): scale surface by sc                                                #
#                                                                                                   #
# attributes:   sc(float)                                                                           #
#               rt(float)                                                                           #
#               position(numpy.array(2,))                                                           #
#               speed(numpy.array(2,))                                                              #
#               accelerate(numpy.array(2,))                                                         #
#               target(numpy.array(2,))                                                             #
#               figure(pygame.surface)                                                              #
#               surface(pygame.surface)                                                             #
#               rect(pygame.rect)                                                                   #
#               position(numpy.array)                                                               #
#               isdrag(bool)                                                                        #
#               istargeting(bool)                                                                   #
#                                                                                                   # 
#####################################################################################################
    
    def __init__(self, fname, posx=512, posy=384, spdx=0, spdy=0, accx=0, accy=0, sc=1, rt=0, isdrag=True):
        self.sc = sc
        self.rt = rt
        self.position = np.array([posx,posy])
        self.load(fname)
        self.speed = np.array([spdx,spdy])
        self.accelerate(np.array([accx,accy]))
        self.isdrag = isdrag
        self.istargeting = False

    def load(self, fname):
        self.figure = pygame.image.load(fname)
        self.surface = self.figure
        self.scale(self.sc)
        self.rotate(self.rt)
        self.rect = self.surface.get_rect()
        self.rect.center = tuple(self.position)
    
    def update(self):
        if self.isdrag: self.drag()
        if self.istargeting: self.targetmove()
        self.move()
        self.rect = self.surface.get_rect()
        self.rect.center = tuple(self.position)

    def settarget(self, pos):
        self.istargeting = True
        self.target = pos

    def targetmove(self):
        if np.all(np.abs(self.position-self.target)<TARGETBUFF):
            self.istargeting = False
            self.speedup(np.array([0,0]))
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
