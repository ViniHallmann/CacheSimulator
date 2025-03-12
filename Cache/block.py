import struct

class Block:
    def __init__(self):
        self.last_access: int = 0
        self.tag:   int = -1
        self.valid: bool = False
        self.data:  list[list] = [None] * 4

    def get_data(self, offset):
        return self.data[offset]
    
    def set_data(self, data):
        for i in range(4):
            self.data[i] = (data >> (8 * (3 - i))) & 0xFF