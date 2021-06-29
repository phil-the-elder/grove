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
    :int fps: game framerate
    """
    def __init__(self, screen_size: tuple, name: str, directory: str, corner_icon: str, fps: int):
        self.screen_size = screen_size
        self.directory = directory
        self.screen = pygame.display.set_mode(screen_size)
        self.running = True
        self.start_game(name, os.path.join(directory, corner_icon))
        self.pc = self.load_character()
        self.dialog = False
        self.fps = fps
        pygame.time.Clock().tick(self.fps)
        self.dialog_img = pygame.image.load(os.path.join(directory, 'Resources/dialog.png'))
        self.map_img = pygame.image.load(os.path.join(directory, 'Resources/map.png'))
        self.map_dimensions = [self.map_img.get_width(), self.map_img.get_height()]
        self.map_location = [0, 0]
    
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

    def update_display(self):

        # self.screen.fill((0, 0, 0)) 

        for event in pygame.event.get():
            does_clear_queue = self.handle_event(event)
            if does_clear_queue:
              pygame.event.clear()
        if self.pc.moveup or self.pc.movedown or self.pc.moveleft or self.pc.moveright:
            index_rate = self.fps // len(self.pc.icons['move_right']) * int(1/self.pc.speed * 2)
            self.pc.icon_index += 1
            if self.pc.icon_index // index_rate == len(self.pc.icons['move_right']):
                self.pc.icon_index = 0
        if self.pc.moveup:
            if self.pc.location[1] > self.screen_size[1] / 2 - 32 and self.pc.location[1] >= 0:
                self.pc.location[1] -= self.pc.speed
            elif self.map_location[1] <= 0:
                self.map_location[1] += self.pc.speed
            elif self.pc.location[1] >= 0:
                self.pc.location[1] -= self.pc.speed
            self.pc.direction = 'N'
            self.pc.icon = self.pc.icons['move_up'][self.pc.icon_index // index_rate]
        if self.pc.movedown:
            if self.pc.location[1] < self.screen_size[1] / 2 - 32 and self.pc.location[1] <= self.screen_size[1]-64:
                self.pc.location[1] += self.pc.speed
            elif self.map_location[1] >= self.screen_size[1] - self.map_dimensions[1]:
                self.map_location[1] -= self.pc.speed
            elif self.pc.location[1] <= self.screen_size[1]-64:
                self.pc.location[1] += self.pc.speed
            self.pc.direction = 'S'
            self.pc.icon = self.pc.icons['move_down'][self.pc.icon_index // index_rate]
        if self.pc.moveleft:
            if self.pc.location[0] > self.screen_size[0] / 2 - 32 and self.pc.location[0] >= 0:
                self.pc.location[0] -= self.pc.speed
            elif self.map_location[0] <= 0:
                self.map_location[0] += self.pc.speed
            elif self.pc.location[0] >= 0:
                self.pc.location[0] -= self.pc.speed
            self.pc.direction = 'W'
            self.pc.icon = self.pc.icons['move_left'][self.pc.icon_index // index_rate]
        if self.pc.moveright:
            if self.pc.location[0] < self.screen_size[0] / 2 - 32 and self.pc.location[0] <= self.screen_size[0]-64:
                self.pc.location[0] += self.pc.speed
            elif self.map_location[0] >= self.screen_size[0] - self.map_dimensions[0]:
                self.map_location[0] -= self.pc.speed
            elif self.pc.location[0] <= self.screen_size[0]-64:
                self.pc.location[0] += self.pc.speed
            self.pc.direction = 'E'
            self.pc.icon = self.pc.icons['move_right'][self.pc.icon_index // index_rate]
        if self.dialog:
            self.dialog_img = pygame.transform.smoothscale(self.dialog_img, (self.screen_size[0] - 100, self.screen_size[1] // 4))
            self.screen.blit(self.dialog_img, (50, int(self.screen_size[1] * 0.75 - 50)))
        self.screen.blit(self.map_img, tuple(self.map_location)) 
        self.screen.blit(self.pc.icon, tuple(self.pc.location))
        pygame.display.update()

    def load_character(self):
        # db_conn = DBManager.DBManager(os.path.join(self.directory, 'Database/main.db'))
        # main_char = db_conn.get_first_row('MainPC')
        # INCOMPLETE - HAVE TO REWORK DBMANAGER CLASS TO HANDLE CHARACTER GRAB
        main_char_icons = {
            'default': pygame.image.load(os.path.join(self.directory, 'Resources/standing.png')),
            'move_left': [pygame.image.load(os.path.join(self.directory, 'Resources/L1.png')),pygame.image.load(os.path.join(self.directory, 'Resources/L2.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/L3.png')),pygame.image.load(os.path.join(self.directory, 'Resources/L4.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/L5.png')),pygame.image.load(os.path.join(self.directory, 'Resources/L6.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/L7.png')),pygame.image.load(os.path.join(self.directory, 'Resources/L8.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/L9.png'))],
            'move_right': [pygame.image.load(os.path.join(self.directory, 'Resources/R1.png')),pygame.image.load(os.path.join(self.directory, 'Resources/R2.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/R3.png')),pygame.image.load(os.path.join(self.directory, 'Resources/R4.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/R5.png')),pygame.image.load(os.path.join(self.directory, 'Resources/R6.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/R7.png')),pygame.image.load(os.path.join(self.directory, 'Resources/R8.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/R9.png'))],
            'move_up': [pygame.image.load(os.path.join(self.directory, 'Resources/L1.png')),pygame.image.load(os.path.join(self.directory, 'Resources/L2.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/L3.png')),pygame.image.load(os.path.join(self.directory, 'Resources/L4.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/L5.png')),pygame.image.load(os.path.join(self.directory, 'Resources/L6.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/L7.png')),pygame.image.load(os.path.join(self.directory, 'Resources/L8.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/L9.png'))],
            'move_down': [pygame.image.load(os.path.join(self.directory, 'Resources/R1.png')),pygame.image.load(os.path.join(self.directory, 'Resources/R2.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/R3.png')),pygame.image.load(os.path.join(self.directory, 'Resources/R4.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/R5.png')),pygame.image.load(os.path.join(self.directory, 'Resources/R6.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/R7.png')),pygame.image.load(os.path.join(self.directory, 'Resources/R8.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/R9.png'))]
        }
        center_position = [self.screen_size[0] / 2 -32, self.screen_size[1] / 2 - 32]
        main_char = Creature.MainPC(self.directory, 1, center_position, 32, 0.2, 'flips', main_char_icons, False, 1, 1, 1, 1, 10, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, [])
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
                self.pc.move('N', True)
            if event.key == pygame.K_a:
                self.pc.move('W', True)
            if event.key == pygame.K_s:
                self.pc.move('S', True)
            if event.key == pygame.K_d:
                self.pc.move('E', True)
            if event.key == pygame.K_e:
                self.open_dialog(self.pc.location, self.pc.direction)
                return True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.pc.move('N', False)
            if event.key == pygame.K_a:
                self.pc.move('W', False)
            if event.key == pygame.K_s:
                self.pc.move('S', False)
            if event.key == pygame.K_d:
                self.pc.move('E', False)

        return False

    def open_dialog(self, location, direction):
        self.dialog = True if not self.dialog else False
