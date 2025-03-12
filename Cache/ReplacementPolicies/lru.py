from typing import Dict, List
from Cache.ReplacementPolicies.base import ReplacementPolicy

class LRU(ReplacementPolicy):
    """Implementa a política de substituição Least Recently Used (LRU)."""
    def __init__(self, nsets: int, assoc: int) -> None:
        """Inicializa a política de substituição LRU."""
        super().__init__(nsets, assoc)
        self.lru_list: Dict[int, List[int]] = {i: [] for i in range(nsets)}

    def select_block(self, index: int) -> int:
        """
        Seleciona o bloco menos recentemente usado para substituição.
            - Se o conjunto não estiver cheio, retorna o próximo bloco disponível.
            - Caso contrário, retorna o bloco no início da lista LRU (o menos usado).
        """
        if len(self.lru_list[index]) < self.assoc:
            block_index = len(self.lru_list[index])
            self.lru_list[index].append(block_index)
        else:
            block_index = self.lru_list[index].pop(0)
            self.lru_list[index].append(block_index)
        return block_index
    
    def update_usage(self, index: int, block_index: int) -> None:
        """
        Atualiza a lista LRU após um acesso a um bloco.
        Move o bloco acessado para o final da lista.
        """
        if block_index in self.lru_list[index]:
            self.lru_list[index].remove(block_index)
        self.lru_list[index].append(block_index)