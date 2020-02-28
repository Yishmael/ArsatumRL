from utils import Vector as Vector_


class Component:
    def __init__(self, entity):
        self.entity = entity

class AiComponent:
    def __init__(self, entity, type_):
        self.entity = entity
        self.type_ = type_
        self.point_a = Vector_(0, 0)
        self.point_b = Vector_(2, 0)
        self.current_point = self.point_a

class TransformComponent:
    def __init__(self, entity, x, y):
        self.entity = entity
        self.x = x
        self.y = y

class HealthComponent:
    def __init__(self, entity, hp):
        self.entity = entity
        self.hp = hp

class EquipmentComponent:
    def __init__(self, entity, items=['leather boots']):
        self.entity = entity
        self.items = items
        self.shown = False

class TemperatureComponent:
    def __init__(self, entity, temperature):
        self.entity = entity
        self.temperature = temperature

class CombatComponent:
    def __init__(self, entity, damage, block):
        self.entity = entity
        self.damage = damage
        self.block = block
    
class StatusComponent:
    def __init__(self, entity, statuses=[]):
        self.entity = entity
        self.statuses = statuses

class InventoryComponent:
    def __init__(self, entity, items=['stick', 'potion']):
        self.entity = entity
        self.items = items
        self.shown = False

class MovementComponent:
    def __init__(self, entity):
        self.entity = entity
        self.dx = 0
        self.dy = 0

class InputComponent:
    def __init__(self, entity):
        self.entity = entity
        self.last_key = None
