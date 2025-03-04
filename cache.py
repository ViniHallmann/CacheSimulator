from parser import Parser
import math


class Cache:
    def __init__(self, nsets, bsize, assoc, subst, flagOut, arquivoEntrada):
        self.nsets: int = nsets
        self.bsize: int = bsize
        self.assoc: int = assoc
        self.subst: str = subst
        self.flagOut: int = flagOut
        self.arquivoEntrada: str = arquivoEntrada

        self.offset_bits = self.get_offset(bsize)
        self.index_bits  = self.get_index(nsets)
        self.tag_bits    = self.get_tag(nsets, bsize)

        self.accessed_addresses = set()

        self.stats = self.Statistics()
        self.cache = self.create_cache(nsets, bsize, assoc)

    def get_offset(self, bsize: int) -> int:
        return int(math.log2(bsize))

    def get_index(self, nsets: int) -> int:
        return int(math.log2(nsets))

    def get_tag(self, nsets: int, bsize: int) -> int:
        return 32 - self.get_offset(bsize) - self.get_index(nsets)
    
    def create_cache(self, nsets: int, bsize: int, assoc: int) -> list:
        cache = []
        for _ in range(nsets):
            sets = []
            for _ in range(assoc):  
                sets.append(self.Block())
            cache.append(sets)
        return cache
    
    def simulate(self):
        with open(self.arquivoEntrada, 'rb') as file:
            address = file.read(4)
            print(address)
    
    class Statistics:
        def __init__(self):
            self.compulsory = 0  
            self.capacity = 0     
            self.conflict = 0
            self.access = 0
            self.hit = 0

        def increment_compulsory(self):
            self.compulsory += 1

        def increment_capacity(self):
            self.capacity += 1

        def increment_conflict(self):
            self.conflict += 1

        def increment_access(self):
            self.access += 1
        
        def increment_hit(self):
            self.hit += 1

        def get_hit_rate(self):
            return self.hit / self.access
        
        def get_miss_rate(self):
            return 1 - self.get_hit_rate()

        def get_total_misses(self):
            return self.compulsory + self.capacity + self.conflict
        
    class Block:
        def __init__(self):
            self.tag = -1
            self.valid = False
            self.last_access = 0

