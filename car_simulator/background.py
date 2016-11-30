import pygame
import numpy as np

BACKGROUND_SPEED = 6
ROADWIDTH = 50
MID = 512

BOUND_YMAX = 768
BOUND_YMIN = 0
WALL = 20

class background:

    def __init__(self, fname, frname, lanenum=3, posx=0, posy=-768):
        self.figure = pygame.image.load(fname)
        self.surface = self.figure
        self.roadfigure = pygame.image.load(frname)
        self.surface = pygame.transform.scale(self.surface, (1024,768*2))
        self.rect = self.surface.get_rect()
        self.position = np.array([posx,posy])
        self.updatespawnpoint(lanenum)

    def update(self):
        self.position += np.array([0,BACKGROUND_SPEED])
        if self.position[1] == 0: self.reload()
        self.rect = self.surface.get_rect()
        self.rect.left,self.rect.top = tuple(self.position)
        self.roadrects = []
        for i,surf in enumerate(self.roadsurfaces):
            rect = surf.get_rect()
            rect.center = tuple(self.spawnpoint[i+1])
            rect.top = self.position[1]
            self.roadrects.append(rect)

    def reload(self):
        self.position = np.array([0,-768])

    def updatespawnpoint(self, lanenum):
        self.roadsurfaces = [pygame.transform.scale(self.roadfigure, (ROADWIDTH,768*2))]*(lanenum)
        lanenum += 2 # out of ordinary road
        self.lanenum = lanenum
        bias = MID - ROADWIDTH * lanenum/2
        self.spawnpoint = [ np.array([ bias+n*ROADWIDTH ,-30]) for n in range(0,lanenum) ]
        self.minbound = np.array([self.spawnpoint[0][0]-WALL, BOUND_YMIN])
        self.maxbound = np.array([self.spawnpoint[lanenum-1][0]+WALL, BOUND_YMAX])
