import pygame
import random
from pygame.locals import *
from config import *
from car import *
from background import *
from font import *

OPPONENTCARSPAWN = pygame.USEREVENT+1
RECORDSIGN = pygame.USEREVENT+2
TIMEDELTA = 30
RECORDSIGNINTERVAL = 5

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
        pygame.time.set_timer(OPPONENTCARSPAWN, TIMEDELTA*100)
        pygame.time.set_timer(RECORDSIGN, TIMEDELTA*25)

        # object queue initialization
        self.objects = []
        self.collideds = []
        main_car = car(fname=IMAGE_PATH+'car.png', sc=0.1)
        self.objects.append(main_car)

        # background and text interface init
        self.background = background(fname=IMAGE_PATH+'bg.png', frname=IMAGE_PATH+'road.png')
        self.status = font(FONT,FONTSIZE, (20,200))
        self.instruction = font(FONT,FONTSIZE, (20,40))
        self.instruction.update( "GAME INSTRUCTION"                             )
        self.instruction.update( "--------------------------"                   )
        self.instruction.update( "SPACE: CHANGE GMAE MODE"                      )
        self.instruction.update( "ARROW KEY: MOVE"                              )
        self.instruction.update( "NUMBER: CHANGE LANE NUMBER"                   )
        self.instruction.update( "A-H: CHANGE LANE"                             )
        self.instruction.update( "R: RECORD"                                    )

        # event message
        self.events = []

        # state init
        self.state = 1
        self.record = False
        self.recordsign = RECORDSIGNINTERVAL

    def input(self):

        # game clock
        self.clock.tick(TIMEDELTA)

        # events handling
        for event in pygame.event.get(): 
            # timer event 
            if event.type==OPPONENTCARSPAWN:
                self.events.append(OPPONENTCARSPAWN)
            if event.type==RECORDSIGN:
                self.events.append(RECORDSIGN)

            # input event
            elif event.type==KEYDOWN:
                if not hasattr(event, 'key'): continue
                elif event.key==K_ESCAPE: self.state = 0
                elif event.key==K_SPACE:
                    if self.state==1: self.state = 2
                    elif self.state==2: self.state = 3
                    elif self.state==3: self.state = 1
                elif event.key==K_r: self.record = not self.record
                else: 
                    self.events.append(event.key)
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
        lanenum = 0
        self.recordsign -= 1
        for key in self.events:
            if key==OPPONENTCARSPAWN:
                l = random.randint(1,self.background.lanenum-2)
                pos = self.background.spawnpoint[l]
                op_car = car(fname=IMAGE_PATH+'opponent_car.png', posx=pos[0], posy=pos[1], spdy=random.uniform(4,12) ,sc=0.1, isdrag=False)
                self.objects.append(op_car)
            if key==RECORDSIGN:
                self.recordsign = RECORDSIGNINTERVAL
            #if key==pygame.K_DOWN: yacc = 1 
            #if key==pygame.K_UP: yacc = -1
            if key==pygame.K_RIGHT: xacc = 1
            if key==pygame.K_LEFT: xacc = -1
            if key==pygame.K_1: lanenum = 1
            if key==pygame.K_2: lanenum = 2
            if key==pygame.K_3: lanenum = 3
            if key==pygame.K_4: lanenum = 4
            if key==pygame.K_5: lanenum = 5
            if key==pygame.K_a: lane = 1
            if key==pygame.K_s: lane = 2
            if key==pygame.K_d: lane = 3
            if key==pygame.K_f: lane = 4
            if key==pygame.K_g: lane = 5
            if key==pygame.K_h: lane = 6
            if key==pygame.K_j: lane = 7

        # update timer
        if OPPONENTCARSPAWN in self.events: self.events.remove(OPPONENTCARSPAWN)
        if RECORDSIGN in self.events: self.events.remove(RECORDSIGN)

        # update main character status: state 1
        if self.state==1:
            self.objects[0].accelerate([xacc,yacc])

        # update main character status: state 2
        if self.state==2 and lane!=0 and lane<=self.background.lanenum:
            pos = np.array(self.background.spawnpoint[lane-1])
            pos[1] = self.objects[0].position[1]
            self.objects[0].settarget(pos)

        # update main background status: state 2
        if lanenum!=0:
            self.background.updatespawnpoint(lanenum)

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
        spd = main.speed
        onLane = 0
        dist = float('inf')
        for i,sp in enumerate(self.background.spawnpoint):
            if abs(sp[0]-main.position[0])<dist:
                dist = abs(sp[0]-main.position[0])
                onLane = i
        dist = float('inf')
        for obj in self.objects[1:]:
            if int(obj.position[0])==int(self.background.spawnpoint[onLane][0]):
                if abs(dist) > abs(main.position[1]-obj.position[1]):
                    dist = main.position[1]-obj.position[1]
        if dist>=350: qdist = 4
        elif dist<-449: qdist = -5
        else: qdist = int((dist+450)/100)-5
            
        self.status.update( "game mode: %d"%self.state )
        self.status.update( "position: %d,%d"%( pos[0], pos[1] ))
        self.status.update( "speed: %d,%d"%( spd[0], spd[1] ))
        self.status.update( "lane: %d"%onLane )
        self.status.update( "nearest distance: %.3f"%dist )
        self.status.update( "quantized distance: %d"%qdist )
        self.background.update()

        # remove redundant objects
        for id in removeid: self.objects.pop(id)
        
        # collision cars
        for collider in self.collideds:
            collider.load( IMAGE_PATH+'hit_car.png' )

        # feature parser
        if self.record:
            f = [0]*15
            f[onLane] = 1
            f[qdist+10] = 1
            return f
        else:
            return None
        

    def render(self):

        # background
        self.screen.fill(BLACK)
        self.screen.blit(self.background.surface, self.background.rect)
        for i,rect in enumerate(self.background.roadrects):
            self.screen.blit(self.background.roadsurfaces[i], rect)

        # objects
        for i,obj in enumerate(self.objects):
            self.screen.blit(obj.surface, obj.rect)

        # font interface
        for text in self.instruction.texts:
            self.screen.blit(text[0], text[1])
        for text in self.status.texts:
            self.screen.blit(text[0], text[1])
        self.status.clear()

        # record sign
        if self.record and self.recordsign>0:
            pygame.draw.circle(self.screen, RED, (900,40), 10)

        # double buffer update
        pygame.display.flip()