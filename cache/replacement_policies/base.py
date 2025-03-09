class ReplacementPolicy:
    def __init__(self, nsets, assoc):
        self.nsets = nsets
        self.assoc = assoc

    def select_block(self, index):
        raise NotImplementedError
    
    def update_usage(self, index, block_index):
        pass