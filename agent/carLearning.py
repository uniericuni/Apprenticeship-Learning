from inverseLearning import *
import game
import scipy.io as sio

class CarLearning(InverseLearning):
    """docstring for CarLearning"""
    def __init__(self, agent, gamemgr, featureSize=15, maxIter=1000, error=0.001, numEstimating=1000, numTraining=-1, numRLTraining=50):
        # print featureSize, maxIter, error, numEstimating, numTraining
        InverseLearning.__init__(self, agent=agent, gamemgr=gamemgr, featureSize=featureSize, error=error, numEstimating=numEstimating, numTraining=numTraining, numRLTraining=numRLTraining)
        self.maxIter = maxIter
        
    def computeExpertExpectation(self):
        # m = np.array([[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        # self.muExpert = np.zeros((self.featureSize,1))
        # cm = np.zeros((self.featureSize,1))
        # counter = 0.0
        # for i in range(1,4):
        #     # -5 -4 -3 -2 -1 0 1 2 3 4
        #     for j in range(10):
        #         if j >= 3 and j <= 7:
        #             continue
        #         else:
        #             m = np.zeros(((self.featureSize,1)))
        #             m[i] = 1
        #             m[5+j] = 1
        #         print m.T
        #         counter += 1
        #         for k in range(self.maxIter):
        #             cm += ( self.gamma ** k ) * m
        # self.muExpert = cm / counter
        # print counter, self.muExpert.T


        # m = np.array([[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        # for i in range(self.maxIter):
        #     self.muExpert += ( self.gamma ** i ) * m.T
        # print self.muExpert.T


        f = sio.loadmat('../assets/car_records/20161211_NastyRightLane.mat')['features']
        print f.shape
        self.muExpert = np.zeros((self.featureSize,1))
        counter = 0
        for i in range(1,f.shape[0]-self.maxIter,self.maxIter//2):
            counter += 1
            for j in range(self.maxIter):
                self.muExpert += ( self.gamma ** j ) * f[i+j-1:i+j].T
            # print self.muExpert.T
        self.muExpert = self.muExpert / counter
        print self.muExpert.T

    def runGame(self):
        # agent init
        mode = self.gamemgr.input()
        feature,state,legal_action = self.gamemgr.update()
        self.agent.registerInitialState((state, legal_action))
        counter = 0
        # print state
        # print legal_action

        # main game loop
        while mode and ( self.agent.isInTesting() or counter<self.maxIter ):
            # print counter
            # action assignment
            action = self.agent.getAction((state,legal_action))
            # print action

            # main game loop
            mode = self.gamemgr.input(action)
            feature,state,legal_action = self.gamemgr.update()
            if self.agent.isInTesting():
                self.gamemgr.render()
            counter += 1

        # final
        self.agent.final((state,legal_action))
        # print self.agent.mu

if __name__ == "__main__":
    from carAgents import * 
    agent = CarAgent(np.ones((15,1)))
    learn = CarLearning(agent)
