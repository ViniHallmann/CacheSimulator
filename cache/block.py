class Block:
    def __init__(self):
        self.tag = -1
        self.valid = False
        self.last_access = 0
        self.data = [None] * 4

    def get_data(self, offset, tag):
        if self.valid and self.tag == tag:
            return self.data[offset]
        return None
    
    def set_data(self, data):
        self.data = data