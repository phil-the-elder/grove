import pygame
import os
from API import Game

def main():
    curr_dir = os.path.dirname(__file__)
    game = Game.Game((1000, 800), 'Moonlight Inn', curr_dir, 'Resources/window_icon.ico', 60)
    while game.running:
        game.update_display()
if __name__ == '__main__':
    main()
        


