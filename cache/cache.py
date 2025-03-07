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
                number = struct.unpack('>I', chunk)[0]  # Converte 4 bytes para inteiro (big-endian)
                numbers.append(str(number))

        if (self.debug):
            max_width = max(len(num) for num in numbers)
            for i in range(0, len(numbers), 15):
                print("  ".join(f"{num:>{max_width}}" for num in numbers[i:i+15]))

    def access_cache(self):
        pass

    def replace_block(self, policy):

        if self.subst == "R":
            pass
        elif self.subst == "L":
            pass

        elif self.subst == "F":
            pass

