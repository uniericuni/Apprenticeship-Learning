import pygame, sys
import game
import time
import scipy.io as sio
from config import *

MAX_ITERATION = 1000

if __name__ == '__main__':

    # import agent
    sys.path.append(AGENT_PATH)
    from carAgents import *
    from carLearning import *

    agent = CarAgent(w=np.zeros([15,1]))
    learn = CarLearning(agent)
    learn.runGame()

    # # game manager init
    # counter = 0
    # features = []
    # gamemgr = game.gamemgr(state=100)
    # status = gamemgr.input()
    # state,legal_action = gamemgr.update()

    # # agent init
    # agent = CarAgent(w=np.zeros([15,1]))
    # agent.registerInitialState((state,legal_action))

    # # main game loop
    # while gamemgr.state and counter<MAX_ITERATION:

    #     # action assignment
    #     action = agent.getAction((state,legal_action))

    #     # main game loop
    #     status = gamemgr.input(action)
    #     state,legal_action = gamemgr.update()
    #     gamemgr.render()

    #     # feature export
    #     if gamemgr.record:
    #         features.append(feature)
    #     elif len(features)>0:
    #         timestr = time.strftime('%y%m%d%H%M%S')
    #         sio.savemat('%s%s_record.mat'%(CAR_RECORD_PATH,timestr), {'features':features})
    #         features = []
    #     counter += 1
        
    # # final
    # agent.final((state,legal_action))

    # # feature export
    # if len(features)>0:
    #     timestr = time.strftime('%y%m%d%H%M%S')
    #     sio.savemat('%s%s_record.mat'%(CAR_RECORD_PATH,timestr), {'features':features})
