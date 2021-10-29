import pygame
import os
from . import Item, Creature

class Block:
    def __init__(self, id: int, location: tuple, size: tuple):
        self.id = id
        self.location = location
        self.size = size

class Portal:
    def __init__(self, map_id: int, location: tuple, size: tuple, dest_id: int):
        self.map_id = map_id
        self.location = location
        self.size = size
        self.dest_id = dest_id

    def get_map(self):
        return self.dest_id

class Map:
    """ Parent class for the game map
    :obj dbconn (input): main game db connection object
    :int game_id (input): the game the map is attached to
    :str directory (input): the game directory
    :str image (input): the filepath for the main map image
    :list location (input): the render coordinates for the map
    :str type (input): the type of map (static, dynamic, sidescroll)
    :list pc_start (input): the coordinates for the pc's starting position
    :list dimensions: the width and height of the map
    :list items: all items to be rendered on the map
    :list blocks: all impassable areas on the map
    :list creatures: all creatures to be rendered on the map
    """
    def __init__(self, dbconn, id: int, game_id: int, directory: str, image: str, location: list, type: str, pc_start: list):
        self.dbconn = dbconn
        self.id = id
        self.game_id = game_id
        self.directory = directory
        self.image_str = image
        self.image = pygame.image.load(os.path.join(self.directory, f'Resources/{image}')).convert()
        self.location = location
        self.type = type
        self.pc_start = pc_start
        self.dimensions = [self.image.get_width(), self.image.get_height()]
        self.items = self.load_items()
        self.blocks = self.load_blocks()
        self.creatures = self.load_creatures()
        self.portals = self.load_portals()

    def load_creatures(self):
        ''' load all creatures on the map
        :return: list creatures
        '''
        creature_list = self.dbconn.get_associated_items('NPCs', 'MapID', self.id)
        formatted_list = []
        for c in creature_list:
            coords = [int(c[2].split(', ')[0]), int(c[2].split(', ')[1])]
            size = (int(c[3].split(', ')[0]), int(c[3].split(', ')[1]))
            speed = float(c[4])
            bounds = [int(c[6].split(', ')[0]), int(c[6].split(', ')[1]), int(c[6].split(', ')[2]), int(c[6].split(', ')[3])]
            move_range = [int(c[7].split(', ')[0]), int(c[7].split(', ')[1])]
            actions = c[9].split(', ')
            talk = False if c[8] == 0 else True
            creature = Creature.NPC(self.directory, c[0], c[1], coords, size, speed, c[5], actions, bounds, move_range, talk)
            formatted_list.append(creature)
        return formatted_list

    def load_items(self):
        ''' load all items on the map
        :return: list items
        '''
        item_list = self.dbconn.get_associated_items('Items', 'MapID', self.id)
        formatted_list = []
        for i in item_list:
            item_type = self.dbconn.get_row_by_id('ItemTypes', i[6])
            coords = [int(i[2].split(', ')[0]), int(i[2].split(', ')[1])]
            size = (int(i[3].split(', ')[0]), int(i[3].split(', ')[1]))
            inv = False if i[4] == 0 else True
            item = Item.Item(i[0], self.directory, i[1], coords, size, i[5], item_type[1], item_type[2], item_type[3], item_type[4], inv)
            if not inv:
                formatted_list.append(item)
        return formatted_list


    def load_blocks(self):
        ''' load all blocks on the map
        :return: list blocks
        '''
        block_list = self.dbconn.get_associated_items('Blocks', 'MapID', self.id)
        formatted_list = []
        for b in block_list:
            coords = [int(b[2].split(', ')[0]), int(b[2].split(', ')[1])]
            size = (int(b[3].split(', ')[0]), int(b[3].split(', ')[1]))
            formatted_list.append(Block(b[0], coords, size))
        return formatted_list
    
    def load_portals(self):
        portal_list = self.dbconn.get_associated_items('Portals', 'MapID', self.id)
        formatted_list = []
        for p in portal_list:
            coords = [int(p[2].split(', ')[0]), int(p[2].split(', ')[1])]
            size = (int(p[3].split(', ')[0]), int(p[3].split(', ')[1]))
            formatted_list.append(Portal(p[3], coords, size, p[4]))
        return formatted_list

    def move(self, index: int, speed: float):
        ''' move the map on player movement
        :int index: whether the map will be moved along the x or y axis
        :float speed: the speed at which the map will move
        :return: None
        '''
        self.location[index] += speed
        for item in self.items:
            item.location[index] += speed
        for block in self.blocks:
            block.location[index] += speed
        for creature in self.creatures:
            creature.location[index] += speed
            if index == 0:
                creature.bounds[0] += speed
                creature.bounds[1] += speed
            elif index == 1:
                creature.bounds[2] += speed
                creature.bounds[3] += speed
        