from approximateAgents import *

class CarAgent(ApproximateQLearningAgent):
    """docstring for CarAgent"""
    def __init__(self,  w, mode=AgentMode.estimating, alpha=0.2, epsilon=0.05, gamma=0.99):
        ApproximateQLearningAgent.__init__(self, w, mode, alpha, epsilon, gamma)

    def getStateFeature(self, state):
        """
        return features base on state
        """
        lane = np.zeros((1, state[0].shape[0]))
        for i in range(state[0].shape[0]):
            if state[0][i][0] == 1:
                lane[0][i] = 1.0
                break
        # print i, lane
        # print state[0][i][1:].reshape((1, state[0][i][1:].size))
        return np.concatenate((lane, state[0][i][1:].reshape((1, state[0][i][1:].size))), 1).T

    def getFeatures(self, state, action):
        """
        return features base on state and action
        """
        lane = np.zeros((1, state[0].shape[0]))
        lane[0][action] = 1.0
        return np.concatenate((lane, state[0][action][1:].reshape((1, state[0][action][1:].size))), 1).T

    def getLegalActions(self, state):
        return state[1]
