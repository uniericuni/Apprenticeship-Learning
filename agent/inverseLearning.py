import numpy as np
from approximateAgents import *

class inverseLearning:
    """docstring for inverseLearning"""
    def __init__(self, gamma, numEstimating, numTraining):
        self.gamma = gamma
        self.numEstimating = numEstimating
        self.numTraining = numTraining

        self.featureSize = 0
        self.w = np.zeros((self.featureSize,1))
        self.mius = []
        self.miuBar = None
        self.miuExpert = None
        
        pass
        
    def train(self):
        self.featureExpectation()
        t = self.updateRewardFunction()

        while t > self.error:
            self.updateAgent()
            self.featureExpectation()
            t = self.updateRewardFunction()

    # override this function
    def computeExpertExpectation(self):
        pass

    def featureExpectation(self):
        self.agent.setMode(AgentMode.estimating)
        miu = np.zeros((self.featureSize, 1))
        for i in range(self.numEstimating):
            self.runGame()
            miu += self.agent.getfeatureExpectation()
        self.mius.append(miu / numEstimating)

    def updateRewardFunction(self):
        if self.miuBar = None:
            self.miuBar = self.mius[0]
            miuBar = self.miuBar
        else:
            coef = (self.mius[-1] - self.miuBar).T.dot(self.miuExpert - self.miuBar)
            coef = coef / (self.mius[-1] - self.miuBar).T.dot(self.mius[-1] - self.miuBar)
            miuBar = self.miuBar + coef * (self.mius[-1] - self.miuBar)
        self.w = self.miuExpert - miuBar
        return np.linalg.norm(self.w)
        
    def updateAgent(self):
        self.agent.setMode(AgentMode.training)
        self.agent.setRewardVector(self.w)
        for i in range(self.numTraining):
            self.runGame()

    # override this function
    def runGame(self):
        pass