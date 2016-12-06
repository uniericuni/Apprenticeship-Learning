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
        # m = np.array([[0.0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
        # self.muExpert = np.zeros((self.featureSize,1))
        # for i in range(self.maxIter):
        #     self.muExpert += ( self.gamma ** i ) * m.T
        # print self.muExpert.T

        f = sio.loadmat('../assets/car_records/161206125021_record.mat')['features']
        self.muExpert = np.zeros((self.featureSize,1))
        counter = 0
        for i in range(1,f.shape[0]-self.maxIter,self.maxIter/2):
            counter += 1
            for j in range(self.maxIter):
                self.muExpert += ( self.gamma ** j ) * f[i+j-1:i+j].T
            # print self.muExpert.T
        self.muExpert = self.muExpert / counter
        # print self.muExpert.T


    def runGame(self):
        # agent init
        mode = self.gamemgr.input()
        feature,state,legal_action = self.gamemgr.update()
        self.agent.registerInitialState((state, legal_action))
        counter = 0

        # main game loop
        while mode and counter<self.maxIter:

            # action assignment
            action = self.agent.getAction((state,legal_action))

            # main game loop
            mode = self.gamemgr.input(action)
            feature,state,legal_action = self.gamemgr.update()
            counter += 1

        # final
        self.agent.final((state,legal_action))
        # print self.agent.mu

if __name__ == "__main__":
    from carAgents import * 
    agent = CarAgent(np.ones((15,1)))
    learn = CarLearning(agent)
