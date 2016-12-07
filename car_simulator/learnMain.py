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

    gamemgr = game.gamemgr(mode=3)
    agent = CarAgent(w=np.zeros([15,1]))
    learn = CarLearning( agent, gamemgr, maxIter=MAX_ITERATION, numEstimating=100, numRLTraining=50, numTraining=100)
    state = np.zeros((5,11))
    state[0][0] = 1
    legal_action = np.array([0,1,2,3,4])
    learn.agent.registerInitialState((state, legal_action))

    # main game loop
    learn.agent.setMode(AgentMode.training)
    while True:
        learn.runGame()
        # action assignment
        # learn.agent.registerInitialState((state, legal_action))
        # for i in range(100):
        #     action = learn.agent.getAction((state,legal_action))
        # learn.agent.final((state,legal_action))


    # agent = CarAgent(w=np.zeros([15,1]))
    # learn = CarLearning(agent=agent,maxIter=100,numEstimating=10,numTraining=10)
    # learn.computeExpertExpectation()
    # learn.train()
    # learn.runGame()
