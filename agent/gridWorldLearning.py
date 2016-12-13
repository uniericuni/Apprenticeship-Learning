from inverseLearning import *


import sys

import numpy as np

class gridWorldLearning(InverseLearning):

	def __init__(self, agent, DaPingTai, featureSize=16, error=0.001, numEstimating=100, numTraining=50, numRLTraining=50):
		InverseLearning.__init__(self, agent=agent, gamemgr=DaPingTai, featureSize=featureSize, error=error, numEstimating=numEstimating, numTraining=numTraining, numRLTraining=numRLTraining)

	def computeExpertExpectation(self):
		self.muExpert =  self.gamemgr.optimalPolicy(self.gamma)
		print('expert', self.muExpert)
		


	def runGame(self):
		#startState = self.gamemgr.getStartState()
		currentState = self.gamemgr.getStartState()
		self.gamemgr.setCurrentState(currentState)
		self.gamemgr.setNegativeScore(0)
		cx, cy = self.gamemgr.int_to_point(currentState)

		self.agent.registerInitialState(currentState)
		count = 0
		#print(self.gamemgr.convertToMatrix(self.gamemgr.ground_r))
		#print('Goal:', self.gamemgr.int_to_point(self.gamemgr.getPostiveRewardState()))
		if self.agent.isInTesting():
			print(self.gamemgr.convertToMatrix(self.gamemgr.ground_r))
			print('Goal:', self.gamemgr.int_to_point(self.gamemgr.getPostiveRewardState()))
			while True:
				currentState = self.gamemgr.getCurrentState()
				cx, cy = self.gamemgr.int_to_point(currentState)
				print('=========================')		
				print('Current state: ', (cx, cy))
				p = np.random.uniform(0, 1)

				if  p > self.gamemgr.wind:	
					action = self.agent.getAction(currentState) # Specific action
					print('Specific action:', action)
					ax, ay = self.gamemgr.getAction(action)     # Action to tuple

				else:
					action = np.random.randint(0, 4)
					print('Random action', action)
					ax, ay = self.gamemgr.getAction(action)

				
				print('Next State:', (cx + ax, cy + ay))
				if cx + ax < 0 or cx + ax >= self.gamemgr.grid_size or cy + ay < 0 or cy + ay >= self.gamemgr.grid_size:
					print('Out of Grid!')
					self.gamemgr.increaseNegativeScore(-1)
					continue

				next_state = self.gamemgr.point_to_int((cx + ax, cy + ay))
				if self.gamemgr.ground_r[next_state] == -1:
					self.gamemgr.increaseNegativeScore(-1)
					print('Step on negative!!')
				self.gamemgr.setCurrentState(next_state)
				#new_state = self.gamemgr.getCurrentState()
				if next_state == self.gamemgr.getPostiveRewardState():
					print('Good!')
					break
				count += 1
		else:
			while True:
				cx, cy = self.gamemgr.int_to_point(self.gamemgr.getCurrentState())
				#print('=========================')		
				#print('Current state: ', (cx, cy))
				
				p = np.random.uniform(0, 1)

				if  p > self.gamemgr.wind:		

					action = self.agent.getAction(currentState) # Specific action
					#print('Specific action:', action)
					ax, ay = self.gamemgr.getAction(action)     # Action to tuple

				else:
					action = np.random.randint(0, 4)
					#print('Random action', action)
					ax, ay = self.gamemgr.getAction(action)

				
				#print('Next State:', (cx + ax, cy + ay))
				if cx + ax < 0 or cx + ax >= self.gamemgr.grid_size or cy + ay < 0 or cy + ay >= self.gamemgr.grid_size:
					#print('Out of Grid!')
					self.gamemgr.increaseNegativeScore(-1)
					continue

				next_state = self.gamemgr.point_to_int((cx + ax, cy + ay))
				if self.gamemgr.ground_r[next_state] == -1:
					self.gamemgr.increaseNegativeScore(-1)
					#print('Step on negative!!')
				self.gamemgr.setCurrentState(next_state)
				#new_state = self.gamemgr.getCurrentState()
				if next_state == self.gamemgr.getPostiveRewardState():
					#print('Good!')
					break
				count += 1

		#print('Negative Score: ', self.gamemgr.getNegativeScore())

if __name__ == "__main__":
	from gridWorldAgent import *
	sys.path.append('../gridworld/')
	from GridWorld import *
	
	DaPingTai = DaPingTai(4, 0.3, 1)
	goalstate = DaPingTai.getPostiveRewardState()
	w = np.zeros((16, 1))
	#w[goalstate] = 1
	agent = gridWorldAgent(w, DaPingTai)

	learn = gridWorldLearning(agent, DaPingTai)

	learn.computeExpertExpectation()

	learn.train()
	learn.test()
	learn.test()
	learn.test()
	learn.test()














