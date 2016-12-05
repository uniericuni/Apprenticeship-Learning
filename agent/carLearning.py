from inverseLearning import *
import game

class CarLearning(InverseLearning):
    """docstring for CarLearning"""
    def __init__(self, agent, featureSize=15, maxIter=1000, error=0.001, numEstimating=1000, numTraining=50):
        InverseLearning.__init__(self, agent, featureSize, error, numEstimating, numTraining)
        self.maxIter = maxIter
        
    def computeExpertExpectation(self):
        pass

    def runGame(self):
        # game manager init
        counter = 0
        gamemgr = game.gamemgr(state=100)
        status = gamemgr.input()
        state,legal_action = gamemgr.update()

        # agent init
        self.agent.registerInitialState((state,legal_action))

        # main game loop
        while gamemgr.state and counter<self.maxIter:

            # action assignment
            action = self.agent.getAction((state,legal_action))

            # main game loop
            status = gamemgr.input(action)
            state,legal_action = gamemgr.update()
            # gamemgr.render()
            counter += 1

        # final
        self.agent.final((state,legal_action))
        print self.agent.mu


if __name__ == "__main__":
    from carAgents import * 
    agent = CarAgent(np.ones((15,1)))
    learn = CarLearning(agent)
