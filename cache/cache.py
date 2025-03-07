from cache.block import Block
from cache.statistics import Statistics
import math
import struct

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

        self.stats = Statistics()
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
                sets.append(Block())
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
        if (self.debug):
            print("Iniciando leitura do arquivo ...\n")

        with open(self.arquivoEntrada, 'rb') as file:
            numbers = []
            while chunk := file.read(4):
                number = struct.unpack('>I', chunk)[0]  # Convert 4 bytes to integer (big-endian)
                numbers.append(str(number))

                tag, index, offset = self.get_address_components(number)
                if self.debug:
                    print(f"Address: {number} => Tag: {tag}, Index: {index}, Offset: {offset}")

                self.stats.increment_access()
                
                miss_conflict = True
                miss_capacity = True

                for i in range(self.assoc):
                    block = self.cache[index][i]

                    if block.tag == tag:

                        data = block.get_data(offset)

                        if not block.valid:
                            self.replace_block()
                            self.stats.increment_compulsory()
                        
                        miss_conflict = False
                        break
                    
                    if not block.valid:
                        miss_capacity = False 

                if miss_conflict:
                    self.replace_block()
                    self.stats.increment_conflict()
                
                if miss_capacity:
                    self.replace_block()
                    self.stats.increment_capacity()
        if (self.debug):
            max_width = max(len(num) for num in numbers)
            for i in range(0, len(numbers), 15):
                print("  ".join(f"{num:>{max_width}}" for num in numbers[i:i+15]))

    def get_simulation(self):
        total_accesses = self.stats.access
        total_hits = self.stats.hit
        total_misses = self.stats.get_total_misses()
        compulsory_misses = self.stats.misses["compulsory"]
        conflict_misses = self.stats.misses["conflict"]
        capacity_misses = self.stats.misses["capacity"]

        hit_rate = self.stats.get_hit_rate()
        miss_rate = self.stats.get_miss_rate()
        compulsory_rate = compulsory_misses / total_misses if total_misses > 0 else 0
        conflict_rate = conflict_misses / total_misses if total_misses > 0 else 0
        capacity_rate = capacity_misses / total_misses if total_misses > 0 else 0

        if self.flagOut == 0:
            print(
                f"Total de acessos: {total_accesses}\n"
                f"Total de hits: {total_hits}\n"
                f"Total de misses: {total_misses}\n"
                f"Misses compulsórios: {compulsory_misses}\n"
                f"Misses de conflito: {conflict_misses}\n"
                f"Misses de capacidade: {capacity_misses}\n"
                f"Taxa de hits: {hit_rate:.2%}\n"
                f"Taxa de misses: {miss_rate:.2%}\n"
                f"Taxa de miss compulsório: {compulsory_rate:.2%}\n"
                f"Taxa de miss de conflito: {conflict_rate:.2%}\n"
                f"Taxa de miss de capacidade: {capacity_rate:.2%}"
            )
        else:
            print(f"{total_accesses}, {hit_rate:.2f}, {miss_rate:.2f}, {compulsory_rate:.2f}, {conflict_rate:.2f}, {capacity_rate:.2f}")

    def replace_block(self):

        if self.subst == "R":
            pass
        elif self.subst == "L":
            pass

        elif self.subst == "F":
            pass

