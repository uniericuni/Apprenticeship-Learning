from approximateAgents import *
from GridWorld import *

class gridWorldAgent(ApproximateQLearningAgent):

	def __init__(self, w, mode, alpha=0.2, epsilon=0.05, gamma=0.9):
		ApproximateQLearningAgent.__init__(self, w, mode, alpha, epsilon, gamma)

	def getStateFeature(self, state):
    """
    return features base on state
    """
    	return DaPingTai.feature_vector(state)

    def getFeatures(self, state, action):
    	sx, sy = DaPingTai.int_to_point(state)
    	ax, ay = DaPingTai.getAction(action)

    	new_sx = sx + ax
    	new_sy = sy + ay

    	new_state = DaPingTai.point_to_int(new_sx, new_sy)

    	return DaPingTai.feature_vector(new_state)

    def getLegalActions(self, state):
    	
    	return DaPingTai.getLegalAction(state)
    	