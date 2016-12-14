# an approximate q learning agent
import numpy as np
import scipy.io as sio
import sys

class AgentMode:
    """
    modes of agents
    """
    estimating = 1
    training = 2
    testing = 3
        

class QLearningAgent:
    """
    Abstract class of approximate q-learning agent.
    Must override 
        getStateFeature(self, state)
        getFeatures(self, state, action)
        getLegalActions(self, state)

    Attributes:
        epsilon         exploration rate
        alpha           learning rate
        gamma           discount rate
        trainEpsilon    exploration rate value
        trainAlpha      learning rate value
        mode            agent mode, esimating, training or testing
        w               reward vector
        t               time
        weights         approximate q table weights
        mu              expection of features
        lastState       previous state
        lastAction      previous action

    Methods:
        __init__(self, alpha, epsilon, gamma, w): initialize

        registerInitialState(self, state): call before game starts
        getAction(self, state): call in game, give a state return an action
        final(self, state): call after game ends

        observeTransition(self, state, action, nextState, deltaReward): observe transition of states
        update(self, state, action, nextState, reward): update parameters

        getScore(self, state): return reward based on state
        getQValue(self, state, action): get q value


    Ussage:
        To run a game
        1. initialize agent
        2. 

    """
    def __init__(self, w, mode=AgentMode.estimating, alpha=0.2, epsilon=0.05, gamma=0.8):
        self.trainEpsilon = float(epsilon)
        self.trainAlpha = float(alpha)
        self.gamma = float(gamma)
        self.mode = mode
        self.w = w
        self.t = 0
        self.setMode(mode)
        self.Qtable = {}

    ##########################
    # methods called in game #
    ##########################
    def registerInitialState(self, state):
        """
        call before game
        """

        self.lastState = None
        self.lastAction = None
        self.episodeRewards = 0.0
        self.mu = self.getStateFeature(state)
        self.t = 0
    
    def getAction(self, state):
        """
        call in each step of game,
        give a state return an action
        """
        if not self.lastState is None: 
            reward = self.getScore(state) # - self.getScore(self.lastState)
            self.observeTransition(self.lastState, self.lastAction, state, reward)

        legalActions = self.getLegalActions(state)
        action = None
        if legalActions.size:
            if np.random.rand(1) < self.epsilon:
                action = np.random.choice( legalActions, 1 )[0]
            else:
                action = self.getPolicy( state )
        self.doAction(state,action)
        return action

    def final(self, state):
        """
        call after the game
        """
        deltaReward = self.getScore(state) # - self.getScore(self.lastState)
        self.observeTransition(self.lastState, self.lastAction, state, deltaReward)
        # print self.episodeRewards
        # print self.episodeRewards


    ##################
    # helper methods #
    ##################
    def observeTransition(self, state, action, nextState, deltaReward):
        self.episodeRewards += deltaReward
        self.update(state, action, nextState, deltaReward)

    def update(self, state, action, nextState, reward):
        """
        update weights and mu if in estimating mode
        """
        # print self.hashableState(state)
        self.getQValue( state, action )
        # print(self.getValue( nextState ).shape, (self.Qtable[self.hashableState(state)])[action].shape)
        # print('h', self.alpha * ( reward + self.gamma * self.getValue( nextState ) - (self.Qtable[self.hashableState(state)])[action] ))
        # print('R',reward)
        (self.Qtable[self.hashableState(state)])[action] += self.alpha * ( reward + self.gamma * self.getValue( nextState ) - (self.Qtable[self.hashableState(state)])[action] )      
        if self.isInEstimating():
            self.mu += self.getStateFeature(nextState) * self.gamma ** self.t
      

    ##############################
    # getter for learning values #
    ##############################
    def getScore(self, state):
        return self.w.T.dot(self.getStateFeature(state))

    def getQValue(self, state, action):
        if self.Qtable.has_key(self.hashableState(state)):
            return (self.Qtable[self.hashableState(state)])[action]

        self.Qtable[self.hashableState(state)] = {}
        for action in self.getLegalActions( state ):
            self.Qtable[self.hashableState(state)][action] = 0.0
        return 0.0
        
  
    def getValue(self, state):
        actions = self.getLegalActions( state )
        if not actions.size:
            return 0.0
        else:
            return max( [ self.getQValue( state, action ) for action in actions ] )
    
    def getPolicy(self, state):
        actions = self.getLegalActions( state )
        if not actions.size:
            return None
        else:
            maxQ = self.getValue( state )
            bestActions = [ action for action in actions if self.getQValue( state, action ) == maxQ ]
            return np.random.choice( bestActions, 1 )[0]

    def getfeatureExpection(self):
        return self.mu

    # overrid this function 
    def getStateFeature(self, state):
        """
        return features base on state
        """
        pass

    # overrid this function 
    def getFeatures(self, state, action):
        """
        return features base on state and action
        """
        pass

    # overrid this function 
    def getLegalActions(self, state):
        """
        return legal actions.
        if no actions return None
        """
        pass

    def hashableState(self, state):
        return str(state)


    #####################
    # getter and setter #
    #####################
    def setMode(self, mode):
        self.mode = mode

        if self.isInTraining():
            self.epsilon = self.trainEpsilon
            self.alpha = self.trainAlpha
        else:
            self.epsilon = 0.0
            self.alpha = 0.0

    def isInEstimating(self):
        return self.mode == AgentMode.estimating

    def isInTraining(self): 
        return self.mode == AgentMode.training
  
    def isInTesting(self):
        return self.mode == AgentMode.testing

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon
    
    def setLearningRate(self, alpha):
        self.alpha = alpha
    
    def setDiscount(self, discount):
        self.gamma = discount

    def setRewardVector(self, w):
        self.w = w
    
    def doAction(self,state,action):
        self.lastState = state
        self.lastAction = action
        self.t += 1

    def getPolicyTable(self):
        return self.Qtable

    def setPolicyTable(self, p):
        self.Qtable = p

    def savePolicy(self, filename):
        sio.savemat(filename, {'Qtable':self.Qtable, 'w':self.w})

    def loadPolicy(self, filename):
        m = sio.loadmat(filename)
        self.Qtable = m['Qtable']
        self.w = m['w']
        # print self.w.T
        # print self.weights.T


class ApproximateQLearningAgent(QLearningAgent):

    def __init__(self, w, mode=AgentMode.estimating, alpha=0.2, epsilon=0.05, gamma=0.8):
        QLearningAgent.__init__(self, w, mode, alpha, epsilon, gamma)
        self.weights = None



    def update(self, state, action, nextState, reward):
        """
        update weights and mu if in estimating mode
        """
        # print self.mu.T, self.mode
        # if reward:
        #     print reward
        features = self.getFeatures( state, action )
        correction = reward + self.gamma * self.getValue( nextState ) - self.getQValue( state, action )
        if self.weights is None:
            self.weights = self.alpha * correction * features
        else:
            self.weights += self.alpha * correction * features
        if self.isInEstimating():
            self.mu += self.getStateFeature(nextState) * self.gamma ** self.t
        # if reward != 0:
        # print self.weights.T, reward

    def getQValue(self, state, action):
        if not self.weights is None:
            features = self.getFeatures(state, action)
            return self.weights.T.dot(features)
        else:
            return 0.0

    def getPolicyTable(self):
        return self.weights

    def setPolicyTable(self, p):
        self.weights = p

    def savePolicy(self, filename):
        sio.savemat(filename, {'weights':self.weights, 'w':self.w})

    def loadPolicy(self, filename):
        m = sio.loadmat(filename)
        self.weights = m['weights']
        self.w = m['w']