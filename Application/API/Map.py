import pygame
import os
from . import Item, DBManager

class Block:
    def __init__(self, id: int, location: list, size: tuple):
        self.id = id
        self.location = location
        self.size = size

class Map:
    def __init__(self, directory: str, image: str, location: list):
        self.directory = directory
        self.image = pygame.image.load(image)
        self.dimensions = [self.image.get_width(), self.image.get_height()]
        self.location = location
        self.items = self.load_items()
        self.blocks = self.load_blocks()
        self.creatures = self.load_creatures()

    def load_creatures(self):
        return []

    def load_items(self):
        # db_conn = DBManager.DBManager(os.path.join(self.directory, 'Database/main.db'))
        # main_char = db_conn.get_first_row('MainPC')
        # INCOMPLETE - HAVE TO REWORK DBMANAGER CLASS TO HANDLE GETTING ALL ACTIVE ITEMS
        item_list = [Item.Item(1, [1000,1000], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1000,1000], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1100,1000], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1200,1000], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1300,1000], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1400,1000], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1500,1000], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1600,1000], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1700,1000], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1800,1000], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1900,1000], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [2000,1000], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [2100,1000], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [2200,1000], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1000,1100], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1000,1100], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1100,1100], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1200,1100], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1300,1100], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1400,1100], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1500,1100], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1600,1100], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1700,1100], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1800,1100], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [1900,1100], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [2000,1100], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [2100,1100], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png')),
        Item.Item(1, [2200,1100], (24,24), 10, 'trophy', os.path.join(self.directory, 'Resources/trophy.png'))]
        return item_list

    def load_blocks(self):
        # db_conn = DBManager.DBManager(os.path.join(self.directory, 'Database/main.db'))
        # main_char = db_conn.get_first_row('MainPC')
        # INCOMPLETE - HAVE TO REWORK DBMANAGER CLASS TO HANDLE GETTING ALL ACTIVE BLOCKS
        # block_list = [Block([1000,1000], (64,64)),
        # Block([1100,1000], (64,64)),
        # Block([1200,1000], (64,64)),
        # Block([1300,1000], (64,64)),
        # Block([1400,1000], (64,64)),
        # Block([1500,1000], (64,64)),
        # Block([1600,1000], (64,64)),
        # Block([1700,1000], (64,64)),
        # Block([1800,1000], (64,64)),
        # Block([1900,1000], (64,64)),
        # Block([2000,1000], (64,64)),
        # Block([2100,1000], (64,64)),
        # Block([2200,1000], (64,64))
        # ]
        block_list = []
        return block_list

    def move(self, index: int, speed: float):
        self.location[index] += speed
        for item in self.items:
            item.location[index] += speed
        for block in self.blocks:
            block.location[index] += speed
        