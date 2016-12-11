from inverseLearning import *
import scipy.io as sio

class EasyLearning(InverseLearning):
    """docstring for CarLearning"""
    def __init__(self, agent, gamemgr, featureSize=3, maxIter=100, error=0.001, numEstimating=500, numTraining=500, numRLTraining=500):
        # print featureSize, maxIter, error, numEstimating, numTraining
        InverseLearning.__init__(self, agent=agent, gamemgr=gamemgr, featureSize=featureSize, error=error, numEstimating=numEstimating, numTraining=numTraining, numRLTraining=numRLTraining)
        self.maxIter = maxIter
        
    def computeExpertExpectation(self):
        m = np.array([[0.0, 1.0, 0.0]])
        self.muExpert = np.zeros((self.featureSize,1))
        for i in range(self.maxIter):
            self.muExpert += ( self.gamma ** i ) * m.T
        print self.muExpert.T

    def runGame(self):
        state = 1;
        self.agent.registerInitialState(state)
        counter = 0
        while ( self.agent.isInTesting() or counter<self.maxIter ):
            action = self.agent.getAction(state)
            if state + action > 2 or state + action < 0:
                print state, action, 'wrong action'
            state = state + action
            counter += 1
        self.agent.final(state)

if __name__ == '__main__':
    from easyAgents import *
    agent = EasyAgent(np.ones((3,1)))
    learn = EasyLearning(agent, 1)
    learn.computeExpertExpectation()
    # learn.train()
    # print learn.muExpert
    reward = np.array([[100],[0.3],[-200]])
    learn.agent.setRewardVector(reward)
    learn.updateAgent()
    learn.featureExpectation()
