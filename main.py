import os
import signal
import sys
import time

from inputhandler import InputHandler
from utils import HEIGHT, WIDTH, clear
from world import World


def signal_handler(signum, frame):
    exit(0)

clear()
title = 'Arsatum v0.0.1'
os.system(f'title {title}')

world = World(WIDTH, HEIGHT)
world.init()

# clear()
# print(f'''Welcome to {title}''')
# print('''-------------------''')
# text = '''
# movement          windows                 actions
# 789 \\|/      i - inventory          p - pick up item
# 4.6 -.-      e - charecter window   space - descend/ascend stairs
# 123 /|\\      l - message log        num 5 - pass turn
#              j - journal
#              n - achievements
# '''.strip()
# print(text)

# input('Press [enter] to start.')

InputHandler(world).start()
world.update(False)
signal.signal(signal.SIGINT, signal_handler)
time.sleep(99999)
