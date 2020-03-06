import os
import random
import sys
import time

from experimental.console import Console
from generators.worldgenerator import WorldGenerator
from gui.journal import Journal
from gui.log import Log
from gui.shop import Shop
from item import Item
from objects import Creature
from utils import Vision, clear
from gui.achievements import AchievementsPane

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
        self.achiev_pane = AchievementsPane(self)
        self.show_achiev_pane = False
        self.log = Log()
        self.turn_count = 0
        self.ground_items = []

    def init(self):
        worldgen = WorldGenerator(self.width, self.height)
        worldgen.generate_world()
        self.zones = worldgen.zones
        self.zone_id = 0
        self.zone = self.zones[self.zone_id]
        self.player = Creature(self.zone, 'You', 15, 5, 
                [Item(i) for i in ['green potion', 'water potion', 'scroll of alchemy']])
        self.zone.units.append(self.player)
        self.display = list(list(row) for row in self.zone.get_grid())
        self.vision = Vision(self.display)

    def tick(self):
        self.zone.tick()
        for u in list(self.zone.units):
            if not u.dead:
                u.tick()
            else:
                if u.icon == '@':
                    self.zone.add_message('You die.')
                else:
                    self.zone.add_message(f'{u} dies.')
                self.achiev_pane.deaths += 1
                u.destroyed = True
         
        self.zone.cleanup()
        self.ground_items = self.zone.get_items_in_range(self.player.x, self.player.y, 0)

    def draw(self):
        for idx, row in enumerate(self.zone.get_grid()):
            self.display[idx] = list(row)

        #self.display = list(list(row) for row in self.zone.get_grid())
        for i in self.zone.items:
            if i.icon:
                self.display[i.y][i.x] = i.icon
        for s in self.zone.staircases:
            self.display[s.y1][s.x1] = s.get_icon(s.zone_id1)
        for u in self.zone.units:
            if u.icon:
                self.display[u.y][u.x] = u.icon
        
        self.vision.reset()
        self.vision.add_source((self.player.x, self.player.y), self.player.vision_distance)
        for unit in self.zone.units:
            # vision.add_source((unit.x, unit.y), 1)
            # vision.add_source((unit.x, unit.y), unit.vision_distance)
            if unit.icon == 'r':
                self.vision.add_line(unit, self.player)
        self.vision.apply()

        self.apply_pane()

        #curses
        if self.console:
            self.console.update_display(self.display)
        else:
            print('\n'.join(''.join(row) for row in self.display))
        # with open('display.txt', 'w') as f:
        #     f.write('\n'.join(''.join(row) for row in self.display))

        if self.player.has_just_moved():
            staircase = self.zone.get_staircase_at(self.player.x, self.player.y)
            if staircase:
                if staircase.get_icon(self.zone_id) == '>':
                    self.log.add_message(f'You see stairs leading down.')
                else:
                    self.log.add_message(f'You see stairs leading up.')
            if self.ground_items:
                self.log.add_message(f'You see {self.ground_items} at your feet.')

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
            self.set_zone_id(zone_id+1)
            self.player.x, self.player.y = 0, 0


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
        elif self.achiev_pane.shown:
            self.achiev_pane.apply_on(self.display)
