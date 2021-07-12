import pygame
import random
from . import Map, Item

class Creature:
    """ Parent class for all NPCs and monsters, as well as the main character.
    :str path: filepath to the main game folder
    :list location: current location (int x, int y)
    :tuple size: size of icon in pixels (int width, int height)
    :int speed: speed rating for creature
    :str name: creature name
    :str icon: filepath to graphic for creature
    :return: None
    """
    def __init__(self, path: str, id: int, location: list, size: tuple, speed: int, name: str, icons: dict):
        self.path = path
        self.id = id
        self.location = location
        self.size = size
        self.speed = speed
        self.name = name
        self.icons = icons
        self.icon = icons['default']
        self.icon_index = 0
        self.is_talking = False
        self.moveup = False
        self.movedown = False
        self.moveleft = False
        self.moveright = False

    def move(self, direction: str, ismoving: bool):
        """ moves the creature given a cardinal direction.
        :str direction: direction to move creature (N, S, E, W)
        :bool ismoving: whether the movement starts or stops in that direction
        :return: None
        """
        if not self.is_talking:
            if direction == 'N':
                self.moveup = ismoving
            elif direction == 'W':
                self.moveleft = ismoving
            elif direction == 'S':
                self.movedown = ismoving
            elif direction == 'E':
                self.moveright = ismoving
        

    def use_tool(self, id: int):
        """ Uses a tool defined by the id. If the user is not within range of a Source that the tool can manipulate, returns
        an error dialog
        :int id: item ID
        :return: None
        """
        return id

    def exchange(self, is_pc: bool):
        """ Starts the exchange (buy/sell) action. If the creature is the PC, adds things to inventory.
        :bool is_pc: second creature's id
        :return: None
        """
        return is_pc

    def sleep(self, is_pc: bool):
        """ Starts the sleep action. If the creature is the PC, returns HP to max.
        :bool is_pc: second creature's id
        :return: None
        """
        return is_pc

class NPC(Creature):
    """ Sub class for all NPCs
    :list bounds: box bounds of creature movement on map (int xmin, int xmax, int ymin, int ymax)
    :list move_range: the 
    :bool wants_to_talk: whether the creature has something to say to PC (red ! if so?)
    :bool is_talking: whether the creature is interacting
    """
    def __init__(self, path: str, id: int, location: list, size: tuple, speed: int, name: str, icons: dict, bounds: list, move_range: list, wants_to_talk: bool):
        super().__init__(path, id, location, size, speed, name, icons)
        self.bounds = bounds
        self.move_range = move_range
        self.wants_to_talk = wants_to_talk

    def action(self, fps, count, index_rate, pc):
        # self.pc.icon = self.pc.icons[direction][self.pc.icon_index // index_rate]
        if not self.is_talking:
            if count == self.move_range[0]:
                str_directions = []
                max_distance = self.speed * fps * (abs(self.move_range[1] - self.move_range[0]) / fps)
                if self.location[0] > self.bounds[0] + max_distance:
                    str_directions.append('W')
                if self.location[0] < self.bounds[1] - max_distance:
                    str_directions.append('E')
                if self.location[1] > self.bounds[2] + max_distance:
                    str_directions.append('N')
                if self.location[1] < self.bounds[3] - max_distance:
                    str_directions.append('S')
                if len(str_directions) > 0:
                    index = random.randint(0, len(str_directions) - 1)
                    direction = str_directions[index]
                    if direction == 'W':
                        self.moveleft = True
                    elif direction == 'E':
                        self.moveright = True
                    elif direction == 'N':
                        self.moveup = True
                    elif direction == 'S':
                        self.movedown = True
                else:
                    direction = 'action'
            elif self.move_range[0] < count <= self.move_range[1]:
                if self.moveup:
                    if abs(self.location[1] - pc.location[1] - pc.size[1]) > 2:
                        self.location[1] -= self.speed
                    direction = 'N'
                elif self.movedown:
                    if abs(self.location[1] + self.size[1] - pc.location[1]) > 2:
                        self.location[1] += self.speed
                    direction = 'S'
                elif self.moveleft:
                    if abs(self.location[0] - pc.location[0] - pc.size[0]) > 2:
                        self.location[0] -= self.speed
                    direction = 'W'
                elif self.moveright:
                    if abs(self.location[0] + self.size[0] - pc.location[0]) > 2:
                        self.location[0] += self.speed
                    direction = 'E'
                else:
                    direction = 'action'
            else:
                direction = 'action'
                self.moveup = False
                self.movedown = False
                self.moveright = False
                self.moveleft = False
            self.icon_index += 1
            if self.icon_index // index_rate == len(self.icons['E']):
                self.icon_index = 0
            self.icon = self.icons[direction][self.icon_index // index_rate]
            

class MainPC(Creature):
    """ Sub class for the main character
    :str direction: player's current direction
    :int strength: player's current strength rating
    :int accuracy: player's current accuracy rating
    :int intelligence: player's current intelligence rating
    :int dexterity: player's current dexterity rating
    :int currHP: player's current HP
    :int maxHP: player's maximum HP
    :int melee: player's current melee attack rating
    :int ranged: player's current ranged attack rating
    :int magic: player's current magic attack rating
    :int farming: player's current farming ability rating
    :int trading: player's current trading ability rating
    :int fishing: player's current fishing ability rating
    :int handling: player's current animal handling ability rating
    :int alchemy: player's current alchemy ability rating
    :int head_equip: id for equipment currently equipped to head (from inventory)
    :int body_equip: id for equipment currently equipped to body (from inventory)
    :int melee_equip: id for equipment currently equipped as melee attack item (from inventory)
    :int ranged_equip: id for equipment currently equipped as ranged attack item (from inventory)
    :int spell_equip: id for equipment currently equipped as spell attack item (from inventory)
    :list inventory: list of integer ids for items in player inventory
    :return: None
    """
    def __init__(self, path, id, location, size, speed, name, icons, strength: int, accuracy: int, intelligence: int, dexterity: int, currHP: int, maxHP: int, melee: int, ranged: int,
                    magic: int, farming: int, trading: int, fishing: int, handling: int, head_equip: int, body_equip: int, melee_equip: int,
                    ranged_equip: int, spell_equip: int, inventory: list):
        super().__init__(path, id, location, size, speed, name, icons)
        self.strength = strength
        self.accuracy = accuracy
        self.intelligence = intelligence
        self.dexterity = dexterity
        self.currHP = currHP
        self.maxHP = maxHP
        self.melee = melee
        self.ranged = ranged
        self.magic = magic
        self.farming = farming
        self.trading = trading
        self.fishing = fishing
        self.handling = handling
        self.head_equip = head_equip
        self.body_equip = body_equip
        self.melee_equip = melee_equip
        self.ranged_equip = ranged_equip
        self.spell_equip = spell_equip
        self.inventory = inventory
        self.direction = 'S'

    def interact(self, game, thing):
        """ Opens up an interaction window with a second object.
        :thing: thing to interact with
        :return: None
        """
        if isinstance(thing, Item.Item):
            game.map.items.remove(thing)
            self.inventory.append(thing)
        elif isinstance(thing, NPC):
            if not thing.moveleft and not thing.moveright and not thing.moveup and not thing.movedown:
                self.is_talking = not self.is_talking
                game.open_dialog(thing.name)
                if not thing.is_talking:
                    thing.is_talking = True
                    if self.direction == 'N':
                        thing.icon = thing.icons['S'][0]
                    elif self.direction == 'S':
                        thing.icon = thing.icons['N'][0]
                    elif self.direction == 'E':
                        thing.icon = thing.icons['W'][0]
                    elif self.direction == 'W':
                        thing.icon = thing.icons['E'][0]
                else:
                    thing.is_talking = False

    def check_surroundings(self, blockers: list, pos_index: int, range_index: int, add_dimensions: bool):
        ''' Checks surroundings for blockers or items
        :list blockers: all blockers currently on map
        :int pos_index: the axis to be checked for blockers (x or y)
        :int range_index: the axis to be checked to indicate whether pc is in the range of a blocker (x or y)
        :bool add_dimensions: whether the size along an axis is to be added to its coordinate (i.e. if approached from the south or east)
        :return: None        
        '''
        for b in blockers:
            is_collision = False
            if b.size[range_index] > self.size[range_index]:
                if b.location[range_index] < self.location[range_index] < b.location[range_index] + b.size[range_index] or b.location[range_index] < self.location[range_index] + self.size[range_index] < b.location[range_index] + b.size[range_index]:
                    is_collision = True
            else:
                if self.location[range_index] < b.location[range_index] < self.location[range_index] + self.size[range_index] or self.location[range_index] < b.location[range_index] + b.size[range_index] < self.location[range_index] + self.size[range_index]:
                    is_collision = True
            if is_collision:
                if add_dimensions:
                    curr_pos = self.location[pos_index]
                    wall = b.location[pos_index] + b.size[pos_index]
                else:
                    curr_pos = self.location[pos_index] + self.size[pos_index]
                    wall = b.location[pos_index]
                if abs(curr_pos - wall) < 2:
                    return b
        return False



    def inspect(self, id: int):
        """ Opens an inspection dialog box with item id.
        :int id: id of item being inspected
        :return: None
        """
        return id

    def attack_melee(self, id: int, alias: list):
        """uses second creature ID and outcome alias to determine melee attack outcome.
        :int id: second creature's id
        :list alias: alias object (3-array matrix) controlling result probabilities
        :return: outcome
        """
        return id, alias

    def attack_ranged(self, id: int, alias: list):
        """uses second creature ID and outcome alias to determine ranged attack outcome.
        :int id: second creature's id
        :list alias: alias object (3-array matrix) controlling result probabilities
        :return: outcome
        """
        return id, alias

    def attack_magic(self, id: int, alias: list):
        """uses second creature ID and outcome alias to determine magic attack outcome.
        :int id: second creature's id
        :list alias: alias object (3-array matrix) controlling result probabilities
        :return: outcome
        """
        return id, alias

    def open_inventory(self):
        """ Opens the inventory dialog box.
        :return: None
        """
        return

    def add_to_inventory(self, id: int):
        """ Adds an item to player's inventory given item ID.
        :int id: item ID
        :return: None
        """
        return id

    def equip_item(self, id: int):
        """ Equips an item given the item ID
        :int id: item ID
        :return: None
        """
        return id

class Monster(NPC):
    """ Sub class for monster/hostile creatures
    :int strength: player's current strength rating
    :int accuracy: player's current accuracy rating
    :int intelligence: player's current intelligence rating
    :int dexterity: player's current dexterity rating
    :int currHP: player's current HP
    :int maxHP: player's maximum HP
    :int melee: player's current melee attack rating
    :int ranged: player's current ranged attack rating
    :int magic: player's current magic attack rating
    :int head_equip: id for equipment currently equipped to head (from inventory)
    :int body_equip: id for equipment currently equipped to body (from inventory)
    :int melee_equip: id for equipment currently equipped as melee attack item (from inventory)
    :int ranged_equip: id for equipment currently equipped as ranged attack item (from inventory)
    :int spell_equip: id for equipment currently equipped as spell attack item (from inventory)
    :int difficulty_rating: difficulty rating for the monster (controls loot, affects combat)
    :return: None
    """
    def __init__(self, path, id, location, size, speed, name, icons, wantstotalk, strength: int, accuracy: int, intelligence: int, dexterity: int, currHP: int, maxHP: int, melee: int, ranged: int,
                    magic: int, head_equip: int, body_equip: int, melee_equip: int,
                    ranged_equip: int, spell_equip: int, difficulty_rating: int):
        super().__init__(path, id, location, size, speed, name, icons, wantstotalk)
        self.strength = strength
        self.accuracy = accuracy
        self.intelligence = intelligence
        self.dexterity = dexterity
        self.currHP = currHP
        self.maxHP = maxHP
        self.melee = melee
        self.ranged = ranged
        self.magic = magic
        self.head_equip = head_equip
        self.body_equip = body_equip
        self.melee_equip = melee_equip
        self.ranged_equip = ranged_equip
        self.spell_equip = spell_equip
        self.difficulty_rating = difficulty_rating

    def attack_melee(self, id: int, alias: list):
        """uses second creature ID and outcome alias to determine melee attack outcome.
        :int id: second creature's id
        :list alias: alias object (3-array matrix) controlling result probabilities
        :return: outcome
        """
        return id, alias

    def attack_ranged(self, id: int, alias: list):
        """uses second creature ID and outcome alias to determine ranged attack outcome.
        :int id: second creature's id
        :list alias: alias object (3-array matrix) controlling result probabilities
        :return: outcome
        """
        return id, alias

    def attack_magic(self, id: int, alias: list):
        """uses second creature ID and outcome alias to determine magic attack outcome.
        :int id: second creature's id
        :list alias: alias object (3-array matrix) controlling result probabilities
        :return: outcome
        """
        return id, alias