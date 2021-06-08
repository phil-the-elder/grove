import pygame
import os
from . import Creature, DBManager

class Game:
    """ Parent class for the main Game configurations
    :tuple screen_size: initial screen size (int x, int y)
    :object screen: main game screen
    :bool running: whether the game is running
    :str name: name 
    """
    def __init__(self, screen_size: tuple, name: str, corner_icon: str):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.running = True
        self.start_game(name, corner_icon)
        self.pc = self.load_character()
    
    def start_game(self, name, corner_icon):
        """ starts the game 
        :str name: name for corner of window
        :str corner_icon: filepath to the corner icon file
        :return: None
        """
        pygame.init()
        pygame.display.set_caption(name)
        icon = pygame.image.load(corner_icon)
        pygame.display.set_icon(icon)

    def load_character(self):
        curr_dir = os.path.dirname(os.path.dirname(__file__))
        db_conn = DBManager.DBManager(os.path.join(curr_dir, 'main.db'))
        # INCOMPLETE - HAVE TO REWORK DBMANAGER CLASS TO HANDLE CHARACTER GRAB

    def change_screen(self, new_size):
        """ sets the screen size to a new size
        :tuple new_size: new screen size (int x, int y)
        :return: None
        """
        self.screen_size = new_size

    def handle_event(self, event):
        """ main event handler for all key, mouse interactions 
        :object event: event type
        return: None
        """
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                print('w')
        return False