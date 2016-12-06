from inverseLearning import *
import game

class CarLearning(InverseLearning):
    """docstring for CarLearning"""
    def __init__(self, agent, featureSize=15, maxIter=1000, error=0.001, numEstimating=1000, numTraining=50):
        InverseLearning.__init__(self, agent, featureSize, error, numEstimating, numTraining)
        self.maxIter = maxIter
        
    def computeExpertExpectation(self):
        m = np.array([0.0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        self.muExpert = m.copy()
        print self.gamma, self.maxIter
        for i in range(self.maxIter):
            self.muExpert += ( self.gamma ** i ) * m

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
            self.gamemgr.render()
            counter += 1

        # final
        print state
        self.agent.final((state,legal_action))
        # print self.agent.mu

if __name__ == "__main__":
    from carAgents import * 
    agent = CarAgent(np.ones((15,1)))
    learn = CarLearning(agent)
