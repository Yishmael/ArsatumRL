
class Factor:
    air = 1
    water = 40
    contact = 10

class Item:
    def __init__(self, temp, mass):
        self.temp = temp
        self.mass = mass
    @property
    def heat(self):
        return self.temp * self.mass
    def __repr__(self):
        return f'({self.temp}°C, {self.mass}kg)'

# every item is in backpack, mass = 1
def transfer_factor(item, other):
    if item is other:
        return 100
    elif item in backpack and other in backpack:
        return 10
    return 1

backpack = [Item(50, 1)]
[backpack.append(Item(50, 1)) for _ in range(100)]

items = [Item(0, 1000), ] + backpack

for i in range(1, 11):
    print(f'Turn {i}')
    for item in items[:2]:
        print(item)
        eq_temp = 0
        tot_mass = 0
        tot_factors = 0
        for other in items:
            factor = transfer_factor(item, other)
            eq_temp += other.heat * factor
            tot_mass += other.mass
            tot_factors += factor
        eq_temp /= (tot_mass + tot_factors)
        # don't change temp of the zone
        if item.mass != 1000:
            item.temp += (eq_temp - item.temp) * 0.01
        print(f'EQUILI: {eq_temp}°C')
        print()
