from inverseLearning import *
import numpy as np

class gridWorldLearning(InverseLearning):

	def __init__(self, agent, DaPingTai, featureSize, error=0.001, numEstimating=100, numTraining=-1, numRLTraining=50):
		InverseLearning.__init__(self, agent=agent, gamemgr=DaPingTai, featureSize=featureSize, error=error, numEstimating=numEstimating, numTraining=numTraining, numRLTraining=numRLTraining)

	def computeExpertExpectation(self):
		return self.gamemgr.optimalPolicy(self.gamma)


	def runGame(self):
		#startState = self.gamemgr.getStartState()
		currentState = self.gamemgr.getStartState()
		cx, cy = self.gamemgr.int_to_point(currentState)

		self.agent.registerInitialState(currentState)
		count = 0

		while True:
		
			p = np.random.uniform(0, 1)

			if  p > self.gamemgr.wind:		

				action = self.agent.getAction(currentState) # Specific action
				ax, ay = self.gamemgr.getAction(action)     # Action to tuple

			else:
				ax, ay = self.gamemgr.getAction(np.random.randint(0, 4))
			if cx + ax < 0 or cx + ax >= self.gamemgr.grid_size or cy + ay < 0 or cy + ay >= self.gamemgr.grid_size:
				print('Out of Grid!')
				break

			self.gamemgr.setCurrentState(self.gamemgr.point_to_int((cx + ax, cy + ay)))
			#new_state = self.gamemgr.getCurrentState()
			if self.gamemgr.ground_r[cx + ax, cy + ay] == 1:
				print('Good!')
				break
			count += 1

		













