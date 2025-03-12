class Statistics:
    """
    Classe para armazenar e calcular estatísticas de um simulador de cache.
    Rastreia acessos, hits e diferentes tipos de misses (compulsórios, capacidade e conflito).
    """
    def __init__(self):
        self.misses: dict[str, int] = {
            "compulsory": 0,
            "capacity":   0,
            "conflict":   0
        }
        self.access: int = 0
        self.hit:    int = 0

    def increment_compulsory(self) -> None:
        """Incrementa o contador de misses compulsórios."""
        self.misses["compulsory"] += 1

    def increment_capacity(self) -> None:
        """Incrementa o contador de misses de capacidade."""
        self.misses["capacity"] += 1

    def increment_conflict(self) -> None:
        """Incrementa o contador de misses de conflito."""
        self.misses["conflict"] += 1

    def increment_hit(self) -> None:
        """Incrementa o contador de hits."""
        self.hit += 1
    
    def increment_access(self) -> None:
        """Incrementa o contador de acessos."""
        self.access += 1

    def get_hit_rate(self) -> float:
        """Calcula a taxa de hits."""
        return self.hit / self.access
    
    def get_miss_rate(self) -> float:
        """Calcula a taxa de hits."""
        return 1 - self.get_hit_rate()

    def get_total_misses(self) -> int:
        """Calcula o total de misses."""
        return self.misses["compulsory"] + self.misses["capacity"] + self.misses["conflict"]