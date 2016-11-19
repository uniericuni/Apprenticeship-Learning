import pygame
import game

if __name__ == '__main__':

    status = 1
    game = game.game()
    while status:
        status = game.input()
        game.update()
        game.render()
