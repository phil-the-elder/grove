import pygame
import os
import operator
import time

from pygame.constants import RESIZABLE
from . import Creature, DBManager, Item, Map

class Game:
    """ Parent class for the main Game configurations
    :int id: game ID
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
    def __init__(self, id, screen_size: tuple, name: str, directory: str, corner_icon: str, fps: int):
        self.id = id
        self.dbconn = DBManager.DBManager(os.path.join(directory, 'Database/main.db'))
        self.screen_size = screen_size
        self.directory = directory
        self.screen = pygame.display.set_mode(screen_size, RESIZABLE)
        self.running = True
        self.start_game(name, os.path.join(directory, corner_icon))
        self.pc = self.load_character(self.id) if self.id != 0 else None
        self.dialog = False
        self.dialog_img = pygame.image.load(os.path.join(directory, 'Resources/dialog.png')).convert()
        self.inventory = False
        self.inventory_img = pygame.image.load(os.path.join(directory, 'Resources/inventory.png')).convert()
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.maps = self.load_all_maps()
        self.map = self.load_map(self.id, True)
        self.npc_move_count = 0

        self.veil_alpha = 0
        self.veil = pygame.Surface((self.screen_size[0], self.screen_size[1]))
        self.veil.fill((0, 0, 0))
        self.veil.set_alpha(self.veil_alpha)
        self.fade_out = False
        self.fade_in = False
        self.transition_map = None

    def load_all_maps(self):
        """ Loads and processes all maps associated with the game, given the Game ID
        :return: list of object Maps
        """
        return_array = []
        db_maps = self.dbconn.get_associated_items('Maps', 'GameID', self.id)
        for m in db_maps:
            coords = [float(m[3].split(', ')[0]), float(m[3].split(', ')[1])]
            pc_start = [int(m[5].split(', ')[0]), int(m[5].split(', ')[1])]
            map = Map.Map(self.dbconn, m[0], m[1], self.directory, m[2], coords, m[4], pc_start)
            if map.dimensions[0] < self.screen_size[0]:
                map.location[0] = (self.screen_size[0] / 2) - (map.dimensions[0] / 2)
            if map.dimensions[1] < self.screen_size[1]:
                map.location[1] = (self.screen_size[1] / 2) - (map.dimensions[1] / 2)
            return_array.append(map)
        return return_array


    def load_map(self, id: int, is_init = False):
        """ Loads the Map class with the game ID (loads default map) or map ID
        :int id: game ID if is_init else map ID
        :bool is_init: Is initial map (true if loading game, false if loading map)(optional: default False)
        :return: object Map
        """
        if is_init:
            possible_maps = self.dbconn.get_associated_items('Maps', 'GameID', id)
            for map in possible_maps:
                if map[6] == 1:
                    map_id = map[0]
        else:
            map_id = id
        for map in self.maps:
            if map.id == map_id:
                self.screen.fill((0, 0, 0))
                if self.id != 0:
                    self.pc.location = map.pc_start
                if map.type == 'static':
                    map.location = [(((map.dimensions[0] // 2) - (self.screen_size[0] // 2)) * -1), (((map.dimensions[1] // 2) - (self.screen_size[1] // 2)) * -1)]
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

    def movement_handler(self, blockers: list, char_limit: float, char_relate, map_limit: float, map_relate, pos_index: int, 
                            range_index: int, direction: str, speed: float, index_rate: int, add_dimensions: bool):
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
            self.fade_out = True
            self.transition_map = self.load_map(interact_obj.get_map())
            print(interact_obj.get_map())
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
        # increase or decrease veil alpha if screen is set to fade out
        if self.fade_out:
            self.veil_alpha += 5
            if self.veil_alpha >= 255:
                self.fade_out = False
                self.map = self.transition_map                    
                self.fade_in = True
                self.transition_map = None
        elif self.fade_in:
            self.veil_alpha -= 5
            if self.veil_alpha <= 0:
                self.fade_in = False 


        self.clock.tick(self.fps)
        if self.npc_move_count > self.fps * 3:
            self.npc_move_count = 0
        # iterate through all user-defined events to see if the event queue needs to be cleared
        for event in pygame.event.get():
            does_clear_queue = self.handle_event(event)
            if does_clear_queue:
              pygame.event.clear()

        # get all current map blocker locations. If the pc is moving, calculate index rate and pass functions to movement handler
        self.screen.blit(self.map.image, tuple(self.map.location)) 
        if self.id != 0:
            if self.pc.moveup or self.pc.movedown or self.pc.moveleft or self.pc.moveright:
                blockers = self.map.items + self.map.blocks + self.map.creatures + self.map.portals
                index_rate = self.get_index_rate(self.pc.icons['E'], self.pc.speed)
                self.pc.icon_index += 1
                if self.pc.icon_index // index_rate == len(self.pc.icons['E']):
                    self.pc.icon_index = 0
            if self.pc.moveup:
                self.movement_handler(blockers, -0.1, operator.gt, 0, operator.le, 1, 0, 'N', 0 - self.pc.speed, index_rate, True)
            if self.pc.movedown:
                self.movement_handler(blockers, min(self.screen_size[1] - self.pc.size[1] - 10, self.map.dimensions[1] - self.pc.size[1] - 10), 
                                        operator.lt, self.screen_size[1] - self.map.dimensions[1], operator.ge, 1, 0, 'S', self.pc.speed, index_rate, False)
            if self.pc.moveleft:
                self.movement_handler(blockers, -0.1, operator.gt, 0, operator.le, 0, 1, 'W', 0 - self.pc.speed, index_rate, True)
            if self.pc.moveright:
                self.movement_handler(blockers, min(self.screen_size[0] - self.pc.size[1] - 1, self.map.dimensions[0] - self.pc.size[0] - 1), 
                                        operator.lt, self.screen_size[0] - self.map.dimensions[0], operator.ge, 0, 1, 'E', self.pc.speed, index_rate, False)
            if self.transition_map == None:
                self.screen.blit(self.pc.icon, tuple(self.pc.location))
        # blit the map, pc location, items, and if necessary the dialog box or inventory
        
        


        for item in self.map.items:
            item.animate(self.fps, self.npc_move_count)
            if not item.inventoried:
                self.screen.blit(item.icon, tuple(item.location))
            else:
                self.map.items.remove(item)
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
        self.veil.set_alpha(self.veil_alpha)
        self.screen.blit(self.veil, (0, 0))

        pygame.display.update()


    def load_character(self, game_id: int):
        ''' Loads the PC on game initialization
        :return: PC Object        
        '''
        c = self.dbconn.get_row_by_id('PC', game_id)
        coords = [self.screen_size[0] / 2 -32, self.screen_size[1] / 2 - 32]
        size = (int(c[3].split(', ')[0]), int(c[3].split(', ')[1]))
        speed = float(c[4])
        actions = c[6].split(', ') if c[6] else []
        inventory_ids = [s[2] for s in self.dbconn.get_associated_items('ItemInventory', 'CreatureID', c[0])]
        inventory = []
        for id in inventory_ids:
            i = self.dbconn.get_row_by_id('Items', id)
            item_type = self.dbconn.get_row_by_id('ItemTypes', i[6])
            coords = [float(i[2].split(', ')[0]), float(i[2].split(', ')[1])]
            size = (int(i[3].split(', ')[0]), int(i[3].split(', ')[1]))
            inv = False if i[4] == 0 else True
            item = Item.Item(i[0], self.directory, i[1], coords, size, i[5], item_type[1], item_type[2], item_type[3], item_type[4], inv)
            inventory.append(item)
        pc = Creature.MainPC(self.directory, c[0], c[1], coords, size, speed, c[5], actions, c[7],
                                c[8], c[9], c[10], c[11], c[12], c[13], c[14], c[15], c[16], c[17], 
                                c[18], c[19], c[20], c[21], c[22], c[23], c[24], c[25], inventory)
        return pc

    def change_screen(self, new_size):
        """ sets the screen size to a new size
        :tuple new_size: new screen size (int x, int y)
        :return: None
        """
        self.screen_size = new_size
        self.load_map(self.map.id)
        self.screen.blit(self.map.image, tuple(self.map.location))


    def new_game(self):
        """ creates a new game by copying records from the template db and mapping necessary items
        return: bool success
        """
        # try:
        game_count = self.dbconn.get_row_count('Games')
        if game_count > 3:
            self.open_dialog('There are already three saved games! Delete a game to create a new one')
        else:
            new_map_id = self.dbconn.get_next_id('Maps')
            new_game_id = self.dbconn.get_next_game_id()
            self.dbconn.insert_row('Games', [new_game_id])
            template_connection = DBManager.DBManager(os.path.join(self.directory, 'Database/template.db'))
            template_maps = template_connection.get_all_rows('Maps')
            for map in template_maps:
                map = list(map)
                map[1] = new_game_id
                old_id = map[0]
                tables_to_update = ['Items', 'Blocks', 'Monsters', 'NPCs', 'PC', 'Portals']
                for table in tables_to_update:
                    template_rows = template_connection.get_associated_items(table, 'MapID', old_id)
                    if table == 'PC':
                        new_item_id = new_game_id
                    else:
                        new_item_id = self.dbconn.get_next_id(table)
                    for item in template_rows:
                        item = list(item)
                        if table == 'Portals':
                            item[4] = new_map_id + item[4] - item[1]
                        item[0] = new_item_id
                        item[1] = new_map_id
                        self.dbconn.insert_row(table, item)
                        new_item_id += 1
                map[0] = new_map_id
                self.dbconn.insert_row('Maps', map)
                new_map_id += 1  
            self.load_game(new_game_id)
        # except Exception as e:
        #     print(e)
        #     return False

    def save_game(self):
        """ save a game given a game ID
        return: bool success
        """
        # try:
        print(self.id)
        for map in self.maps:
            for item in map.items:
                inventoried = 1 if item.inventoried else 0
                item_dict = {
                    'MapID': item.map_id,
                    'Location': ', '.join([str(i) for i in item.location]),
                    'Inventoried': inventoried
                }
                self.dbconn.update_row('Items', item.id, item_dict)
            for creature in map.creatures:
                c_dict = {
                    'MapID': creature.map_id,
                    'Location': ', '.join([str(c) for c in creature.location]),
                    'Speed': creature.speed
                }
                self.save_creature(creature, 'NPCs', c_dict)
            for monster in map.monsters:
                m_dict = {
                    'MapID': monster.map_id,
                    'Location': ', '.join([str(l) for l in monster.location]),
                    'Speed': monster.speed,
                    'HeadEquip': monster.head_equip,
                    'BodyEquip': monster.body_equip,
                    'MeleeEquip': monster.melee_equip,
                    'RangedEquip': monster.ranged_equip,
                    'SpellEquip': monster.spell_equip
                }
                self.save_creature(monster, 'Monsters', m_dict)
        for inventoried_item in self.pc.inventory:
            inventory_dict = {
                'MapID': 99999,
                'Inventoried': 1
            }
            self.dbconn.update_row('Items', inventoried_item.id, inventory_dict)
        p = self.pc
        p_dict = {
            'Size': ', '.join([str(p) for p in p.size]),
            'Speed': p.speed,
            'Name': p.name,
            'Strength': p.strength,
            'Accuracy': p.accuracy,
            'Intelligence': p.intelligence,
            'Dexterity': p.dexterity,
            'CurrHP': p.currHP,
            'MaxHP': p.maxHP,
            'Melee': p.melee,
            'Ranged': p.ranged,
            'Magic': p.magic,
            'Farming': p.farming,
            'Trading': p.trading,
            'Fishing': p.fishing,
            'Handling': p.handling,
            'Alchemy': p.alchemy,
            'HeadEquip': p.head_equip,
            'BodyEquip': p.body_equip,
            'MeleeEquip': p.melee_equip,
            'RangedEquip': p.ranged_equip,
            'SpellEquip': p.spell_equip
        }
        self.save_creature(p, 'PC', p_dict)
        print('wwwwooooootst34k')
        return True
        # except Exception as e:
        #     print(e)
        #     return False

    def save_creature(self, creature_obj, table, row):
        """ sub-function of save_game for saving PC, NPCs and monsters
        :obj creature: Creature object to save
        :str table: table name to save to
        :dict row: dictionary containing fields, values to update for the row
        return: bool success
        """
        db_inventory_ids = [s[2] for s in self.dbconn.get_associated_items('ItemInventory', 'CreatureID', creature_obj.id)]
        pc_inventory_ids = [s.id for s in creature_obj.inventory]
        rows_to_delete = []
        for i in db_inventory_ids:
            if i not in pc_inventory_ids:
                rows_to_delete.append(i)
        self.dbconn.delete_rows('ItemInventory', rows_to_delete, 'ItemID')
        for p in pc_inventory_ids:
            if p not in db_inventory_ids:
                self.dbconn.insert_row('ItemInventory', [creature_obj.id, 'P', p])
        self.dbconn.update_row(table, creature_obj.id, row)

    def load_game(self, id):
        """ loads a game given a game ID
        :int id: game ID
        return: bool success
        """
        # try:
        self.pc = self.load_character(id)
        self.id = id
        self.dialog = False
        self.inventory = False
        self.clock = pygame.time.Clock()
        self.maps = self.load_all_maps()
        self.fade_out = True
        self.transition_map = self.load_map(self.id, True)
        self.npc_move_count = 0
        return True
        # except Exception as e:
        #     print(e)
        #     return False

    def delete_game(self, id):
        """ deletes a game, associated maps, and all associated items and creatures given an id
        :int id: game ID
        return: bool success
        """
        print(id)
        # try:
        associated_maps = self.dbconn.get_associated_items('Maps', 'GameID', id)
        for map in associated_maps:
            tables_to_delete = ['Items', 'Blocks', 'Monsters', 'NPCs', 'PC', 'Portals']
            for table in tables_to_delete:
                rows_to_delete = [r[0] for r in self.dbconn.get_associated_items(table, 'MapID', map[0])]
                self.dbconn.delete_rows(table, rows_to_delete)
                if table == 'PC' and len(rows_to_delete) > 0:
                    pc_id = rows_to_delete[0]
                    self.dbconn.delete_rows('ItemInventory', [pc_id], 'CreatureID')
            self.dbconn.delete_rows('Maps', [map[0]])
        self.dbconn.delete_rows('Games', [id])
        print('it worked!')
        return True
        # except Exception as e:
        #     print(e)
        #     return False


    def handle_event(self, event):
        """ main event handler for all key, mouse interactions 
        :object event: event type
        return: None
        """
        if event.type == pygame.VIDEORESIZE:
            self.change_screen((event.w, event.h))
        if event.type == pygame.QUIT:
            self.running = False
        if self.id == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # left click
                    self.check_interact('X', pygame.mouse.get_pos())
        else:
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
                if event.key == pygame.K_q:
                    self.open_inventory()
                    return True
                if event.key == pygame.K_1:
                    self.new_game()
                if event.key == pygame.K_2:
                    self.save_game()
                if event.key == pygame.K_3:
                    self.load_game(3 if self.id == 1 else 1)
                if event.key == pygame.K_4:
                    self.delete_game(4)
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
        if direction == 'X':
            self.check_menu(mouse_loc)
        else:
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
                thing = self.pc.interact(self, interact_obj)
                if not isinstance(interact_obj, Item.Item):
                    self.pc.is_talking = not self.pc.is_talking
    
    def check_menu(self, loc):
        ''' Check the event against a map menu and fire the appropriate function
        :tuple mouse_loc: location of the mouse on OnClick
        :return: None        
        '''
        adjusted_location = (((self.map.dimensions[0] // 2) - (self.screen_size[0] // 2)), ((self.map.dimensions[1] // 2) - (self.screen_size[1] // 2)))
        for p in self.map.portals:
            if p.location[0] < loc[0] + adjusted_location[0] < p.location[0] + p.size[0] and p.location[1] < loc[1] + adjusted_location[1] < p.location[1] + p.size[1]:
                if str(p.dest_id)[:5] == '44444':
                    self.delete_game(int(str(p.dest_id)[-1]))
                elif p.dest_id == 55555:
                    self.new_game()
                elif str(p.dest_id)[:5] == '66666':
                    self.load_game(int(str(p.dest_id)[-1]))
                else:
                    self.fade_out = True
                    self.transition_map = self.load_map(p.get_map())
                


    def open_inventory(self):
        ''' Toggles the inventory screen
        :return: None        
        '''
        self.inventory = not self.inventory

    def open_dialog(self, text: str):
        ''' Toggles the dialog screen
        :str text: text to display on the dialog screen
        :return: None        
        '''
        if self.id != 0:
            self.pc.movedown = False
            self.pc.moveleft = False
            self.pc.moveup = False
            self.pc.moveright = False
            self.pc.is_talking = not self.pc.is_talking
        self.dialog = not self.dialog
        print(text)
