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

    def __init__(self, mode=1):
        
        # random seed
        random.seed() 

        # mode init
        self.mode = mode
        self.record = False
        self.recordsign = RECORDSIGNINTERVAL

        # game screen initialization
        pygame.init()
        if self.mode!=100:
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

    def input(self, action=None):

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
                elif event.key==K_ESCAPE: self.mode = 0
                elif event.key==K_SPACE:
                    if self.mode==1: self.mode = 2
                    elif self.mode==2: self.mode = 3
                    elif self.mode==3: self.mode = 1
                elif event.key==K_r: self.record = not self.record
                else: 
                    self.events.append(event.key)
            elif event.type==KEYUP:
                if not hasattr(event, 'key'): continue
                if event.key in self.events: self.events.remove(event.key)

        # training mode
        if self.mode==100:
            if action==1: self.events.append(pygame.K_a)
            elif action==2: self.events.append(pygame.K_s)
            elif action==3: self.events.append(pygame.K_d)
            elif action==4: self.events.append(pygame.K_f)
            elif action==5: self.events.append(pygame.K_g)

        # return game state
        return self.mode

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
                op_car = car(fname=IMAGE_PATH+'opponent_car.png', posx=pos[0], posy=pos[1], spdy=random.uniform(4,12) ,sc=0.1, isdrag=False, lane=l)
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
        if self.mode==1:
            self.objects[0].accelerate([xacc,yacc])

        # update main character status: state 2
        if lane!=0 and lane<=self.background.lanenum:
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
        dist = np.array([float('inf')]*5)
        for obj in self.objects[1:]:
            l = obj.lane
            if abs(dist[l]) > abs(main.position[1]-obj.position[1]):
                    dist[l] = main.position[1]-obj.position[1]
        qdist = (dist+450)/100-5
        qdist[np.where(dist>=350)]=4
        qdist[np.where(dist<-449)]=-5
        qdist = qdist.astype('int')
            
        self.status.update( "game mode: %d"%self.mode )
        self.status.update( "position: %d,%d"%( pos[0], pos[1] ))
        self.status.update( "speed: %d,%d"%( spd[0], spd[1] ))
        self.status.update( "lane: %d"%onLane )
        for i in range(0,5):
            self.status.update( "nearest distance: %.3f"%dist[i] )
        for i in range(0,5):
            self.status.update( "quantized distance: %d"%qdist[i] )
        self.background.update()

        # remove redundant objects
        for id in removeid: self.objects.pop(id)
        
        # collision cars
        for collider in self.collideds:
            collider.load( IMAGE_PATH+'hit_car.png' )

        # feature parser
        feature = None
        legal_action = np.array([0,1,2,3,4])
        state = np.zeros([5,11]).astype('int')
        state[onLane,0] = 1
        for i in range(0,5):
            state[i,qdist[i]+6] = 1
        if self.record:
            feature = [0]*15
            feature[onLane] = 1
            feature[qdist[onLane]+10] = 1

        return feature,state,legal_action

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
