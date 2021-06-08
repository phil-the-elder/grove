import pygame
import os
from API import Game, Creature

def main():
    curr_dir = os.path.dirname(__file__)
    game = Game.Game((1000, 800), 'Moonlight Inn', os.path.join(curr_dir, 'Resources/window_icon.ico'))
    while game.running:
        for event in pygame.event.get():
            does_clear_queue = game.handle_event(event)
            if does_clear_queue:
              pygame.event.clear()  
    pygame.display.update()

if __name__ == '__main__':
    main()
        



