import random

class Staircase:
    def __init__(self, x1, y1, zone_id1, x2=None, y2=None, zone_id2=None):
        self.x1 = x1
        self.y1 = y1
        self.zone_id1 = zone_id1
        self.x2 = x2
        self.y2 = y2
        self.zone_id2 = zone_id2
        
    def __repr__(self):
        return '({},{},zone{})->({},{},zone{})'.format(self.x1, self.y1, self.zone_id1,
                                                       self.x2, self.y2, self.zone_id2)

    def get_descend_message(self):
        zone_id = max((self.zone_id1, self.zone_id2))
        if self.zone_id2:
            return f'You descend the stairs. Depth level {zone_id}.'
        else:
            return 'The stairs lead to a brick wall.'
    
    def get_ascend_message(self):
        zone_id = min((self.zone_id1, self.zone_id2))
        if self.zone_id1 is not None: # TODO deal with disabled stairs properly
            message = f'You ascend the stairs. Depth level {zone_id}. '
            if zone_id == 0:
                if random.random() < 0.4:
                    message +=  'Your eyes take a few seconds to adjust.'
        else:
            message = 'The stairs lead to a brick wall.'
        return message

    def get_exit_location(self, x, y, zone_id):
        if (x, y, zone_id) not in  ((self.x1, self.y1, self.zone_id1), (self.x2, self.y2, self.zone_id2)):
            return None
        if (x, y, zone_id) == (self.x1, self.y1, self.zone_id1):
            return (self.x2, self.y2, self.zone_id2)
        else:
            return (self.x1, self.y1, self.zone_id1)

    def get_icon(self, zone_id):
        if zone_id not in [self.zone_id1, self.zone_id2]:
            raise ValueError(self, ' does not have any location')
        elif self.zone_id1 is not None and self.zone_id2 is not None:
            # current zone is at smaller depth
            if zone_id == min([self.zone_id1, self.zone_id2]):
                return '>'
            # current zone is at greater depth
            elif zone_id == max([self.zone_id1, self.zone_id2]):
                return '<'
        else:
            # doesn't lead anywhere
            return 'x'

    # @staticmethod
    # def get_reversed(staircase):
    #     return Staircase(staircase.x2, staircase.y2, staircase.zone_id2, 
    #                      staircase.x1, staircase.y1, staircase.zone_id1)
            
        
