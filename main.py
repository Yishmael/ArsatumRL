import os
import signal
import sys
import time

from inputhandler import InputHandler
from utils import HEIGHT, WIDTH
from world import World


def signal_handler(signum, frame):
    exit(0)

os.system('cls')
title = 'Arsatum v0.0.1'
os.system(f'title {title}')

world = World(WIDTH, HEIGHT)
world.init()

# print(f'''Welcome to {title}''')
# input('Press [enter] to start.')

InputHandler(world).start()

world.update(False)
signal.signal(signal.SIGINT, signal_handler)
time.sleep(99999)
