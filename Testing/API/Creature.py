import pygame

class Creature:
    """ Parent class for all NPCs, monsters, as well as the main character.
    :str path: filepath to the main game folder
    :list location: current position (int x, int y)
    :tuple size: size of icon in pixels (int width, int height)
    :int speed: speed rating for creature
    :str name: creature name
    :str icon: filepath to graphic for creature
    :bool wantstotalk: whether the creature has something to say to PC (red ! if so?)
    :return: None
    """
    def __init__(self, path: str, id: int, location: tuple, size: tuple, speed: int, name: str, icon: str, wantstotalk: bool = False):
        self.path = path
        self.id = id
        self.location = location
        self.size = size
        self.speed = speed
        self.name = name
        self.icon = pygame.image.load(icon)
        self.wantstotalk = wantstotalk
        self.moveup = False
        self.movedown = False
        self.moveleft = False
        self.moveright = False

    def move(self):
        """ moves the creature given a cardinal direction.
        :str direction: direction to move creature (N, S, E, W)
        :return: None
        """

    def interact(self, id: int):
        """ Opens up an interaction window with a id-defined second creature.
        :int id: second creature's id
        :return: None
        """
        return id

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

class MainPC(Creature):
    """ Sub class for the main character
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
    def __init__(self, path, id, location, size, speed, name, icon, wantstotalk, strength: int, accuracy: int, intelligence: int, dexterity: int, currHP: int, maxHP: int, melee: int, ranged: int,
                    magic: int, farming: int, trading: int, fishing: int, handling: int, head_equip: int, body_equip: int, melee_equip: int,
                    ranged_equip: int, spell_equip: int, inventory: list):
        super().__init__(path, id, location, size, speed, name, icon, wantstotalk)
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

class Monster(Creature):
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
    def __init__(self, path, id, location, size, speed, name, icon, wantstotalk, strength: int, accuracy: int, intelligence: int, dexterity: int, currHP: int, maxHP: int, melee: int, ranged: int,
                    magic: int, head_equip: int, body_equip: int, melee_equip: int,
                    ranged_equip: int, spell_equip: int, difficulty_rating: int):
        super().__init__(path, id, location, size, speed, name, icon, wantstotalk)
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