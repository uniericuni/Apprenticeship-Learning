import pygame
import numpy as np

ROADWIDTH = 50
MID = 500

BOUND_YMAX = 768
BOUND_YMIN = 0

class background:

    def __init__(self, fname, frname, lanenum=3, posx=0, posy=-768):
        self.figure = pygame.image.load(fname)
        self.surface = self.figure
        self.roadfigure = pygame.image.load(frname)
        self.surface = pygame.transform.scale(self.surface, (1024,768*2))
        self.rect = self.surface.get_rect()

        self.lanenum = lanenum
        self.updatespawnpoint(lanenum)

        self.position = np.array([posx,posy])
        self.roadpositions = [np.array([pos[0], self.position[1]]) for pos in self.spawnpoint]

    def update(self):
        self.position += np.array([0,2])
        if self.position[1] == 0: self.reload()
        self.roadpositions = [np.array([pos[0], self.position[1]]) for pos in self.spawnpoint]
        self.rect = self.surface.get_rect()
        self.rect.left,self.rect.top = tuple(self.position)
        self.roadrects = []
        for i,surf in enumerate(self.roadsurfaces):
            rect = surf.get_rect()
            rect.center = tuple(self.spawnpoint[i])
            rect.top = self.position[1]
            self.roadrects.append(rect)

    def reload(self):
        self.position = np.array([0,-768])

    def updatespawnpoint(self, lanenum):
        self.roadsurfaces = [pygame.transform.scale(self.roadfigure, (ROADWIDTH,768*2))]*lanenum
        bias = MID - ROADWIDTH * lanenum/4
        self.spawnpoint = [ np.array([ bias+n*ROADWIDTH ,-30]) for n in range(0,lanenum) ]
        self.minbound = np.array([MID-ROADWIDTH*(1+lanenum/2), BOUND_YMIN])
        self.maxbound = np.array([MID+ROADWIDTH*(1+lanenum/2), BOUND_YMAX])
