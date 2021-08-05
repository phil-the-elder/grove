'''
Name: Data_Loader.py
Purpose: to be an input-based database populator wizard for all data types
Author: Phil Elder
Creation Date: 20210802
'''

import sys
import os
helper_path = f'{os.path.dirname(os.path.dirname(__file__))}/Application'
sys.path.insert(1, f'{helper_path}/API')
from DBManager import DBManager

print("\n\nOH HI WELCOME TO THE DATA LOADING WIZARD MY NAME IS NONE OF YOUR FUCKING BUSINESS WHAT WILL WE BE LOADING TODAY?\n")
data_type = input("Block [B], Portal [P], Creature [C], Item [I], Item Type [IT], Map [M]: ").lower()

if data_type in ['creature', 'c']:
    print("\nFUCK YOU REILLY I DIDN'T REALIZE YOU'D BE ADDING YOUR MOM TO THIS GAME TELL HER SHE CAN COMPETE AT MY GYM ANYTIME SHE WANTS\n")
    # 1. Common traits
    type = input("Monster [M] or NPC [N]: ")
    name = input("Name: ")
    mapid = input("Map ID: ")
    location = input("Location (format: x, y): ")
    bounds = input("Bounds (format: xmin, xmax, ymin, ymax): ")
    size = input("Size (format: x, y): ")
    speed = input("Speed: ")
    range = input("Range (format: movestart, actionstart): ")
    inventory = input("Inventory items (format: itemid1, itemid2): ")
    actions = input("Available Actions (format: action1, action2): ")
    # 2. Monster-specific traits
    if type.lower() in ['m', 'monster']:
        strength = input("Strength: ")
        dexterity = input("Dexterity: ")
        accuracy = input("Accuracy: ")
        intelligence = input("Intelligence: ")
        currhp = input("Current HP: ")
        maxhp = input("Max HP: ")
        melee = input("Melee Skill: ")
        ranged = input("Ranged Skill: ")
        magic = input("Magic Skill: ")
        difficulty = input("Difficulty Rating: ")
        headequip = input("Head Equipped Item (by item id): ")
        bodyequip = input("Body Equipped Item (by item id): ")
        meleeequip = input("Melee Equipped Item (by item id): ")
        rangedequip = input("Ranged Equipped item (by item id): ")
        magicequip = input("Magic Equipped Item (by item id): ")
        table = 'Monsters'
        creature_type = 'M'
        row = [mapid, location, bounds, range, size, speed, name, strength, accuracy, intelligence, dexterity, currhp, maxhp, melee, ranged,
                magic, headequip, bodyequip, meleeequip, rangedequip, magicequip, difficulty, actions]
    else:
        table = 'NPCs'
        creature_type = 'N'
        row = [mapid, location, size, speed, name, bounds, range, 0, actions]

elif data_type in ['block', 'b']:
    print("\nFUCK YOU JONESEY I'M SURPRISED YOU KNOW HOW TO SPELL BLOCK AFTER YOUR STAT LINE THIS SEASON GIVE YOUR BALLS A TUG\n")
    location = input("Coordinates of top left corner (format: x, y): ")
    size = input("Size (format: x, y): ")
    mapid = input("Map ID: ")
    row = [location, size, mapid]
    table = 'Blocks'

elif data_type in ['portal', 'p']:
    print("\nFUCK YOU REILLY TELL YOUR MOM SHE HAS TO STOP CALLING MY DICK THE PORTAL GUN OR WE'RE GOING TO HEAR FROM THE VALVE LEGAL TEAM\n")
    location = input("Coordinates of top left corner (format: x, y): ")
    size = input("Size (format: x, y): ")
    mapid = input("Origin Map ID: ")
    destmapid  = input("Destination Map ID: ")
    row = [location, size, mapid, destmapid]
    table = 'Portals'

elif data_type in ['item', 'i']:
    print("\nFUCK YOU JONESEY I ENTERED MY ITEM INTO YOUR MOM'S DATABASE LAST WEEK AND IT CORRUPTED HER ENTIRE BACKEND\n")
    location = input("Coordinates of top left corner (format: x, y): ")
    size = input("Size (format: x, y): ")
    mapid = input("Origin Map ID: ")
    name = input("Name: ")
    type  = input("Type (ID): ")
    row = [mapid, location, size, 0, name, type]
    table = 'Items'

elif data_type in ['item type', 'it']:
    print("\nFUCK YOU REILLY YOU PROBABLY THING SEX IS A LEGENDARY ITEM TYPE BECAUSE YOU'VE NEVER SEEN IT OFFERED IN GAMEPLAY\n")
    name = input("Name: ")
    description  = input("Description: ")
    rarity = input("Rarity (common, uncommon, rare, legendary): ")
    value = input("Value: ")
    row = [name, description, rarity, value]
    table = 'ItemTypes'

elif data_type in ['map', 'm']:
    print("\nFUCK YOU JONESEY I COULDN'T MAP YOUR WAY TO A PERSONALITY WITH A COMPASS AND A TEAM OF SEASONED ARCTIC EXPLORERS YOU'RE A FUCKING TRAGEDY\n")
    gameid = input("Game ID (if testing, just put 1): ")
    image = input("Name of Image File: ")
    coordinates = input("Coordinates of top left corner (format: x, y): ")
    type  = input("Type (static, dynamic, sidescroll): ")
    pcstart = input("Starting Coordinates for top left corner of PC (x, y): ")
    row = [gameid, image, coordinates, type, pcstart]
    table = 'Maps'



# 3. Database loading logic
try:
    conn = DBManager(f'{helper_path}/Database/main.db')
    new_id = conn.get_next_id(table)
    row.insert(0, new_id)
    row = tuple(row)
    result_id = conn.insert_row(table, row)
    if data_type in ['creature', 'c']:
        for i in inventory.split(', '):
            conn.insert_row('ItemInventory', (result_id, creature_type, i))
    input(f'THAT WORKED YOUR NEW ITEM ID IS {result_id} NOW HIT ENTER YOUR WIZARD COMMANDS YOU')
except Exception as e:
    input(f"I FUCKING KNEW YOU'D DROP THE SHOT THIS IS WHAT HAPPENED: {e}. DO BETTER NEXT TIME.")






