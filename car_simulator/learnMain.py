import pygame, sys
import game
import time
import scipy.io as sio
from config import *

MAX_ITERATION = 100

if __name__ == '__main__':

    # import agent
    sys.path.append(AGENT_PATH)
    from carAgents import *
    from carLearning import *

    gamemgr = game.gamemgr(mode=100)
    mode = gamemgr.input()
    feature,state,legal_action = gamemgr.update()
    sys.stdout.write('pre-running ...'+'\n')
    for i in range(0,100):
        mode = gamemgr.input()
        feature,state,legal_action = gamemgr.update()

    agent = CarAgent(w=np.zeros([15,1]))
    learn = CarLearning( agent, gamemgr, maxIter=MAX_ITERATION, numEstimating=100, numRLTraining=100, numTraining=50)
    r = np.zeros((15,1));
    r[0] = -5.0
    r[2] = 0.5
    r[4] = -5.0
    r[11] = -5.0
    r[10] = -10.0
    r[9] = -5.0
    r[14] = 0.5
    # r[10] = 10.0
    # r[0] = -5
    # r[4] = -5 
    # r = r - np.min(r)
    r = r / np.sum(np.abs(r))
    learn.agent.setRewardVector(r)
    learn.updateAgent()
    print agent.w.T
    print agent.weights.T

    gamemgr = game.gamemgr(mode=3)
    mode = gamemgr.input()
    feature,state,legal_action = gamemgr.update()
    sys.stdout.write('pre-running ...'+'\n')
    for i in range(0,100):
        mode = gamemgr.input()
        feature,state,legal_action = gamemgr.update()
    learn = CarLearning( agent, gamemgr, maxIter=MAX_ITERATION, numEstimating=100, numRLTraining=50, numTraining=50)
    learn.test()