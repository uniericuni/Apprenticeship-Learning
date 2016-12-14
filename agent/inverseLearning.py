import numpy as np
import sys
from approximateAgents import *
import pickle

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
        self.mus = np.zeros((featureSize,0))
        self.policies = []

        self.muBar = None
        
    def train(self):
        sys.stdout.write('training:'+'\n')
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
        sys.stdout.write('training finished'+'\n')

    def test(self):
        sys.stdout.write('testing:'+'\n')
        self.agent.setMode(AgentMode.testing)
        self.runGame()

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
        self.mus = np.concatenate((self.mus,mu/self.numEstimating),1)
        self.policies.append(self.agent.getPolicyTable())
        # print 'mu'
        # print self.mus
        # print self.policies

    def updateRewardFunction(self):

        mus = self.mus[:,-1].reshape((self.featureSize,1))
        # print 'mus',mus.T
        if self.muBar is None:
            self.muBar = mus
            muBar = self.muBar
        else:
            coef = (mus - self.muBar).T.dot(self.muExpert - self.muBar)
            # if coef != 0:
            coef = coef / (mus - self.muBar).T.dot(mus - self.muBar)
            muBar = self.muBar + coef * (mus - self.muBar)
        self.w = self.muExpert - muBar
        self.w = self.w / np.sum(np.abs(self.w))
        # print('w', self.w.T)
        self.muBar = muBar
        self.agent.setRewardVector(self.w)
        # print 'w'
        # print self.w.T
        return np.linalg.norm(self.muExpert - muBar)
        
    def updateAgent(self):
        self.agent.setMode(AgentMode.training)
        for i in range(self.numRLTraining):
            self.printStatus(float(i)/self.numRLTraining)
            self.runGame()
        # print 'weights'
        # print self.agent.weights.T

    # override this function
    def runGame(self):
        pass

    def savePolicy(self, filename):
        f = open(filename, 'w')
        pickle.dump({'policies':self.policies, 'mus':self.mus},f)
        f.close()
        # sio.savemat(filename, {'policies':self.policies, 'mus':self.mus})
        # print self.policies[-1]

    def loadPolicy(self, filename, i=-1):
        f = open(filename)
        m = pickle.load(f)
        # m = sio.loadmat(filename)
        self.policies = m['policies']
        self.mus = m['mus']
        self.agent.setPolicyTable(m['policies'][i])
        # print self.policies[-1]
        # print r.T
        # print self.mus.shape


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
