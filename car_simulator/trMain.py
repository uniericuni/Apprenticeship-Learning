import pygame, sys, getopt
import game
import time
import scipy.io as sio
from config import *

MAX_ITERATION = 1000

def main(argv):
    # parser
    try:
        opts, args = getopt.getopt(argv,"m:i:")
    except getopt.GetoptError:
        print 'usage: main.py -m gamemode'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-m':
            gamemode = arg
            print 'gamemode: ' + arg
            if arg=='train': gamemode = 100
            elif arg=='driving': gamemode = 2
            elif arg=='auto': gamemode = 3
        elif opt == '-i':
            MAX_ITERATION = arg
            print 'max iteration: ' + arg
        else: 
            print 'usage: main.py -m gamemode'
            sys.exit(2)

    agent = CarAgent(w=np.zeros([15,1]))
    learn = CarLearning(agent)
    learn.runGame()

    # game manager init
    counter = 0
    features = []
    gamemgr = game.gamemgr(gamemode)
    status = gamemgr.input()
    state,legal_action = gamemgr.update()

    # agent init
    agent = CarAgent(w=np.zeros([15,1]))
    agent.registerInitialState((state,legal_action))
    action = None

    # main game loop
    while gamemgr.state:
        
        # training break
        if gamemgr.state==100:
            counter += 1
            if counter > MAX_ITERATION:
                break
            action = agent.getAction((game_state,legal_action))

        # main game loop
        state = gamemgr.input(action)
        game_state,legal_action = gamemgr.update()
        gamemgr.render()

        # feature export
        if gamemgr.record:
            features.append(feature)
        elif len(features)>0:
            timestr = time.strftime('%y%m%d%H%M%S')
            sio.savemat('%s%s_record.mat'%(CAR_RECORD_PATH,timestr), {'features':features})
            features = []
      
    # final
    agent.final((game_state,legal_action))

    # feature export
    if len(features)>0:
        timestr = time.strftime('%y%m%d%H%M%S')
        sio.savemat('%s%s_record.mat'%(CAR_RECORD_PATH,timestr), {'features':features})

if __name__ == '__main__':
    # import agent
    sys.path.append(AGENT_PATH)
    from carAgents import *
    from carLearning import *

    main(sys.argv[1:])
