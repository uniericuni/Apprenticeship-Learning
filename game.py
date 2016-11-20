import pygame
from pygame.locals import *
from car import *
from config import *

# game object
class game:

    def __init__(self):

        # game screen initialization
        pygame.init()
        self.screen = pygame.display.set_mode((1024,768), DOUBLEBUF)

        # game clock initialization
        self.clock = pygame.time.Clock()

        # object queue initialization
        self.objects = []
        self.objects.append(car('car.png'))
        self.bg = pygame.image.load( IMAGE_PATH + 'bg.png')

        # event message
        self.events = []

    def input(self):

        # game clock delta
        self.clock.tick(30)

        # input event message
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if not hasattr(event, 'key'): continue
                if event.key == K_ESCAPE: return 0
                self.events.append(event.key)
            elif event.type==KEYUP:
                if not hasattr(event, 'key'): continue
                if event.key in self.events: self.events.remove(event.key)

        # return status
        return 1

    def update(self):

        # event handler
        yacc = 0
        xacc = 0
        for key in self.events:
            if key==K_DOWN: yacc = 1 
            elif key==K_UP: yacc = -1
            if key==K_RIGHT: xacc = 1
            elif key==K_LEFT: xacc = -1
        self.objects[0].accelerate([xacc,yacc])

        # object status updage
        for obj in self.objects:
            obj.update()

    def render(self):

        # figures filled
        self.screen.fill(BLACK)
        self.screen.blit(self.bg, self.bg.get_rect())
        for obj in self.objects:
            rect = obj.surface.get_rect()
            rect.center = tuple(obj.position)
            self.screen.blit(obj.surface, rect)

        # double buffer update
        pygame.display.flip()
