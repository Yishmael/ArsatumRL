import os
import sys
import json
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import clear, WIDTH, HEIGHT
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
        path = 'graph.json'
        if __name__ != '__main__':
            path = 'generators/' + path
        with open(path) as f:
            self.graph = json.load(f)
        # with open(path, 'w') as f:
        #     json.dump(self.graph, f, indent=2)
        self.generators = {'town': TownGen(self.width, self.height),
                           'snail': SnailGen(self.width, self.height),
                           'blank': BlankGen(self.width, self.height)}
        
    def _generate_zones(self):
        self.zones = {}
        for zone_id in self.graph['zones'].keys():
            try:
                gen = self.generators[self.graph['generators'][zone_id]]
            except KeyError:
                raise KeyError(f'Missing generator for zone {zone_id}.')
            gen.generate()
            zone = gen.zone
            zone.id = int(zone_id)
            zone.temperature = 5 - 10*int(zone_id)
            zone.init()
            self.zones[zone.id] = zone
            
    def _connect_zones(self):
        # print(self.zones)
        for idx, zone in enumerate(self.zones.values()):
            adj_ids = [int(a) for a in self.graph['zones'][str(zone.id)]]
            print(zone.id, adj_ids)
            for adj_id in adj_ids:
                # find stairs leading to the adj zone
                for sc in zone.staircases:
                    if sc.zone_id2 == adj_id:
                        break
                else:
                    # no stairs linking current zone to adj zone
                    # create such a link
                    x, y = zone.get_recommended_stairs_coords()                    
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
                        x, y = self.zones[adj_id].get_recommended_stairs_coords()
                        adj_sc = Staircase(x, y, adj_id, sc.x1, sc.y1, sc.zone_id1)
                        print('Connect', adj_sc)

                        self.zones[adj_id].staircases.append(adj_sc)
                        print('created new sc for adjecent', adj_sc)
                    # join them
                    sc.x2 = adj_sc.x1
                    sc.y2 = adj_sc.y1
                    sc.zone_id2 = adj_sc.zone_id1

    def generate_world(self):
        # print(json.dumps(graph, indent=2))
        self._generate_zones()
        self._connect_zones()
        # print()

if __name__ == '__main__':
    clear()
    worldgen = WorldGenerator(WIDTH, HEIGHT)
    worldgen.generate_world()
    print()
    for zone_id, zone in enumerate(worldgen.zones.values()):
        print(zone_id)
        print(zone.staircases)
        zone.print(0); print()
        pass
