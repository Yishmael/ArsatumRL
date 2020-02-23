import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import clear
if __name__ == '__main__':
    from snailgen import SnailGen
    from towngen import TownGen
    from staircase import Staircase
else:
    from generators.snailgen import SnailGen
    from generators.towngen import TownGen
    from generators.staircase import Staircase

class WorldGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snail = SnailGen(self.width, self.height)
        self.town = TownGen(self.width, self.height)
    def _connect_zones(self):
        pass
    def generate_world(self):
        path = 'graph.json'
        if __name__ != '__main__':
            path = 'generators/' + path
        with open(path) as f:
            graph = json.load(f)
        print(json.dumps(graph, indent=2))

        # creating n zones
        zone_count = len(graph)
        zones = []
        for i in range(zone_count):
            self.snail.generate((0, 0), (3*i, 3))
            zone = self.snail.zone
            zone.id = i
            zones.append(zone)
        print(zones)
        for zone in zones:
            print(zone.id, graph[str(zone.id)])
            for adjec_id in graph[str(zone.id)]:
                adjec_id = int(adjec_id)
                print(adjec_id)
                sc = Staircase(0, 0, zone.id, 0, 0, adjec_id)



        return
        self.town.generate((11, 5))
        zone = self.town.zone
        # print('\n'.join([''.join(row) for row in zone.grid]))
        self.zones = [zone]
        max_depth = 3
        for depth in range(1, max_depth + 1):
            zone_id = len(self.zones)
            up = (0, 0)
            down = (5, zone_id+2)
            if depth == 1:
                up = (25, 1)
                down = (28, 4)
            elif depth == 2:
                up = (58, 2)
                down = (52, 3)
            elif depth == 3:
                up = (55, 6)
                down = (6, 5)

            self.snail.generate(down, up)
            zone = self.snail.zone
            stairs_prev = self.zones[-1].get_staircases_coords()[0]
            stairs_current = zone.get_staircases_coords()[0]
            sc = Staircase(stairs_prev[1], stairs_prev[2], zone_id-1,
                           stairs_current[1], stairs_current[2], zone_id)
            self.zones[-1].staircases.append(sc)
            self.zones[-1].grid[stairs_prev[2]][stairs_prev[1]] = '>'
            zone.staircases.append(Staircase.get_reversed(sc))
            zone.grid[stairs_current[2]][stairs_current[1]] = '<'
            self.zones.append(zone)

WIDTH, HEIGHT = 65, 12
if __name__ == '__main__':
    clear()
    worldgen = WorldGenerator(WIDTH, HEIGHT)
    worldgen.generate_world()
    for zone_id, zone in enumerate(worldgen.zones):
        print(zone_id)
        print(zone.staircases)
        # zone.print(0)
        print()
