
class Item:
    """ Parent class for all items.
    :int id: item ID
    :tuple location: current position (int x, int y)
    :tuple size: size of icon in pixels (int width, int height)
    :bool inventoried: whether item is currently in inventory
    :int value: value of item
    :str name: item name
    :str icon: filepath to graphic for item
    :return: None
    """
    def __init__(self, id: int, location: tuple, size: tuple, value: int, name: str, icon: str, inventoried: bool = False):
        self.id = id
        self.location = location
        self.size = size
        self.value = value
        self.name = name
        self.icon = icon
        self.inventoried = inventoried


class Tool(Item):
    """ Sub class for a Tool
    :int source_id: the type of source that the tool can manipulate
    :return: None
    """
    def __init__(self, source_id: int):
        self.source_id = source_id

class Weapon(Item):
    """ Sub class for a Weapon
    :int modifier: the amount added to stats when this weapon is equipped
    :return: None
    """
    def __init__(self, modifier: int):
        self.modifier = modifier

class Armor(Item):
    """ Sub class for a Armor
    :int modifier: the amount added to stats when this armor is equipped
    :return: None
    """
    def __init__(self, modifier: int):
        self.modifier = modifier

class Potion(Item):
    """ Sub class for a Potion
    :int modifier: the amount added to stats when this Potion is used
    :return: None
    """
    def __init__(self, modifier: int):
        self.modifier = modifier

class Source(Item):
    """ Sub class for a Source item
    :int child_resource: the resource gathered from this source (e.g. fish, stone)
    :int stage: current stage of resource (e.g. seed, young, ready)
    :int regen_days: the amount of time it takes for this resource to fully regenerate
    :int harvest_time: the amount of time it takes to harvest this resource
    :return: None
    """
    def __init__(self, child_resource: int, stage: int, regen_days: int, harvest_time: int):
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
    def __init__(self, parent_source: int, is_ingredient: bool):
        self.parent_source = parent_source
        self.is_ingredient = is_ingredient