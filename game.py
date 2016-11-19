import pygame
import colors
from pygame.locals import *

# game object
class game:

    def __init__(self):
        # game screen initialization
        pygame.init()
        self.screen = pygame.display.set_mode((1024,768), DOUBLEBUF)
        # game clock initialization
        self.clock = pygame.time.Clock()
        # game clock initialization
        self.car = pygame.image.load('test.png')
        self.speed = 1

    def input(self):
        # game clock delta
        self.clock.tick(30)
        # event handler
        for event in pygame pygame.event.get():
            if not hasattr(event, 'key'): continue
            if event.key == K_RIGHT: self.speed += 1
            elif event.key == K_LEFT: self.speed -= 1

    def update(self):
        self.position += speed

    def render(self):
        self.screen.fill(colors.BLACK)
        pygame.display.flip()
