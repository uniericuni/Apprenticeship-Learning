import pygame
import game

if __name__ == '__main__':

    status = 1
    gamemgr = game.gamemgr()

    # main game loop
    while status:
        status = gamemgr.input()
        gamemgr.update()
        gamemgr.render()
