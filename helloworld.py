import pygame
import game

if __name__ == '__main__':
   
    game = game.game()
    while True:
        game.input()
        game.update()
        game.render()
