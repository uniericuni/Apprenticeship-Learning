import numpy as np
from approximateAgents import *

class InverseLearning:
    """docstring for inverseLearning"""
    def __init__(self, agent, featureSize, error=0.001, numEstimating=100, numTraining=50):
        self.agent = agent
        self.gamma = agent.gamma
        self.numEstimating = numEstimating
        self.numTraining = numTraining
        self.error = error
        self.featureSize = featureSize
        self.w = np.zeros((self.featureSize,1))
        self.mus = []
        self.muBar = None

        
    def train(self):
        self.featureExpectation()
        t = self.updateRewardFunction()

        while t > self.error:
            self.updateAgent()
            self.featureExpectation()
            t = self.updateRewardFunction()
            print t

    # override this function
    def computeExpertExpectation(self):
        """
        compure self.muExpert
        """
        pass

    def featureExpectation(self):
        self.agent.setMode(AgentMode.estimating)
        mu = np.zeros((self.featureSize, 1))
        for i in range(self.numEstimating):
            self.runGame()
            mu += self.agent.getfeatureExpection()
        self.mus.append(mu / self.numEstimating)

    def updateRewardFunction(self):
        if self.muBar == None:
            self.muBar = self.mus[0]
            muBar = self.muBar
        else:
            coef = (self.mus[-1] - self.muBar).T.dot(self.muExpert - self.muBar)
            coef = coef / (self.mus[-1] - self.muBar).T.dot(self.mus[-1] - self.muBar)
            muBar = self.muBar + coef * (self.mus[-1] - self.muBar)
        self.w = self.muExpert - muBar
        self.muBar = muBar
        self.agent.setRewardVector(self.w)
        return np.linalg.norm(self.w)
        
    def updateAgent(self):
        self.agent.setMode(AgentMode.training)
        for i in range(self.numTraining):
            self.runGame()

    # override this function
    def runGame(self):
        pass