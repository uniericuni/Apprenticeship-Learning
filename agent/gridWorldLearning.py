from inverseLearning import *
import matplotlib.pyplot as plt

import sys

import numpy as np

class gridWorldLearning(InverseLearning):


	def __init__(self, agent, DaPingTai, random, numberOfTrajectories, featureSize=25, error=0.001, numEstimating=100, numTraining=50, numRLTraining=300):
		InverseLearning.__init__(self, agent=agent, gamemgr=DaPingTai, featureSize=featureSize, error=error, numEstimating=numEstimating, numTraining=numTraining, numRLTraining=numRLTraining)
		self.t =[]
		self.count = []
		self.random = random
		self.numberOfTrajectories = numberOfTrajectories
	def computeExpertExpectation(self):
		self.muExpert =  self.gamemgr.optimalPolicy(self.gamma, self.numberOfTrajectories)
		
	def getError(self, t, count):
		self.t.append(t)
		self.count.append(count)

	def train(self):
		sys.stdout.write('training:'+'\n')
		self.featureExpectation()
		t = self.updateRewardFunction()
		counter = 0
		while t > self.error and ( self.numTraining < 0 or counter < self.numTraining ):
			self.updateAgent()
			self.featureExpectation()
			self.getError(t, counter)
			t = self.updateRewardFunction()
			sys.stdout.write( '\r' )
			sys.stdout.write( ' ' * 70 )
			sys.stdout.write( '\r' )
			sys.stdout.write( ' ' * 39)
			sys.stdout.write( ' i = {1}, error: {0}'.format(t, counter) )
			counter += 1
		sys.stdout.write('training finished'+'\n')
	def setRandom(self):
		return np.random.uniform(0, 1)	

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
				if self.random == True:
					p = np.random.uniform(0, 1)
				else:
					p = 1
				action = self.agent.getAction(currentState)
				if  p > self.gamemgr.wind:	
					 # Specific action
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
				# print('Current state')
				currentState = self.gamemgr.getCurrentState()
				cx, cy = self.gamemgr.int_to_point(self.gamemgr.getCurrentState())
				#print('=========================')		
				#print('Current state: ', (cx, cy))
				# print('P')
				if self.random == True:
					p = np.random.uniform(0, 1)
				else:
					p = 1
				p = np.random.uniform(0, 1)
				action = self.agent.getAction(currentState) 
				if  p > self.gamemgr.wind:		

					# Specific action
					#print('Specific action:', action)
					ax, ay = self.gamemgr.getAction(action)     # Action to tuple

				else:
					action = np.random.randint(0, 4)
					#print('Random action', action)
					ax, ay = self.gamemgr.getAction(action)


				# print('OffGrid')
				#print('Next State:', (cx + ax, cy + ay))
				if cx + ax < 0 or cx + ax >= self.gamemgr.grid_size or cy + ay < 0 or cy + ay >= self.gamemgr.grid_size:
					#print('Out of Grid!')
					self.gamemgr.increaseNegativeScore(-1)
					continue
				# print('nextstate')
				next_state = self.gamemgr.point_to_int((cx + ax, cy + ay))
				if self.gamemgr.ground_r[next_state] == -1:
					self.gamemgr.increaseNegativeScore(-1)
					#print('Step on negative!!')
				self.gamemgr.setCurrentState(next_state)
				#new_state = self.gamemgr.getCurrentState()
				# print('Check goal')
				if next_state == self.gamemgr.getPostiveRewardState():
					#print('Good!')
					break
				count += 1
		self.agent.final(next_state)


		#print('Negative Score: ', self.gamemgr.getNegativeScore())

def experiment(DaPingTai, random = True, SpecificReward = False, numberOfTrajectories = 25, labelName = 'Normal'):
	print('Running: '+labelName)
	size = DaPingTai.n_states
	w = np.zeros((size, 1))
	if SpecificReward == True:
		w = DaPingTai.ground_r
		w[DaPingTai.getPostiveRewardState()] = 1
		w = np.reshape(w, (size, 1))

	agent = gridWorldAgent(w, DaPingTai)
	learn = gridWorldLearning(agent, DaPingTai, random, numberOfTrajectories)
	if SpecificReward == True:
		learn.updateAgent()
	else:
		learn.computeExpertExpectation()
		learn.train()

	plt.plot(learn.count, learn.t, alpha = 0.5, linewidth = 2, label =labelName)
	learn.test()
	learn.test()
	learn.test()
	learn.test()

def experiment2(DaPingTai, random = True):
	plt.figure()
	size = DaPingTai.n_states
	w = np.zeros((size, 1))
	agent = gridWorldAgent(w, DaPingTai)
	learn = gridWorldLearning(agent, DaPingTai, random, numberOfTrajectories = size)
	learn.computeExpertExpectation()
	learn.train()
	plt.plot(learn.count, learn.t , alpha = 0.5, linewidth = 2, label ='Normal Agent')
	learn.test()
	agent = gridWorldQAgent(w, DaPingTai)
	learn = gridWorldLearning(agent, DaPingTai, random, numberOfTrajectories = size)	
	learn.computeExpertExpectation()
	learn.train()
	learn.test()
	plt.plot(learn.count, learn.t, alpha = 0.5, linewidth = 2, linestyle = '--', label ='Q Agent')
	plt.xlabel('Iterations')
	plt.ylabel('Error')
	plt.legend(loc='best')
	plt.show()




if __name__ == "__main__":
	from gridWorldAgent import *
	sys.path.append('../gridworld/')
	from GridWorld import *
	
	DaPingTai = DaPingTai(5, 0.3, 1)
	goalstate = DaPingTai.getPostiveRewardState()

	# w = np.array([0, 0, -1, 1, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0]).reshape(16, 1)
	#w[goalstate] = 1
	# Normal Agent
	plt.figure()
	# learn.updateAgent()
	# experiment(DaPingTai, random = True, SpecificReward = False, numberOfTrajectories = DaPingTai.n_states, labelName = 'Normal')
	# experiment(DaPingTai, random = False, SpecificReward = False, numberOfTrajectories = DaPingTai.n_states, labelName = 'Remove Random')
	# experiment(DaPingTai, random = True, SpecificReward = False, numberOfTrajectories = 20, labelName = 'Specified Trajectories')




	
	# Q Agent
	# agent = gridWorldQAgent(w, DaPingTai)
	# learn = gridWorldLearning(agent, DaPingTai, random = True, numberOfTrajectories = DaPingTai.n_states)
	# learn.computeExpertExpectation()	
	# learn.train()
	# plt.plot(learn.t, learn.count, alpha = 0.5, label ='Q Agent')

	plt.xlabel('Iterations')
	plt.ylabel('Error')
	plt.legend(loc='best')
	plt.show()

	# experiment2(DaPingTai)
	plt.figure()
	experiment(DaPingTai, random = True, SpecificReward = True, numberOfTrajectories = DaPingTai.n_states, labelName = 'Spedicfied Reward')


















