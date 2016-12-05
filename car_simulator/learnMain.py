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
    learn = CarLearning(agent,maxIter=100,numEstimating=10,numTraining=10)
    learn.computeExpertExpectation()
    learn.train()
    # learn.runGame()