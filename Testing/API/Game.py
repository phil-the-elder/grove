import pygame
import os
from . import Creature, DBManager

class Game:
    """ Parent class for the main Game configurations
    :tuple screen_size: initial screen size (int x, int y)
    :object screen: main game screen
    :bool running: whether the game is running
    :str name: name
    :str directory: game directory
    :str corner_icon: filepath for corner icon 
    """
    def __init__(self, screen_size: tuple, name: str, directory: str, corner_icon: str):
        self.screen_size = screen_size
        self.directory = directory
        self.screen = pygame.display.set_mode(screen_size)
        self.running = True
        self.start_game(name, os.path.join(directory, corner_icon))
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
        db_conn = DBManager.DBManager(os.path.join(self.directory, 'Database/main.db'))
        # main_char = db_conn.get_first_row('MainPC')
        # INCOMPLETE - HAVE TO REWORK DBMANAGER CLASS TO HANDLE CHARACTER GRAB
        main_char = Creature.MainPC(self.directory, 1, [200,200], 32, 0.5, 'flips', os.path.join(self.directory, 'Resources/1_E.png'), False, 1, 1, 1, 1, 10, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, [])
        return main_char

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
                self.pc.moveup = True
            if event.key == pygame.K_a:
                self.pc.moveleft = True
            if event.key == pygame.K_s:
                self.pc.movedown = True
            if event.key == pygame.K_d:
                self.pc.moveright = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.pc.moveup = False
            if event.key == pygame.K_a:
                self.pc.moveleft = False
            if event.key == pygame.K_s:
                self.pc.movedown = False
            if event.key == pygame.K_d:
                self.pc.moveright = False

        return False