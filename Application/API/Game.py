import pygame
import os
import operator

from pygame.constants import RESIZABLE
from . import Creature, DBManager, Item, Map

class Game:
    """ Parent class for the main Game configurations
    :tuple screen_size (input): initial screen size (int x, int y)
    :object screen: main game screen
    :bool running: whether the game is running
    :str name (input): name
    :object pc: main character
    :bool dialog: whether the dialog box is displayed
    :object dialog_img: pygame rendered dialog box image
    :bool inventory: whether the inventory box is displayed
    :object inventory_img: pygame rendered inventory image
    :str directory (input): game directory
    :str corner_icon (input): filepath for corner icon 
    :int fps (input): game framerate
    """
    def __init__(self, screen_size: tuple, name: str, directory: str, corner_icon: str, fps: int):
        self.dbconn = DBManager.DBManager(os.path.join(directory, 'Database/main.db'))
        self.screen_size = screen_size
        self.directory = directory
        self.screen = pygame.display.set_mode(screen_size, RESIZABLE)
        self.running = True
        self.start_game(name, os.path.join(directory, corner_icon))
        self.pc = self.load_character()
        self.dialog = False
        self.dialog_img = pygame.image.load(os.path.join(directory, 'Resources/dialog.png'))
        self.inventory = False
        self.inventory_img = pygame.image.load(os.path.join(directory, 'Resources/inventory.png'))
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.map = self.load_map(1)
        self.npc_move_count = 0

    def load_map(self, id: int):
        """ Loads the Map class with the defined map image at the defined coordinates
        :string directory: filepath to 
        :string map: filepath to the map image
        :list coordinates: x/y coordinates of the top left corner of rendered map
        :string type: type of map
        :tuple pc_start: the pc's starting location for that map
        :return: None
        """
        db_row = self.dbconn.get_row_by_id('Maps', id)
        coords = [int(db_row[3].split(', ')[0]), int(db_row[3].split(', ')[1])]
        pc_start = [int(db_row[5].split(', ')[0]), int(db_row[5].split(', ')[1])]
        self.screen.fill((0, 0, 0))
        map = Map.Map(self.dbconn, db_row[0], db_row[1], self.directory, db_row[2], coords, db_row[4], pc_start)
        if map.dimensions[0] < self.screen_size[0]:
            map.location[0] = (self.screen_size[0] / 2) - (map.dimensions[0] / 2)
        if map.dimensions[1] < self.screen_size[1]:
            map.location[1] = (self.screen_size[1] / 2) - (map.dimensions[1] / 2)
        self.pc.location = map.pc_start
        return map

    
    def start_game(self, name: str, corner_icon: str):
        """ starts the game 
        :str name: name for corner of window
        :str corner_icon: filepath to the corner icon file
        :return: None
        """
        pygame.init()
        pygame.display.set_caption(name)
        icon = pygame.image.load(corner_icon)
        pygame.display.set_icon(icon)

    def movement_handler(self, blockers: list, char_limit: float, char_relate, map_limit: float, map_relate, pos_index: int, range_index: int, direction: str, speed: float, index_rate: int, add_dimensions: bool):
        """ Handles the main movement mechanic for the PC
        :list blockers: list of unpassable rectangular objects
        :float char_limit: the limit the pc can move in a certain direction (usually the game screen boundary)
        :operator char_relate: whether the position comparison is greater or less than
        :float map_limit: the map boundary of a certain direction
        :operator map_relateL whether the map comparison is greater or less than
        :int pos_index: whether the character position being changed is the X or Y
        :int range_index: whether the pc's x or y coordinate is compared with the blockers
        :str direction: whether the PC is heading N, S, E, or W
        :float speed: the pc's speed
        :index_rate: the rate of sprite image swapping for the pc (equation: fps / number of animation sprites * (1 / speed * 2))
        :bool add_dimensions: whether to add the size of the blocker to its coordinate (i.e. if approaching from the south or east)
        :return: None
        """
        interact_obj = self.pc.check_surroundings(blockers, pos_index, range_index, add_dimensions)
        if type(interact_obj) == Map.Portal:
            self.map = self.load_map(interact_obj.get_map())
        elif not interact_obj:
            if char_relate(self.pc.location[pos_index], self.screen_size[pos_index] / 2 - 32) and char_relate(self.pc.location[pos_index], char_limit):
                self.pc.location[pos_index] += speed
            elif map_relate(self.map.location[pos_index], map_limit):
                self.map.move(pos_index, 0 - speed)
            elif char_relate(self.pc.location[pos_index], char_limit):
                self.pc.location[pos_index] += speed
        self.pc.direction = direction
        self.pc.icon = self.pc.icons[direction][self.pc.icon_index // index_rate]

    def get_index_rate(self, icons, speed):
        return self.fps // len(icons) * int(1/speed * 2)

    def update_display(self):
        ''' Main function to update the map display
        :return: None        
        '''
        self.clock.tick(self.fps)
        if self.npc_move_count > self.fps * 3:
            self.npc_move_count = 0
        # iterate through all user-defined events to see if the event queue needs to be cleared
        for event in pygame.event.get():
            does_clear_queue = self.handle_event(event)
            if does_clear_queue:
              pygame.event.clear()
        # get all current map blocker locations. If the pc is moving, calculate index rate and pass functions to movement handler
        if self.pc.moveup or self.pc.movedown or self.pc.moveleft or self.pc.moveright:
            blockers = self.map.items + self.map.blocks + self.map.creatures + self.map.portals
            index_rate = self.get_index_rate(self.pc.icons['E'], self.pc.speed)
            self.pc.icon_index += 1
            if self.pc.icon_index // index_rate == len(self.pc.icons['E']):
                self.pc.icon_index = 0
        if self.pc.moveup:
            self.movement_handler(blockers, -0.1, operator.gt, 0, operator.le, 1, 0, 'N', 0 - self.pc.speed, index_rate, True)
        if self.pc.movedown:
            self.movement_handler(blockers, min(self.screen_size[1] - self.pc.size[1] - 10, self.map.dimensions[1] - self.pc.size[1] - 10), operator.lt, self.screen_size[1] - self.map.dimensions[1], operator.ge, 1, 0, 'S', self.pc.speed, index_rate, False)
        if self.pc.moveleft:
            self.movement_handler(blockers, -0.1, operator.gt, 0, operator.le, 0, 1, 'W', 0 - self.pc.speed, index_rate, True)
        if self.pc.moveright:
            self.movement_handler(blockers, min(self.screen_size[0] - self.pc.size[1] - 1, self.map.dimensions[0] - self.pc.size[0] - 1), operator.lt, self.screen_size[0] - self.map.dimensions[0], operator.ge, 0, 1, 'E', self.pc.speed, index_rate, False)
        # blit the map, pc location, items, and if necessary the dialog box or inventory
        self.screen.blit(self.map.image, tuple(self.map.location)) 
        self.screen.blit(self.pc.icon, tuple(self.pc.location))
        for item in self.map.items:
            self.screen.blit(item.icon, tuple(item.location))
        for creature in self.map.creatures:
            npc_index_rate = self.get_index_rate(creature.icons['E'], creature.speed)
            creature.action(self.fps, self.npc_move_count, npc_index_rate, self.pc)
            self.screen.blit(creature.icon, tuple(creature.location))
        if self.dialog:
            self.dialog_img = pygame.transform.smoothscale(self.dialog_img, (self.screen_size[0] - 100, self.screen_size[1] // 4))
            self.screen.blit(self.dialog_img, (50, int(self.screen_size[1] * 0.75 - 50)))
        if self.inventory:
            self.inventory_img = pygame.transform.smoothscale(self.inventory_img, (self.screen_size[0] - 100, self.screen_size[1] // 2))
            self.screen.blit(self.inventory_img, (50, int(self.screen_size[1] * 0.5 - 50)))
            inv_x = 80
            inv_y = int(self.screen_size[1] * 0.5 - 20)
            for item in self.pc.inventory:
                self.screen.blit(item.inv_icon, (inv_x, inv_y))
                inv_x += self.inventory_img.get_width() / 9
        self.npc_move_count += 1
        pygame.display.update()


    def load_character(self):
        ''' Loads the PC on game initialization (TODO: load from database)
        :return: None        
        '''
        # TODO: get inventory from db
        c = self.dbconn.get_first_row('PC')
        # coords = [int(c[2].split(', ')[0]), int(c[2].split(', ')[1])]
        coords = [self.screen_size[0] / 2 -32, self.screen_size[1] / 2 - 32]
        size = (int(c[3].split(', ')[0]), int(c[3].split(', ')[1]))
        speed = float(c[4])
        actions = c[6].split(', ') if c[6] else []
        pc = Creature.MainPC(self.directory, c[0], c[1], coords, size, speed, c[5], actions, c[7], 
                                c[8], c[9], c[10], c[11], c[12], c[13], c[14], c[15], c[16], c[17], c[18], c[19], c[20], c[21], c[22], c[23], c[24], c[25], [])
        return pc

    def change_screen(self, new_size):
        """ sets the screen size to a new size
        :tuple new_size: new screen size (int x, int y)
        :return: None
        """
        self.screen_size = new_size
        self.load_map(self.map.image_str, self.map.location, self.map.type, self.map.pc_start)
        self.screen.blit(self.map.image, tuple(self.map.location))

    def handle_event(self, event):
        """ main event handler for all key, mouse interactions 
        :object event: event type
        return: None
        """
        if event.type == pygame.VIDEORESIZE:
            self.change_screen((event.w, event.h))
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
                self.check_interact(self.pc.direction)
                return True
            if event.key == pygame.K_m:
                self.map = self.load_map('Resources/map_2.png', [0, 0], 'dynamic', [50, 200])
            if event.key == pygame.K_q:
                self.open_inventory()
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
                self.check_interact(self.pc.direction, pygame.mouse.get_pos())
            if event.button == 3:
                # right click
                self.check_interact(self.pc.direction, pygame.mouse.get_pos())
            if event.button == 4:
                # scroll up
                self.check_interact(self.pc.direction, pygame.mouse.get_pos())
            if event.button == 5:
                # scroll down
                self.check_interact(self.pc.direction, pygame.mouse.get_pos())
        return False

    def check_interact(self, direction: str, mouse_loc: tuple = (0, 0)):
        ''' Check the surrounding on Interact request to find item, to interact with
        :str direction: direction the player is facing (N, S, E, W)
        :tuple mouse_loc (optional): location of the mouse on OnClick
        :return: None        
        '''
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


    def open_inventory(self):
        ''' Toggles the inventory screen
        :return: None        
        '''
        self.inventory = True if not self.inventory else False

    def open_dialog(self, text: str):
        ''' Toggles the dialog screen
        :str text: text to display on the dialog screen
        :return: None        
        '''
        self.pc.movedown = False
        self.pc.moveleft = False
        self.pc.moveup = False
        self.pc.moveright = False
        self.pc.is_talking = not self.pc.is_talking
        self.dialog = True if not self.dialog else False
        print(text)
