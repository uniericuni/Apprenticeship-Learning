from inverseLearning import *
from gridWorldLearning import *
import sys
import numpy as np




if __name__ == "__main__":
    from gridWorldAgent import *
    sys.path.append('../gridworld/')
    from GridWorld import *
    
    DaPingTai = DaPingTai(5, 0.3, 1)
    goalstate = DaPingTai.getPostiveRewardState()
    w = np.zeros((25, 1))
    # w = np.array([0, 0, -1, 1, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0]).reshape(16, 1)
    #w[goalstate] = 1
    agent = gridWorldAgent(w, DaPingTai)

    learn = gridWorldLearning(agent, DaPingTai)

    learn.computeExpertExpectation()
    # learn.updateAgent()
    
    learn.train()
    
    learn.test()

    learn.test()
    learn.test()
    learn.test()