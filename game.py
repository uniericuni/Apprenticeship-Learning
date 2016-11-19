import pygame
import car
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

        # object queue initialization
        self.objects = []
        self.objects.append(car('car.png'))

        # event message
        self.events = {}

    def input(self):

        # game clock delta
        self.clock.tick(30)

        # event messagge
        for event in pygame pygame.event.get():
            down = event.type==KEYDOWN
            if not hasattr(event, 'key'): continue
            if event.key == K_UP: self.events['horizontal_acc'] = (0,1)
            elif event.key == K_DOWN: self.events['horizontal_acc'] = (0,-1)
            if event.key == K_RIGHT: self.events['vertical_acc'] = (1,0)
            elif event.key == K_LEFT: self.events['vertical_acc'] = (-1,0)
            if event.key == K_ESCAPE: return 0
        return 1

    def update(self):

        # event handler
        for key in self.events:
            if key=='horizontal_acc' or key=='vertical_acc':
                msg = self.events[key]
                self.objects[0].accelerate(msg)

        # object status updage
        for obj in self.objects:
            obj.update()

    def render(self):

        # figures filled
        self.screen.fill(colors.BLACK)
        for obj in self.objects:
            rect = obj.get_rect()
            rect.center = obj.position
            screen.blit(obj.figure, rect)

        # double buffer update
        pygame.display.flip()
