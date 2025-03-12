import struct
from typing import List, Optional
class Block:
    """
    Representa um bloco de dados em uma cache.
    Cada bloco contém uma tag, bit de validade, contador de último acesso e dados.
    """
    def __init__(self, block_size: int):
        """
        Inicializa um bloco de cache vazio.
        """
        self.last_access: int = 0 
        self.tag: int = -1              
        self.valid: bool = False      
        self.data: List[Optional[int]] = [None] * block_size  
        self.block_size = block_size

    def get_data(self, offset):
        """Retorna o byte de dado no deslocamento especificado."""
        return self.data[offset]
    
    def set_data(self, data):
        """Define os dados do bloco."""
        for i in range(4):
            self.data[i] = (data >> (8 * (self.block_size - 1 - i))) & 0xFF

    def is_valid(self) -> bool:
        """Retorna se o bloco é válido."""
        return self.valid
    
    def invalidate(self) -> None:
        """Marca o bloco como inválido."""
        self.valid = False