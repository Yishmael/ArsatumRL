import os
import sys
import json
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import clear
if __name__ == '__main__':
    from snailgen import SnailGen
    from towngen import TownGen
    from blankgen import BlankGen
    from staircase import Staircase
else:
    from generators.snailgen import SnailGen
    from generators.towngen import TownGen
    from generators.blankgen import BlankGen
    from generators.staircase import Staircase

class WorldGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snail = SnailGen(self.width, self.height)
        self.town = TownGen(self.width, self.height)
        self.blank = BlankGen(self.width, self.height)
        
    def _generate_zones(self, zone_count):
        # TODO pass list of generators instead of just the count
        self.zones = []
        for i in range(zone_count):
            if i == 0:
                # self.snail.generate(i)
                self.town.generate(i)
                zone = self.town.zone
            else:
                self.snail.generate()
                zone = self.snail.zone
            zone.id = i
            zone.temperature = 5 - 10*i
            zone.init()
            self.zones.append(zone)
            
    def _connect_zones(self, graph):
        # print(self.zones)
        for idx, zone in enumerate(self.zones):
            adj_ids = [int(a) for a in graph[str(zone.id)]]
            print(zone.id, adj_ids)
            for adj_id in adj_ids:
                # find stairs leading to the adj zone
                for sc in zone.staircases:
                    if sc.zone_id2 == adj_id:
                        break
                else:
                    # no stairs linking current zone to adj zone
                    # create such a link
                    recommendations = zone.recommended_stairs_coords
                    if len(recommendations) > 0:
                        x, y = recommendations[0]
                    else:
                        x, y = zone.id*2 + random.randint(5, 20), 5
                    
                    sc = Staircase(x, y, zone.id)
                    print('current:', sc)
                    zone.staircases.append(sc)
                    # find back leading staircase
                    for adj_sc in self.zones[adj_id].staircases:
                        # print('updating', adj_sc)
                        if adj_sc.zone_id2 == None:
                            adj_sc.x2 = sc.x1
                            adj_sc.y2 = sc.y1
                            adj_sc.zone_id2 = sc.zone_id1
                            print('updated adj sc', adj_sc)
                            break
                    else: # adj starcase not found
                        # create adj staircase
                        recommendations = self.zones[adj_id].recommended_stairs_coords
                        # TODO do this directly from the zone, without checking if set is empty
                        # TODO make it random, but don't allow the same recommendation 
                        # to be used more than once
                        if len(recommendations) > 1:
                            x, y = recommendations[1]
                        else:
                            x, y = adj_id*2 + random.randint(5, 20), 8
                        adj_sc = Staircase(x, y, adj_id, sc.x1, sc.y1, sc.zone_id1)

                        self.zones[adj_id].staircases.append(adj_sc)
                        print('created new sc for adjecent', adj_sc)
                    # join them
                    sc.x2 = adj_sc.x1
                    sc.y2 = adj_sc.y1
                    sc.zone_id2 = adj_sc.zone_id1

    def generate_world(self):
        path = 'graph.json'
        if __name__ != '__main__':
            path = 'generators/' + path
        with open(path) as f:
            graph = json.load(f)
        # print(json.dumps(graph, indent=2))
        zone_count = len(graph)
        self._generate_zones(zone_count)
        self._connect_zones(graph)
        # print()

WIDTH, HEIGHT = 65, 12
if __name__ == '__main__':
    clear()
    worldgen = WorldGenerator(WIDTH, HEIGHT)
    worldgen.generate_world()
    print()
    for zone_id, zone in enumerate(worldgen.zones):
        # print(zone_id)
        # print(zone.staircases)
        zone.print(0); print()
        pass
else:
    # disabling printing if just importing
    print = lambda *x: None
