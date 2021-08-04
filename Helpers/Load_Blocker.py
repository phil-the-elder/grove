'''
Name: Load_Creatures.py
Purpose: to be an input-based database populator for NPCs and monsters
Author: Phil Elder
Creation Date: 20210802
'''

import sys
import os
helper_path = f'{os.path.dirname(os.path.dirname(__file__))}/Application'
sys.path.insert(1, f'{helper_path}/API')
from DBManager import DBManager

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
            magic, headequip, bodyequip, meleeequip, rangedequip, magicequip, difficulty]
else:
    table = 'NPCs'
    creature_type = 'N'
    row = [mapid, location, size, speed, name, bounds, range, 0]

# 3. Database loading logic
try:
    conn = DBManager(f'{helper_path}/Database/main.db')
    new_id = conn.get_next_id(table)
    row.insert(0, new_id)
    row = tuple(row)
    creature_id = conn.insert_row(table, row)
    for i in inventory.split(', '):
        conn.insert_row('ItemInventory', (creature_id, creature_type, i))
    input(f'Load successful! New creature id is {creature_id}. Press enter to exit.')
except Exception as e:
    input(f'Load failed. Reason: {e}. Try again without sucking as hard!')






