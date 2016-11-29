import pygame
import numpy as np

ROADWIDTH = 100
ROADMARGIN = 10
ROAD1X = 512

ROAD2X = ROAD1X + ROADWIDTH + 2*ROADMARGIN
ROAD3X = ROAD1X - ROADWIDTH - 2*ROADMARGIN
BOUND_XMAX = ROAD1X + 2*ROADWIDTH + 5*ROADMARGIN
BOUND_XMIN = ROAD1X - 2*ROADWIDTH - 5*ROADMARGIN
BOUND_YMAX = 768
BOUND_YMIN = 0

class background:

    def __init__(self, fname, posx=0, posy=-768):
        self.figure = pygame.image.load(fname)
        self.surface = self.figure
        self.surface = pygame.transform.scale(self.surface, (1024,768*2))
        self.rect = self.surface.get_rect()
        self.position = np.array([posx,posy])

        self.minbound = np.array([BOUND_XMIN, BOUND_YMIN])
        self.maxbound = np.array([BOUND_XMAX, BOUND_YMAX])

        self.spawnpoint = [ np.array([ROAD1X+ROADWIDTH/4,-30]),
                            np.array([ROAD1X-ROADWIDTH/4,-30]),
                            np.array([ROAD2X+ROADWIDTH/4,-30]),
                            np.array([ROAD2X-ROADWIDTH/4,-30]),
                            np.array([ROAD3X+ROADWIDTH/4,-30]),
                            np.array([ROAD3X-ROADWIDTH/4,-30]) ]

    def update(self):
        self.position += np.array([0,2])
        if self.position[1] == 0: self.reload()
        self.rect = self.surface.get_rect()
        self.rect.left,self.rect.top = tuple(self.position)

    def reload(self):
        self.position = np.array([0,-768])
