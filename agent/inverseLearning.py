import numpy as np
from approximateAgents import *

class InverseLearning:
    """docstring for inverseLearning"""
    def __init__(self, agent, gamemgr, featureSize, error=0.001, numEstimating=100, numTraining=-1, numRLTraining=50):
        self.agent = agent
        self.gamemgr = gamemgr
        self.gamma = agent.gamma
        self.numEstimating = numEstimating
        self.numTraining = numTraining
        self.numRLTraining = numRLTraining
        self.error = error
        self.featureSize = featureSize
        self.w = np.zeros((self.featureSize,1))
        self.mus = []
        self.muBar = None
        
    def train(self):
        print 'training:'
        self.featureExpectation()
        t = self.updateRewardFunction()
        counter = 0
        while t > self.error and ( self.numTraining < 0 or counter < self.numTraining ):
            self.updateAgent()
            self.featureExpectation()
            t = self.updateRewardFunction()
            sys.stdout.write( '\r' )
            sys.stdout.write( ' ' * 70 )
            sys.stdout.write( '\r' )
            sys.stdout.write( ' ' * 39)
            sys.stdout.write( ' i = {1}, error: {0}'.format(t, counter) )
            counter += 1
        print 'training finished'

    def test(self):
        print "testing:"
        self.agent.setMode(AgentMode.testing)
        self.runTest()

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
            self.printStatus(float(i)/self.numEstimating)
            self.runGame()
            mu += self.agent.getfeatureExpection()
        self.mus.append(mu / self.numEstimating)

    def updateRewardFunction(self):
        if self.muBar is None:
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
        for i in range(self.numRLTraining):
            self.printStatus(float(i)/self.numRLTraining)
            self.runGame()

    # override this function
    def runGame(self):
        pass


    def printStatus(self, percent):
        pl = 27
        ml = 12
        sys.stdout.write('\r')
        sys.stdout.write(' '*(pl+ml))
        sys.stdout.write('\r')
        modeStr = ""
        if self.agent.isInEstimating():
            modeStr = "Estimating: "
        if self.agent.isInTraining():
            modeStr = "Training:   "
        pStr = self.progressStr(pl,percent)
        sys.stdout.write(modeStr + pStr)
        sys.stdout.flush()



    def progressStr(self, length=27.0, percent=0.0):
        ret = '['
        barLength = length-7
        for i in range(barLength):
            if float(i) / barLength <= percent:
                ret += '='
            else:
                ret += ' '
        ret += ']'
        percentStr = '%s' % str(int(percent*100)).rjust(3)
        ret = ret + percentStr + '%'
        return ret
