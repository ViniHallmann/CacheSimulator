from parser import Parser
import math

class Cache:
    def __init__(self, nsets, bsize, assoc, subst, flagOut, arquivoEntrada, debug):
        self.nsets: int = nsets
        self.bsize: int = bsize
        self.assoc: int = assoc
        self.subst: str = subst
        self.flagOut: int = flagOut
        self.arquivoEntrada: str = arquivoEntrada
        self.debug = debug

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
    
    def get_address_components(self, address: int) -> tuple:
        offset = address & ((1 << self.offset_bits) - 1)
        index = (address >> self.offset_bits) & ((1 << self.index_bits) - 1)
        tag = (address >> (self.offset_bits + self.index_bits)) & ((1 << self.tag_bits) - 1)
        return tag, index, offset
    
    def create_cache(self, nsets: int, bsize: int, assoc: int) -> list:
        cache = []
        for _ in range(nsets):
            sets = []
            for _ in range(assoc):  
                sets.append(self.Block())
            cache.append(sets)
        return cache

    def get_info(self) -> None:
        num_sets = self.nsets
        blocks_per_set = self.assoc
        block_size = self.bsize
        total_cache_size = self.nsets * self.assoc * self.bsize
        offset = self.offset_bits
        index = self.index_bits
        tag = self.tag_bits

        print(
            "\n🔹 CONFIGURAÇÃO DA CACHE 🔹\n"
            "============================\n"
            f"📌 Número de Conjuntos    : {num_sets}\n"
            f"📌 Blocos por Conjunto    : {blocks_per_set}\n"
            f"📌 Tamanho do Bloco       : {block_size} bytes\n"
            f"📌 Tamanho Total da Cache : {total_cache_size} bytes\n"
            "----------------------------\n"
            f"🔢 Bits de Offset         : {offset} bits\n"
            f"🔢 Bits de Índice         : {index} bits\n"
            f"🔢 Bits de Tag            : {tag} bits\n"
            "============================\n"
        )
        
    def simulate(self):
        with open(self.arquivoEntrada, 'rb') as file:
            address = file.read(4)
            print(address)

    def access_cache(self):
        pass

    def replace_block(self, policy):

        if self.subst == "R":
            pass
        elif self.subst == "L":
            pass

        elif self.subst == "F":
            pass

    
    class Statistics:
        def __init__(self):
            self.misses = {
                "compulsory": 0,
                "capacity": 0,
                "conflict": 0
            }
            self.access = 0
            self.hit = 0

        def increment_compulsory(self):
            self.misses["compulsory"] += 1

        def increment_capacity(self):
            self.misses["capacity"] += 1

        def increment_conflict(self):
            self.access["conflict"] += 1

        def increment_access(self):
            self.access += 1
        
        def increment_hit(self):
            self.hit += 1

        def get_hit_rate(self):
            return self.hit / self.access
        
        def get_miss_rate(self):
            return 1 - self.get_hit_rate()

        def get_total_misses(self):
            return self.misses["compulsory"] + self.misses["capacity"] + self.misses["conflict"]
        
    class Block:
        def __init__(self):
            self.tag = -1
            self.valid = False
            self.last_access = 0

