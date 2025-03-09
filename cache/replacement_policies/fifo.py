from cache.replacement_policies.base import ReplacementPolicy

class FIFO(ReplacementPolicy):
    def __init__(self, nsets, assoc):
        super().__init__(nsets, assoc)
        self.fifo_list = {i: [] for i in range(nsets)}

    def select_block(self, index):
        if len(self.fifo_list[index]) < self.assoc:
            block_index = len(self.fifo_list[index])
            self.fifo_list[index].append(block_index)
            return block_index
        else:
            evicted_index = self.fifo_list[index].pop(0)
            self.fifo_list[index].append(evicted_index)
            return evicted_index