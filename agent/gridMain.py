from inverseLearning import *
from gridWorldLearning import *
import sys
import numpy as np

if __name__ == "__main__":
    from gridWorldAgent import *
    sys.path.append('../gridworld/')
    from GridWorld import *

    DaPingTai = DaPingTai(4, 0.3, 1)
    goalstate = DaPingTai.getPostiveRewardState()
    w = np.zeros((16, 1))
    #w[goalstate] = 1
    agent = gridWorldAgent(w, DaPingTai)

    learn = gridWorldLearning(agent, DaPingTai)

    print(learn.gamemgr.convertToMatrix(learn.gamemgr.ground_r)), goalstate
    learn.computeExpertExpectation()
