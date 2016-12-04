import numpy as np

class inverseLearning:
    """docstring for inverseLearning"""
    def __init__(self, gamma, numEstimating):
        self.gamma = gamma
        self.numEstimating

        self.w = None
        self.mius = []
        self.miuBar = None
        self.miuExpert = None
        
    def train(self):
        self.featureExpection()
        t = self.updateRewardFunction()

        while t > self.error:
            self.updateAgent()
            self.featureExpection()
            t = self.updateRewardFunction()

    def computeExpertExpection(self):
        pass

    def featureExpection(self):
        for i in range(self.numEstimating):

        pass

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
        pass