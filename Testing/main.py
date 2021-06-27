import pygame
import os
from API import Game

def main():
    curr_dir = os.path.dirname(__file__)
    game = Game.Game((1000, 800), 'Moonlight Inn', curr_dir, 'Resources/window_icon.ico')
    while game.running:
        for event in pygame.event.get():
            does_clear_queue = game.handle_event(event)
            if does_clear_queue:
              pygame.event.clear()
        if game.pc.moveup:
            game.pc.location[1] -= game.pc.speed
        if game.pc.movedown:
            game.pc.location[1] += game.pc.speed
        if game.pc.moveleft:
            game.pc.location[0] -= game.pc.speed
        if game.pc.moveright:
            game.pc.location[0] += game.pc.speed
        game.screen.fill((0, 0, 0)) 
        game.screen.blit(game.pc.icon, tuple(game.pc.location))
        pygame.display.update()
if __name__ == '__main__':
    main()
        



