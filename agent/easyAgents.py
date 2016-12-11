from approximateAgents import *

class EasyAgent(ApproximateQLearningAgent):
    """docstring for CarAgent"""
    def __init__(self,  w, mode=AgentMode.estimating, alpha=0.2, epsilon=0.05, gamma=0.99):
        ApproximateQLearningAgent.__init__(self, w, mode, alpha, epsilon, gamma)

    def getStateFeature(self, state):
        """
        return features base on state
        """
        f = np.zeros((3,1))
        f[state] = 1
        return f

    def getFeatures(self, state, action):
        """
        return features base on state and action
        """
        f = np.zeros((3,1))
        f[state+action] = 1
        return f

    def getLegalActions(self, state):
        if state == 0:
            return np.array([0, 1])
        elif state == 1:
            return np.array([-1, 0, 1])
        else:
            return np.array([-1, 0])
