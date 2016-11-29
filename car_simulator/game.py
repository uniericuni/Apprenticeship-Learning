import pygame
import random
from pygame.locals import *
from config import *
from car import *
from background import *
from font import *

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
        self.collideds = []
        main_car = car(fname=IMAGE_PATH+'car.png', sc=0.1)
        self.objects.append(main_car)

        # background and text interface init
        self.background = background(fname=IMAGE_PATH+'bg.png')
        self.status = font(FONT,FONTSIZE, (40,200))
        self.instruction = font(FONT,FONTSIZE, (40,40))
        self.instruction.update( "GAME INSTRUCTION"             )
        self.instruction.update( "-------------------"          ) 
        self.instruction.update( "SPACE: CHANGE MODE"           )
        self.instruction.update( "RIGHT: MOVE RIGHT"            )
        self.instruction.update( "LEFT: MOVE LEFT"              )
        self.instruction.update( "NUMBER: CHANGE LANE"          )

        # event message
        self.events = []

        # state init
        self.state = 1

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
                elif event.key == K_ESCAPE: self.state = 0
                elif event.key==K_SPACE:
                    if self.state==1: self.state = 2
                    elif self.state==2: self.state = 1
                else: self.events.append(event.key)
            elif event.type==KEYUP:
                if not hasattr(event, 'key'): continue
                if event.key in self.events: self.events.remove(event.key)

        # return game state
        return self.state

    def update(self):

        # update message handling
        yacc = 0
        xacc = 0
        lane = 0
        for key in self.events:
            if key==OPPONENTCARSPAWN:
                pos = self.background.spawnpoint[random.randint(0,5)]
                op_car = car(fname=IMAGE_PATH+'opponent_car.png', posx=pos[0], posy=pos[1], spdy=random.uniform(12,24) ,sc=0.1, rt=180, isdrag=False)
                self.objects.append(op_car)
            if key==K_DOWN: yacc = 1 
            if key==K_UP: yacc = -1
            if key==K_RIGHT: xacc = 1
            if key==K_LEFT: xacc = -1
            if key==K_1: lane = 1
            if key==K_2: lane = 2
            if key==K_3: lane = 3
            if key==K_4: lane = 4
            if key==K_5: lane = 5
            if key==K_6: lane = 6
            if key==K_7: lane = 7
            if key==K_8: lane = 8
            if key==K_9: lane = 9

        # update opponent spawning
        if OPPONENTCARSPAWN in self.events: self.events.remove(OPPONENTCARSPAWN)

        # update main character status
        if self.state==1:
            self.objects[0].accelerate([xacc,yacc])
        if self.state==2 and lane!=0:
            pos = np.array(self.background.spawnpoint[lane-1])
            pos[1] = self.objects[0].position[1]
            self.objects[0].settarget(pos)

        # update other objects status
        while self.collideds:
            self.collideds[-1].load( IMAGE_PATH+'opponent_car.png' )
            self.collideds.pop()
        removeid = []
        main = self.objects[0]
        for i,obj in enumerate(self.objects):
            obj.update()
            x,y = obj.position
            rect = obj.surface.get_rect()
            if i==0:
                if x < self.background.minbound[0]: x = self.background.minbound[0]
                if y < self.background.minbound[1]: y = self.background.minbound[1]
                if x > self.background.maxbound[0]: x = self.background.maxbound[0]
                if y > self.background.maxbound[1]: y = self.background.maxbound[1]
                obj.position = np.array([x,y])
            if i!=0:
                if y > self.background.maxbound[1]+20: removeid.append(i)
                if main.rect.colliderect(obj.rect): self.collideds.append(obj)

        # update background and font interface
        pos = main.position
        self.status.update( "game state: %d"%self.state )
        self.status.update( "position: %d,%d"%( pos[0], pos[1] ))
        self.status.update( "lane: %d"%1 )
        self.status.update( "hit: %d"%len(self.collideds) )
        self.background.update()

        # remove redundant objects
        for id in removeid: self.objects.pop(id)
        
        # collision cars
        for collider in self.collideds:
            collider.load( IMAGE_PATH+'hit_car.png' )

    def render(self):

        # background
        self.screen.fill(BLACK)
        self.screen.blit(self.background.surface, self.background.rect)

        # objects
        for i,obj in enumerate(self.objects):
            self.screen.blit(obj.surface, obj.rect)

        # font interface
        for text in self.instruction.texts:
            self.screen.blit(text[0], text[1])
        for text in self.status.texts:
            self.screen.blit(text[0], text[1])
        self.status.clear()

        # double buffer update
        pygame.display.flip()
