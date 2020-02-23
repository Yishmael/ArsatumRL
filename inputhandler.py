import os
import sys
import signal

import curses
from pynput import keyboard

from utils import get_dir, WIDTH, HEIGHT
from world import World
Key = keyboard.Key

class InputHandler:
    def __init__(self, world):
        self.world = world
        self.listener = keyboard.Listener(
            on_press=self.on_press_mapper,
            on_release=lambda f: None
        )
        
    def on_press_mapper(self, key):
        name = ''
        if type(key) is keyboard._win32.KeyCode:
            name = key.char
        elif type(key) is Key:
            name = key.name
        else:
            raise Exception(f'Unknown key: {key}, type:{type(key)}')
        name = str(name)
        self.on_press(name)

    def on_press(self, key):
        advance_turn = False
        key = key.lower()
        if key == '`':
            locs = []
            locs.append(f'@: ({self.world.player.x}, {self.world.player.y})')
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    icon = self.world.zone.get_tile_at(x, y)
                    if icon not in ['#', '.']:
                        locs.append(f'{icon}: ({x}, {y})')
            self.world.log.add_message(', '.join(locs))
        elif key == 'esc':
            if not (self.world.show_inv or self.world.show_shop or self.world.show_char_pane or \
                    self.world.show_journal or self.world.show_log):
                #curses
                if self.world.console:
                    self.world.console.close()
                os.kill(os.getpid(), signal.SIGINT)
            self.close_all_panes()
        elif self.world.show_inv:
            self.world.player.inv.recv_key(key)
        elif self.world.show_shop:
            self.world.shop.recv_key(key)
        elif self.world.show_char_pane:
            self.world.char_pane.recv_key(key)
        elif self.world.show_journal:
            self.world.journal.recv_key(key)
        elif self.world.show_log:
            self.world.log.recv_key(key)
        elif key in ['home', 'up', 'page_up', 'left', 'right', 'end', 'down', 'page_down']:
            advance_turn = True
            self.world.player.move_delta(get_dir(key)[0], get_dir(key)[1])
        elif key == 'none': # numpad 5
            advance_turn = True
        elif key == 'i':
            self.world.show_inv = True
        elif key == 'p':
            self.world.player.pickup()
        elif key == 'e':
            self.world.show_char_pane = True
        elif key == 'j':
            self.world.show_journal = True
        elif key == 'l':
            self.world.show_log = True
        if key == 'space':
            self.close_all_panes()
            x, y = self.world.player.x, self.world.player.y
            icon = self.world.zone.get_tile_at(x, y)
            if icon in  ['>', '<']:
                self.world.change_zone()
            advance_turn = True

        #self.world.console.set_tile(0, 15, key, 4)

        self.world.update(advance_turn)
  
    def start(self):
        self.listener.start()

    def close_all_panes(self):
        self.world.show_inv = False
        self.world.show_shop = False
        self.world.show_char_pane = False
        self.world.show_journal = False
        self.world.show_log = False