import pygame
import game
import time
import scipy.io as sio
from config import *

if __name__ == '__main__':

    # game manager init
    gamemgr = game.gamemgr(state=100)
    features = []

    # main game loop
    while gamemgr.state:

        # action assignment
        action = 4

        # main game loop
        status = gamemgr.input(action)
        state,legal_action = gamemgr.update()
        gamemgr.render()

        # feature export
        if gamemgr.record:
            features.append(feature)
        elif len(features)>0:
            timestr = time.strftime('%y%m%d%H%M%S')
            sio.savemat('%s%s_record.mat'%(CAR_RECORD_PATH,timestr), {'features':features})
            features = []

    # feature export
    if len(features)>0:
        timestr = time.strftime('%y%m%d%H%M%S')
        sio.savemat('%s%s_record.mat'%(CAR_RECORD_PATH,timestr), {'features':features})
