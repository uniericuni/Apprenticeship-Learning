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
        # pre-run
        sys.stdout.write('pre-running ...'+'\n')
        for i in range(0,100):
            mode = gamemgr.input()
            feature,state,legal_action = gamemgr.update()
        agent = CarAgent3(w=np.zeros([15,1]))
        learn = CarLearning( agent, gamemgr, maxIter=MAX_ITERATION, numEstimating=100, numRLTraining=300, numTraining=50)
        # learn.agent.loadPolicy('policy.mat')
        learn.computeExpertExpectation()
        learn.train()
        # learn.agent.savePolicy('policyMiddle2.mat')
        learn.savePolicy('policy.mat')

    # auto mode
    elif gamemode==3:
        # pre-run
        sys.stdout.write('pre-running ...'+'\n')
        for i in range(0,100):
            mode = gamemgr.input()
            feature,state,legal_action = gamemgr.update()
        agent = CarAgent3(w=np.zeros([15,1]))
        learn = CarLearning( agent, gamemgr, maxIter=MAX_ITERATION, numEstimating=10, numRLTraining=10)
        # learn.loadPolicy('policyNormal.mat', 47)
        # learn.loadPolicy('policyBumping.mat',45)
        # learn.loadPolicy('policyMiddle3.mat',45)
        # learn.loadPolicy('policyRight.mat',48)
        learn.loadPolicy('policyNastyRight.mat',45)
        learn.computeExpertExpectation()
        learn.test()

    # playing mode
    else:
        # main game loop
        count = 0
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
