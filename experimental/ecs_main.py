import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from experimental.components import *
from utils import Vector, get_direction

class Entity:
    def __init__(self, id_):
        self.id_ = id_
        self.comps = []
    def __repr__(self):
        return f'E{self.id_}'
    def add_comp(self, comp):
        for c in self.comps:
            c_name = c.__class__.__name__
            comp_name = comp.__class__.__name__
            if c_name == comp_name:
                raise ValueError(f'Component {c_name} already present.')
        else:
            self.comps.append(comp)

    def get_comp(self, type_):
        for comp in self.comps:
            if type(comp) == type_:
                return comp
        return None

class InputSystem:
    def __init__(self, entities):
        self.entities = entities
    def update(self, key):
        ent = self.entities[0]
        phys = ent.get_comp(TransformComponent)
        inv = ent.get_comp(InventoryComponent)
        key = 'i'
        if inv.shown:
            inv.shown = False
        elif key == 'i':
            inv.shown = True
        elif key == 'e' and state == 0:
            print('move right')
            phys.x += 1

class AiSystem:
    def __init__(self, entities):
        self.entities = entities
        self.ai_comps = [entity.get_comp(AiComponent) for entity in self.entities]
    def update(self):
        for ai in self.ai_comps:
            if ai is None:
                continue
            ent = entities[ai.entity]
            if ai.type_ == 'patrol': # move between point_a and point_b
                phys = ent.get_comp(TransformComponent)
                x, y = phys.x, phys.y
                if ai.current_point == ai.point_a:
                    direction = get_direction((x, y), (ai.point_b.x, ai.point_b.y))
                    phys.x += direction.x
                    phys.y += direction.y
                    if Vector(phys.x, phys.y) == ai.point_b:
                        ai.current_point = ai.point_b
                elif ai.current_point == ai.point_b:
                    direction = get_direction((x, y), (ai.point_a.x, ai.point_a.y))
                    phys.x += direction.x
                    phys.y += direction.y
                    if Vector(phys.x, phys.y) == ai.point_a:
                        ai.current_point = ai.point_a
                print(f'E{ai.entity}', phys.x, phys.y)

if 'idlelib' not in sys.modules:
    os.system('cls')
entities = []
ent = Entity(0)
ent.add_comp(TransformComponent(0, 0, 0))
ent.add_comp(InputComponent(0))
ent.add_comp(InventoryComponent(0))
entities.append(ent)

# creating a unit
ent = Entity(1)
ent.add_comp(TransformComponent(1, 0, 0))
ent.add_comp(AiComponent(1, 'patrol'))
ent.add_comp(MovementComponent(1))
ent.add_comp(HealthComponent(1, 100))
ent.add_comp(StatusComponent(1))
entities.append(ent)

# update InputComponent
# update AiComponent
# update PhysComponent

phys_comps = [entity.get_comp(TransformComponent) for entity in entities]
ai_system = AiSystem(entities)
inp_system = InputSystem(entities)
# main update loop
frames = 8
for _ in range(frames):
    ai_system.update()
    #key = input('Key: ')
    key = ''
    #inp_system.update(key)

for _ in range(frames):
    ai_system.update()
    #key = input('Key: ')
    key = ''
    #inp_system.update(key)


    
