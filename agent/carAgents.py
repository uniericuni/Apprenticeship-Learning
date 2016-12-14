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


class CarAgent2(CarAgent):
    """docstring for CarAgent2"""
    def __init__(self,  w, mode=AgentMode.estimating, alpha=0.2, epsilon=0.05, gamma=0.99):
        CarAgent.__init__(self,  w, mode, alpha, epsilon, gamma)
        
    def getFeatures(self, state, action):
        """
        return features base on state and action
        """
        myLane = 0.0
        for i in range(state[0].shape[0]):
            if state[0][i][0] == 1:
                myLane = i
                break

        distance = abs(action - myLane)

        nearestFront = 0
        for i in range(distance,state[0].shape[0]):
            if state[0][action][6+i] == 1:
                nearestFront = 5-i
                break

        nearestBack = 10
        for i in range(distance+state[0].shape[0]):
            if state[0][action][6+distance-i] == 1:
                nearestBack = i
                break

        lane = np.zeros((1, state[0].shape[0]))
        lane[0][action] = 1.0
        # print np.concatenate((lane, np.array([[nearestFront, nearestBack]])),1)
        return np.concatenate((lane, np.array([[nearestFront, nearestBack]])),1).T


class CarAgent3(QLearningAgent):
    """docstring for CarAgent"""
    def __init__(self,  w, mode=AgentMode.estimating, alpha=0.2, epsilon=0.05, gamma=0.99):
        QLearningAgent.__init__(self, w, mode, alpha, epsilon, gamma)

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
        myLane = 0.0
        for i in range(state[0].shape[0]):
            if state[0][i][0] == 1:
                myLane = i
                break
        # print myLane
        if myLane == 0:
            return np.array([0, 1])
        elif myLane == 4:
            return np.array([3, 4])
        else:
            return np.array([myLane-1, myLane, myLane+1])

    def hashableState(self, state):
        # state[0].flags.writeable = False
        return str(state[0])