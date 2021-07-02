import pygame
import os
from . import Creature, DBManager, Item, Map

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
        self.map = self.load_map()

    def load_map(self):
        return Map.Map(self.directory, os.path.join(self.directory, 'Resources/map.png'), [0, 0])

    
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
        for event in pygame.event.get():
            does_clear_queue = self.handle_event(event)
            if does_clear_queue:
              pygame.event.clear()
        blockers = self.map.items + self.map.blocks
        if self.pc.moveup or self.pc.movedown or self.pc.moveleft or self.pc.moveright:
            index_rate = self.fps // len(self.pc.icons['move_right']) * int(1/self.pc.speed * 2)
            self.pc.icon_index += 1
            if self.pc.icon_index // index_rate == len(self.pc.icons['move_right']):
                self.pc.icon_index = 0
        if self.pc.moveup:
            if not self.pc.check_surroundings(blockers, 1, 0, True):
                if self.pc.location[1] > self.screen_size[1] / 2 - 32 and self.pc.location[1] >= 0:
                    self.pc.location[1] -= self.pc.speed
                elif self.map.location[1] <= 0:
                    self.map.move(1, self.pc.speed)
                elif self.pc.location[1] >= 0:
                    self.pc.location[1] -= self.pc.speed
            self.pc.direction = 'N'
            self.pc.icon = self.pc.icons['move_up'][self.pc.icon_index // index_rate]
        if self.pc.movedown:
            if not self.pc.check_surroundings(blockers, 1, 0, False):
                if self.pc.location[1] < self.screen_size[1] / 2 - 32 and self.pc.location[1] <= self.screen_size[1]-64:
                    self.pc.location[1] += self.pc.speed
                elif self.map.location[1] >= self.screen_size[1] - self.map.dimensions[1]:
                    self.map.move(1, 0 - self.pc.speed)
                elif self.pc.location[1] <= self.screen_size[1]-64:
                    self.pc.location[1] += self.pc.speed
            self.pc.direction = 'S'
            self.pc.icon = self.pc.icons['move_down'][self.pc.icon_index // index_rate]
        if self.pc.moveleft:
            if not self.pc.check_surroundings(blockers, 0, 1, True):
                if self.pc.location[0] > self.screen_size[0] / 2 - 32 and self.pc.location[0] >= 0:
                    self.pc.location[0] -= self.pc.speed
                elif self.map.location[0] <= 0:
                    self.map.move(0, self.pc.speed)
                elif self.pc.location[0] >= 0:
                    self.pc.location[0] -= self.pc.speed
            self.pc.direction = 'W'
            self.pc.icon = self.pc.icons['move_left'][self.pc.icon_index // index_rate]
        if self.pc.moveright:
            if not self.pc.check_surroundings(blockers, 0, 1, False):
                if self.pc.location[0] < self.screen_size[0] / 2 - 32 and self.pc.location[0] <= self.screen_size[0]-64:
                    self.pc.location[0] += self.pc.speed
                elif self.map.location[0] >= self.screen_size[0] - self.map.dimensions[0]:
                    self.map.move(0, 0 - self.pc.speed)
                elif self.pc.location[0] <= self.screen_size[0]-64:
                    self.pc.location[0] += self.pc.speed
            self.pc.direction = 'E'
            self.pc.icon = self.pc.icons['move_right'][self.pc.icon_index // index_rate]
        # self.screen.fill((0, 0, 0)) 
        self.screen.blit(self.map.image, tuple(self.map.location)) 
        self.screen.blit(self.pc.icon, tuple(self.pc.location))
        for item in self.map.items:
            self.screen.blit(item.icon, tuple(item.location))
        if self.dialog:
            self.dialog_img = pygame.transform.smoothscale(self.dialog_img, (self.screen_size[0] - 100, self.screen_size[1] // 4))
            self.screen.blit(self.dialog_img, (50, int(self.screen_size[1] * 0.75 - 50)))
        pygame.display.update()


    def load_character(self):
        # db_conn = DBManager.DBManager(os.path.join(self.directory, 'Database/main.db'))
        # main_char = db_conn.get_first_row('MainPC')
        # INCOMPLETE - HAVE TO REWORK DBMANAGER CLASS TO HANDLE CHARACTER GRAB
        main_char_icons = {
            'default': pygame.image.load(os.path.join(self.directory, 'Resources/D2.png')),
            'move_left': [pygame.image.load(os.path.join(self.directory, 'Resources/L1.png')),pygame.image.load(os.path.join(self.directory, 'Resources/L2.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/L3.png')),pygame.image.load(os.path.join(self.directory, 'Resources/L2.png'))],
            'move_right': [pygame.image.load(os.path.join(self.directory, 'Resources/R1.png')),pygame.image.load(os.path.join(self.directory, 'Resources/R2.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/R3.png')),pygame.image.load(os.path.join(self.directory, 'Resources/R2.png'))],
            'move_up': [pygame.image.load(os.path.join(self.directory, 'Resources/U1.png')),pygame.image.load(os.path.join(self.directory, 'Resources/U2.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/U3.png')),pygame.image.load(os.path.join(self.directory, 'Resources/U2.png'))],
            'move_down': [pygame.image.load(os.path.join(self.directory, 'Resources/D1.png')),pygame.image.load(os.path.join(self.directory, 'Resources/D2.png')),
            pygame.image.load(os.path.join(self.directory, 'Resources/D3.png')),pygame.image.load(os.path.join(self.directory, 'Resources/D2.png'))]
        }
        center_position = [self.screen_size[0] / 2 -32, self.screen_size[1] / 2 - 32]
        main_char = Creature.MainPC(self.directory, 1, center_position, (64, 64), 0.2, 'flips', main_char_icons, False, 1, 1, 1, 1, 10, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, [])
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
                self.check_interact(self.pc.location, self.pc.direction)
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # left click
                self.check_interact(self.pc.location, self.pc.direction, pygame.mouse.get_pos())
            if event.button == 3:
                # right click
                self.check_interact(self.pc.location, self.pc.direction, pygame.mouse.get_pos())
            if event.button == 4:
                # scroll up
                self.check_interact(self.pc.location, self.pc.direction, pygame.mouse.get_pos())
            if event.button == 5:
                # scroll down
                self.check_interact(self.pc.location, self.pc.direction, pygame.mouse.get_pos())
        return False

    def check_interact(self, location: list, direction: str, mouse_loc: tuple = (0, 0)):
        interaction_points = self.map.creatures + self.map.items
        if direction == 'N':
            interact_obj = self.pc.check_surroundings(interaction_points, 1, 0, True)
        elif direction == 'S':
            interact_obj = self.pc.check_surroundings(interaction_points, 1, 0, False)
        elif direction == 'E':
            interact_obj = self.pc.check_surroundings(interaction_points, 0, 1, False)
        elif direction == 'W':
            interact_obj = self.pc.check_surroundings(interaction_points, 0, 1, True)
        if not interact_obj:
            self.open_dialog('Hmmm... nothing to see here...')
        else:
            self.pc.interact(self, interact_obj)




    def open_dialog(self, text: str):
        self.dialog = True if not self.dialog else False
        print(text)
