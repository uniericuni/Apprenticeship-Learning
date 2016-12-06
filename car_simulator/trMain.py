import pygame, sys, time
import scipy.io as sio
import game
from parser import parser
from config import *

# main
def main(argv):

    # command parser
    gamemode,MAX_ITERATION = parser(argv)

    # game manager init
    features = []
    gamemgr = game.gamemgr(mode=gamemode)
    mode = gamemgr.input()
    feature,state,legal_action = gamemgr.update()

    # training mode
    if gamemode==100:
        agent = CarAgent(w=np.zeros([15,1]))
        learn = CarLearning( agent, gamemgr, maxIter=MAX_ITERATION, numEstimating=10, numTraining=10)
        learn.computeExpertExpectation()
        learn.train()

    # playing mode
    else:
        # main game loop
        while gamemgr.mode:
            mode = gamemgr.input()
            feature,state,legal_action = gamemgr.update()
            gamemgr.render()

            # feature export
            if gamemgr.record:
                features.append(feature)
            elif len(features)>0:
                timestr = time.strftime('%y%m%d%H%M%S')
                sio.savemat('%s%s_record.mat'%(CAR_RECORD_PATH,timestr), {'features':features})
                features = []

    # feature export
    if len(features)>0:
        timestr = time.strftime('%y%m%d%H%M%S')
        sio.savemat('%s%s_record.mat'%(CAR_RECORD_PATH,timestr), {'features':features})

# main
if __name__ == '__main__':
    # import agent
    sys.path.append(AGENT_PATH)
    from carAgents import *
    from carLearning import *
    main(sys.argv[1:])
