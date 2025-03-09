import random

class Random:
    def select_block(self, sets):
        return random.randint(0, len(sets) - 1)