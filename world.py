import os
import sys
import time
import random

from experimental.console import Console
from objects import Creature
from utils import apply_fov, clear
from gui.shop import Shop
from gui.journal import Journal
from gui.log import Log
from item import Item 
from generators.worldgenerator import WorldGenerator

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.console = None
        # self.console = Console()
        self.shop = Shop(self)
        self.show_shop = False
        self.journal = Journal(self)
        self.show_journal = False
        self.log = Log()
        self.display = None
        self.turn_count = 0
        self.ground_items = []

    def init(self):
        worldgen = WorldGenerator(self.width, self.height)
        worldgen.generate_world()
        self.zones = worldgen.zones
        self.zone_id = 0
        self.zone = self.zones[self.zone_id]
        self.player = Creature(self.zone, 'You', 15, 5, 
                [Item(i) for i in ['unlit torch', 'green potion', 'water potion', 'scroll of alchemy']])
        self.zone.units.append(self.player)

    # def spawn(self, name, x, y, zone_id=None, items=[]):
    #     if zone_id is None:
    #         zone_id = self.zone_id
    #     zone = self.zones[zone_id]
    #     zone.units.append(Creature(zone, name, x, y, items))

    def tick(self):
        self.zone.tick()
        for u in list(self.zone.units):
            for item in self.zone.get_items_in_range(u.x, u.y, 0):
                if item.name == 'glass shard':
                    item.affect_unit(u, 'stepped on')
            if not u.dead:
                u.tick()
            else:
                if u.icon == '@':
                    self.zone.add_message('You die.')
                else:
                    self.zone.add_message(f'{u} dies.')
                u.destroyed = True
         
        self.zone.cleanup()
        self.ground_items = self.zone.get_items_in_range(self.player.x, self.player.y, 0)

    def draw(self):
        self.display = list(list(row) for row in self.zone.get_grid())
        for i in self.zone.items:
            if i.icon:
                self.display[i.y][i.x] = i.icon
        for s in self.zone.staircases:
            self.display[s.y1][s.x1] = s.get_icon(s.zone_id1)
        for u in self.zone.units:
            if u.icon:
                self.display[u.y][u.x] = u.icon
        # apply_fov(self.player, self.display, 3)
        self.apply_pane()

        #curses
        if self.console:
            self.console.update_display(self.display)
        else:
            print('\n'.join(''.join(row) for row in self.display))
        # with open('display.txt', 'w') as f:
        #     f.write('\n'.join(''.join(row) for row in self.display))

        if self.ground_items and self.player.has_just_moved():
            self.log.add_message(f'You see {self.ground_items} at your feet.')
        staircase = self.zone.get_staircase_at(self.player.x, self.player.y)
        if staircase:
            if staircase.get_icon(self.zone_id) == '>':
                self.log.add_message(f'You see stairs leading down.')
            else:
                self.log.add_message(f'You see stairs leading up.')

        print(self.log.get_last_message())
        print(', '.join([f'HP:{self.player.hp:.0f}', f'XP:{self.player.exp}', 
                        f'STA:{self.player.stamina:.0f}', f'T:{self.turn_count}',
                        f'WATER:{self.player.water:.0f}', f'FOOD:{self.player.food:.0f}',
                        f'TEMP:{self.player.temperature:.1f}°C',
                        ]))
                
        print(f', '.join(self.player.statuses))

    def set_zone_id(self, index):
        self.zone.units.remove(self.player)
        self.zone_id = index
        self.zone = self.zones[self.zone_id]
        self.player.zone = self.zone
        self.zone.units.append(self.player)

    def change_zone(self):
        for staircase in self.zone.staircases:
            loc = staircase.get_exit_location(self.player.x, self.player.y, self.zone_id)
            if not loc:
                continue
            x, y, zone_id = loc
            if zone_id is not None:
                if zone_id > self.zone_id:
                    self.log.add_message(staircase.get_descend_message())
                else:
                    self.log.add_message(staircase.get_ascend_message())
                self.set_zone_id(zone_id)
                self.player.x, self.player.y = x, y
                self.log.add_message(f'Temperature is {self.zone.temperature}°C.')
                break

    def update(self, advance_turn):
        if advance_turn:
            self.turn_count += 1
        clear()
        if advance_turn:
            self.tick()
        for message in self.zone.get_messages():
            self.log.add_message(message)
        self.draw()
        self.log.hide_last_message()

    def apply_pane(self):
        if self.player.inv.shown:
            self.player.inv.apply_on(self.display)
        elif self.show_shop:
            self.shop.apply_on(self.display)
        elif self.player.char_pane.shown:
            self.player.char_pane.apply_on(self.display)
        elif self.show_journal:
            self.journal.apply_on(self.display)
        elif self.log.shown:
            self.log.apply_on(self.display)