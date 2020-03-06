from .pane import Pane
from item import Item
from utils import WIDTH

class AchievementsPane(Pane):
    def __init__(self, world):
        Pane.__init__(self, 0, 0)
        self.world = world
        self.achievements = {'deaths witnessed': [0, 200]}
        self.shown = False

    def recv_key(self, key):
        if key == 'n':
            self.shown = False

    # drawing
    def apply_on(self, display):
        super().apply_on(display)
        left = self.x + 2

        title = 'Achievements'
        display[1][left:left+len(title)] = list(title)

        for idx, (name, (curr, goal)) in enumerate(self.achievements.items()):
            if curr == 0:
                continue
            text = f'{name}:' + f'{curr}/{goal}'
            display[2+idx][left:left+len(text)] = list(text)

        text = 'Press [esc] to close.'
        display[self.h-2][left:left+len(text)] = list(text)

    @property
    def deaths(self):
        return self.achievements['deaths witnessed'][0]

    @deaths.setter
    def deaths(self, value):
        self.achievements['deaths witnessed'][0] = value