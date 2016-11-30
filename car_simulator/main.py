import pygame
import game
import time
import scipy.io as sio
from config import *

if __name__ == '__main__':

    status = 1
    gamemgr = game.gamemgr()
    features = []
    time = time.strftime('%y%m%d%H%M%S')

    # main game loop
    while status:
        status = gamemgr.input()
        feature = gamemgr.update()
        gamemgr.render()
        features.append(feature)
    sio.savemat('%s%s_record.mat'%(CAR_RECORD_PATH,time), {'features':features})
