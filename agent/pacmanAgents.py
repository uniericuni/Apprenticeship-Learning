# an approximate q learning agent
import util
import random
from game import Directions, Agent, Actions
from game import *
from featureExtractors import *

class ApproximateAgent(Agent):
    """docstring for ApproximateAgent"""
    def __init__(self, actionFn=None, alpha=0.2, epsilon=0.05, gamma=0.8, numTraining=100, extractor='IdentityExtractor'):
        if actionFn == None:
            actionFn = lambda state: state.getLegalActions()
        self.actionFn = actionFn
        self.episodesSoFar = 0
        self.accumTrainRewards = 0.0 
        self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.gamma = float(gamma)

        self.featExtractor = util.lookup(extractor, globals())()
        self.weights = util.Counter()
        self.index = 0

    # from approximate q-learning
    def getQValue(self, state, action):
        feats = self.featExtractor.getFeatures( state, action )
        return feats * self.weights
    
    def update(self, state, action, nextState, reward):
        feats = self.featExtractor.getFeatures( state, action )
        correction = reward + self.gamma * self.getValue( nextState ) - self.getQValue( state, action )
        keys = feats.keys()
        for key in keys:
            self.weights[key] += self.alpha * correction * feats[key]
        return

    def getAction(self, state):
        legalActions = self.getLegalActions(state)
        action = None
        if legalActions:
            if util.flipCoin( self.epsilon ):
                action = random.choice( legalActions )
            else:
                action = self.getPolicy( state )
        self.doAction(state,action)
        return action

    # from q-learning
  
    def getValue(self, state):
        actions = self.getLegalActions( state )
        if not actions:
            return 0.0

        return max( [ self.getQValue( state, action ) for action in actions ] )
    
    def getPolicy(self, state):
        actions = self.getLegalActions( state )
        if not actions:
          return None

        maxQ = self.getValue( state )
        bestActions = [ action for action in actions if self.getQValue( state, action ) == maxQ ]
        return random.choice( bestActions )

    # from reinforcement learning
    def getLegalActions(self, state):
        return self.actionFn(state)

    def observeTransition(self, state, action, nextState, deltaReward):
        self.episodeRewards += deltaReward
        self.update(state, action, nextState, deltaReward)

    def startEpisode(self):
        self.lastState = None
        self.lastAction = None
        self.episodeRewards = 0.0

    def stopEpisode(self):
        if self.episodesSoFar < self.numTraining:
            self.accumTrainRewards += self.episodeRewards
        else:
            self.accumTestRewards += self.episodeRewards
        self.episodesSoFar += 1    
        if self.episodesSoFar >= self.numTraining:
                # Take off the training wheels
            self.epsilon = 0.0    # no exploration
            self.alpha = 0.0      # no learning
    
    def isInTraining(self): 
        return self.episodesSoFar < self.numTraining
  
    def isInTesting(self):
        return not self.isInTraining()

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon
    
    def setLearningRate(self, alpha):
        self.alpha = alpha
    
    def setDiscount(self, discount):
        self.gamma = discount
    
    def doAction(self,state,action):
        self.lastState = state
        self.lastAction = action
  
    def observationFunction(self, state):
        if not self.lastState is None: 
            reward = state.getScore() - self.lastState.getScore()
            self.observeTransition(self.lastState, self.lastAction, state, reward)
        return state    
     
    def registerInitialState(self, state):
        self.startEpisode()      
        if self.episodesSoFar == 0:
            print 'Beginning %d episodes of Training' % (self.numTraining)
    
    def final(self, state):
        deltaReward = state.getScore() - self.lastState.getScore()
        self.observeTransition(self.lastState, self.lastAction, state, deltaReward)
        self.stopEpisode()
    
        # Make sure we have this var
        if not 'episodeStartTime' in self.__dict__:
            self.episodeStartTime = time.time()
        if not 'lastWindowAccumRewards' in self.__dict__:
            self.lastWindowAccumRewards = 0.0
        self.lastWindowAccumRewards += state.getScore()
        
        NUM_EPS_UPDATE = 100
        if self.episodesSoFar % NUM_EPS_UPDATE == 0:
            print 'Reinforcement Learning Status:'
            windowAvg = self.lastWindowAccumRewards / float(NUM_EPS_UPDATE)
            if self.episodesSoFar <= self.numTraining:
                trainAvg = self.accumTrainRewards / float(self.episodesSoFar)                
                print '\tCompleted %d out of %d training episodes' % (
                       self.episodesSoFar,self.numTraining)
                print '\tAverage Rewards over all training: %.2f' % (
                        trainAvg)
            else:
                testAvg = float(self.accumTestRewards) / (self.episodesSoFar - self.numTraining)
                print '\tCompleted %d test episodes' % (self.episodesSoFar - self.numTraining)
                print '\tAverage Rewards over testing: %.2f' % testAvg
            print '\tAverage Rewards for last %d episodes: %.2f'  % (
                    NUM_EPS_UPDATE,windowAvg)
            print '\tEpisode took %.2f seconds' % (time.time() - self.episodeStartTime)
            self.lastWindowAccumRewards = 0.0
            self.episodeStartTime = time.time()
            
        if self.episodesSoFar == self.numTraining:
            msg = 'Training Done (turning off epsilon and alpha)'
            print '%s\n%s' % (msg,'-' * len(msg))
