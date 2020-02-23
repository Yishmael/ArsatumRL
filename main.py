import os
import signal
import sys
import time

from generators.snailgen import SnailGen
from inputhandler import InputHandler
from item import Item
from objects import Creature
from utils import HEIGHT, WIDTH
from world import World


def signal_handler(signum, frame):
    exit(0)

os.system('cls')
title = 'Arsatum v0.0.1'
os.system(f'title {title}')

world = World(WIDTH, HEIGHT)
world.init()
world.spawn('white rat', 22, 7, 0, [Item(i) for i in ['cotton sweater']])
world.spawn('coyote', 32, 2, 0)
world.spawn('coyote', 33, 2, 0)
world.spawn('coyote', 34, 2, 0)
world.spawn('coyote', 35, 2, 0)
world.place('hearty meal', 12, 4, 0)
world.place('barrel top', 12, 3, 0)
world.place('glass flask', 18, 5, 0)
# world.place(Item('pebble'), 27, 4, 0)

world.place('motivation', 55, 10, 1)

# print(f'''Welcome to {title}''')
# input('Press [enter] to start.')

InputHandler(world).start()

world.update(True)
signal.signal(signal.SIGINT, signal_handler)
time.sleep(99999)
