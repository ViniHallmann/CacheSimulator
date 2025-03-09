import random
from replacement_policies.base import ReplacementPolicy
class Random(ReplacementPolicy):
    def __init__(self, nsets, assoc):
        super().__init__(nsets, assoc)
        self.blocks = {i: list(range(assoc)) for i in range(nsets)}
        
    def select_block(self, index):
        if len(self.blocks[index]) < self.assoc:
            block_index = len(self.blocks[index])
            return block_index
        else:
            return random.randint(0, self.assoc - 1)