from cache.replacement_policies.base import ReplacementPolicy

class LRU(ReplacementPolicy):
    def __init__(self, nsets, assoc):
        super().__init__(nsets, assoc)
        self.lru_list = {i: [] for i in range(nsets)}

    def select_block(self, index):
        if len(self.lru_list[index]) < self.assoc:
            block_index = len(self.lru_list[index])
            self.lru_list[index].append(block_index)
        else:
            block_index = self.lru_list[index].pop(0)
            self.lru_list[index].append(block_index)
        return block_index
    
    def update_usage(self, index, block_index):
        if block_index in self.lru_list[index]:
            self.lru_list[index].remove(block_index)
        self.lru_list[index].append(block_index)