from typing import Dict, List
from Cache.ReplacementPolicies.base import ReplacementPolicy

class FIFO(ReplacementPolicy):
    """Implementa a política de substituição First In First Out (FIFO)."""
    def __init__(self, nsets: int, assoc: int) -> None:
        super().__init__(nsets, assoc)
        self.fifo_list: Dict[int, List[int]] = {i: [] for i in range(nsets)}

    def select_block(self, index: int) -> int:
        """
        Seleciona o bloco mais antigo para substituição.
        """
        if len(self.fifo_list[index]) < self.assoc:
            block_index = len(self.fifo_list[index])
            self.fifo_list[index].append(block_index)
            return block_index
        else:
            evicted_index = self.fifo_list[index].pop(0)
            self.fifo_list[index].append(evicted_index)
            return evicted_index