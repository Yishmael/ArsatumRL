import os
import sys

from utils import Vector, get_direction

class Entity:
    def __init__(self, id_):
        self.id_ = id_
        self.comps = []
    def __repr__(self):
        return f'E{self.id_}'
    def add_comp(self, class_):
        if class_ is PhysicsComponent:
            self.comps.append(class_(self.id_, 0, 0))
        elif class_ is AiComponent:
            self.comps.append(class_(self.id_, 'patrol'))
        elif class_ is InputComponent:
            self.comps.append(class_(self.id_))
        elif class_ is InventoryComponent:
            self.comps.append(class_(self.id_))

    def get_comp(self, type_):
        for comp in self.comps:
            if type(comp) == type_:
                return comp
        return None

class AiComponent:
    def __init__(self, entity, type_):
        self.entity = entity
        self.type_ = type_
        self.point_a = Vector(0, 0)
        self.point_b = Vector(2, 0)
        self.current_point = 'a'

class PhysicsComponent:
    gravity = -10
    def __init__(self, entity, x, y):
        self.entity = entity
        self.x = x
        self.y = y

class InputComponent:
    def __init__(self, entity):
        self.entity = entity
        self.last_key = None

class InventoryComponent:
    def __init__(self, entity):
        self.entity = entity
        self.items = ['stick', 'potion']
        self.shown = False

class InputSystem:
    def __init__(self, entities):
        self.entities = entities
    def update(self, key):
        ent = self.entities[0]
        phys = ent.get_comp(PhysicsComponent)
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
                phys = ent.get_comp(PhysicsComponent)
                x, y = phys.x, phys.y
                if ai.current_point == 'a':
                    direction = get_direction((x, y), ai.point_b)
                    phys.x += direction.x
                    phys.y += direction.y
                    if (phys.x, phys.y) == ai.point_b:
                        ai.current_point = 'b'
                elif ai.current_point == 'b':
                    direction = get_direction((x, y), ai.point_a)
                    phys.x += direction.x
                    phys.y += direction.y
                    if (phys.x, phys.y) == ai.point_a:
                        ai.current_point = 'a'

if 'idlelib' not in sys.modules:
    os.system('cls')
entities = []
ent = Entity(0)
ent.add_comp(PhysicsComponent)
ent.add_comp(InputComponent)
ent.add_comp(InventoryComponent)
entities.append(ent)
ent = Entity(1)
ent.add_comp(PhysicsComponent)
ent.add_comp(AiComponent)
entities.append(ent)

# update InputComponent
# update AiComponent
# update PhysComponent

phys_comps = [entity.get_comp(PhysicsComponent) for entity in entities]

ai_system = AiSystem(entities)
inp_system = InputSystem(entities)
# main update loop
for _ in range(5):
    ai_system.update()
    #key = input('Key: ')
    key = ''
    inp_system.update(key)


    
