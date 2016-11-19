import pygame
import config

SPEED = 1
ACCELERATION = 1
DRAG = 0.1

class car:
    
    def __init__(self, fname):
        self.figure = pygame.image.load(config.image_path+fname)
        self.position = (100,100)
        self.speed = (0,0)
        self.acceleration = (0,0)
    
    def update(self):
        self.speedup()
        self.move()
   
    def move(self):
        xpos = self.position[0] + self.speed[0] * SPEED
        ypos = self.position[1] + self.speed[1] * SPEED
        self.position = (xpos, ypos)

    def speedup(self):
        # accelerate
        xspeed = self.speed[0] + self.acceleration[0] * ACCELERATION
        yspeed = self.speed[1] + self.acceleration[1] * ACCELERATION
        self.speed = (xspeed, yspeed)
        # drag
        xspeed = self.speed[0] - DRAG
        yspeed = self.speed[1] - DRAG
        if xspeed*self.speed[0]<0: xspeed = 0
        if yspeed*self.speed[1]<0: yspeed = 0
        self.speed = (xspeed, yspeed)

    def accelerate(self, acc):
        # change acceleration
        self.acceleration = acc 
