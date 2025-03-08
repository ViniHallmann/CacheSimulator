import struct

class Block:
    def __init__(self):
        self.tag = -1
        self.valid = False
        self.last_access = 0
        self.data = [None] * 4

    def get_data(self, offset):
        return self.data[offset]
    
    def set_data(self, data):
        for i in range(4):
            self.data[i] = (data >> (8 * (3 - i))) & 0xFF