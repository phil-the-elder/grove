import pygame
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
    def __init__(self, id: int, map_id: int, location: list, size: tuple, value: int, name: str, icon: str, inv_icon: str, inventoried: bool = False):
        self.id = id
        self.map_id = map_id
        self.location = location
        self.size = size
        self.value = value
        self.name = name
        self.icon = pygame.image.load(icon)
        self.inv_icon = pygame.image.load(inv_icon)
        self.inventoried = inventoried


class Tool(Item):
    """ Sub class for a Tool
    :int source_id: the type of source that the tool can manipulate
    :return: None
    """
    def __init__(self, id, map_id, location, size, value, name, icon, inventoried, source_id: int):
        super().__init__(id, map_id, location, size, value, name, icon, inventoried)
        self.source_id = source_id

class Weapon(Item):
    """ Sub class for a Weapon
    :int modifier: the amount added to stats when this weapon is equipped
    :return: None
    """
    def __init__(self, id, map_id, location, size, value, name, icon, inventoried, modifier: int):
        super().__init__(id, map_id, location, size, value, name, icon, inventoried)
        self.modifier = modifier

class Armor(Item):
    """ Sub class for a Armor
    :int modifier: the amount added to stats when this armor is equipped
    :return: None
    """
    def __init__(self, id, map_id, location, size, value, name, icon, inventoried, modifier: int):
        super().__init__(id, map_id, location, size, value, name, icon, inventoried)
        self.modifier = modifier

class Potion(Item):
    """ Sub class for a Potion
    :int modifier: the amount added to stats when this Potion is used
    :return: None
    """
    def __init__(self, id, map_id, location, size, value, name, icon, inventoried, modifier: int):
        super().__init__(id, map_id, location, size, value, name, icon, inventoried)
        self.modifier = modifier

class Source(Item):
    """ Sub class for a Source item
    :int child_resource: the resource gathered from this source (e.g. fish, stone)
    :int stage: current stage of resource (e.g. seed, young, ready)
    :int regen_days: the amount of time it takes for this resource to fully regenerate
    :int harvest_time: the amount of time it takes to harvest this resource
    :return: None
    """
    def __init__(self, id, map_id, location, size, value, name, icon, inventoried, child_resource: int, stage: int, regen_days: int, harvest_time: int):
        super().__init__(id, map_id, location, size, value, name, icon, inventoried)
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
    def __init__(self, id, map_id, location, size, value, name, icon, inventoried, parent_source: int, is_ingredient: bool):
        super().__init__(id, map_id, location, size, value, name, icon, inventoried)
        self.parent_source = parent_source
        self.is_ingredient = is_ingredient