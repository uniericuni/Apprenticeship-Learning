import pygame
import numpy as np
from config import *

LINEWIDTHMUL = 1.5

class font:

    def __init__(self, fontname, size, pos):
        self.font = pygame.font.SysFont(fontname, size)
        self.fontname = fontname
        self.size = size
        self.pos = pos
        self.texts = []

    def update(self, content):
        text = self.font.render(content, True, WHITE)
        posx = self.pos[0]
        posy = self.pos[1] + len(self.texts) * self.size * LINEWIDTHMUL
        self.texts.append( (text, (posx,posy)) )
    
    def clear(self):
        self.texts = []
