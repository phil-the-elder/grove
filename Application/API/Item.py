import pygame
import os

class Item:
    """ Parent class for all items.
    :int id: item ID
    :int map_id: id of home map
    :tuple location: current position (int x, int y)
    :tuple size: size of icon in pixels (int width, int height)
    :int value: value of item
    :str name: item name
    :str icon: filepath to graphic for item
    :str inv_icon: filepath to inventory graphic for item
    :bool inventoried: whether the item is inventoried
    :return: None
    """
    def __init__(self, id: int, directory: str, map_id: int, location: list, size: tuple, name: str, type: str, desc: str, rarity: str, value: int, inventoried: bool = False):
        self.id = id
        self.directory = directory
        self.map_id = map_id
        self.location = location
        self.size = size
        self.name = name
        self.type = type
        self.desc = desc
        self.rarity = rarity
        self.value = value
        self.icons = self.load_images()
        self.icon = self.icons[0]
        self.inv_icon = pygame.image.load(os.path.join(self.directory, f'Resources/{name}_inv.png')).convert_alpha()
        self.inventoried = inventoried

    def load_images(self):
        image_arr = [pygame.image.load(os.path.join(self.directory, f'Resources/{self.name}1.png')).convert_alpha(),pygame.image.load(os.path.join(self.directory, f'Resources/{self.name}2.png')).convert_alpha(),
            pygame.image.load(os.path.join(self.directory, f'Resources/{self.name}3.png')).convert_alpha(),pygame.image.load(os.path.join(self.directory, f'Resources/{self.name}2.png')).convert_alpha()]

        return image_arr

    def animate(self, fps, move_count):
        if 0 <= move_count % fps < 15:
            self.icon = self.icons[0]
        elif 15 <= move_count % fps < 30:
            self.icon = self.icons[1]
        elif 30 <= move_count % fps < 45:
            self.icon = self.icons[2]
        else:
            self.icon = self.icons[3]


class Tool(Item):
    """ Sub class for a Tool
    :int source_id: the type of source that the tool can manipulate
    :return: None
    """
    def __init__(self, id, directory, map_id, location, size, name, type, desc, rarity, value, inventoried, source_id: int):
        super().__init__(id, directory, map_id, location, size, name, type, desc, rarity, value, inventoried)
        self.source_id = source_id

class Weapon(Item):
    """ Sub class for a Weapon
    :int modifier: the amount added to stats when this weapon is equipped
    :return: None
    """
    def __init__(self, id, directory, map_id, location, size, name, type, desc, rarity, value, inventoried, modifier: int):
        super().__init__(id, directory, map_id, location, size, name, type, desc, rarity, value, inventoried)
        self.modifier = modifier

class Armor(Item):
    """ Sub class for a Armor
    :int modifier: the amount added to stats when this armor is equipped
    :return: None
    """
    def __init__(self, id, directory, map_id, location, size, name, type, desc, rarity, value, inventoried, modifier: int):
        super().__init__(id, directory, map_id, location, size, name, type, desc, rarity, value, inventoried)
        self.modifier = modifier

class Potion(Item):
    """ Sub class for a Potion
    :int modifier: the amount added to stats when this Potion is used
    :return: None
    """
    def __init__(self, id, directory, map_id, location, size, name, type, desc, rarity, value, inventoried, modifier: int):
        super().__init__(id, directory, map_id, location, size, name, type, desc, rarity, value, inventoried)
        self.modifier = modifier

class Source(Item):
    """ Sub class for a Source item
    :int child_resource: the resource gathered from this source (e.g. fish, stone)
    :int stage: current stage of resource (e.g. seed, young, ready)
    :int regen_days: the amount of time it takes for this resource to fully regenerate
    :int harvest_time: the amount of time it takes to harvest this resource
    :return: None
    """
    def __init__(self, id, directory, map_id, location, size, name, type, desc, rarity, value, inventoried, child_resource: int, stage: int, regen_days: int, harvest_time: int):
        super().__init__(id, directory, map_id, location, size, name, type, desc, rarity, value, inventoried)
        self.child_resource = child_resource
        self.stage = stage
        self.regen_days = regen_days
        self.harvest_time = harvest_time

class Resource(Item):
    """ Sub class for a Resource item
    :int parent_source: the source that provides this resource (e.g. lake, tree)
    :bool is_ingredient: whether the resource is an ingredient for crafting
    :return: None
    """
    def __init__(self, id, directory, map_id, location, size, name, type, desc, rarity, value, inventoried, parent_source: int, is_ingredient: bool):
        super().__init__(id, directory, map_id, location, size, name, type, desc, rarity, value, inventoried)
        self.parent_source = parent_source
        self.is_ingredient = is_ingredient