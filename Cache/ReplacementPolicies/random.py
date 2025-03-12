import random
from typing import Dict, List
from Cache.ReplacementPolicies.base import ReplacementPolicy

class Random(ReplacementPolicy):
    """Implementa a política de substituição aleatória (Random)."""
    def __init__(self, nsets: int, assoc: int) -> None:
        """Inicializa a política de substituição Random."""
        super().__init__(nsets, assoc)
        self.blocks: Dict[int, List[int]] = {i: list(range(assoc)) for i in range(nsets)}
        
    def select_block(self, index: int) -> int:
        """Seleciona um bloco aleatório para substituição no conjunto especificado."""
        if len(self.blocks[index]) < self.assoc:
            block_index = len(self.blocks[index])
            return block_index
        else:
            return random.randint(0, self.assoc - 1)