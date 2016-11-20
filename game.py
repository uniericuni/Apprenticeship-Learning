import pygame
import random
from pygame.locals import *
from config import *
from car import *
from background import *

OPPONENTCARSPAWN = pygame.USEREVENT+1

# game manager object
class gamemgr:

    def __init__(self):
        
        # random seed
        random.seed() 

        # game screen initialization
        pygame.init()
        self.screen = pygame.display.set_mode((1024,768), DOUBLEBUF)

        # game clock initialization
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(OPPONENTCARSPAWN, 30*50)

        # object queue initialization
        self.objects = []
        main_car = car(fname=IMAGE_PATH+'car.png', sc=0.1)
        self.objects.append(main_car)
        self.background = background(fname=IMAGE_PATH+'bg.png')

        # event message
        self.events = []

    def input(self):

        # game clock
        self.clock.tick(30)

        # events handling
        for event in pygame.event.get():
            
            # timer event 
            if event.type==OPPONENTCARSPAWN:
                self.events.append(OPPONENTCARSPAWN)

            # input event
            elif event.type==KEYDOWN:
                if not hasattr(event, 'key'): continue
                if event.key == K_ESCAPE: return 0
                self.events.append(event.key)
            elif event.type==KEYUP:
                if not hasattr(event, 'key'): continue
                if event.key in self.events: self.events.remove(event.key)

        # return status
        return 1

    def update(self):

        # update message handling
        yacc = 0
        xacc = 0
        for key in self.events:
            if key==OPPONENTCARSPAWN:
                pos = self.background.spawnpoint[random.randint(0,5)]
                op_car = car(fname=IMAGE_PATH+'opponent_car.png', posx=pos[0], posy=pos[1], spdy=random.uniform(12,24) ,sc=0.1, rt=180, isdrag=False)
                self.objects.append(op_car)
            if key==K_DOWN: yacc = 1 
            if key==K_UP: yacc = -1
            if key==K_RIGHT: xacc = 1
            if key==K_LEFT: xacc = -1
        if OPPONENTCARSPAWN in self.events: self.events.remove(OPPONENTCARSPAWN)
        self.objects[0].accelerate([xacc,yacc])

        # object status update:
        self.background.update()
        removeid = []
        for i,obj in enumerate(self.objects):
            obj.update()
            x,y = obj.position
            if i==0:
                if x < self.background.minbound[0]: x = self.background.minbound[0]
                if y < self.background.minbound[1]: y = self.background.minbound[1]
                if x > self.background.maxbound[0]: x = self.background.maxbound[0]
                if y > self.background.maxbound[1]: y = self.background.maxbound[1]
                obj.position = np.array([x,y])
            if i!=0 and y > self.background.maxbound[1]+20: removeid.append(i)

        # remove redundant objects:
        for id in removeid: self.objects.pop(id)

    def render(self):

        # background
        self.screen.fill(BLACK)
        rect = self.background.surface.get_rect()
        rect.left,rect.top = tuple(self.background.position)
        self.screen.blit(self.background.surface, rect)

        # objects
        for i,obj in enumerate(self.objects):
            rect = obj.surface.get_rect()
            rect.center = tuple(obj.position)
            self.screen.blit(obj.surface, rect)

        # double buffer update
        pygame.display.flip()
