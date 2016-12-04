from approximateAgents import *

class CarAgent(ApproximateQLearningAgent):
    """docstring for CarAgent"""
    def __init__(self,  w, mode=AgentMode.estimating, alpha=0.2, epsilon=0.05, gamma=0.8):
        super(CarAgent, self).__init__(w, mode, alpha, epsilon, gamma)

    def getStateFeature(self, state):
        """
        return features base on state
        """
        lane = np.zeros((1, state[0].shape[0]))
        for i in range(state[0].shape[0]):
            if state[0][i][0] == 1:
                lane[i] = 1.0
                break
        return np.concatenate((lane, state[0][i][1:]))

    def getFeatures(self, state, action):
        """
        return features base on state and action
        """
        lane = np.zeros((1, state[0].shape[0]))
        lane[action] = 1.0
        return np.concatenate((lane, state[0][action][1:]))

    def getLegalActions(self, state):
        return state[1]
