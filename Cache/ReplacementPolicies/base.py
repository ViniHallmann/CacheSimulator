class ReplacementPolicy:
    def __init__(self, nsets, assoc):
        self.nsets = nsets
        self.assoc = assoc

    def select_block(self, index: int) -> int:
        """Seleciona um bloco para substituição no conjunto especificado."""
        raise NotImplementedError
    
    def update_usage(self, index: int, block_index: int) -> None:
        """
        Atualiza informações de uso após acesso a um bloco.
        Implementação padrão não faz nada, subclasses podem sobrescrever.
        """
        pass