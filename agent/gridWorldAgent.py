from approximateAgents import *
import sys
sys.path.append('../gridworld/')
from GridWorld import *
import numpy as np

class gridWorldAgent(ApproximateQLearningAgent):

	def __init__(self, w, gamemgr, mode=AgentMode.estimating, alpha=0.2, epsilon=0.05, gamma=0.9):
		ApproximateQLearningAgent.__init__(self, w, mode, alpha, epsilon, gamma)
		self.gamemgr = gamemgr

	def getStateFeature(self, state):
		"""
		return features base on state
		"""

		return np.reshape(self.gamemgr.feature_vector(state), (self.gamemgr.n_states, 1))

	def getFeatures(self, state, action):
		sx, sy = self.gamemgr.int_to_point(state)
		ax, ay = self.gamemgr.getAction(action)

		new_sx = sx + ax
		new_sy = sy + ay

		new_state = self.gamemgr.point_to_int((new_sx, new_sy))

		return np.reshape(self.gamemgr.feature_vector(new_state), (self.gamemgr.n_states, 1))

	def getLegalActions(self, state):
		
		return np.array(self.gamemgr.getLegalAction(state))
		