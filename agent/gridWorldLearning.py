from inverseLearning import *
import numpy as np

class gridWorldLearning(InverseLearning):

	def __init__(self, agent, DaPingTai, featureSize, error=0.001, numEstimating=100, numTraining=-1, numRLTraining=50):
		InverseLearning.__init__(self, agent=agent, gamemgr=DaPingTai, featureSize=featureSize, error=error, numEstimating=numEstimating, numTraining=numTraining, numRLTraining=numRLTraining)

	def computeExpertExpectation(self):
		pass

	def runGame(self):
		#startState = self.gamemgr.getStartState()
		currentState = self.gamemgr.getCurrentState()
		cx, cy = self.gamemgr.point_to_int(currentState)

		self.agent.registerInitialState(currentState)
		
		p = np.random.uniform(0, 1)

		if  p > self.gamemgr.wind:		

			action = self.agent.getAction(currentState)
			ax, ay = self.gamemgr.getAction(action)

		else:
			ax, ay = self.gamemgr.getAction(np.random.randint(0, 4))

		currentState = self.gamemgr.point_to_int((cx + ax, cy + ay))

		self.gamemgr.setCurrentState(currentState)








