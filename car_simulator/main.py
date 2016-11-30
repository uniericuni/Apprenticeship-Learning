import pygame
import game
import time
import scipy.io as sio
from config import *

if __name__ == '__main__':

    status = 1
    gamemgr = game.gamemgr()
    features = []

    # main game loop
    while status:
        status = gamemgr.input()
        feature = gamemgr.update()
        gamemgr.render()
        if feature:
            features.append(feature)
        elif feature==None and len(features)>0:
            timestr = time.strftime('%y%m%d%H%M%S')
            sio.savemat('%s%s_record.mat'%(CAR_RECORD_PATH,timestr), {'features':features})
            features = []
    if len(features)>0:
        timestr = time.strftime('%y%m%d%H%M%S')
        sio.savemat('%s%s_record.mat'%(CAR_RECORD_PATH,timestr), {'features':features})
