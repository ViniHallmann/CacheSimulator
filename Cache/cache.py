from Cache.block                        import Block
from Cache.statistics                   import Statistics
from Cache.ReplacementPolicies.random  import Random
from Cache.ReplacementPolicies.fifo    import FIFO
from Cache.ReplacementPolicies.lru     import LRU
import math
import struct
import random

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

        self.mapping_type: str = ""
        if self.nsets > 1 and self.assoc == 1:
            self.mapping_type = "direct"
        elif self.nsets > 1 and self.assoc > 1:
            self.mapping_type = "set"
        elif self.nsets == 1 and self.assoc > 1:
            self.mapping_type = "fully"

        self.accessed_addresses = set()

        self.stats = Statistics()
        self.cache = self.create_cache(nsets, bsize, assoc)

        #So usa politica de substituicao se nao for mapeamento direto
        if self.mapping_type != "direct":
            self.replacement_policy = self.init_replacement_policy(subst)
        else:
            self.replacement_policy = None

    def init_replacement_policy(self, subst):
        if subst == "R":
            return Random(self.nsets, self.assoc)
        elif subst == "F":
            return FIFO(self.nsets, self.assoc)
        elif subst == "L":
            return LRU(self.nsets, self.assoc)
        else:
            raise ValueError("Política de substituição inválida.")

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
            addresses = []
            while chunk := file.read(4):
                address = struct.unpack('>I', chunk)[0]  # Convert 4 bytes to integer (big-endian)
                addresses.append(str(address))

                tag, index, offset = self.get_address_components(address)
                if self.debug:
                    print(f"Address: {address} => Tag: {tag}, Index: {index}, Offset: {offset}")
                
                if self.mapping_type == "direct":
                    self.simulate_direct_mapped(address)
                elif self.mapping_type == "set":
                    self.simulate_set_associative(address)
                elif self.mapping_type == "fully":
                    self.simulate_fully_associative(address)

                """self.stats.increment_access()
                
                miss_conflict = True
                miss_capacity = True
                found_invalid_block = False

                for i in range(self.assoc):
                    block = self.cache[index][i]

                    if block.tag == tag:
                        data = block.get_data(offset)
                        self.stats.increment_hit()
                        #self.replacement_policy.update_usage(index, i)
                        miss_conflict = False
                        miss_capacity = False
                        break

                    if not block.valid:
                        found_invalid_block = True

                if miss_conflict:
                    if found_invalid_block:
                        self.replace_block(self.cache[index], number)
                        self.stats.increment_compulsory()
                    else:
                        if self.is_cache_full(index):
                            self.replace_block(self.cache[index], number)
                            self.stats.increment_capacity()
                        else:
                            self.replace_block(self.cache[index], number)
                            self.stats.increment_conflict()"""
        if (self.debug):
            max_width = max(len(num) for num in addresses)
            for i in range(0, len(addresses), 15):
                print("  ".join(f"{num:>{max_width}}" for num in addresses[i:i+15]))

    
    
    def simulate_direct_mapped(self, address):
        #ACESSO DIRETO AO BLOCO
        tag, index, offset = self.get_address_components(address)
        
        self.stats.increment_access()
        block = self.cache[index][0]
        
        if block.valid and block.tag == tag:
            self.stats.increment_hit()
            return True
        
        if not block.valid:
            self.stats.increment_compulsory()
        else:
            self.stats.increment_conflict()

        block.tag = tag
        block.valid = True
        block.set_data(address)
        
        return False
    
    def simulate_set_associative(self, address):
        tag, index, offset = self.get_address_components(address)
        
        self.stats.increment_access()

        #PROCURA POR HIT
        for i in range(self.assoc):
            block = self.cache[index][i]
            if block.valid and block.tag == tag:
                self.stats.increment_hit()
                self.replacement_policy.update_usage(index, i)
                return True
        
        #PROCURA POR ESPAÇO VAZIO
        for i in range(self.assoc):
            block = self.cache[index][i]
            if not block.valid:
                block.tag = tag
                block.valid = True
                block.set_data(address)
                self.replacement_policy.update_usage(index, i)
                self.stats.increment_compulsory()
                return False
            
        #CACHE CHEIA 
        block_index = self.replacement_policy.select_block(index)
        block = self.cache[index][block_index]
        block.tag = tag
        block.valid = True
        block.set_data(address)
        self.replacement_policy.update_usage(index, block_index)
        
        if self.is_cache_full(index):
            self.stats.increment_capacity()
        else:
            self.stats.increment_conflict()

        return False

    def simulate_fully_associative(self, address):
        tag, index, offset = self.get_address_components(address)
    
        self.stats.increment_access()
        
        # PROCURA POR HIT
        for i in range(self.assoc):
            block = self.cache[0][i]
            if block.valid and block.tag == tag:
                self.stats.increment_hit()
                self.replacement_policy.update_usage(0, i)
                return True
        
        # PROCURA POR ESPAÇO VAZIO
        for i in range(self.assoc):
            block = self.cache[0][i]
            if not block.valid:
                block.tag = tag
                block.valid = True
                block.set_data(address)
                self.replacement_policy.update_usage(0, i)
                self.stats.increment_compulsory()
                return False
        
        #CACHE CHEIA 
        block_index = self.replacement_policy.select_block(0)
        block = self.cache[0][block_index]
        block.tag = tag
        block.valid = True
        block.set_data(address)
        self.replacement_policy.update_usage(0, block_index)

        self.stats.increment_capacity()
        
        return False
            
    def is_cache_full(self, index):
        return all(block.valid for block in self.cache[index])

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
            print(f"{total_accesses}, {hit_rate:.2f}, {miss_rate:.2f}, {compulsory_rate:.2f}, {capacity_rate:.2f}, {conflict_rate:.2f}")

    def replace_block(self, sets, data):
        tag, index, offset = self.get_address_components(data)
    
        block_index = self.replacement_policy.select_block(index)
        block = sets[block_index]
        
        block.tag = tag
        block.valid = True
        block.set_data(data)

        self.replacement_policy.update_usage(index, block_index)
        
        return block

